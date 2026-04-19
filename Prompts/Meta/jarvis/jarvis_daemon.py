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

# Segundos que Jarvis permanece en modo escucha activa tras el wake word.
# Cada interacción reinicia el contador. Ajusta según tu preferencia.
MODO_ESCUCHA_TIMEOUT = 60

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

    hablar               = _mod.hablar
    escuchar             = _mod.escuchar
    detectar_intent      = _mod.detectar_intent
    actualizar_historial = _mod.actualizar_historial
    historial_sesion     = _mod.historial_sesion
    despachar_intent     = _mod.despachar_intent
except Exception as e:
    print(f"[ERROR] No pude importar jarvis.py: {e}")
    sys.exit(1)


# ── Índice del vault ──────────────────────────────────────────────────────────

def cargar_indice_vault() -> str:
    """Construye lista de slugs por categoría para el contexto de Groq.
    Se llama una vez al arrancar; resultado en variable global."""
    base = CEREBRO_PATH / "Conocimiento" / "Conceptos"
    if not base.exists():
        return ""
    archivos = sorted(base.glob("**/*.md"))
    lineas = ["Conceptos disponibles en el vault (slug : categoría):"]
    for f in archivos:
        lineas.append(f"- {f.stem} ({f.parent.name})")
    resultado = "\n".join(lineas)
    log(f"Índice del vault cargado: {len(archivos)} conceptos.")
    return resultado


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

_DESPEDIDAS = (
    "te hablo luego", "hasta luego", "bye", "chau", "adiós", "adios",
    "descansa", "modo espera", "ya terminé", "ya termine", "para jarvis",
)


def _es_despedida(texto: str) -> bool:
    t = texto.lower()
    return any(d in t for d in _DESPEDIDAS)


def procesar_comando(indice_vault: str) -> bool:
    """Escucha un comando y despacha via jarvis.py. Retorna True si hubo comando."""
    texto = escuchar()
    if texto is None:
        return False

    # Detección de despedida por keywords, sin pasar por Groq (más confiable).
    if _es_despedida(texto):
        log(f"Despedida detectada: '{texto}'")
        hablar("Hasta luego. Di Hey Jarvis cuando me necesites.")
        _mod._salir_escucha[0] = True
        return True

    intent, params = detectar_intent(texto, historial_sesion, indice_vault)
    log(f"Intent: {intent} | Params: {params}")
    actualizar_historial(texto, (intent, params))
    despachar_intent(intent, params, texto)
    return True


def modo_escucha_activo(indice_vault: str) -> None:
    """Mantiene Jarvis en escucha activa por MODO_ESCUCHA_TIMEOUT segundos.
    El timer se reinicia DESPUÉS de que Mónica termina de hablar, via callback."""
    import time

    # Contenedor mutable para que el callback pueda actualizar el deadline.
    _deadline = [time.time() + MODO_ESCUCHA_TIMEOUT]

    def _reset_timer():
        _deadline[0] = time.time() + MODO_ESCUCHA_TIMEOUT
        log(f"Timer reiniciado ({MODO_ESCUCHA_TIMEOUT}s) tras respuesta completa.")

    _mod._response_complete_callback = _reset_timer
    _mod._salir_escucha[0] = False
    log(f"Modo escucha activo ({MODO_ESCUCHA_TIMEOUT}s). Sin wake word necesario.")

    while time.time() < _deadline[0]:
        procesar_comando(indice_vault)
        if _mod._salir_escucha[0]:
            log("Modo escucha cerrado por despedida del usuario.")
            break

    _mod._response_complete_callback = None
    _mod._salir_escucha[0] = False
    log("Volviendo al loop de wake word.")


def loop_principal(oww_model, stream, indice_vault: str) -> None:
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
                oww_model.reset()  # vacía el buffer antes de entrar al modo escucha
                modo_escucha_activo(indice_vault)
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
        indice_vault = cargar_indice_vault()
        oww_model    = init_wakeword()
        pa, stream   = init_stream()
        loop_principal(oww_model, stream, indice_vault)
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
