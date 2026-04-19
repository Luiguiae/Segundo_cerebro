#!/usr/local/bin/python3.11
"""
jarvis.py — Interfaz de voz para el Segundo Cerebro (Mejora 002 + 002c)

Uso:
    python3 Prompts/Meta/jarvis/jarvis.py

Escucha UN comando de voz, lo procesa y responde en voz alta.
Debe ejecutarse desde ~/Documents/Segundo_cerebro/ como working directory.
"""

import json
import logging
import os
import requests
import subprocess
import sys
from collections import Counter
from pathlib import Path

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"

# Historial de sesión en memoria — ventana deslizante de 10 turnos (20 mensajes)
historial_sesion: list[dict] = []


# ── TTS ────────────────────────────────────────────────────────────────────────

def hablar(texto: str) -> None:
    """Convierte texto a voz usando pyttsx3."""
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
        hablar("Falta la librería speech_recognition. Instálala con pip3 install SpeechRecognition.")
        return None

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Escuchando... (habla ahora)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
    except AttributeError:
        hablar("Micrófono no disponible. Instala pyaudio con pip3 install pyaudio.")
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


# ── Intent detection — Groq ────────────────────────────────────────────────────

def detectar_intent_groq(texto: str, historial: list[dict], indice_vault: str) -> tuple[str, dict]:
    """Clasifica el intent usando Groq llama-3.3-70b. Retorna (intent, params)."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY no está en las variables de entorno.")

    system_prompt = f"""Eres el clasificador de intents de Jarvis, asistente de voz del Segundo Cerebro de Luigui.

INTENTS DISPONIBLES:
- crear_concepto: params: {{"tema": "<descripción del tema en lenguaje natural>"}}
- profundizar_concepto: params: {{"nombre": "<slug-del-concepto>"}}
- correlacionar: params: {{"concepto_a": "<slug>", "concepto_b": "<slug>"}}
- listar_conceptos: params: {{}}
- consulta_vault: params: {{"pregunta": "<pregunta literal del usuario>", "conceptos_mencionados": ["<slug>"], "categoria": "<categoria o vacío>"}}
  Usar cuando el usuario hace una PREGUNTA sobre el vault, no una acción.
  Ejemplos: "¿qué concepto es más interesante?", "explícame vibe coding",
  "¿cuál es la diferencia entre X e Y?", "¿qué tengo sobre producto?", "¿qué correlaciones tengo?"
- conversacion_libre: params: {{"mensaje": "<texto literal del usuario>"}}
  Usar cuando el usuario dice algo que no es una acción sobre el vault ni una consulta de conocimiento.
  Ejemplos: saludos, preguntas personales a Jarvis, comentarios, expresiones emocionales.
- desconocido: params: {{"razon": "<por qué no se pudo clasificar>"}}

CONCEPTOS DISPONIBLES EN EL VAULT:
{indice_vault}

REGLAS:
- Los slugs usan guiones medios (ej: "vibe-coding", "capital-de-contexto").
- Si el usuario dice un nombre aproximado, resuélvelo al slug más cercano del vault.
- Usa el historial para resolver referencias pronominales ("lo", "ese", "el mismo").
- Responde ÚNICAMENTE con JSON válido. Sin explicaciones. Sin markdown.

EJEMPLOS:
- "junta capital de contexto con la fábrica oscura" → {{"intent": "correlacionar", "params": {{"concepto_a": "capital-de-contexto", "concepto_b": "fabrica-oscura-de-software"}}}}
- "háblame de vibe coding" → {{"intent": "consulta_vault", "params": {{"pregunta": "háblame de vibe coding", "conceptos_mencionados": ["vibe-coding"], "categoria": ""}}}}
- "¿cuál es la diferencia entre vibe coding y spec driven?" → {{"intent": "consulta_vault", "params": {{"pregunta": "¿cuál es la diferencia entre vibe coding y spec driven?", "conceptos_mencionados": ["vibe-coding", "spec-driven-development"], "categoria": ""}}}}
- "¿qué tengo sobre producto?" → {{"intent": "consulta_vault", "params": {{"pregunta": "¿qué tengo sobre producto?", "conceptos_mencionados": [], "categoria": "producto"}}}}
- "qué conceptos tengo sobre ia" → {{"intent": "listar_conceptos", "params": {{}}}}
- "crea un concepto sobre diseño especulativo" → {{"intent": "crear_concepto", "params": {{"tema": "diseño especulativo"}}}}"""

    mensajes = [{"role": "system", "content": system_prompt}]
    mensajes += historial[-10:]
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
    intent = data.get("intent", "desconocido")
    params = data.get("params", {})
    return intent, params


# ── Intent detection — keywords (fallback) ────────────────────────────────────

def detectar_intent_keywords(texto: str) -> tuple[str, dict]:
    """Clasificación por keywords exactas. Se usa si Groq no está disponible."""
    # crear_concepto: "crea un concepto sobre X"
    if ("crea" in texto or "agrega" in texto) and "concepto" in texto:
        for kw in ["sobre", "acerca de", "llamado", "titulado"]:
            if kw in texto:
                tema = texto.split(kw, 1)[-1].strip()
                return "crear_concepto", {"tema": tema}
        tema = texto.split("concepto", 1)[-1].strip()
        return "crear_concepto", {"tema": tema or "sin definir"}

    # profundizar_concepto: "profundiza el concepto X" / "profundiza X"
    if "profundiza" in texto:
        for kw in ["concepto", "el", "la"]:
            texto = texto.replace(kw, " ")
        nombre = texto.replace("profundiza", "").strip().replace(" ", "-")
        return "profundizar_concepto", {"nombre": nombre}

    # correlacionar: "correlaciona X con Y"
    if "correlaciona" in texto and " con " in texto:
        parte = texto.replace("correlaciona", "").strip()
        if " con " in parte:
            a, b = parte.split(" con ", 1)
            return "correlacionar", {
                "concepto_a": a.strip().replace(" ", "-"),
                "concepto_b": b.strip().replace(" ", "-"),
            }

    # listar_conceptos
    if "concepto" in texto and any(w in texto for w in ["tengo", "lista", "muestra", "hay"]):
        return "listar_conceptos", {}

    return "desconocido", {}


# ── Intent detection — wrapper con fallback ───────────────────────────────────

def detectar_intent(texto: str, historial: list[dict] | None = None,
                    indice_vault: str = "") -> tuple[str, dict]:
    """Intenta Groq primero; si falla, usa keywords. Loggea el método usado."""
    if historial is None:
        historial = []
    try:
        intent, params = detectar_intent_groq(texto, historial, indice_vault)
        print(f"[Intent via Groq] {intent} | {params}")
        return intent, params
    except Exception as e:
        print(f"[Groq falló ({e}), usando keywords]")
        intent, params = detectar_intent_keywords(texto)
        print(f"[Intent via keywords] {intent} | {params}")
        return intent, params


# ── Historial de sesión ────────────────────────────────────────────────────────

def actualizar_historial(texto_usuario: str, resultado_intent: tuple[str, dict]) -> None:
    """Agrega el turno al historial global con ventana deslizante de 10 turnos."""
    intent, params = resultado_intent
    historial_sesion.append({"role": "user", "content": texto_usuario})
    historial_sesion.append({
        "role": "assistant",
        "content": f"Intent clasificado: {json.dumps({'intent': intent, 'params': params}, ensure_ascii=False)}",
    })
    # Ventana deslizante: máximo 20 mensajes (10 turnos)
    while len(historial_sesion) > 20:
        historial_sesion.pop(0)
        historial_sesion.pop(0)


# ── Consultas conversacionales ────────────────────────────────────────────────

def cargar_contenido_vault(params: dict) -> str:
    """Carga el contenido relevante del vault según los params del intent consulta_vault.
    Trunca a 8000 caracteres para no exceder el contexto de Groq."""
    base  = CEREBRO_PATH / "Conocimiento"
    partes: list[str] = []

    # Conceptos específicos mencionados
    for slug in params.get("conceptos_mencionados", []):
        matches = list((base / "Conceptos").glob(f"**/{slug}.md"))
        if matches:
            partes.append(matches[0].read_text(encoding="utf-8"))

    # Categoría completa
    categoria = params.get("categoria", "").strip()
    if categoria:
        cat_dir = base / "Conceptos" / categoria
        if cat_dir.exists():
            for f in sorted(cat_dir.glob("*.md")):
                partes.append(f.read_text(encoding="utf-8"))

    # Correlaciones si la pregunta las menciona
    pregunta = params.get("pregunta", "").lower()
    if "correlaci" in pregunta:
        for f in sorted((base / "Correlaciones").glob("*.md")):
            partes.append(f.read_text(encoding="utf-8"))

    # Fallback: ATLAS.md como resumen general
    if not partes:
        atlas = base / "ATLAS.md"
        if atlas.exists():
            partes.append(atlas.read_text(encoding="utf-8"))

    texto = "\n\n---\n\n".join(partes)
    return texto[:8000]


def responder_con_groq(pregunta: str, contenido_vault: str, historial: list[dict],
                       system_prompt_override: str | None = None) -> str:
    """Genera una respuesta conversacional usando Groq.
    Si system_prompt_override se provee, lo usa directamente como system prompt."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "No tengo acceso a Groq para responder esta consulta."

    if system_prompt_override:
        system_prompt = system_prompt_override
    else:
        system_prompt = f"""Eres Jarvis, asistente de voz del Segundo Cerebro de Luigui.
Respondes preguntas sobre el vault de conocimiento de forma concisa y audible.

REGLAS:
- Máximo 4 oraciones en tu respuesta.
- En español, tono conversacional.
- No uses listas ni bullets — esto se leerá en voz alta.
- Responde directamente. "Según el vault..." está bien. "Como Jarvis..." no.

CONTENIDO DEL VAULT:
{contenido_vault}"""

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
                "max_tokens": 200,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[responder_con_groq error] {e}")
        return "No pude consultar el vault en este momento."


# ── Acciones ───────────────────────────────────────────────────────────────────

def construir_prompt(intent: str, params: dict) -> str | None:
    """Construye el prompt para Claude Code CLI según el intent."""
    if intent == "crear_concepto":
        tema = params["tema"]
        return (
            f'Jarvis, agrega el concepto {tema}. '
            f'Usa la taxonomía en Plantillas/taxonomia.md para determinar la categoría '
            f'y guárdalo en la subcarpeta correcta bajo Conocimiento/Conceptos/.'
        )

    if intent == "profundizar_concepto":
        nombre = params["nombre"]
        return (
            f'Lee Prompts/Meta/profundizador-conceptos/SKILL.md y aplícala sobre '
            f'el concepto {nombre}. Localiza el archivo buscando recursivamente en '
            f'Conocimiento/Conceptos/**/{nombre}.md — el concepto puede estar en '
            f'cualquier subcarpeta de categoría.'
        )

    if intent == "correlacionar":
        a = params["concepto_a"]
        b = params["concepto_b"]
        return (
            f'Jarvis, correlaciona {a} y {b}. '
            f'Usa Conocimiento/ATLAS.md para inferir el campo relacionado. '
            f'Guarda el archivo en Conocimiento/Correlaciones/ con el formato estándar.'
        )

    return None


def ejecutar_claude(prompt: str) -> str:
    """Ejecuta claude CLI con el prompt dado y devuelve el output."""
    if not _claude_disponible():
        hablar("Claude Code CLI no está disponible. Instálalo y vuelve a intentarlo.")
        sys.exit(1)

    resultado = subprocess.run(
        ["claude", "--print", prompt],
        cwd=str(CEREBRO_PATH),
        capture_output=True,
        text=True,
        timeout=120,
    )
    return resultado.stdout or resultado.stderr


def resumir_output(output: str) -> str:
    """Extrae un resumen de 1-2 oraciones del output de Claude Code.
    Si detecta rechazo o error, devuelve la línea completa con la razón."""
    lineas = [l.strip() for l in output.splitlines() if l.strip()]
    RECHAZO = ["rechazado", "no encontrado", "no existe", "error", "❌", "fallo", "falló"]
    EXITO   = ["creado", "guardado", "generado", "✅", "concepto", "correlación"]
    # Prioridad: líneas de rechazo primero (para leer la razón completa)
    for linea in lineas:
        low = linea.lower()
        if any(k in low for k in RECHAZO):
            return linea[:300]
    for linea in lineas:
        low = linea.lower()
        if any(k in low for k in EXITO):
            return linea[:200]
    relevantes = [l for l in lineas if len(l) > 10][:2]
    return " ".join(relevantes)[:200] if relevantes else "Listo."


def listar_conceptos() -> str:
    """Lee el filesystem y construye resumen por categoría (sin invocar Claude Code)."""
    base = CEREBRO_PATH / "Conocimiento" / "Conceptos"
    if not base.exists():
        return "No encontré la carpeta de conceptos."

    archivos = list(base.glob("**/*.md"))
    if not archivos:
        return "No hay conceptos en el vault."

    categorias = Counter(f.parent.name for f in archivos)
    resumen_partes = ", ".join(f"{n} de {cat}" for cat, n in sorted(categorias.items()))
    return f"Tienes {len(archivos)} conceptos en {len(categorias)} categorías: {resumen_partes}."


def _claude_disponible() -> bool:
    resultado = subprocess.run(["which", "claude"], capture_output=True)
    return resultado.returncode == 0


# ── Dispatch central (usado por main() y por jarvis_daemon.py) ────────────────

def despachar_intent(intent: str, params: dict, texto_transcrito: str) -> None:
    """Ejecuta la acción correspondiente al intent. Única fuente de verdad del dispatch."""

    if intent == "listar_conceptos":
        respuesta = listar_conceptos()
        print(f"[Respuesta] {respuesta}")
        hablar(respuesta)
        return

    if intent == "desconocido":
        hablar(f"No entendí: {params.get('razon', 'comando no reconocido')}")
        return

    if intent == "conversacion_libre":
        mensaje = params.get("mensaje", texto_transcrito)
        system_chat = (
            "Eres Jarvis, asistente personal de Luigui. "
            "Tienes personalidad: directo, inteligente, algo irónico pero amable. "
            "Respondes en español, máximo 2 oraciones, tono conversacional natural."
        )
        respuesta = responder_con_groq(mensaje, "", historial_sesion,
                                       system_prompt_override=system_chat)
        print(f"[Conversación] {respuesta}")
        hablar(respuesta)
        actualizar_historial(texto_transcrito, (intent, {"respuesta": respuesta}))
        return

    if intent == "consulta_vault":
        pregunta = params.get("pregunta", texto_transcrito)
        hablar("Un momento, consultando el vault.")
        contenido = cargar_contenido_vault(params)
        respuesta = responder_con_groq(pregunta, contenido, historial_sesion)
        print(f"[Consulta vault] {respuesta}")
        hablar(respuesta)
        actualizar_historial(texto_transcrito, (intent, {"respuesta": respuesta}))
        return

    if intent not in ("crear_concepto", "profundizar_concepto", "correlacionar"):
        hablar(f"No sé cómo ejecutar el intent: {intent}")
        return

    prompt = construir_prompt(intent, params)

    if intent == "correlacionar":
        hablar(f"Correlacionando {params.get('concepto_a')} con {params.get('concepto_b')}, un momento.")
    elif intent == "profundizar_concepto":
        hablar(f"Profundizando el concepto {params.get('nombre')}, un momento.")
    elif intent == "crear_concepto":
        hablar(f"Creando un concepto sobre {params.get('tema')}, un momento.")
    else:
        hablar("Procesando. Un momento.")

    try:
        output = ejecutar_claude(prompt)
        resumen = resumir_output(output)
    except subprocess.TimeoutExpired:
        hablar("Claude Code tardó demasiado. Revisa el resultado en la terminal.")
        return
    except Exception as e:
        hablar("Hubo un error al ejecutar el comando.")
        print(f"[Error] {e}")
        return

    print(f"[Output resumido] {resumen}")
    hablar(resumen if resumen else "Listo.")


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
