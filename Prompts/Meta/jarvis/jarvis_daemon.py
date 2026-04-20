#!/usr/local/bin/python3.11
"""
jarvis_daemon.py — Daemon de wake word para el Segundo Cerebro (Mejora 003)

Corre en segundo plano, escucha "Jarvis" o "Hola Jarvis" via STT (Google),
y al detectarlo ejecuta el flujo completo de jarvis.py.

Requiere conexión a internet para el reconocimiento de voz (Google STT).
Logs: Prompts/Meta/jarvis/jarvis.log
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"
JARVIS_DIR   = CEREBRO_PATH / "Prompts" / "Meta" / "jarvis"
LOG_PATH     = JARVIS_DIR / "jarvis.log"

WAKE_WORD           = "jarvis"   # basta con que aparezca en el texto
MODO_ESCUCHA_TIMEOUT = 60        # segundos de escucha activa tras el wake word

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


# ── Wake word via STT ─────────────────────────────────────────────────────────

def esperar_wake_word() -> None:
    """Escucha en loop cortos hasta detectar 'jarvis' en la transcripción STT."""
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    log(f"Esperando wake word '{WAKE_WORD}'...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            texto = recognizer.recognize_google(audio, language="es-ES").lower()
            log(f"[Wake] Escuchado: '{texto}'")
            if WAKE_WORD in texto:
                return
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except Exception as e:
            log(f"[Wake] Error: {e}")
            continue


# ── Ciclo de escucha activa ───────────────────────────────────────────────────

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
        hablar("Hasta luego. Di Jarvis cuando me necesites.")
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


# ── Ciclo principal ───────────────────────────────────────────────────────────

def loop_principal(indice_vault: str) -> None:
    """Ciclo infinito: espera wake word via STT, ejecuta flujo de escucha activa."""
    log("Daemon iniciado. Di 'Jarvis' para activar.")

    try:
        while True:
            esperar_wake_word()
            log("Wake word detectado.")
            hablar("Dime.")
            modo_escucha_activo(indice_vault)
            log("Volviendo al loop de wake word.")
    except KeyboardInterrupt:
        log("Daemon detenido por KeyboardInterrupt.")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    log("=== Jarvis Daemon arrancando ===")

    try:
        indice_vault = cargar_indice_vault()
        loop_principal(indice_vault)
    except Exception as e:
        log(f"ERROR fatal: {e}")
        try:
            hablar("El daemon encontró un error y se está cerrando.")
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
