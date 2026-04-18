#!/usr/bin/env python3
"""
jarvis.py — Interfaz de voz para el Segundo Cerebro (Mejora 002)

Uso:
    python3 Prompts/Meta/jarvis/jarvis.py

Escucha UN comando de voz, lo procesa y responde en voz alta.
Debe ejecutarse desde ~/Documents/Segundo_cerebro/ como working directory.
"""

import subprocess
import sys
from collections import Counter
from pathlib import Path

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"

# ── TTS ────────────────────────────────────────────────────────────────────────

def hablar(texto: str) -> None:
    """Convierte texto a voz usando pyttsx3."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        # Voz en español si está disponible
        for voice in engine.getProperty("voices"):
            if "spanish" in voice.name.lower() or "es_" in voice.id.lower():
                engine.setProperty("voice", voice.id)
                break
        engine.setProperty("rate", 160)
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
        print(f"[Transcripción] {texto}")
        return texto.lower()
    except Exception:
        hablar("No entendí lo que dijiste. Intenta de nuevo.")
        return None


# ── Intent detection ───────────────────────────────────────────────────────────

def detectar_intent(texto: str) -> tuple[str, dict]:
    """
    Clasifica el texto en uno de los 4 intents y extrae parámetros.
    Retorna (intent, params).
    """
    palabras = texto.split()

    # crear_concepto: "crea un concepto sobre X"
    if ("crea" in texto or "agrega" in texto) and "concepto" in texto:
        for kw in ["sobre", "acerca de", "llamado", "titulado"]:
            if kw in texto:
                tema = texto.split(kw, 1)[-1].strip()
                return "crear_concepto", {"tema": tema}
        # fallback: todo después de "concepto"
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

    # listar_conceptos: "qué conceptos tengo" / "lista mis conceptos"
    if "concepto" in texto and any(w in texto for w in ["tengo", "lista", "muestra", "hay"]):
        return "listar_conceptos", {}

    return "desconocido", {}


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
    """Extrae un resumen de 1-2 oraciones del output de Claude Code."""
    lineas = [l.strip() for l in output.splitlines() if l.strip()]
    # Busca líneas con palabras clave de confirmación
    for linea in lineas:
        low = linea.lower()
        if any(k in low for k in ["creado", "guardado", "generado", "✅", "concepto", "correlación"]):
            return linea[:200]
    # fallback: primeras dos líneas con contenido
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
    return (
        f"Tienes {len(archivos)} conceptos en {len(categorias)} categorías: {resumen_partes}."
    )


def _claude_disponible() -> bool:
    resultado = subprocess.run(["which", "claude"], capture_output=True)
    return resultado.returncode == 0


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=== Jarvis — Segundo Cerebro ===")
    hablar("Jarvis listo. ¿Qué necesitas?")

    texto = escuchar()
    if texto is None:
        return

    intent, params = detectar_intent(texto)
    print(f"[Intent] {intent} | [Params] {params}")

    if intent == "listar_conceptos":
        respuesta = listar_conceptos()
        print(f"[Respuesta] {respuesta}")
        hablar(respuesta)
        return

    if intent == "desconocido":
        hablar("No reconocí el comando. Puedes decir: crea un concepto, profundiza, correlaciona, o qué conceptos tengo.")
        return

    prompt = construir_prompt(intent, params)
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


if __name__ == "__main__":
    main()
