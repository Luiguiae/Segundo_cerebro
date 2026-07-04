#!/usr/local/bin/python3.11
"""
jarvis.py — Interfaz de voz para el Segundo Cerebro

Arquitectura: STT → clasificación en intents → tres carriles:
  - conversacion_libre / despedirse → Groq directo
  - consulta_simple / razonamiento_profundo → Groq con contexto del vault
  - accion_directa → Claude Code
  - operacion_archivo → mejora_006_filesystem (Groq o TTS directo)
  - ver_pantalla / relacionar_con_vault → mejora_007_vision + Groq
  - profundizar_pantalla / capturar_como_concepto → mejora_007_vision + Claude Code
"""

import json
import logging
import os
import requests
import subprocess
import sys
import threading
import time
import re
from datetime import datetime, timedelta
from pathlib import Path

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"
MEMORIA_PATH = Path(__file__).parent / "memoria.md"

if str(Path(__file__).parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent))

try:
    from mejora_006_filesystem import operacion_archivo as _operacion_archivo
    _filesystem_disponible = True
    print("[Módulo] mejora_006_filesystem importado OK — operacion_archivo disponible.", flush=True)
except ImportError as _e006:
    _filesystem_disponible = False
    print(f"[Módulo] mejora_006_filesystem NO disponible: {_e006}", flush=True)

try:
    from mejora_007_vision import (
        ver_pantalla as _ver_pantalla,
        profundizar_pantalla as _profundizar_pantalla,
        capturar_como_concepto as _capturar_como_concepto,
        relacionar_con_vault as _relacionar_con_vault,
        es_error_vision as _es_error_vision,
    )
    _vision_pantalla_disponible = True
except ImportError:
    _vision_pantalla_disponible = False

# Historial de sesión en memoria — ventana deslizante de 10 turnos (20 mensajes)
historial_sesion: list[dict] = []

# Último archivo leído vía operacion_archivo — persiste entre comandos de voz
_ultimo_archivo_leido: dict = {"ruta": None, "contenido": None}

_CONTEXT_REFS = (
    "esto", "este archivo", "este documento", "esta nota",
    "lo que leíste", "lo que acabas de leer", "el archivo que leíste",
    "lo anterior", "lo que me mostraste", "el contenido que leíste",
    "profundiza esto", "profundiza este", "analiza esto", "sobre esto",
    "de esto", "en esto", "con esto",
)


# ── Dashboard ──────────────────────────────────────────────────────────────────

def emitir_evento(tipo: str, mensaje: str) -> None:
    """Envía evento al dashboard via HTTP POST. Fire-and-forget: nunca bloquea Jarvis."""
    try:
        requests.post(
            "http://localhost:7777/event",
            json={"tipo": tipo, "mensaje": mensaje,
                  "timestamp": datetime.now().isoformat()},
            timeout=0.1,
        )
    except Exception:
        pass


# ── TTS ────────────────────────────────────────────────────────────────────────

_jarvis_hablando: bool = False
_last_hablar_end_time: float = 0.0   # timestamp de fin del último TTS — usado para buffer de eco
_last_spoken_text: str = ""           # texto del último hablar() — para detección de eco en daemon
_hablar_lock = threading.Lock()  # serializa llamadas TTS entre threads


def hablar(texto: str) -> None:
    """TTS via `say` nativo de macOS. Una sola llamada, sin chunking, thread-safe."""
    global _jarvis_hablando, _last_hablar_end_time, _last_spoken_text
    with _hablar_lock:
        _jarvis_hablando = True
        _last_spoken_text = texto.lower()
        _end_time_seteado = False
        try:
            subprocess.run(
                ["say", "-v", "Mónica", texto.strip()],
                timeout=60,
                check=False,
            )
            _last_hablar_end_time = time.time()
            _end_time_seteado = True
        except subprocess.TimeoutExpired:
            print(f"[TTS] Timeout — matando say")
            subprocess.run(["killall", "say"], check=False)
        except Exception as e:
            print(f"[TTS] {texto}")
            print(f"[TTS error] {e}")
        finally:
            _jarvis_hablando = False
            if not _end_time_seteado:
                _last_hablar_end_time = time.time()


def hablar_respuesta(texto: str, max_chars: int = 600) -> None:
    """Para respuestas de vault: trunca con gracia si es muy larga."""
    if len(texto) > max_chars:
        corte = texto[:max_chars].rfind('.')
        texto = texto[:corte + 1] + " Hay más información disponible." if corte > 0 else texto[:max_chars] + "..."
    hablar(texto)


# ── STT ────────────────────────────────────────────────────────────────────────

_ECO_BUFFER = 0.5  # segundos de margen tras fin del TTS antes de abrir el micrófono
# 0.2s en hablar() cubre el tail de CoreAudio; 0.5s aquí cubre el eco físico de la sala.


def escuchar() -> str | None:
    """Captura audio del micrófono y devuelve el texto transcrito (o None si falla)."""
    # Esperar a que Jarvis termine de hablar y dejar que el eco físico se disipe
    while _jarvis_hablando:
        time.sleep(0.05)
    eco_restante = _ECO_BUFFER - (time.time() - _last_hablar_end_time)
    if eco_restante > 0:
        time.sleep(eco_restante)

    try:
        import speech_recognition as sr
    except ImportError:
        hablar("Falta la librería speech_recognition.")
        return None

    recognizer = sr.Recognizer()
    # device_index=None deja que PortAudio use el default del sistema.
    # Cuando el daemon llama escuchar(), ya fijó el dispositivo via seleccionar_dispositivo_entrada().
    # En modo standalone (jarvis.py directo), None es correcto.
    for intento in range(2):
        try:
            with sr.Microphone(device_index=None) as source:
                print("Escuchando... (habla ahora)")
                recognizer.adjust_for_ambient_noise(source, duration=0.05)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        except AttributeError:
            hablar("Micrófono no disponible.")
            return None
        except sr.WaitTimeoutError:
            return None  # silencio normal — sin hablar, sin eco
        except Exception as e:
            print(f"[Micrófono error] {e}")
            return None

        try:
            texto = recognizer.recognize_google(audio, language="es-ES").lower()
            print(f"[Transcripción] {texto}")
            logging.info(f"Transcripción: {texto}")
            return texto
        except sr.UnknownValueError:
            # Audio capturado pero STT no pudo transcribir (ej. "sí" muy corto)
            if intento < 1:
                time.sleep(0.2)
                continue
            return None
        except Exception:
            return None

    return None


# ── Normalización de texto (correcciones de STT) ─────────────────────────────

def normalizar_texto(texto: str) -> str:
    """Corrige errores frecuentes del STT antes de clasificar."""
    reemplazos = {
        "baúl": "vault",
        "baul": "vault",
        "ball": "vault",
        "bal ": "vault",
        "downloads": "descargas",
        "desktop": "escritorio",
        "documents": "documentos",
    }
    texto_lower = texto.lower()
    for error, correcto in reemplazos.items():
        texto_lower = texto_lower.replace(error, correcto)
    return texto_lower


# ── Clasificación binaria — Groq ──────────────────────────────────────────────

def detectar_intent_groq(texto: str, historial: list[dict]) -> tuple[str, dict]:
    """Clasifica en una de las categorías soportadas (ver system_prompt)."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no disponible.")

    system_prompt = """Eres el clasificador de Jarvis, asistente de voz del Segundo Cerebro de Luigui.

Clasifica el mensaje en UNA de estas categorías:

conversacion_libre: saludo, pregunta personal a Jarvis, comentario casual que NO involucra el vault ni el filesystem.
  Ejemplos: "cómo estás", "qué hora es", "gracias", "muy bien".

despedirse: el usuario quiere terminar la sesión de escucha activa.
  Ejemplos: "bye", "hasta luego", "ya terminé", "modo espera", "para", "descansa", "chau".

consulta_simple: pregunta sobre los CONCEPTOS o el historial del vault del Segundo Cerebro. Solo aplica cuando la pregunta es sobre conocimiento guardado en el vault, no sobre archivos del sistema operativo.
  Ejemplos: "cuántos conceptos tengo", "qué conceptos hay en producto", "lista mis correlaciones", "cuál es el más reciente",
  "qué hemos hecho hoy", "qué cambios se hicieron", "qué actualizaciones hubo", "cuéntame el resumen del día".

accion_directa: instrucción que modifica el vault o ejecuta una tarea concreta en el Segundo Cerebro.
  Ejemplos: "crea un concepto sobre X", "correlaciona X con Y", "audita el vault", "profundiza X", "procesa esta fuente".

razonamiento_profundo: análisis, evaluación o recomendaciones que requieren leer el contenido completo de los conceptos.
  Ejemplos: "qué correlaciones me faltan", "cuál es el concepto más débil", "qué patrones ves en mis conceptos de IA",
  "qué debería explorar próximamente", "qué concepto tiene menos conexiones", "evalúa la calidad del vault".

operacion_archivo: el usuario quiere operar sobre archivos o carpetas reales de su computadora (NO conceptos del vault).
  Señales fuertes: menciona "carpeta", "directorio", "archivo" junto con una ubicación del sistema operativo.
  Ubicaciones del sistema operativo reconocidas: downloads, descargas, desktop, escritorio, wayta, documentos, vault, home.
  Frases que activan este intent: "qué hay en", "lista los archivos de", "lee el [archivo]", "abre el archivo",
  "crea una carpeta", "mueve el [archivo]", "elimina el [archivo]", "borra el [archivo]", "busca en [carpeta]".
  Ejemplos (TODOS estos son operacion_archivo, no consulta_simple):
    - "qué hay en la carpeta de descargas"
    - "qué hay en downloads"
    - "qué hay en el escritorio"
    - "lista los archivos de wayta"
    - "lee el SPEC.md de wayta"
    - "crea una carpeta llamada propuestas en documentos"
    - "mueve el PDF de downloads a documentos"
    - "busca en wayta archivos que digan diseño"

ver_pantalla: el usuario quiere saber qué hay en su pantalla o que le expliquen/describan/opinen sobre lo que está viendo.
  Señales: "qué estoy viendo", "de qué trata esto", "explícame esto", "qué es esto", "qué hay aquí",
  "qué dice la pantalla", "qué estoy leyendo", "describe lo que ves", "explica esto".
  Params: accion = "describir" (default) | "resumir" | "opinar"

profundizar_pantalla: el usuario quiere investigar más, profundizar o buscar fuentes sobre lo que está viendo en pantalla.
  Señales: "profundiza sobre lo que estoy leyendo", "profundiza esto", "investiga más sobre esto",
  "busca más sobre el autor", "profundiza sobre el tema de la pantalla", "investiga esto".
  Params: foco = "tema o autor específico si lo menciona, sino vacío"

capturar_como_concepto: el usuario quiere guardar o convertir lo que ve en pantalla como concepto del vault.
  Señales: "guarda esto como concepto", "crea un concepto de esto", "esto me parece importante",
  "captura esto", "agrega esto al vault", "guarda esto en el vault".
  Params: titulo_candidato = "título sugerido por el usuario si lo menciona, sino null"

relacionar_con_vault: el usuario quiere saber si tiene conceptos en el vault relacionados con lo que está viendo.
  Señales: "¿hay algo en el vault sobre esto?", "¿tengo algo relacionado?", "¿tengo un concepto sobre esto?",
  "busca relaciones con el vault", "¿se relaciona con algo que tengo?".
  Params: {}

auditar_huerfanos: el usuario quiere saber qué conceptos del vault no tienen backlinks apuntando hacia ellos.
  Señales: "conceptos huérfanos", "qué conceptos no están conectados", "qué notas no tienen links",
  "qué conceptos están solos", "audita huérfanos", "encuentra los huérfanos".
  Params: {}

buscar_por_tag: el usuario quiere listar conceptos que tienen un tag específico.
  Señales: "conceptos con el tag X", "qué tiene el tag X", "busca por tag X",
  "qué hay en el tag X", "lista los de tag X", "filtra por tag X".
  Params: tag = "el tag que menciona el usuario"

sincronizar_vault: el usuario quiere traer los cambios del servidor remoto (Jarvis VPS) al vault local.
  Señales: "sincroniza el segundo cerebro", "sincroniza con la nube", "actualiza el vault",
  "trae los cambios del servidor", "sincroniza el vault", "actualiza desde el servidor".
  Params: {}

recordar_hecho: el usuario quiere que Jarvis recuerde o olvide un dato personal suyo
  (no un concepto del vault, no una acción del sistema — un hecho sobre Luigui).
  Señales agregar: "recuerda que...", "mi [dato] es...", "anota que...", "no olvides que...".
  Señales olvidar: "olvida que...", "ya no...", "borra de tu memoria que...".
  Params: accion = "agregar" | "olvidar", hecho = "el dato tal cual lo dijo el usuario, sin el verbo recuerda/olvida"

subir_cambios: el usuario quiere publicar los cambios locales del vault al servidor remoto (GitHub).
  Es lo opuesto a sincronizar_vault (que TRAE cambios) — este los SUBE.
  Señales: "sube los cambios", "sube los cambios al servidor", "sincroniza hacia arriba",
  "push al servidor", "publica los cambios".
  Params: {}

REGLA DE DESAMBIGUACIÓN CRÍTICA: Si el mensaje menciona una ubicación del sistema operativo
(downloads, descargas, escritorio, desktop, wayta, home, o "carpeta de [nombre]") → clasifica SIEMPRE
como operacion_archivo, nunca como consulta_simple ni conversacion_libre.

REGLA PANTALLA: "profundiza esto" o "profundiza lo que estoy leyendo" → profundizar_pantalla (NO accion_directa).
"guarda esto como concepto" → capturar_como_concepto. "qué estoy viendo" → ver_pantalla.

Responde ÚNICAMENTE con JSON válido.

Para conversacion_libre, despedirse, consulta_simple, accion_directa, razonamiento_profundo:
{"intent": "<categoria>", "instruccion": "<texto literal del usuario>", "archivos_relevantes": ["<categoria_o_ruta>"]}

Para operacion_archivo:
{"intent": "operacion_archivo", "instruccion": "<texto literal>", "archivos_relevantes": [], "operacion": "<listar|leer|crear_carpeta|mover|eliminar|buscar>", "ruta": "<alias o path>", "archivo": "<nombre o vacío>", "destino": "<alias o path o vacío>", "query": "<texto o vacío>", "extension": "<ext o vacío>"}

Para ver_pantalla:
{"intent": "ver_pantalla", "instruccion": "<texto literal>", "archivos_relevantes": [], "accion": "<describir|resumir|opinar>"}

Para profundizar_pantalla:
{"intent": "profundizar_pantalla", "instruccion": "<texto literal>", "archivos_relevantes": [], "foco": "<tema o autor específico, o vacío>"}

Para capturar_como_concepto:
{"intent": "capturar_como_concepto", "instruccion": "<texto literal>", "archivos_relevantes": [], "titulo_candidato": "<título sugerido o null>"}

Para relacionar_con_vault:
{"intent": "relacionar_con_vault", "instruccion": "<texto literal>", "archivos_relevantes": []}

Para auditar_huerfanos:
{"intent": "auditar_huerfanos", "instruccion": "<texto literal>", "archivos_relevantes": []}

Para buscar_por_tag:
{"intent": "buscar_por_tag", "instruccion": "<texto literal>", "archivos_relevantes": [], "tag": "<tag que mencionó el usuario>"}

Para sincronizar_vault:
{"intent": "sincronizar_vault", "instruccion": "<texto literal>", "archivos_relevantes": []}

Para recordar_hecho:
{"intent": "recordar_hecho", "instruccion": "<texto literal>", "archivos_relevantes": [], "accion": "<agregar|olvidar>", "hecho": "<el dato, sin el verbo>"}

Para subir_cambios:
{"intent": "subir_cambios", "instruccion": "<texto literal>", "archivos_relevantes": []}

Para razonamiento_profundo incluye en archivos_relevantes las categorías relevantes (ej. ["ia", "producto", "Correlaciones"]).
Para los demás tipos archivos_relevantes puede ser []."""

    mensajes = [{"role": "system", "content": system_prompt}]
    mensajes += historial[-6:]
    mensajes += [{"role": "user", "content": texto}]

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": mensajes,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=10,
    )
    response.raise_for_status()
    _raw = response.json()["choices"][0]["message"]["content"]
    print(f"[Groq raw intent] {_raw}")
    data = json.loads(_raw)
    intent = data.get("intent", "accion_directa")
    params = {
        "instruccion": data.get("instruccion", texto),
        "archivos_relevantes": data.get("archivos_relevantes", []),
        # operacion_archivo
        "operacion":  data.get("operacion", ""),
        "ruta":       data.get("ruta", ""),
        "archivo":    data.get("archivo", ""),
        "destino":    data.get("destino", ""),
        "query":      data.get("query", ""),
        "extension":  data.get("extension", ""),
        # vision de pantalla
        "accion":           data.get("accion", "describir"),
        "foco":             data.get("foco", ""),
        "titulo_candidato": data.get("titulo_candidato", ""),
        # mcp vault
        "tag": data.get("tag", ""),
        # memoria personal
        "hecho": data.get("hecho", ""),
    }
    # Compatibilidad con formato anterior (conversacion_libre usa "mensaje")
    if intent == "conversacion_libre":
        params["mensaje"] = params["instruccion"]
    return intent, params


def _inferir_operacion_archivo(t: str) -> str:
    """Infiere la operación de filesystem a partir de las keywords del texto —
    usado por el fallback de keywords cuando Groq no está disponible.
    Sin esto, mejora_006_filesystem.py rechaza toda operación con 'operacion' vacía."""
    if any(k in t for k in ("qué hay en", "que hay en", "lista los archivos")):
        return "listar"
    if any(k in t for k in ("lee el archivo", "lee el", "lee la")):
        return "leer"
    if any(k in t for k in ("crea una carpeta", "crea la carpeta")):
        return "crear_carpeta"
    if any(k in t for k in ("mueve el", "mueve la")):
        return "mover"
    if any(k in t for k in ("elimina el", "elimina la", "borra el", "borra la")):
        return "eliminar"
    if "busca en" in t:
        return "buscar"
    return "listar"  # default conservador — solo se mencionó una ubicación, sin verbo de acción


def detectar_intent_keywords(texto: str) -> tuple[str, dict]:
    """Fallback si Groq no está disponible: clasificación por keywords."""
    t = texto.lower()
    DESPEDIDAS_FRASES = ("hasta luego", "ya terminé", "ya termine", "modo espera", "te hablo luego")
    DESPEDIDAS_PALABRAS = {"bye", "chau", "adiós", "adios", "descansa", "detente", "stop"}
    if any(f in t for f in DESPEDIDAS_FRASES):
        return "despedirse", {"instruccion": texto, "archivos_relevantes": []}
    palabras = set(t.split())
    if palabras & DESPEDIDAS_PALABRAS and len(palabras) <= 3:
        return "despedirse", {"instruccion": texto, "archivos_relevantes": []}
    CASUAL = ("cómo estás", "como estas", "qué hora", "gracias", "de nada", "hola jarvis")
    if any(c in t for c in CASUAL) and len(t.split()) < 6:
        return "conversacion_libre", {"mensaje": texto, "instruccion": texto, "archivos_relevantes": []}
    RAZONAMIENTO = (
        "qué correlaciones", "que correlaciones", "concepto más débil", "concepto mas debil",
        "qué patrones", "que patrones", "debería explorar", "deberia explorar",
        "menos conexiones", "evalúa", "evalua", "calidad del vault",
    )
    if any(r in t for r in RAZONAMIENTO):
        return "razonamiento_profundo", {"instruccion": texto, "archivos_relevantes": []}
    CONSULTA = (
        "cuántos conceptos", "cuantos conceptos", "qué conceptos hay", "que conceptos hay",
        "lista mis", "cuál es el más reciente", "cual es el mas reciente",
    )
    if any(c in t for c in CONSULTA):
        return "consulta_simple", {"instruccion": texto, "archivos_relevantes": []}
    FS_KEYWORDS = (
        # frases de acción
        "lista los archivos", "qué hay en", "que hay en",
        "lee el archivo", "crea una carpeta", "crea la carpeta",
        "mueve el", "mueve la", "elimina el", "elimina la",
        "borra el", "borra la", "busca en archivos", "busca en",
        # ubicaciones del sistema — señal suficiente para operacion_archivo
        "de wayta", "en wayta", "de downloads", "en downloads",
        "de descargas", "en descargas", "del escritorio", "en el escritorio",
        "del desktop", "en el desktop", "de la carpeta", "en la carpeta",
    )
    if any(k in t for k in FS_KEYWORDS):
        _fs_params = {"instruccion": texto, "archivos_relevantes": [],
                      "operacion": _inferir_operacion_archivo(t), "ruta": "", "archivo": "",
                      "destino": "", "query": "", "extension": "",
                      "accion": "describir", "foco": "", "titulo_candidato": ""}
        return "operacion_archivo", _fs_params

    MCP_HUERFANOS = ("conceptos huérfanos", "conceptos huerfanos", "no están conectados",
                     "no tienen links", "audita huérfanos", "audita huerfanos",
                     "qué conceptos están solos", "que conceptos estan solos")
    if any(k in t for k in MCP_HUERFANOS):
        return "auditar_huerfanos", {"instruccion": texto, "archivos_relevantes": [], "tag": "",
                                     "accion": "describir", "foco": "", "titulo_candidato": "",
                                     "operacion": "", "ruta": "", "archivo": "", "destino": "", "query": "", "extension": ""}

    MCP_TAG_KEYWORDS = ("conceptos con el tag", "busca por tag", "qué hay en el tag", "que hay en el tag",
                        "filtra por tag", "lista los de tag")
    for k in MCP_TAG_KEYWORDS:
        if k in t:
            tag_extraido = t.split(k)[-1].strip().split()[0] if t.split(k)[-1].strip() else ""
            return "buscar_por_tag", {"instruccion": texto, "archivos_relevantes": [], "tag": tag_extraido,
                                      "accion": "describir", "foco": "", "titulo_candidato": "",
                                      "operacion": "", "ruta": "", "archivo": "", "destino": "", "query": "", "extension": ""}

    VISION_KEYWORDS = (
        "qué estoy viendo", "que estoy viendo",
        "de qué trata esto", "de que trata esto",
        "explícame esto", "explicame esto",
        "qué hay en la pantalla", "que hay en la pantalla",
        "qué dice la pantalla", "que dice la pantalla",
        "qué estoy leyendo", "que estoy leyendo",
        "profundiza lo que estoy", "profundiza sobre lo que",
        "investiga más sobre esto", "investiga mas sobre esto",
        "guarda esto como concepto", "crea un concepto de esto",
        "captura esto", "esto me parece importante", "agrega esto al vault",
        "hay algo en el vault sobre esto", "tengo algo relacionado",
        "tengo un concepto sobre esto", "se relaciona con algo",
    )
    _vision_base = {"instruccion": texto, "archivos_relevantes": [],
                    "accion": "describir", "foco": "", "titulo_candidato": "",
                    "operacion": "", "ruta": "", "archivo": "", "destino": "", "query": "", "extension": ""}
    if any(k in t for k in VISION_KEYWORDS):
        if any(k in t for k in ("guarda esto", "crea un concepto de", "captura esto", "agrega esto al vault")):
            return "capturar_como_concepto", _vision_base
        if any(k in t for k in ("hay algo en el vault", "tengo algo relacionado", "tengo un concepto sobre", "se relaciona con")):
            return "relacionar_con_vault", _vision_base
        if any(k in t for k in ("profundiza", "investiga más", "investiga mas")):
            return "profundizar_pantalla", _vision_base
        return "ver_pantalla", _vision_base

    SINCRONIZAR = (
        "sincroniza el segundo cerebro", "sincroniza con la nube",
        "actualiza el vault", "trae los cambios", "sincroniza el vault",
        "actualiza desde el servidor",
    )
    if any(k in t for k in SINCRONIZAR):
        return "sincronizar_vault", {"instruccion": texto, "archivos_relevantes": [],
                                     "accion": "describir", "foco": "", "titulo_candidato": "",
                                     "operacion": "", "ruta": "", "archivo": "", "destino": "", "query": "", "extension": ""}

    RECORDAR = ("recuerda que", "no olvides que", "anota que")
    OLVIDAR = ("olvida que", "borra de tu memoria que")
    if any(k in t for k in RECORDAR) or any(k in t for k in OLVIDAR):
        accion = "olvidar" if any(k in t for k in OLVIDAR) else "agregar"
        hecho = texto
        for trig in (OLVIDAR if accion == "olvidar" else RECORDAR):
            if trig in t:
                hecho = texto[t.index(trig) + len(trig):].strip()
                break
        return "recordar_hecho", {"instruccion": texto, "archivos_relevantes": [],
                                  "accion": accion, "hecho": hecho, "foco": "", "titulo_candidato": "",
                                  "operacion": "", "ruta": "", "archivo": "", "destino": "", "query": "", "extension": ""}

    SUBIR_CAMBIOS = (
        "sube los cambios", "sincroniza hacia arriba", "push al servidor",
        "publica los cambios",
    )
    if any(k in t for k in SUBIR_CAMBIOS):
        return "subir_cambios", {"instruccion": texto, "archivos_relevantes": [],
                                 "accion": "describir", "foco": "", "titulo_candidato": "",
                                 "operacion": "", "ruta": "", "archivo": "", "destino": "", "query": "", "extension": ""}

    return "accion_directa", {"instruccion": texto, "archivos_relevantes": [],
                               "accion": "describir", "foco": "", "titulo_candidato": ""}


def detectar_intent(texto: str, historial: list[dict] | None = None) -> tuple[str, dict]:
    """Intenta Groq primero; si falla, usa keywords."""
    if historial is None:
        historial = []
    texto_normalizado = normalizar_texto(texto)
    if texto_normalizado != texto:
        print(f"[Normalización] '{texto}' → '{texto_normalizado}'")
    try:
        intent, params = detectar_intent_groq(texto_normalizado, historial)
        print(f"[Intent via Groq] {intent} | {params}")
        return intent, params
    except Exception as e:
        print(f"[Groq falló ({e}), usando keywords]")
        intent, params = detectar_intent_keywords(texto_normalizado)
        print(f"[Intent via keywords] {intent} | {params}")
        return intent, params


# ── Historial de sesión ────────────────────────────────────────────────────────

def actualizar_historial(texto_usuario: str, resultado_intent: tuple[str, dict]) -> None:
    """Agrega el turno al historial con ventana deslizante de 10 turnos."""
    intent, params = resultado_intent
    historial_sesion.append({"role": "user", "content": texto_usuario})
    historial_sesion.append({
        "role": "assistant",
        "content": f"Intent: {json.dumps({'intent': intent, 'params': params}, ensure_ascii=False)}",
    })
    while len(historial_sesion) > 20:
        historial_sesion.pop(0)
        historial_sesion.pop(0)


# ── Conversación casual — Groq ────────────────────────────────────────────────

def responder_con_groq(pregunta: str, historial: list[dict],
                       system_prompt_override: str | None = None) -> str:
    """Genera respuesta conversacional casual usando Groq."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "No tengo acceso a Groq en este momento."

    system_prompt = system_prompt_override or (
        "Eres Jarvis, asistente personal de Luigui. "
        "Tienes personalidad: directo, inteligente, algo irónico pero amable. "
        "Respondes en español, máximo 2 oraciones, tono conversacional natural. "
        "De vez en cuando llama al usuario por su nombre: Luigui. No en cada respuesta."
    )

    mensajes = [{"role": "system", "content": system_prompt}]
    mensajes += historial[-6:]
    mensajes += [{"role": "user", "content": pregunta}]

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": mensajes,
                "temperature": 0.3,
                "max_tokens": 150,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[Groq error] {e}")
        return "No pude responder en este momento."


# ── Memoria personal ──────────────────────────────────────────────────────────

def cargar_memoria() -> str:
    """Lee memoria.md para inyectar como contexto en Groq. Vacío si no existe aún."""
    if not MEMORIA_PATH.exists():
        return ""
    try:
        return MEMORIA_PATH.read_text(encoding="utf-8")
    except Exception as e:
        logging.warning(f"[Memoria] No se pudo leer memoria.md: {e}")
        return ""


# ── Consulta simple — carga contexto según pregunta ──────────────────────────

_LOG_KEYWORDS = ("hoy", "hicimos", "cambios", "actualizaciones", "historial", "hiciste", "resumen del día", "resumen del dia")

_ENCABEZADO_LOG = re.compile(r"^#{2,3} (\d{4}-\d{2}-\d{2})", re.MULTILINE)


def _parsear_periodo(instruccion: str):
    """Reconoce 'ayer'/'hoy'/'esta semana' en la instrucción y devuelve (desde, hasta)
    como objetos date. None si no hay período explícito — en ese caso
    cargar_contenido_vault_por_pregunta usa el comportamiento anterior (últimas 100 líneas)."""
    t = instruccion.lower()
    hoy = datetime.now().date()
    if "ayer" in t:
        ayer = hoy - timedelta(days=1)
        return (ayer, ayer)
    if "esta semana" in t or "última semana" in t or "ultima semana" in t:
        return (hoy - timedelta(days=7), hoy)
    if "hoy" in t:
        return (hoy, hoy)
    return None


def _filtrar_log_por_periodo(contenido: str, desde, hasta) -> str:
    """Filtra las entradas de JARVIS_LOG.md cuyo encabezado de fecha cae dentro de
    [desde, hasta] inclusive. Reconoce los dos formatos que coexisten en el archivo:
    '## YYYY-MM-DD HH:MM — TIPO' (registrar_en_jarvis_log) y '### YYYY-MM-DD — texto'
    (formato documentado en CLAUDE.md, usado por sesiones de Claude Code)."""
    matches = list(_ENCABEZADO_LOG.finditer(contenido))
    entradas = []
    for i, m in enumerate(matches):
        inicio = m.start()
        fin = matches[i + 1].start() if i + 1 < len(matches) else len(contenido)
        try:
            fecha = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        if desde <= fecha <= hasta:
            entradas.append(contenido[inicio:fin].strip())
    return "\n\n".join(entradas)


def cargar_contenido_vault_por_pregunta(instruccion: str) -> str:
    """Carga JARVIS_LOG.md si la pregunta es sobre historial/cambios — filtrado por
    período si se detecta uno explícito (ayer/hoy/esta semana), o las últimas 100
    líneas si no — o ATLAS.md si es sobre el índice de conceptos."""
    if any(k in instruccion.lower() for k in _LOG_KEYWORDS):
        log_path = CEREBRO_PATH / "JARVIS_LOG.md"
        logging.info(f"[Debug] Buscando JARVIS_LOG en: {log_path}")
        logging.info(f"[Debug] Existe: {log_path.exists()}")
        if not log_path.exists():
            logging.info("[Debug] Contenido cargado: VACÍO")
            return ""
        contenido_completo = log_path.read_text(encoding="utf-8")
        periodo = _parsear_periodo(instruccion)
        if periodo:
            desde, hasta = periodo
            filtrado = _filtrar_log_por_periodo(contenido_completo, desde, hasta)
            if not filtrado.strip():
                return f"No se encontró ninguna entrada registrada en JARVIS_LOG.md entre {desde} y {hasta}."
            logging.info(f"[Debug] Log filtrado por período {desde}..{hasta}: {len(filtrado)} chars")
            return filtrado
        lineas = contenido_completo.splitlines()
        contenido = "\n".join(lineas[-100:])
        logging.info(f"[Debug] Contenido cargado: {contenido[:100] if contenido else 'VACÍO'}")
        return contenido
    atlas_path = CEREBRO_PATH / "Conocimiento" / "ATLAS.md"
    if atlas_path.exists():
        return atlas_path.read_text(encoding="utf-8")[:4000]
    return ""


# ── Razonamiento profundo ─────────────────────────────────────────────────────

def cargar_contenido_para_razonamiento(archivos_relevantes: list[str]) -> str:
    """Carga hasta 3 archivos del vault como contexto para razonamiento (max 3000 chars c/u)."""
    base = CEREBRO_PATH / "Conocimiento"
    contenido = []

    for ruta in archivos_relevantes[:3]:
        if "/" not in ruta and not ruta.endswith(".md"):
            # Categoría simple: cargar los primeros 3 .md de esa subcarpeta
            categoria_path = base / "Conceptos" / ruta
            if categoria_path.exists():
                for f in list(categoria_path.glob("*.md"))[:3]:
                    texto = f.read_text(encoding="utf-8")[:3000]
                    contenido.append(f"### {f.stem}\n{texto}")
        elif ruta.rstrip("/").endswith("**") or ruta.endswith("/"):
            dir_name = ruta.rstrip("/**").rstrip("/")
            dir_path = base / dir_name
            if dir_path.exists():
                for f in list(dir_path.glob("*.md"))[:3]:
                    texto = f.read_text(encoding="utf-8")[:3000]
                    contenido.append(f"### {f.stem}\n{texto}")
        else:
            matches = list(base.glob(f"**/{ruta}"))
            if matches:
                texto = matches[0].read_text(encoding="utf-8")[:3000]
                contenido.append(texto)

    if not contenido:
        atlas = base / "ATLAS.md"
        if atlas.exists():
            contenido.append(atlas.read_text(encoding="utf-8")[:3000])

    return "\n\n---\n\n".join(contenido)


# ── Acciones — Claude Code ─────────────────────────────────────────────────────

def ejecutar_claude(instruccion: str) -> str:
    """Ejecuta claude CLI con la instrucción y devuelve el output."""
    if not _claude_disponible():
        # Nunca sys.exit aquí: esta función corre dentro de threads del daemon,
        # no en un proceso standalone — un exit mataría el proceso completo.
        raise RuntimeError("Claude Code CLI no está disponible.")

    env_limpia = {k: v for k, v in os.environ.items()
                  if not k.startswith(("CLAUDE", "CURSOR_SPAWN"))}
    resultado = subprocess.run(
        ["claude", "--print", instruccion],
        cwd=str(CEREBRO_PATH),
        capture_output=True,
        text=True,
        timeout=600,
        env=env_limpia,
    )
    return resultado.stdout or resultado.stderr


_AUDIT_MARKERS = (
    "auditoría", "auditoria", "conceptos activos", "borrador", "rechazado"
)

_AUDIT_CRITICOS = (
    "rechazado", "falla", "error", "advertencia", "normaliz", "sin fuente", "gate"
)


def _resumir_auditoria(output: str) -> str:
    """Construye respuesta de voz concisa a partir de un output de auditoría."""
    import re
    lineas = output.splitlines()

    activos = borradores = correlaciones = None
    for linea in lineas:
        l = linea.lower()
        m = re.search(r"(\d+)\s+conceptos?\s+activos?", l)
        if m:
            activos = m.group(1)
        m = re.search(r"(\d+)\s+(?:en\s+)?borrador", l)
        if m:
            borradores = m.group(1)
        m = re.search(r"(\d+)\s+correlaciones?", l)
        if m:
            correlaciones = m.group(1)

    nums = []
    if activos:
        nums.append(f"{activos} conceptos activos")
    if borradores:
        nums.append(f"{borradores} en borrador")
    if correlaciones:
        nums.append(f"{correlaciones} correlaciones documentadas")

    partes = ["Auditoría completada."]
    if nums:
        partes.append(", ".join(nums) + ".")

    for linea in lineas:
        l = linea.strip()
        if any(k in l.lower() for k in _AUDIT_CRITICOS) and len(l) > 15:
            l = re.sub(r"[*_`#|>\-]", "", l).strip()
            if l:
                partes.append(l[:150] + ("." if not l.endswith(".") else ""))
                break

    return " ".join(partes)


def resumir_output_para_voz(output: str, max_chars: int = 600) -> str:
    """Extrae una respuesta apta para TTS del output de Claude Code."""
    if any(k in output.lower() for k in _AUDIT_MARKERS):
        return _resumir_auditoria(output)

    SKIP_PREFIXES = ("```", "---", "##", "**", "• ", "- ", "* ", "> ", "|")
    lineas = [
        l.strip() for l in output.splitlines()
        if l.strip()
        and not any(l.strip().startswith(p) for p in SKIP_PREFIXES)
        and len(l.strip()) > 10
    ]
    if not lineas:
        return "Listo."
    texto = " ".join(lineas)
    if len(texto) <= max_chars:
        return texto
    truncado = texto[:max_chars]
    ultimo_punto = max(truncado.rfind("."), truncado.rfind("!"), truncado.rfind("?"))
    if ultimo_punto > max_chars // 2:
        return truncado[:ultimo_punto + 1]
    return truncado.rstrip() + "."


def _claude_disponible() -> bool:
    return subprocess.run(["which", "claude"], capture_output=True).returncode == 0


# ── Log ────────────────────────────────────────────────────────────────────────

def registrar_en_jarvis_log(tipo: str, instruccion: str, resultado: str) -> None:
    log_path = CEREBRO_PATH / "JARVIS_LOG.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entrada = f"\n## {timestamp} — {tipo}\n**Instrucción:** {instruccion}\n**Resultado:** {resultado}\n"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entrada)
    except Exception as e:
        logging.warning(f"No se pudo escribir en JARVIS_LOG: {e}")


# ── Dispatch central (usado por main() y por jarvis_daemon.py) ────────────────

# Callback invocado justo después de la última hablar() de cada respuesta.
_response_complete_callback: "callable | None" = None

# Flag que señala al daemon que debe salir del modo escucha activa.
_salir_escucha: list[bool] = [False]


def _contexto_archivo_si_referenciado(texto: str) -> str | None:
    """Retorna el contenido del último archivo leído si el texto lo referencia."""
    if _ultimo_archivo_leido["contenido"] is None:
        return None
    if any(ref in texto.lower() for ref in _CONTEXT_REFS):
        return _ultimo_archivo_leido["contenido"]
    return None


def _ultimo_slug_de_historial() -> str | None:
    """Busca en el historial de sesión el slug más reciente mencionado por Jarvis.
    Útil cuando el usuario dice 'léelo' sin especificar archivo después de una consulta."""
    conceptos_path = CEREBRO_PATH / "Conocimiento" / "Conceptos"
    slugs_vault = {
        p.stem for p in conceptos_path.rglob("*.md")
    }
    # Recorrer historial en reversa buscando slugs en las respuestas de Jarvis
    for entrada in reversed(historial_sesion):
        if entrada.get("role") != "assistant":
            continue
        contenido = entrada.get("content", "").lower()
        for slug in slugs_vault:
            if slug in contenido:
                return slug
    return None


def despachar_intent(intent: str, params: dict, texto_transcrito: str, vision_callback=None) -> None:
    """Ejecuta la acción y al terminar dispara _response_complete_callback.
    Defensa en profundidad: ningún error dentro de _despachar_intent_impl (ni siquiera
    uno inesperado en un intent futuro) puede tumbar el proceso del daemon completo."""
    print(f"[Dispatch] intent='{intent}' | fs_disponible={_filesystem_disponible} | params={params}", flush=True)
    try:
        _despachar_intent_impl(intent, params, texto_transcrito, vision_callback=vision_callback)
    except Exception as e:
        print(f"[Dispatch] ERROR no manejado en intent '{intent}': {e}", flush=True)
        logging.exception(f"[Dispatch] ERROR no manejado en intent '{intent}'")
        try:
            hablar("Hubo un error al procesar ese comando, Luigui.")
        except Exception:
            pass
    emitir_evento("idle", "Esperando wake word...")
    if _response_complete_callback:
        import time
        logging.info("[Timer] Callback registrado — reiniciando deadline.")
        _response_complete_callback()
        logging.info(f"[Timer] Deadline reiniciado (now={time.time():.0f})")
    else:
        logging.info("[Timer] _response_complete_callback es None.")


def _despachar_intent_impl(intent: str, params: dict, texto_transcrito: str, vision_callback=None) -> None:
    instruccion = params.get("instruccion", texto_transcrito)

    CAPACIDADES_TRIGGERS = (
        "qué puedes hacer", "que puedes hacer",
        "qué sabes hacer", "que sabes hacer",
        "cuáles son tus capacidades", "cuales son tus capacidades",
        "para qué sirves", "para que sirves",
    )
    if any(t in instruccion.lower() for t in CAPACIDADES_TRIGGERS):
        hablar(
            "Puedo ayudarte con tu Segundo Cerebro de tres formas: "
            "responder preguntas sobre tus conceptos, analizar y razonar sobre el vault "
            "con Groq, y ejecutar acciones como crear conceptos, correlacionar o "
            "auditar el vault con Claude Code."
        )
        return

    if intent == "despedirse":
        hablar("Hasta luego, Luigui. Di Jarvis cuando me necesites.")
        _salir_escucha[0] = True
        return

    if intent == "conversacion_libre":
        mensaje = params.get("mensaje") or instruccion
        emitir_evento("procesando", "Consultando Groq...")
        _memoria = cargar_memoria()
        _system_conv = (
            "Eres Jarvis, asistente personal de Luigui. "
            "Tienes personalidad: directo, inteligente, algo irónico pero amable. "
            "Respondes en español, máximo 2 oraciones, tono conversacional natural. "
            "De vez en cuando llama al usuario por su nombre: Luigui. No en cada respuesta."
            + (f"\n\nMEMORIA — hechos y preferencias conocidas de Luigui (úsalos si son relevantes, no los repitas sin que venga a cuento):\n{_memoria}" if _memoria.strip() else "")
        )
        respuesta = responder_con_groq(mensaje, historial_sesion, system_prompt_override=_system_conv)
        print(f"[Conversación] {respuesta}")
        emitir_evento("respondiendo", respuesta[:80])
        hablar_respuesta(respuesta)
        actualizar_historial(texto_transcrito, (intent, {"respuesta": respuesta}))
        if vision_callback:
            vision_callback(respuesta)
        return

    if intent == "consulta_simple":
        emitir_evento("procesando", instruccion[:60])
        hablar("Un momento.")
        atlas = cargar_contenido_vault_por_pregunta(instruccion)
        _ctx = _contexto_archivo_si_referenciado(instruccion)
        _memoria = cargar_memoria()
        system = (
            "Eres Jarvis, asistente del Segundo Cerebro de Luigui. "
            "Responde en español, máximo 3 oraciones, sin bullets ni listas — "
            "la respuesta se leerá en voz alta.\n\n"
            f"ÍNDICE DEL VAULT:\n{atlas}"
            + (f"\n\nARCHIVO LEÍDO RECIENTEMENTE (úsalo si el usuario lo referencia):\n{_ctx[:3000]}" if _ctx else "")
            + (f"\n\nMEMORIA — hechos y preferencias conocidas de Luigui:\n{_memoria}" if _memoria.strip() else "")
        )
        respuesta = responder_con_groq(instruccion, historial_sesion, system_prompt_override=system)
        print(f"[Consulta] {respuesta}")
        emitir_evento("respondiendo", respuesta[:80])
        hablar_respuesta(respuesta)
        registrar_en_jarvis_log("CONSULTA", instruccion, respuesta)
        if vision_callback:
            vision_callback(respuesta)
        return

    if intent == "razonamiento_profundo":
        emitir_evento("procesando", instruccion[:60])
        hablar("Analizando el vault, dame un momento.")
        archivos = params.get("archivos_relevantes", [])
        contenido = cargar_contenido_para_razonamiento(archivos)
        _ctx = _contexto_archivo_si_referenciado(instruccion)
        if _ctx:
            contenido = f"ARCHIVO LEÍDO RECIENTEMENTE:\n{_ctx[:3000]}\n\n---\n\n{contenido}"
        system = (
            "Eres Jarvis. Responde en español, máximo 3 oraciones, sin bullets. "
            "La respuesta se leerá en voz alta.\n\n"
            f"CONTEXTO DEL VAULT:\n{contenido}"
        )
        respuesta = responder_con_groq(instruccion, historial_sesion, system_prompt_override=system)
        print(f"[Razonamiento] {respuesta}")
        emitir_evento("respondiendo", respuesta[:80])
        hablar_respuesta(respuesta)
        registrar_en_jarvis_log("RAZONAMIENTO", instruccion, respuesta)
        if vision_callback:
            vision_callback(respuesta)
        return

    if intent == "operacion_archivo":
        if not _filesystem_disponible:
            hablar("El módulo de filesystem no está disponible.")
            return
        # Si es una lectura sin archivo especificado, intentar recuperar del historial o contexto
        _operacion_raw = params.get("operacion", "").strip().lower()
        if _operacion_raw in ("leer", "lee", "read", "mostrar", "abre"):
            _archivo_raw = (params.get("archivo", "") or "").strip()
            _ruta_raw = (params.get("ruta", "") or "").strip()
            if not _archivo_raw and not _ruta_raw:
                # Buscar el último slug de vault mencionado en el historial de sesión
                _slug_recuperado = _ultimo_slug_de_historial()
                if _slug_recuperado:
                    params = dict(params, archivo=_slug_recuperado, ruta="conceptos")
                    print(f"[FS] Léelo sin contexto → recuperado del historial: {_slug_recuperado}", flush=True)
                elif _ultimo_archivo_leido["ruta"]:
                    print(f"[FS] Léelo sin contexto → reutilizando último leído: {_ultimo_archivo_leido['ruta']}", flush=True)
                    hablar_respuesta(_ultimo_archivo_leido["contenido"] or "No hay archivo en contexto.")
                    return
                else:
                    hablar("No sé qué concepto leer. Dime el nombre del concepto.")
                    return
        emitir_evento("procesando", instruccion[:60])
        print("[FS] Llamando operacion_archivo con params:", params, flush=True)
        try:
            resultado = _operacion_archivo(params)
            print("[FS] Resultado:", repr(resultado), flush=True)
        except Exception as _fs_err:
            print("[FS] ERROR:", _fs_err, flush=True)
            import traceback
            traceback.print_exc()
            hablar("Error en el módulo de filesystem.")
            return
        _operacion = params.get("operacion", "").strip().lower()
        _es_lectura = _operacion in ("leer", "lee", "read", "mostrar", "abre")

        if _es_lectura:
            emitir_evento("respondiendo", instruccion[:80])
            hablar_respuesta(resultado)
            # Bug 3: guardar contexto si la lectura fue exitosa (no es un mensaje de error)
            _es_error = resultado.startswith(
                ("El archivo", "No puedo", "Error al", "La ruta", "No encontré", "'")
            )
            if not _es_error:
                _ruta_leida = "/".join(filter(None, [
                    params.get("ruta", ""), params.get("archivo", "")
                ]))
                _ultimo_archivo_leido["ruta"] = _ruta_leida or instruccion
                _ultimo_archivo_leido["contenido"] = resultado
                print(f"[Contexto] Archivo guardado en sesión: {_ultimo_archivo_leido['ruta']}")
        elif len(resultado) <= 180:
            emitir_evento("respondiendo", resultado[:80])
            hablar(resultado)
        else:
            system = (
                "Eres Jarvis. Resume el siguiente resultado de una operación de filesystem "
                "en máximo 2 oraciones en español, sin bullets ni listas, apto para TTS.\n\n"
                f"RESULTADO:\n{resultado[:3000]}"
            )
            resumen = responder_con_groq(instruccion, historial_sesion, system_prompt_override=system)
            emitir_evento("respondiendo", resumen[:80])
            hablar_respuesta(resumen)
        registrar_en_jarvis_log("FILESYSTEM", instruccion, resultado[:200])
        if vision_callback:
            vision_callback(resultado)
        return

    if intent == "ver_pantalla":
        if not _vision_pantalla_disponible:
            hablar("El módulo de visión de pantalla no está disponible.")
            return
        emitir_evento("procesando", "Leyendo pantalla...")
        hablar("Un momento, voy a ver qué estás leyendo.")
        resultado = _ver_pantalla(params)
        if _es_error_vision(resultado):
            hablar(resultado)
            return
        emitir_evento("procesando", "Consultando Groq...")
        respuesta = responder_con_groq(resultado, historial_sesion)
        print(f"[Vision] {respuesta}")
        emitir_evento("respondiendo", respuesta[:80])
        hablar_respuesta(respuesta)
        registrar_en_jarvis_log("VISION", instruccion, respuesta[:200])
        if vision_callback:
            vision_callback(respuesta)
        return

    if intent == "profundizar_pantalla":
        if not _vision_pantalla_disponible:
            hablar("El módulo de visión de pantalla no está disponible.")
            return
        emitir_evento("procesando", "Leyendo pantalla...")
        hablar("Un momento, leo lo que tienes en pantalla.")
        prompt = _profundizar_pantalla(params)
        if _es_error_vision(prompt):
            hablar(prompt)
            return
        hablar("Profundizando lo que estás leyendo. Revisa Claude Code en un momento.")
        emitir_evento("ejecutando", instruccion[:60])
        try:
            output = ejecutar_claude(prompt)
            resumen = resumir_output_para_voz(output)
        except subprocess.TimeoutExpired:
            hablar("Claude tardó demasiado al profundizar.")
            registrar_en_jarvis_log("VISION", instruccion, "TIMEOUT")
            return
        except RuntimeError:
            hablar("Claude Code no está disponible, Luigui.")
            registrar_en_jarvis_log("VISION", instruccion, "ERROR: Claude Code no disponible")
            return
        except Exception as e:
            hablar("Hubo un error al profundizar el concepto.")
            print(f"[Vision error] {e}")
            registrar_en_jarvis_log("VISION", instruccion, f"ERROR: {e}")
            return
        print(f"[Vision profundizar] {resumen}")
        emitir_evento("respondiendo", resumen[:80] if resumen else "Listo.")
        hablar_respuesta(resumen if resumen else "Listo, Luigui.")
        registrar_en_jarvis_log("VISION", instruccion, resumen[:200] if resumen else "OK")
        if vision_callback:
            vision_callback(resumen or "")
        return

    if intent == "capturar_como_concepto":
        if not _vision_pantalla_disponible:
            hablar("El módulo de visión de pantalla no está disponible.")
            return
        emitir_evento("procesando", "Leyendo pantalla...")
        hablar("Un momento, leo el contenido.")
        prompt = _capturar_como_concepto(params)
        if _es_error_vision(prompt):
            hablar(prompt)
            return
        hablar("Generando el concepto. Revisa Claude Code para aprobarlo.")
        emitir_evento("ejecutando", instruccion[:60])
        try:
            output = ejecutar_claude(prompt)
            resumen = resumir_output_para_voz(output)
        except subprocess.TimeoutExpired:
            hablar("Claude tardó demasiado al generar el concepto.")
            registrar_en_jarvis_log("VISION", instruccion, "TIMEOUT")
            return
        except RuntimeError:
            hablar("Claude Code no está disponible, Luigui.")
            registrar_en_jarvis_log("VISION", instruccion, "ERROR: Claude Code no disponible")
            return
        except Exception as e:
            hablar("Hubo un error al generar el concepto.")
            print(f"[Vision error] {e}")
            registrar_en_jarvis_log("VISION", instruccion, f"ERROR: {e}")
            return
        print(f"[Vision capturar] {resumen}")
        emitir_evento("respondiendo", resumen[:80] if resumen else "Listo.")
        hablar_respuesta(resumen if resumen else "Concepto listo, Luigui.")
        registrar_en_jarvis_log("VISION", instruccion, resumen[:200] if resumen else "OK")
        if vision_callback:
            vision_callback(resumen or "")
        return

    if intent == "relacionar_con_vault":
        if not _vision_pantalla_disponible:
            hablar("El módulo de visión de pantalla no está disponible.")
            return
        emitir_evento("procesando", "Leyendo pantalla...")
        hablar("Un momento, busco conexiones con el vault.")
        resultado = _relacionar_con_vault(params)
        if _es_error_vision(resultado):
            hablar(resultado)
            return
        emitir_evento("procesando", "Consultando Groq...")
        respuesta = responder_con_groq(resultado, historial_sesion)
        print(f"[Vision vault] {respuesta}")
        emitir_evento("respondiendo", respuesta[:80])
        hablar_respuesta(respuesta)
        registrar_en_jarvis_log("VISION", instruccion, respuesta[:200])
        if vision_callback:
            vision_callback(respuesta)
        return

    if intent == "auditar_huerfanos":
        from mejora_009_mcp import detectar_huerfanos
        huerfanos = detectar_huerfanos()
        if not huerfanos:
            hablar("Todos los conceptos tienen al menos un backlink. El vault está bien conectado.")
        else:
            hablar_respuesta(f"Encontré {len(huerfanos)} conceptos huérfanos. Los primeros son: {', '.join(huerfanos[:5])}")
        return

    if intent == "buscar_por_tag":
        tag = params.get("tag", "")
        from mejora_009_mcp import buscar_por_tag
        resultados = buscar_por_tag(tag)
        hablar_respuesta(f"Encontré {len(resultados)} conceptos con el tag {tag}: {', '.join(resultados[:5])}")
        return

    if intent == "sincronizar_vault":
        emitir_evento("procesando", "Sincronizando vault...")
        hablar("Sincronizando actualizaciones del servidor online...")
        _git_env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        try:
            subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "fetch", "origin", "main"],
                capture_output=True, text=True, timeout=30, check=True,
                stdin=subprocess.DEVNULL, env=_git_env,
            )
            diff = subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "diff", "--name-only", "HEAD", "origin/main"],
                capture_output=True, text=True, timeout=10, check=True,
                stdin=subprocess.DEVNULL,
            )
            archivos_remotos = [f.strip() for f in diff.stdout.splitlines() if f.strip()]
            pull = subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "pull", "origin", "main"],
                capture_output=True, text=True, timeout=60,
                stdin=subprocess.DEVNULL, env=_git_env,
            )
            if pull.returncode != 0:
                hablar("Hubo un problema al sincronizar, Luigui. Revisa la conexión.")
                registrar_en_jarvis_log("SYNC", instruccion, f"ERROR pull: {pull.stderr[:100]}")
                return
            if archivos_remotos:
                slugs = [Path(f).stem for f in archivos_remotos]
                n = len(slugs)
                lista = ", ".join(slugs[:5]) + ("..." if n > 5 else "")
                hablar(f"Listo Luigui, segundo cerebro actualizado. Se agregaron {n} archivos: {lista}.")
            else:
                hablar("El segundo cerebro ya estaba al día, Luigui.")
            registrar_en_jarvis_log("SYNC", instruccion, f"{len(archivos_remotos)} archivos actualizados")
        except subprocess.TimeoutExpired:
            hablar("Hubo un problema al sincronizar, Luigui. Revisa la conexión.")
            registrar_en_jarvis_log("SYNC", instruccion, "TIMEOUT")
        except Exception as e:
            hablar("Hubo un problema al sincronizar, Luigui. Revisa la conexión.")
            registrar_en_jarvis_log("SYNC", instruccion, f"ERROR: {e}")
        return

    if intent == "subir_cambios":
        emitir_evento("procesando", "Subiendo cambios...")
        _git_env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        try:
            status = subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "status", "--porcelain"],
                capture_output=True, text=True, timeout=15,
                stdin=subprocess.DEVNULL,
            )
            if not status.stdout.strip():
                hablar("No había cambios pendientes.")
                registrar_en_jarvis_log("SYNC", instruccion, "Sin cambios pendientes")
                return

            hablar("Subiendo los cambios al servidor...")
            subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "add", "-A"],
                capture_output=True, text=True, timeout=15,
                stdin=subprocess.DEVNULL,
            )
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            # Sin check=True: si el watcher ya commiteó estos mismos cambios en una
            # carrera (serializada por lock_interaccion pero posible entre invocaciones),
            # "nothing to commit" no es un error real — seguimos al pull/push igual.
            subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "commit", "-m", f"feat: cambios via Jarvis {timestamp}"],
                capture_output=True, text=True, timeout=15,
                stdin=subprocess.DEVNULL,
            )

            pull = subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "pull", "--rebase", "origin", "main"],
                capture_output=True, text=True, timeout=30,
                stdin=subprocess.DEVNULL, env=_git_env,
            )
            if pull.returncode != 0:
                subprocess.run(
                    ["git", "-C", str(CEREBRO_PATH), "rebase", "--abort"],
                    capture_output=True, text=True, timeout=10,
                    stdin=subprocess.DEVNULL,
                )
                hablar("Hubo un problema al subir los cambios. Revisa la conexión.")
                registrar_en_jarvis_log("SYNC", instruccion, f"ERROR pull --rebase: {pull.stderr[:150]}")
                return

            push = subprocess.run(
                ["git", "-C", str(CEREBRO_PATH), "push", "origin", "main"],
                capture_output=True, text=True, timeout=30,
                stdin=subprocess.DEVNULL, env=_git_env,
            )
            if push.returncode != 0:
                hablar("Hubo un problema al subir los cambios. Revisa la conexión.")
                registrar_en_jarvis_log("SYNC", instruccion, f"ERROR push: {push.stderr[:150]}")
                return

            hablar("Listo, cambios subidos al servidor.")
            registrar_en_jarvis_log("SYNC", instruccion, "Cambios subidos correctamente")
        except subprocess.TimeoutExpired:
            hablar("Hubo un problema al subir los cambios. Revisa la conexión.")
            registrar_en_jarvis_log("SYNC", instruccion, "TIMEOUT")
        except Exception as e:
            hablar("Hubo un problema al subir los cambios. Revisa la conexión.")
            registrar_en_jarvis_log("SYNC", instruccion, f"ERROR: {e}")
        return

    if intent == "recordar_hecho":
        accion = params.get("accion", "agregar")
        hecho = (params.get("hecho") or "").strip()
        if not hecho:
            hablar("No entendí qué querías que recuerde, Luigui.")
            return
        try:
            if MEMORIA_PATH.exists():
                contenido_actual = MEMORIA_PATH.read_text(encoding="utf-8")
            else:
                contenido_actual = (
                    "# Memoria de Jarvis — Luigui Avila\n\n"
                    "> Actualizado automáticamente. Jarvis carga este archivo en cada sesión.\n\n"
                    "## Hechos personales\n\n## Preferencias\n\n## Notas de contexto\n"
                )

            if accion == "agregar":
                hoy = datetime.now().strftime("%Y-%m-%d")
                marcador = "## Hechos personales"
                idx = contenido_actual.find(marcador)
                if idx == -1:
                    nuevo_contenido = contenido_actual.rstrip() + f"\n\n{marcador}\n- [{hoy}] {hecho}\n"
                else:
                    fin_seccion = contenido_actual.find("\n## ", idx + len(marcador))
                    if fin_seccion == -1:
                        fin_seccion = len(contenido_actual)
                    antes = contenido_actual[:fin_seccion].rstrip()
                    despues = contenido_actual[fin_seccion:]
                    nuevo_contenido = antes + f"\n- [{hoy}] {hecho}\n" + despues
                MEMORIA_PATH.write_text(nuevo_contenido, encoding="utf-8")
                hablar("Anotado, lo recordaré.")
                registrar_en_jarvis_log("MEMORIA", instruccion, f"Agregado: {hecho}")
            else:
                # "Olvidar": se le pide a Groq solo la línea exacta a borrar (no el archivo
                # completo — responder_con_groq trunca a max_tokens=150, insuficiente para
                # devolver memoria.md entero). Se borra por coincidencia exacta en Python,
                # nunca reescribiendo el resto del archivo.
                prompt_olvidar = (
                    f"Estas son las líneas de memoria.md de Jarvis:\n{contenido_actual}\n\n"
                    f"El usuario pidió olvidar este dato: \"{hecho}\"\n\n"
                    "Responde ÚNICAMENTE con la línea EXACTA (tal como aparece en el archivo, "
                    "empezando con '- [') que corresponde a ese dato. Si ninguna línea corresponde, "
                    "responde exactamente: NINGUNA"
                )
                linea = responder_con_groq(prompt_olvidar, [], system_prompt_override=(
                    "Eres un asistente que identifica líneas exactas dentro de un archivo de texto. "
                    "Responde solo con la línea pedida o la palabra NINGUNA — sin explicaciones, sin comillas."
                )).strip()
                if linea and linea != "NINGUNA" and linea in contenido_actual:
                    nuevo_contenido = contenido_actual.replace(linea + "\n", "", 1)
                    if nuevo_contenido == contenido_actual:
                        nuevo_contenido = contenido_actual.replace(linea, "", 1)
                    MEMORIA_PATH.write_text(nuevo_contenido, encoding="utf-8")
                    hablar("Listo, lo olvidé.")
                    registrar_en_jarvis_log("MEMORIA", instruccion, f"Olvidado: {linea}")
                else:
                    hablar("No encontré eso en mi memoria, Luigui.")
                    registrar_en_jarvis_log("MEMORIA", instruccion, f"No encontrado para olvidar: {hecho}")
        except Exception as e:
            hablar("Hubo un problema al actualizar mi memoria, Luigui.")
            registrar_en_jarvis_log("MEMORIA", instruccion, f"ERROR: {e}")
        return

    # accion_directa (y vault_accion como alias para compatibilidad)
    emitir_evento("ejecutando", instruccion[:60])
    hablar("Dame un momento, Luigui.")
    _AUDIT_KEYWORDS = ("audita", "auditar", "corrige", "corregir", "evalúa", "evaluar", "revisa", "tag", "tags")
    _es_auditoria = any(k in instruccion.lower() for k in _AUDIT_KEYWORDS)
    _criterio_tags = (
        "\n\nCRITERIO PARA TAGS NO NORMALIZADOS:"
        "\n- Si el tag es demasiado específico o ya está cubierto por conceptos relacionados existentes → eliminar."
        "\n- Si el tag representa una dimensión temática nueva que podría agrupar 2 o más conceptos futuros → "
        "proponer añadirlo al vocabulario controlado en Plantillas/taxonomia.md y conservarlo en el concepto actual."
        "\nEl reporte debe incluir una sección 'Tags propuestos para vocabulario controlado: [lista]' "
        "con justificación de por qué cada tag merece ser añadido."
    ) if _es_auditoria else ""
    _ctx = _contexto_archivo_si_referenciado(instruccion)
    _ctx_prefix = (
        f"\n\nContexto — archivo leído recientemente ({_ultimo_archivo_leido['ruta']}):\n"
        f"{_ctx[:2000]}\n"
    ) if _ctx else ""
    cmd = (
        f"Responde en español. Si es una pregunta o consulta, responde en máximo 3 oraciones "
        f"sin bullets ni listas — la respuesta se leerá en voz alta. "
        f"Si es una acción sobre el vault, ejecútala y confirma en 1-2 oraciones qué hiciste."
        f"{_criterio_tags}"
        f"{_ctx_prefix} "
        f"Instrucción de voz de Luigui: \"{texto_transcrito}\""
    )
    try:
        output = ejecutar_claude(f"Jarvis, {cmd}")
        resumen = resumir_output_para_voz(output)
    except subprocess.TimeoutExpired:
        hablar("Claude tardó demasiado. Revisa la terminal, Luigui.")
        registrar_en_jarvis_log("ACCION", texto_transcrito, "TIMEOUT")
        return
    except RuntimeError:
        hablar("Claude Code no está disponible, Luigui.")
        registrar_en_jarvis_log("ACCION", texto_transcrito, "ERROR: Claude Code no disponible")
        return
    except Exception as e:
        hablar("Hubo un error al ejecutar el comando.")
        print(f"[Error] {e}")
        registrar_en_jarvis_log("ACCION", texto_transcrito, f"ERROR: {e}")
        return

    print(f"[Claude output] {resumen}")
    emitir_evento("respondiendo", resumen[:80] if resumen else "Listo.")
    hablar_respuesta(resumen if resumen else "Listo, Luigui.")
    registrar_en_jarvis_log("ACCION", texto_transcrito, resumen)
    if vision_callback:
        vision_callback(resumen or "")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=== Jarvis — Segundo Cerebro ===")
    hablar("Jarvis listo. ¿Qué necesitas?")

    texto_transcrito = escuchar()
    if texto_transcrito is None:
        return

    intent, params = detectar_intent(texto_transcrito, historial_sesion)
    print(f"[Intent] {intent} | [Params] {params}")
    actualizar_historial(texto_transcrito, (intent, params))
    despachar_intent(intent, params, texto_transcrito)


if __name__ == "__main__":
    main()
