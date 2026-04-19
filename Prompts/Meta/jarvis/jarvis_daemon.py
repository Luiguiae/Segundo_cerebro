#!/usr/local/bin/python3.11
"""
jarvis_daemon.py — Daemon de wake word para el Segundo Cerebro (Mejora 002b)

Corre en segundo plano, escucha "Hey Jarvis" de forma offline con Pvporcupine,
y al detectarlo ejecuta el flujo completo de jarvis.py.

Requiere: PICOVOICE_KEY en variables de entorno (nunca hardcodeada)
Logs:     Prompts/Meta/jarvis/jarvis.log
"""

import os
import sys
import signal
import logging
from datetime import datetime
from pathlib import Path

# Agrega el directorio del proyecto al path para importar jarvis.py
CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"
JARVIS_DIR   = CEREBRO_PATH / "Prompts" / "Meta" / "jarvis"
LOG_PATH     = JARVIS_DIR / "jarvis.log"

sys.path.insert(0, str(CEREBRO_PATH))

# ── Logging ────────────────────────────────────────────────────────────────────

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log(msg: str) -> None:
    logging.info(msg)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ── Importar funciones de jarvis.py ───────────────────────────────────────────

try:
    from Prompts.Meta.jarvis.jarvis import (
        hablar,
        escuchar,
        detectar_intent,
        construir_prompt,
        ejecutar_claude,
        resumir_output,
        listar_conceptos,
    )
except ImportError:
    # Fallback: importar por ruta directa si el módulo no está en el path
    import importlib.util
    spec = importlib.util.spec_from_file_location("jarvis", JARVIS_DIR / "jarvis.py")
    jarvis_mod = importlib.util.load_from_spec(spec)
    spec.loader.exec_module(jarvis_mod)
    hablar          = jarvis_mod.hablar
    escuchar        = jarvis_mod.escuchar
    detectar_intent = jarvis_mod.detectar_intent
    construir_prompt= jarvis_mod.construir_prompt
    ejecutar_claude = jarvis_mod.ejecutar_claude
    resumir_output  = jarvis_mod.resumir_output
    listar_conceptos= jarvis_mod.listar_conceptos


# ── Porcupine ─────────────────────────────────────────────────────────────────

def init_porcupine():
    """Inicializa Pvporcupine con la keyword 'jarvis' (built-in tier gratuito)."""
    import pvporcupine
    key = os.environ.get("PICOVOICE_KEY")
    if not key:
        log("ERROR: PICOVOICE_KEY no está en las variables de entorno.")
        hablar("Falta la API key de Picovoice. Revisa la configuración del daemon.")
        sys.exit(1)
    return pvporcupine.create(access_key=key, keywords=["jarvis"])


def init_recorder(frame_length: int):
    """Inicializa PvRecorder con el frame_length que requiere Porcupine."""
    from pvrecorder import PvRecorder
    return PvRecorder(device_index=-1, frame_length=frame_length)


# ── Ciclo principal ───────────────────────────────────────────────────────────

def procesar_comando() -> None:
    """Escucha, detecta intent y ejecuta la acción correspondiente."""
    texto = escuchar()
    if texto is None:
        return

    intent, params = detectar_intent(texto)
    log(f"Intent: {intent} | Params: {params}")

    if intent == "listar_conceptos":
        respuesta = listar_conceptos()
        log(f"Respuesta: {respuesta}")
        hablar(respuesta)
        return

    if intent == "desconocido":
        hablar("No reconocí el comando. Puedes decir: crea un concepto, profundiza, correlaciona, o qué conceptos tengo.")
        return

    prompt = construir_prompt(intent, params)
    hablar("Procesando. Un momento.")

    try:
        import subprocess
        output = ejecutar_claude(prompt)
        resumen = resumir_output(output)
    except subprocess.TimeoutExpired:
        log("ERROR: Claude Code timeout")
        hablar("Claude Code tardó demasiado. Revisa el log para más detalles.")
        return
    except Exception as e:
        log(f"ERROR en ejecutar_claude: {e}")
        hablar("Hubo un error al ejecutar el comando.")
        return

    log(f"Output resumido: {resumen}")
    hablar(resumen if resumen else "Listo.")


def loop_principal(porcupine, recorder) -> None:
    """Ciclo infinito: escucha frames de audio, detecta wake word, ejecuta flujo."""
    log("Daemon iniciado. Escuchando wake word 'Hey Jarvis'...")
    recorder.start()

    try:
        while True:
            frame = recorder.read()
            resultado = porcupine.process(frame)

            if resultado >= 0:
                log("Wake word detectado.")
                hablar("Dime.")
                procesar_comando()
                log("Volviendo al loop de wake word.")

    except KeyboardInterrupt:
        log("Daemon detenido por KeyboardInterrupt.")


def cleanup(porcupine, recorder) -> None:
    """Libera recursos de Porcupine y PvRecorder."""
    try:
        recorder.stop()
        recorder.delete()
    except Exception:
        pass
    try:
        porcupine.delete()
    except Exception:
        pass
    log("Recursos liberados.")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    log("=== Jarvis Daemon arrancando ===")

    porcupine = None
    recorder  = None

    try:
        porcupine = init_porcupine()
        recorder  = init_recorder(porcupine.frame_length)
        loop_principal(porcupine, recorder)
    except Exception as e:
        log(f"ERROR fatal: {e}")
        try:
            hablar("El daemon encontró un error y se está cerrando.")
        except Exception:
            pass
        sys.exit(1)
    finally:
        if porcupine and recorder:
            cleanup(porcupine, recorder)


if __name__ == "__main__":
    main()
