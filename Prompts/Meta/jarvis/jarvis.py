#!/usr/local/bin/python3.11
"""
jarvis.py — Interfaz de voz para el Segundo Cerebro

Arquitectura: STT → clasificación en 5 intents → tres carriles:
  - conversacion_libre / despedirse → Groq directo
  - consulta_simple → Groq con contexto de ATLAS.md
  - accion_directa → Claude Code
  - razonamiento_profundo → Ollama (Qwen2.5:14b) lee vault y razona
"""

import json
import logging
import os
import requests
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"

# Historial de sesión en memoria — ventana deslizante de 10 turnos (20 mensajes)
historial_sesion: list[dict] = []


# ── TTS ────────────────────────────────────────────────────────────────────────

def hablar(texto: str) -> None:
    """Convierte texto a voz usando pyttsx3 con voz Monica."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.voice.compact.es-ES.Monica')
        engine.setProperty('rate', 175)
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS] {texto}")
        print(f"[TTS error] {e}")


# ── STT ────────────────────────────────────────────────────────────────────────

def escuchar() -> str | None:
    """Captura audio del micrófono y devuelve el texto transcrito (o None si falla)."""
    try:
        import speech_recognition as sr
    except ImportError:
        hablar("Falta la librería speech_recognition.")
        return None

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Escuchando... (habla ahora)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
    except AttributeError:
        hablar("Micrófono no disponible.")
        return None
    except Exception as e:
        hablar("No pude acceder al micrófono.")
        print(f"[Micrófono error] {e}")
        return None

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        texto_transcrito = texto.lower()
        print(f"[Transcripción] {texto_transcrito}")
        logging.info(f"Transcripción: {texto_transcrito}")
        return texto_transcrito
    except Exception:
        hablar("No entendí lo que dijiste. Intenta de nuevo.")
        return None


# ── Normalización de texto (correcciones de STT) ─────────────────────────────

def normalizar_texto(texto: str) -> str:
    """Corrige errores frecuentes del STT antes de clasificar."""
    reemplazos = {
        "baúl": "vault",
        "baul": "vault",
        "ball": "vault",
        "bal ": "vault",
    }
    texto_lower = texto.lower()
    for error, correcto in reemplazos.items():
        texto_lower = texto_lower.replace(error, correcto)
    return texto_lower


# ── Clasificación binaria — Groq ──────────────────────────────────────────────

def detectar_intent_groq(texto: str, historial: list[dict], indice_vault: str) -> tuple[str, dict]:
    """Clasifica en conversacion_libre | despedirse | consulta_simple | accion_directa | razonamiento_profundo."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no disponible.")

    system_prompt = """Eres el clasificador de Jarvis, asistente de voz del Segundo Cerebro de Luigui.

Clasifica el mensaje en UNA de estas cinco categorías:

conversacion_libre: saludo, pregunta personal a Jarvis, comentario casual que NO involucra el vault.
  Ejemplos: "cómo estás", "qué hora es", "gracias", "muy bien".

despedirse: el usuario quiere terminar la sesión de escucha activa.
  Ejemplos: "bye", "hasta luego", "ya terminé", "modo espera", "para", "descansa", "chau".

consulta_simple: pregunta factual sobre el vault respondible con el índice (cuántos conceptos hay, qué categorías existen, cuáles son los slugs).
  Ejemplos: "cuántos conceptos tengo", "qué conceptos hay en producto", "lista mis correlaciones", "cuál es el más reciente".

accion_directa: instrucción que modifica el vault o ejecuta una tarea concreta.
  Ejemplos: "crea un concepto sobre X", "correlaciona X con Y", "audita el vault", "profundiza X", "procesa esta fuente".

razonamiento_profundo: análisis, evaluación o recomendaciones que requieren leer el contenido completo de los conceptos, no solo el índice.
  Ejemplos: "qué correlaciones me faltan", "cuál es el concepto más débil", "qué patrones ves en mis conceptos de IA",
  "qué debería explorar próximamente", "qué concepto tiene menos conexiones", "evalúa la calidad del vault".

Responde ÚNICAMENTE con JSON válido:
{"intent": "<categoria>", "instruccion": "<texto literal del usuario>", "archivos_relevantes": ["<categoria_o_ruta>"]}

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
    data = json.loads(response.json()["choices"][0]["message"]["content"])
    intent = data.get("intent", "accion_directa")
    params = {
        "instruccion": data.get("instruccion", texto),
        "archivos_relevantes": data.get("archivos_relevantes", []),
    }
    # Compatibilidad con formato anterior (conversacion_libre usa "mensaje")
    if intent == "conversacion_libre":
        params["mensaje"] = params["instruccion"]
    return intent, params


def detectar_intent_keywords(texto: str) -> tuple[str, dict]:
    """Fallback si Groq no está disponible: clasificación por keywords."""
    t = texto.lower()
    DESPEDIDAS_FRASES = ("hasta luego", "ya terminé", "ya termine", "modo espera", "te hablo luego")
    DESPEDIDAS_PALABRAS = {"bye", "chau", "adiós", "adios", "descansa", "para", "detente", "stop"}
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
    return "accion_directa", {"instruccion": texto, "archivos_relevantes": []}


def detectar_intent(texto: str, historial: list[dict] | None = None,
                    indice_vault: str = "") -> tuple[str, dict]:
    """Intenta Groq primero; si falla, usa keywords."""
    if historial is None:
        historial = []
    texto_normalizado = normalizar_texto(texto)
    if texto_normalizado != texto:
        print(f"[Normalización] '{texto}' → '{texto_normalizado}'")
    try:
        intent, params = detectar_intent_groq(texto_normalizado, historial, indice_vault)
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


# ── Consulta simple — carga ATLAS para contexto Groq ─────────────────────────

def cargar_atlas() -> str:
    atlas_path = CEREBRO_PATH / "Conocimiento" / "ATLAS.md"
    if atlas_path.exists():
        return atlas_path.read_text(encoding="utf-8")[:4000]
    return ""


# ── Razonamiento profundo — Ollama ────────────────────────────────────────────

def cargar_contenido_para_razonamiento(archivos_relevantes: list[str]) -> str:
    """Carga hasta 3 archivos del vault para contexto de Ollama (max 3000 chars c/u)."""
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


# TODO: reactivar con Mac Studio M4 Pro
# def razonar_con_ollama(pregunta: str, contenido_vault: str) -> str | None:
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/chat",
#             json={
#                 "model": "qwen2.5:7b",
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": (
#                             "Eres el cerebro analítico de Jarvis, asistente del Segundo Cerebro de Luigui. "
#                             "Tienes acceso al contenido del vault. Responde en español, máximo 4 oraciones, "
#                             "tono directo y útil. Sin listas ni bullets — esto se leerá en voz alta.\n\n"
#                             f"CONTENIDO DEL VAULT:\n{contenido_vault}"
#                         ),
#                     },
#                     {"role": "user", "content": pregunta},
#                 ],
#                 "stream": False,
#                 "options": {"temperature": 0.3, "num_predict": 200},
#             },
#             timeout=120,
#         )
#         response.raise_for_status()
#         return response.json()["message"]["content"].strip()
#     except requests.exceptions.ConnectionError:
#         logging.warning("Ollama no está corriendo")
#         return None
#     except requests.exceptions.Timeout:
#         logging.warning("Ollama tardó más de 60s")
#         return None
#     except Exception as e:
#         logging.warning(f"Ollama error: {e}")
#         return None


# ── Acciones — Claude Code ─────────────────────────────────────────────────────

def ejecutar_claude(instruccion: str) -> str:
    """Ejecuta claude CLI con la instrucción y devuelve el output."""
    if not _claude_disponible():
        hablar("Claude Code CLI no está disponible.")
        sys.exit(1)

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


def resumir_output_para_voz(output: str, max_chars: int = 600) -> str:
    """Extrae una respuesta apta para TTS del output de Claude Code."""
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


def despachar_intent(intent: str, params: dict, texto_transcrito: str) -> None:
    """Ejecuta la acción y al terminar dispara _response_complete_callback."""
    _despachar_intent_impl(intent, params, texto_transcrito)
    if _response_complete_callback:
        import time
        logging.info("[Timer] Callback registrado — reiniciando deadline.")
        _response_complete_callback()
        logging.info(f"[Timer] Deadline reiniciado (now={time.time():.0f})")
    else:
        logging.info("[Timer] _response_complete_callback es None.")


def _despachar_intent_impl(intent: str, params: dict, texto_transcrito: str) -> None:
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
            "con Ollama, y ejecutar acciones como crear conceptos, correlacionar o "
            "auditar el vault con Claude Code."
        )
        return

    if intent == "despedirse":
        hablar("Hasta luego, Luigui. Di Jarvis cuando me necesites.")
        _salir_escucha[0] = True
        return

    if intent == "conversacion_libre":
        mensaje = params.get("mensaje") or instruccion
        respuesta = responder_con_groq(mensaje, historial_sesion)
        print(f"[Conversación] {respuesta}")
        hablar(respuesta)
        actualizar_historial(texto_transcrito, (intent, {"respuesta": respuesta}))
        return

    if intent == "consulta_simple":
        hablar("Un momento.")
        atlas = cargar_atlas()
        system = (
            "Eres Jarvis, asistente del Segundo Cerebro de Luigui. "
            "Responde en español, máximo 3 oraciones, sin bullets ni listas — "
            "la respuesta se leerá en voz alta.\n\n"
            f"ÍNDICE DEL VAULT:\n{atlas}"
        )
        respuesta = responder_con_groq(instruccion, historial_sesion, system_prompt_override=system)
        print(f"[Consulta] {respuesta}")
        hablar(respuesta)
        registrar_en_jarvis_log("CONSULTA", instruccion, respuesta)
        return

    if intent == "razonamiento_profundo":
        hablar("Analizando el vault, dame un momento.")
        archivos = params.get("archivos_relevantes", [])
        contenido = cargar_contenido_para_razonamiento(archivos)
        system = (
            "Eres Jarvis. Responde en español, máximo 3 oraciones, sin bullets. "
            "La respuesta se leerá en voz alta.\n\n"
            f"CONTEXTO DEL VAULT:\n{contenido}"
        )
        respuesta = responder_con_groq(instruccion, historial_sesion, system_prompt_override=system)
        print(f"[Razonamiento] {respuesta}")
        hablar(respuesta)
        registrar_en_jarvis_log("RAZONAMIENTO", instruccion, respuesta)
        return

    # accion_directa (y vault_accion como alias para compatibilidad)
    hablar("Dame un momento, Luigui.")
    cmd = (
        f"Responde en español. Si es una pregunta o consulta, responde en máximo 3 oraciones "
        f"sin bullets ni listas — la respuesta se leerá en voz alta. "
        f"Si es una acción sobre el vault, ejecútala y confirma en 1-2 oraciones qué hiciste. "
        f"Instrucción de voz de Luigui: \"{texto_transcrito}\""
    )
    try:
        output = ejecutar_claude(f"Jarvis, {cmd}")
        resumen = resumir_output_para_voz(output)
    except subprocess.TimeoutExpired:
        hablar("Claude tardó demasiado. Revisa la terminal, Luigui.")
        registrar_en_jarvis_log("ACCION", texto_transcrito, "TIMEOUT")
        return
    except Exception as e:
        hablar("Hubo un error al ejecutar el comando.")
        print(f"[Error] {e}")
        registrar_en_jarvis_log("ACCION", texto_transcrito, f"ERROR: {e}")
        return

    print(f"[Claude output] {resumen}")
    hablar(resumen if resumen else "Listo, Luigui.")
    registrar_en_jarvis_log("ACCION", texto_transcrito, resumen)


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
