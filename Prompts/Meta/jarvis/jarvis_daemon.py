#!/usr/local/bin/python3.11
"""
jarvis_daemon.py — Daemon de wake word para el Segundo Cerebro (Mejora 002b)

Corre en segundo plano, escucha "Hey Jarvis" de forma offline con OpenWakeWord,
y al detectarlo ejecuta el flujo completo de jarvis.py.

Sin API keys — OpenWakeWord es completamente local y open source.
Logs: Prompts/Meta/jarvis/jarvis.log
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"
JARVIS_DIR   = CEREBRO_PATH / "Prompts" / "Meta" / "jarvis"
LOG_PATH     = JARVIS_DIR / "jarvis.log"

WAKE_WORD       = "hey_jarvis"
WAKE_THRESHOLD  = 0.5
SAMPLE_RATE     = 16000
CHUNK_SIZE      = 1280  # frames requeridos por OpenWakeWord

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
    import importlib.util
    _spec = importlib.util.spec_from_file_location("jarvis", JARVIS_DIR / "jarvis.py")
    _mod  = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)

    hablar           = _mod.hablar
    escuchar         = _mod.escuchar
    detectar_intent  = _mod.detectar_intent
    construir_prompt = _mod.construir_prompt
    ejecutar_claude  = _mod.ejecutar_claude
    resumir_output   = _mod.resumir_output
    listar_conceptos = _mod.listar_conceptos
except Exception as e:
    print(f"[ERROR] No pude importar jarvis.py: {e}")
    sys.exit(1)


# ── OpenWakeWord ───────────────────────────────────────────────────────────────

def init_wakeword():
    """Carga modelo OpenWakeWord para 'hey_jarvis'."""
    try:
        from openwakeword.model import Model
        model = Model(wakeword_models=[WAKE_WORD], inference_framework="onnx")
        log(f"Modelo OpenWakeWord cargado: {WAKE_WORD}")
        return model
    except Exception as e:
        log(f"ERROR al cargar OpenWakeWord: {e}")
        hablar("No pude cargar el modelo de wake word. Revisa el log.")
        sys.exit(1)


def init_stream():
    """Abre stream pyaudio continuo a 16kHz mono."""
    try:
        import pyaudio
        pa     = pyaudio.PyAudio()
        stream = pa.open(
            rate=SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )
        log("Stream de audio iniciado (16kHz, mono).")
        return pa, stream
    except Exception as e:
        log(f"ERROR al abrir stream de audio: {e}")
        hablar("No pude acceder al micrófono. Revisa los permisos en Preferencias del Sistema.")
        sys.exit(1)


# ── Ciclo principal ───────────────────────────────────────────────────────────

def procesar_comando() -> None:
    """Escucha un comando tras el wake word y ejecuta la acción correspondiente."""
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
        output  = ejecutar_claude(prompt)
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


def loop_principal(oww_model, stream) -> None:
    """Ciclo infinito: lee chunks de audio, detecta wake word, ejecuta flujo."""
    import numpy as np

    log("Daemon iniciado. Escuchando wake word 'Hey Jarvis'...")

    try:
        while True:
            chunk = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            audio = np.frombuffer(chunk, dtype=np.int16)

            scores = oww_model.predict(audio)
            score  = scores.get(WAKE_WORD, 0.0)

            if score > WAKE_THRESHOLD:
                log(f"Wake word detectado (score={score:.2f}).")
                hablar("Dime.")
                procesar_comando()
                # Vacía el buffer para evitar que el TTS active el wake word
                oww_model.reset()
                log("Volviendo al loop de wake word.")

    except KeyboardInterrupt:
        log("Daemon detenido por KeyboardInterrupt.")


def cleanup(pa, stream) -> None:
    """Cierra el stream y libera pyaudio."""
    try:
        stream.stop_stream()
        stream.close()
    except Exception:
        pass
    try:
        pa.terminate()
    except Exception:
        pass
    log("Recursos de audio liberados.")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    log("=== Jarvis Daemon arrancando ===")

    pa     = None
    stream = None

    try:
        oww_model    = init_wakeword()
        pa, stream   = init_stream()
        loop_principal(oww_model, stream)
    except Exception as e:
        log(f"ERROR fatal: {e}")
        try:
            hablar("El daemon encontró un error y se está cerrando.")
        except Exception:
            pass
        sys.exit(1)
    finally:
        if pa and stream:
            cleanup(pa, stream)


if __name__ == "__main__":
    main()
