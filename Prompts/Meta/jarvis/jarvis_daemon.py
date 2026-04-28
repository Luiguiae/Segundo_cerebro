#!/usr/local/bin/python3.11
"""
jarvis_daemon.py — Daemon de wake word para el Segundo Cerebro

Corre en segundo plano, escucha "Hey Jarvis" via STT y al detectarlo
ejecuta el flujo completo de jarvis.py.

Mejora 002g: watcher proactivo del vault — detecta cambios en
Conocimiento/ y notifica en voz sin que el usuario lo pida.

Logs: Prompts/Meta/jarvis/jarvis.log
"""

import sys
import logging
import threading
import time
import requests
from datetime import datetime
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"
JARVIS_DIR   = CEREBRO_PATH / "Prompts" / "Meta" / "jarvis"
LOG_PATH     = JARVIS_DIR / "jarvis.log"

WAKE_WORD = "jarvis"

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

    hablar                  = _mod.hablar
    escuchar                = _mod.escuchar
    detectar_intent         = _mod.detectar_intent
    actualizar_historial    = _mod.actualizar_historial
    historial_sesion        = _mod.historial_sesion
    despachar_intent        = _mod.despachar_intent
    ejecutar_claude         = _mod.ejecutar_claude
    responder_con_groq      = _mod.responder_con_groq
    resumir_output_para_voz = _mod.resumir_output_para_voz
    registrar_en_jarvis_log = _mod.registrar_en_jarvis_log
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


# ── Watcher proactivo — utilidades ───────────────────────────────────────────

def leer_titulo_frontmatter(path: str) -> str | None:
    """Lee las primeras 10 líneas del .md y extrae el campo titulo: del frontmatter YAML."""
    try:
        lineas = Path(path).read_text(encoding="utf-8").splitlines()[:10]
        for linea in lineas:
            if linea.startswith("titulo:"):
                return linea.split(":", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return None


def escuchar_respuesta(timeout: int = 30) -> str | None:
    """Escucha una respuesta del usuario con el timeout dado. Retorna texto o None."""
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
        return recognizer.recognize_google(audio, language="es-ES").lower()
    except Exception:
        return None


# ── Watcher proactivo — handler ───────────────────────────────────────────────

class VaultEventHandler(FileSystemEventHandler):
    def __init__(self, on_nuevo_concepto, on_nueva_correlacion,
                 on_concepto_modificado, lock_interaccion):
        self._on_nuevo_concepto      = on_nuevo_concepto
        self._on_nueva_correlacion   = on_nueva_correlacion
        self._on_concepto_modificado = on_concepto_modificado
        self.lock_interaccion        = lock_interaccion
        self._timers: dict           = {}

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".md"):
            return
        self._debounce(event.src_path, self._handle_created)

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".md"):
            return
        self._debounce(event.src_path, self._handle_modified)

    def _debounce(self, path, handler):
        if path in self._timers:
            self._timers[path].cancel()
        timer = threading.Timer(3.0, handler, args=[path])
        self._timers[path] = timer
        timer.start()

    def _handle_created(self, path):
        if self.lock_interaccion.locked():
            log(f"[Watcher] {Path(path).name} creado — diferido (interacción activa)")
            return
        slug = Path(path).stem
        if "Correlaciones" in path:
            self._on_nueva_correlacion(slug, path)
        elif "Conceptos" in path:
            self._on_nuevo_concepto(slug, path)

    def _handle_modified(self, path):
        if self.lock_interaccion.locked():
            return
        if "Conceptos" in path:
            self._on_concepto_modificado(Path(path).stem, path)


# ── Watcher proactivo — callbacks ─────────────────────────────────────────────

_AFIRMACIONES = ("sí", "si", "dale", "claro", "adelante", "ok", "sí por favor")


def on_nuevo_concepto(slug: str, path: str) -> None:
    titulo = leer_titulo_frontmatter(path) or slug
    log(f"[Watcher] Nuevo concepto detectado: {slug}")
    hablar(
        f"Identifico un nuevo concepto: {titulo}. "
        f"¿Quieres que lo evalúe contra la rúbrica y actualice el INDEX?"
    )
    respuesta = escuchar_respuesta(timeout=30)
    if respuesta and any(s in respuesta for s in _AFIRMACIONES):
        instruccion = (
            f"Evalúa el concepto {slug} contra la rúbrica en Plantillas/rubrica.md, "
            f"actualiza su campo estado en el frontmatter, regenera INDEX.md con "
            f"generar_index.py, y propón 2 correlaciones con conceptos existentes del vault."
        )
        output = ejecutar_claude(instruccion)
        hablar(resumir_output_para_voz(output))
        registrar_en_jarvis_log("WATCHER", f"Nuevo concepto: {slug}", "Evaluado y correlacionado")
    else:
        log(f"[Watcher] Evaluación de {slug} omitida.")


def on_nueva_correlacion(slug: str, path: str) -> None:
    log(f"[Watcher] Nueva correlación detectada: {slug}")
    hablar(f"Identifico una nueva correlación: {slug}. ¿Quieres que la lea?")
    respuesta = escuchar_respuesta(timeout=30)
    if respuesta and any(s in respuesta for s in _AFIRMACIONES):
        contenido = Path(path).read_text(encoding="utf-8")[:2000]
        resumen = responder_con_groq(
            f"Resume esta correlación en 3 oraciones para leer en voz alta:\n{contenido}",
            [],
        )
        hablar(resumen)
    else:
        log(f"[Watcher] Lectura de correlación {slug} omitida.")


def on_concepto_modificado(slug: str, path: str) -> None:
    log(f"[Watcher] Concepto modificado: {slug}")
    hablar(f"Detecté cambios en {slug}. ¿Quieres que lo re-evalúe?")
    respuesta = escuchar_respuesta(timeout=30)
    if respuesta and any(s in respuesta for s in _AFIRMACIONES):
        instruccion = f"Re-evalúa el concepto {slug} contra la rúbrica y actualiza su estado."
        output = ejecutar_claude(instruccion)
        hablar(resumir_output_para_voz(output))
        registrar_en_jarvis_log("WATCHER", f"Concepto modificado: {slug}", "Re-evaluado")
    else:
        log(f"[Watcher] Re-evaluación de {slug} omitida.")


# ── Wake word via STT ─────────────────────────────────────────────────────────

def esperar_wake_word() -> None:
    """Escucha en loops cortos hasta detectar 'jarvis' via STT."""
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    log(f"Esperando wake word '{WAKE_WORD}'...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
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


# ── Ciclo principal ───────────────────────────────────────────────────────────

_DESPEDIDAS = (
    "te hablo luego", "hasta luego", "bye", "chau", "adiós", "adios",
    "descansa", "modo espera", "ya terminé", "ya termine", "para jarvis",
)


def _es_despedida(texto: str) -> bool:
    t = texto.lower()
    return any(d in t for d in _DESPEDIDAS)


def procesar_comando(indice_vault: str, lock_interaccion: threading.Lock) -> bool:
    """Escucha un comando y despacha via jarvis.py. Retorna True si hubo comando."""
    texto = escuchar()
    if texto is None:
        return False

    with lock_interaccion:
        if _es_despedida(texto):
            log(f"Despedida detectada: '{texto}'")
            hablar("Hasta luego, Luigui. Di Jarvis cuando me necesites.")
            _mod._salir_escucha[0] = True
            return True

        intent, params = detectar_intent(texto, historial_sesion, indice_vault)
        log(f"Intent: {intent} | Params: {params}")
        actualizar_historial(texto, (intent, params))
        despachar_intent(intent, params, texto)
    return True


def modo_escucha_activo(indice_vault: str, lock_interaccion: threading.Lock) -> None:
    """Mantiene Jarvis en escucha activa por MODO_ESCUCHA_TIMEOUT segundos.
    El timer se reinicia DESPUÉS de que Mónica termina de hablar, via callback."""
    _deadline = [time.time() + MODO_ESCUCHA_TIMEOUT]

    def _reset_timer():
        _deadline[0] = time.time() + MODO_ESCUCHA_TIMEOUT
        log(f"Timer reiniciado ({MODO_ESCUCHA_TIMEOUT}s) tras respuesta completa.")

    _mod._response_complete_callback = _reset_timer
    _mod._salir_escucha[0] = False
    log(f"Modo escucha activo ({MODO_ESCUCHA_TIMEOUT}s). Sin wake word necesario.")

    while time.time() < _deadline[0]:
        procesar_comando(indice_vault, lock_interaccion)
        if _mod._salir_escucha[0]:
            log("Modo escucha cerrado por despedida del usuario.")
            break

    _mod._response_complete_callback = None
    _mod._salir_escucha[0] = False
    log("Volviendo al loop de wake word.")


def loop_principal(indice_vault: str, lock_interaccion: threading.Lock) -> None:
    """Ciclo infinito: espera wake word via STT, ejecuta flujo de escucha activa."""
    log("Daemon iniciado. Di 'Jarvis' para activar.")

    try:
        while True:
            esperar_wake_word()
            log("Wake word detectado.")
            hablar("Dime, Luigui.")
            modo_escucha_activo(indice_vault, lock_interaccion)
            log("Volviendo al loop de wake word.")
    except KeyboardInterrupt:
        log("Daemon detenido por KeyboardInterrupt.")


# ── Main ───────────────────────────────────────────────────────────────────────

def precargar_ollama() -> None:
    """Carga qwen2.5:7b en RAM para que la primera consulta real no espere cold start."""
    try:
        requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:7b",
                "messages": [{"role": "user", "content": "hola"}],
                "stream": False,
                "options": {"num_predict": 1},
            },
            timeout=180,
        )
        logging.info("Modelo Ollama precargado en RAM.")
    except Exception as e:
        logging.warning(f"Precarga Ollama fallida (no bloqueante): {e}")


def main():
    log("=== Jarvis Daemon arrancando ===")

    observer = None
    try:
        indice_vault     = cargar_indice_vault()
        precargar_ollama()
        lock_interaccion = threading.Lock()

        handler = VaultEventHandler(
            on_nuevo_concepto=on_nuevo_concepto,
            on_nueva_correlacion=on_nueva_correlacion,
            on_concepto_modificado=on_concepto_modificado,
            lock_interaccion=lock_interaccion,
        )
        observer = Observer()
        observer.schedule(handler, str(CEREBRO_PATH / "Conocimiento"), recursive=True)
        observer.start()
        log("Watcher activo en Conocimiento/")

        loop_principal(indice_vault, lock_interaccion)
    except Exception as e:
        log(f"ERROR fatal: {e}")
        try:
            hablar("El daemon encontró un error y se está cerrando.")
        except Exception:
            pass
        sys.exit(1)
    finally:
        if observer is not None:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    main()
