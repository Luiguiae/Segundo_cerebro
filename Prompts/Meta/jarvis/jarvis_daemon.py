#!/usr/local/bin/python3.11
"""
jarvis_daemon.py — Daemon de wake word para el Segundo Cerebro

Corre en segundo plano, escucha "Hey Jarvis" via STT y al detectarlo
ejecuta el flujo completo de jarvis.py.

Mejora 002g: watcher proactivo del vault — detecta cambios en
Conocimiento/ y notifica en voz sin que el usuario lo pida.

Logs: Prompts/Meta/jarvis/jarvis.log
"""

import fcntl
import os
import queue
import re
import subprocess
import sys
import logging
import logging.handlers
import threading
import time
from datetime import datetime
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"
JARVIS_DIR   = CEREBRO_PATH / "Prompts" / "Meta" / "jarvis"
LOG_PATH     = JARVIS_DIR / "jarvis.log"

WAKE_WORD  = "jarvis"
PID_FILE   = JARVIS_DIR / "jarvis.pid"

# Segundos que Jarvis permanece en modo escucha activa tras el wake word.
# Cada interacción reinicia el contador. Ajusta según tu preferencia.
MODO_ESCUCHA_TIMEOUT = 60

# Cola de eventos del watcher generados durante una sesión activa.
# Los callbacks enqueuean aquí; loop_principal drena al salir de modo escucha.
_watcher_queue: queue.Queue = queue.Queue()

# Ref-box para que los callbacks accedan al lock de interacción sin globals extra.
_lock_interaccion_ref: list = [None]

# Señal para pausar esperar_wake_word() mientras otra sesión tiene el micrófono.
# Sin esto, PortAudio entrega el audio a ambos streams y Jarvis responde dos veces.
_pausa_wake_word: threading.Event = threading.Event()

# Acción pendiente del watcher que el usuario aún no confirmó.
# Se setea en los callbacks cuando escuchar_respuesta falla o no captura "sí".
# procesar_comando() la chequea antes de llamar a Groq — si el usuario dice una
# afirmación mientras hay pendiente, ejecuta la acción directamente sin clasificar.
_accion_pendiente_watcher: list = [None]  # [(tipo, param)] o [None]

# Previene dos modo_escucha_activo() corriendo en paralelo.
# Se setea al inicio de modo_escucha_activo() y se limpia en su finally.
_escucha_activa: threading.Event = threading.Event()

# Token de generación de sesión — evita que una sesión de escucha vieja (bloqueada
# dentro de escuchar() cuando loop_principal fuerza una nueva sesión) pise el estado
# global que ya pertenece a la sesión nueva al terminar tardíamente.
_session_counter: list = [0]
_current_session_id: list = [0]

# Controla si el loop de visión está procesando (ojos abiertos).
# Comienza en False — se activa con "Jarvis abre los ojos".
# Cuando está cleared el loop de cámara corre a 1fps sin detección ni gestos.
_vision_activa: threading.Event = threading.Event()

# ── Logging ────────────────────────────────────────────────────────────────────
# RotatingFileHandler en vez de un FileHandler simple: el daemon corre indefinidamente
# en segundo plano — sin rotación, jarvis.log crece sin límite.

_log_handler = logging.handlers.RotatingFileHandler(
    filename=str(LOG_PATH), maxBytes=5_000_000, backupCount=3, encoding="utf-8",
)
_log_handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
))
logging.basicConfig(level=logging.INFO, handlers=[_log_handler])

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
    emitir_evento           = _mod.emitir_evento
    # Diagnóstico de módulos opcionales
    fs_ok = getattr(_mod, "_filesystem_disponible", False)
    v7_ok = getattr(_mod, "_vision_pantalla_disponible", False)
    print(f"[Daemon] _filesystem_disponible={fs_ok} | _vision_pantalla_disponible={v7_ok}", flush=True)
except Exception as e:
    print(f"[ERROR] No pude importar jarvis.py: {e}")
    sys.exit(1)

try:
    if str(JARVIS_DIR) not in sys.path:
        sys.path.insert(0, str(JARVIS_DIR))
    import rubrica_local
    _rubrica_local_disponible = True
except Exception as _e_rubrica:
    _rubrica_local_disponible = False
    print(f"[Daemon] rubrica_local no disponible: {_e_rubrica}", flush=True)


# ── Estado compartido audio ↔ vision ─────────────────────────────────────────

_vision_lock = threading.Lock()
_vision_estado = {
    "presencia_activa": False,
    "archivos_mencionados": [],       # rutas absolutas del vault mencionadas en la última respuesta
    "archivos_abiertos_por_jarvis": [],
    "solicitar_descanso": False,      # el daemon pide al vision loop que desactive la presencia
}


# ── Callback vision ───────────────────────────────────────────────────────────

def _extraer_slugs_mencionados(texto: str) -> list:
    """Retorna rutas absolutas de conceptos cuyo slug o título aparece en texto."""
    base = CEREBRO_PATH / "Conocimiento" / "Conceptos"
    if not base.exists():
        return []
    texto_lower = texto.lower()
    mencionados = []
    for archivo in base.glob("**/*.md"):
        slug = archivo.stem
        if slug in texto_lower or slug.replace("-", " ") in texto_lower:
            mencionados.append(str(archivo))
    return mencionados


def _vision_callback(texto_respuesta: str) -> None:
    """Extrae slugs del vault mencionados en la respuesta y actualiza estado compartido."""
    rutas = _extraer_slugs_mencionados(texto_respuesta)
    if rutas:
        with _vision_lock:
            _vision_estado["archivos_mencionados"] = rutas
        log(f"[Vision] Archivos mencionados: {[Path(r).stem for r in rutas]}")


def _vision_despedir() -> None:
    """Callback de despedida por gesto: sale del modo escucha activa y vuelve al wake word loop."""
    log("[Vision] Despedida por gesto — volviendo a modo wake word.")
    emitir_evento("idle", "Esperando wake word...")
    _vision_solicitar_descanso()
    try:
        _mod._salir_escucha[0] = True
    except Exception:
        pass


def _vision_solicitar_descanso() -> None:
    """Pide al loop de visión que desactive la presencia activa.
    Usado cuando el usuario dice 'chau Jarvis' por voz."""
    with _vision_lock:
        _vision_estado["solicitar_descanso"] = True
        _vision_estado["presencia_activa"] = False
    log("[Vision] Descanso solicitado — presencia será desactivada.")


def cargar_rutas_filesystem() -> str:
    """Construye resumen de aliases de filesystem para contexto y logging.
    Se llama una vez al arrancar, solo por su efecto de loguear los aliases disponibles."""
    try:
        if str(JARVIS_DIR) not in sys.path:
            sys.path.insert(0, str(JARVIS_DIR))
        from mejora_006_filesystem import RUTAS_CONOCIDAS
        lineas = ["Aliases de filesystem disponibles (alias → ruta):"]
        for alias, ruta in RUTAS_CONOCIDAS.items():
            lineas.append(f"- {alias} → {ruta}")
        resultado = "\n".join(lineas)
        log(f"Rutas de filesystem cargadas: {len(RUTAS_CONOCIDAS)} aliases.")
        return resultado
    except ImportError:
        log("[Filesystem] mejora_006_filesystem.py no encontrado — operacion_archivo no disponible.")
        return ""


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


def _es_eco_de_jarvis(transcripcion: str) -> bool:
    """True si la transcripción se parece demasiado al último texto que Jarvis habló.
    Detecta cuando el micrófono captura el rebote de los altavoces antes de que
    el usuario haya podido responder.

    Bypass automático para respuestas cortas (≤2 palabras) — afirmaciones como
    "sí", "dale", "ok" nunca se filtran aunque coincidan por accidente.
    """
    import re

    ultimo = getattr(_mod, "_last_spoken_text", "")
    if not ultimo or not transcripcion:
        return False

    # Respuestas muy cortas (afirmaciones, negaciones) nunca son eco
    if len(transcripcion.split()) <= 2:
        return False

    def _normalizar(texto: str) -> set:
        texto = re.sub(r"[¿?¡!.,;:()\"\']", " ", texto.lower())
        texto = re.sub(r"[-–—]", " ", texto)   # separar slugs con guiones
        return {w for w in texto.split() if len(w) > 2}  # descartar stopwords cortas

    palabras_habladas = _normalizar(ultimo)
    palabras_oidas    = _normalizar(transcripcion)

    if not palabras_oidas:
        return False

    overlap = len(palabras_oidas & palabras_habladas) / len(palabras_oidas)
    log(f"[EcoCheck] overlap={overlap:.2f} oído='{transcripcion[:50]}'")
    return overlap > 0.5


def _ejecutar_accion_pendiente_con_lock(tipo: str, param: str) -> None:
    """Toma lock_interaccion (si ya está disponible) antes de ejecutar la acción confirmada
    del watcher — mismo patrón que procesar_comando (~línea 648). Sin este lock, un comando
    de voz simultáneo podría lanzar otro proceso `claude` escribiendo el vault en paralelo."""
    lock = _lock_interaccion_ref[0]
    if lock is not None:
        with lock:
            _ejecutar_accion_pendiente(tipo, param)
    else:
        _ejecutar_accion_pendiente(tipo, param)


# ── Watcher conversacional — evaluar/reportar/confirmar/guardar (mejora-006, Fase 5a) ──

def _resolver_ruta_concepto(param: str) -> "Path | None":
    """`param` puede ser un slug o una ruta ya completa (como llega desde el watcher,
    que pasa el path del evento de filesystem)."""
    p = Path(param)
    if p.exists():
        return p
    conceptos_dir = CEREBRO_PATH / "Conocimiento" / "Conceptos"
    for candidato in conceptos_dir.rglob(f"{param}.md"):
        return candidato
    return None


def _dividir_frontmatter(contenido: str) -> tuple[str, str]:
    """Separa el bloque de frontmatter (con delimitadores '---') del cuerpo, sin
    parsear campos — se usa para reemplazar quirúrgicamente tags/cuerpo preservando
    el resto del frontmatter byte a byte."""
    partes = contenido.split("---", 2)
    if len(partes) < 3:
        raise ValueError("El archivo no tiene frontmatter YAML delimitado por '---'.")
    frontmatter_completo = f"---{partes[1]}---"
    cuerpo = partes[2].lstrip("\n")
    return frontmatter_completo, cuerpo


def _reemplazar_tags(frontmatter: str, tags_nuevos: list) -> str:
    """Reemplaza SOLO la línea `tags: [...]` dentro del bloque de frontmatter —
    nunca toca titulo/familia/relacionado/estado/fuentes/edges."""
    tags_str = ", ".join(str(t) for t in tags_nuevos)
    return re.sub(
        r"^tags:\s*\[.*?\]", f"tags: [{tags_str}]", frontmatter,
        count=1, flags=re.MULTILINE,
    )


def _guardar_propuesta(ruta: Path, slug: str, resultado: dict) -> bool:
    """Aplica la propuesta de rubrica_local al archivo: reemplaza tags: (si vienen)
    sin tocar el resto del frontmatter, y reemplaza el cuerpo completo si Groq
    propuso uno nuevo. Corre generar_index.py y hace git commit. True si se
    guardó sin error — nunca lanza."""
    try:
        contenido_actual = ruta.read_text(encoding="utf-8")
        frontmatter, cuerpo_actual = _dividir_frontmatter(contenido_actual)

        propuesta_fm = resultado.get("propuesta_frontmatter") or {}
        tags_nuevos = propuesta_fm.get("tags")
        if tags_nuevos:
            frontmatter = _reemplazar_tags(frontmatter, tags_nuevos)

        cuerpo_nuevo = resultado.get("propuesta_cuerpo") or cuerpo_actual
        nuevo_contenido = frontmatter + "\n\n" + cuerpo_nuevo.strip() + "\n"
        ruta.write_text(nuevo_contenido, encoding="utf-8")

        subprocess.run(
            [sys.executable, str(CEREBRO_PATH / "Prompts" / "Meta" / "generar_index.py")],
            capture_output=True, text=True, timeout=30,
        )
        ruta_relativa = str(ruta.relative_to(CEREBRO_PATH))
        subprocess.run(
            ["git", "-C", str(CEREBRO_PATH), "add", ruta_relativa],
            capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "-C", str(CEREBRO_PATH), "commit", "-m", f"feat: reevalúa {slug} via Jarvis"],
            capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL,
        )
        return True
    except Exception as e:
        log(f"[Watcher] Error guardando propuesta para {slug}: {e}")
        return False


# ── Profundización externa vía VPS — fusión local (mejora-006, Fase 5b) ──────

def _agregar_fuentes(frontmatter: str, fuentes_nuevas: list) -> str:
    """Agrega entradas nuevas al bloque `fuentes:` del frontmatter (sin duplicar
    URLs ya presentes), o crea el campo si no existe — preserva el resto del
    frontmatter línea por línea, mismo espíritu quirúrgico que _reemplazar_tags."""
    urls_existentes = set(re.findall(r'url:\s*"?([^"\n]*)"?', frontmatter))
    hoy = datetime.now().strftime("%Y-%m-%d")
    entradas = []
    for f in fuentes_nuevas or []:
        url = (f.get("url") or "").strip()
        if not url or url in urls_existentes:
            continue
        titulo = str(f.get("titulo", "")).replace('"', "'")
        fecha_acceso = f.get("fecha_acceso", hoy)
        entradas.append(f'  - titulo: "{titulo}"\n    url: "{url}"\n    fecha_acceso: {fecha_acceso}')
        urls_existentes.add(url)
    if not entradas:
        return frontmatter

    lineas = frontmatter.split("\n")
    idx_fuentes = next((i for i, l in enumerate(lineas) if l.startswith("fuentes:")), None)
    nuevas_lineas = [l for e in entradas for l in e.split("\n")]

    if idx_fuentes is None:
        idx_cierre = len(lineas) - 1
        while idx_cierre > 0 and lineas[idx_cierre].strip() != "---":
            idx_cierre -= 1
        lineas[idx_cierre:idx_cierre] = ["fuentes:"] + nuevas_lineas
    else:
        idx_fin = idx_fuentes + 1
        while idx_fin < len(lineas) and (lineas[idx_fin].startswith(" ") or lineas[idx_fin].startswith("-")):
            idx_fin += 1
        lineas[idx_fin:idx_fin] = nuevas_lineas

    return "\n".join(lineas)


def _fusionar_secciones_cuerpo(cuerpo: str, datos_y_evidencia: str, ejes_investigados: str) -> str:
    """Reemplaza (o agrega al final si no existen) las secciones '## Datos y
    evidencia' y '## Ejes investigados' del cuerpo — preserva el resto intacto."""
    def _reemplazar_o_agregar(cuerpo: str, encabezado: str, contenido_nuevo: str) -> str:
        if not contenido_nuevo:
            return cuerpo
        patron = re.compile(rf"^## {re.escape(encabezado)}\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
        bloque_nuevo = f"## {encabezado}\n{contenido_nuevo.strip()}\n\n"
        if patron.search(cuerpo):
            return patron.sub(bloque_nuevo, cuerpo, count=1)
        return cuerpo.rstrip() + "\n\n" + bloque_nuevo

    cuerpo = _reemplazar_o_agregar(cuerpo, "Datos y evidencia", datos_y_evidencia)
    cuerpo = _reemplazar_o_agregar(cuerpo, "Ejes investigados", ejes_investigados)
    return cuerpo


def _guardar_profundizacion(ruta: Path, slug: str, borrador: dict) -> bool:
    """Fusiona las secciones enriquecidas (Datos y evidencia, Ejes investigados,
    fuentes) del concepto_borrador devuelto por /evaluar del VPS DENTRO del archivo
    existente — preserva titulo/familia/tags/relacionado/edges/estado originales.
    Nunca pasa por /confirmar del VPS (rechaza con 409 porque el slug ya existe,
    ver hallazgo 3 de docs/plan-006.md). Mismo mecanismo de escritura que
    _guardar_propuesta: escribir → generar_index.py → git commit. True si se
    guardó sin error — nunca lanza."""
    try:
        contenido_actual = ruta.read_text(encoding="utf-8")
        frontmatter, cuerpo_actual = _dividir_frontmatter(contenido_actual)

        frontmatter = _agregar_fuentes(frontmatter, borrador.get("fuentes"))
        cuerpo_nuevo = _fusionar_secciones_cuerpo(
            cuerpo_actual,
            borrador.get("datos_y_evidencia", ""),
            borrador.get("ejes_investigados", ""),
        )
        nuevo_contenido = frontmatter + "\n\n" + cuerpo_nuevo.strip() + "\n"
        ruta.write_text(nuevo_contenido, encoding="utf-8")

        subprocess.run(
            [sys.executable, str(CEREBRO_PATH / "Prompts" / "Meta" / "generar_index.py")],
            capture_output=True, text=True, timeout=30,
        )
        ruta_relativa = str(ruta.relative_to(CEREBRO_PATH))
        subprocess.run(
            ["git", "-C", str(CEREBRO_PATH), "add", ruta_relativa],
            capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL,
        )
        subprocess.run(
            ["git", "-C", str(CEREBRO_PATH), "commit", "-m", f"feat: profundiza {slug} con fuentes externas via Jarvis"],
            capture_output=True, text=True, timeout=15, stdin=subprocess.DEVNULL,
        )
        return True
    except Exception as e:
        log(f"[Watcher] Error guardando profundización para {slug}: {e}")
        return False


def _flujo_evaluacion_conversacional(ruta: Path, slug: str) -> None:
    """Evalúa un concepto contra la rúbrica real (Groq local, sin Claude Code CLI —
    permite el diálogo de varios turnos que ejecutar_claude no puede dar), reporta
    hallazgos por voz, pregunta si guardar, y pregunta si profundizar con fuentes
    externas (Fase 5b — todavía no implementada, ver más abajo).

    Asume que el caller YA tiene lock_interaccion tomado (tanto
    _ejecutar_accion_pendiente_con_lock como procesar_comando lo hacen) — no toma
    el lock de nuevo acá."""
    if not _rubrica_local_disponible:
        hablar("El módulo de evaluación no está disponible, Luigui.")
        registrar_en_jarvis_log("WATCHER", f"Reevaluación: {slug}", "rubrica_local no disponible")
        return

    hablar(f"Un momento, evaluando {slug} contra la rúbrica...")
    try:
        resultado = rubrica_local.evaluar_concepto_con_groq(ruta)
    except Exception as e:
        log(f"[Watcher] Error evaluando {slug}: {e}")
        hablar("Hubo un problema al evaluar el concepto, Luigui.")
        registrar_en_jarvis_log("WATCHER", f"Reevaluación: {slug}", f"ERROR: {e}")
        return

    hallazgos = resultado.get("hallazgos") or []
    hablar(" ".join(hallazgos[:3]) if hallazgos else "No tengo observaciones puntuales.")

    tiene_propuesta = bool(resultado.get("propuesta_frontmatter") or resultado.get("propuesta_cuerpo"))
    guardado = False
    if tiene_propuesta:
        hablar("¿Guardo estos cambios?")
        respuesta = escuchar_respuesta(timeout=30)
        if respuesta and any(s in respuesta for s in _AFIRMACIONES):
            guardado = _guardar_propuesta(ruta, slug, resultado)
            hablar("Listo, guardé los cambios." if guardado else "Hubo un problema al guardar, Luigui.")
        else:
            hablar("Entendido, no guardo nada.")

    hablar("¿Quieres que profundice con fuentes externas?")
    respuesta2 = escuchar_respuesta(timeout=30)
    if respuesta2 and any(s in respuesta2 for s in _AFIRMACIONES):
        hablar("Investigando con fuentes externas, esto puede tardar un minuto...")
        cuerpo_para_investigar = ruta.read_text(encoding="utf-8")
        vps_resultado = _mod._profundizar_via_vps(cuerpo_para_investigar)

        if vps_resultado is None:
            # El error de conexión/timeout/token ya quedó hablado dentro de _profundizar_via_vps.
            registrar_en_jarvis_log(
                "WATCHER", f"Profundización externa: {slug}",
                f"{'Guardado' if guardado else 'Sin guardar'} — ERROR en llamada al VPS"
            )
            return

        if vps_resultado.get("estado") == "candidato_rechazado":
            hablar(vps_resultado.get("resumen_voz") or "El contenido no pasó la evaluación externa.")
            registrar_en_jarvis_log(
                "WATCHER", f"Profundización externa: {slug}",
                f"{'Guardado' if guardado else 'Sin guardar'} — rechazado por el VPS"
            )
            return

        hablar(vps_resultado.get("resumen_voz") or "Encontré información adicional.")
        hablar("¿Guardo la versión enriquecida?")
        respuesta3 = escuchar_respuesta(timeout=30)
        if respuesta3 and any(s in respuesta3 for s in _AFIRMACIONES):
            borrador = vps_resultado.get("concepto_borrador") or {}
            guardado_vps = _guardar_profundizacion(ruta, slug, borrador)
            hablar("Listo, guardé la versión enriquecida." if guardado_vps else "Hubo un problema al guardar, Luigui.")
            registrar_en_jarvis_log(
                "WATCHER", f"Profundización externa: {slug}",
                "Guardado" if guardado_vps else "ERROR al guardar"
            )
        else:
            hablar("Entendido, no guardo la versión enriquecida.")
            registrar_en_jarvis_log(
                "WATCHER", f"Profundización externa: {slug}",
                "Investigado, no guardado por decisión del usuario"
            )
    else:
        hablar("Entendido. ¿En qué más te puedo ayudar?")
        registrar_en_jarvis_log(
            "WATCHER", f"Reevaluación: {slug}",
            f"{'Guardado' if guardado else 'Sin guardar'} — {len(hallazgos)} hallazgos"
        )


def _ejecutar_accion_pendiente(tipo: str, param: str) -> None:
    """Ejecuta la acción del watcher que el usuario acaba de confirmar."""
    if tipo == "reevaluar_concepto":
        ruta = _resolver_ruta_concepto(param)
        slug = ruta.stem if ruta else param
        if ruta is None:
            hablar(f"No encontré el archivo de {param}, Luigui.")
            registrar_en_jarvis_log("WATCHER", f"Concepto modificado: {param}", "ERROR: archivo no encontrado")
            return
        _flujo_evaluacion_conversacional(ruta, slug)
    elif tipo == "evaluar_concepto":
        instruccion = (
            f"Evalúa el concepto {param} contra la rúbrica en Plantillas/rubrica.md, "
            f"actualiza su campo estado en el frontmatter, regenera INDEX.md con "
            f"generar_index.py, y propón 2 correlaciones con conceptos existentes del vault."
        )
        output = ejecutar_claude(instruccion)
        hablar(resumir_output_para_voz(output))
        registrar_en_jarvis_log("WATCHER", f"Nuevo concepto: {param}", "Evaluado y correlacionado")
    elif tipo == "leer_correlacion":
        try:
            contenido = Path(param).read_text(encoding="utf-8")[:2000]
            resumen = responder_con_groq(
                f"Resume esta correlación en 3 oraciones para leer en voz alta:\n{contenido}",
                [],
            )
            hablar(resumen)
        except Exception as e:
            log(f"[Watcher] Error leyendo correlación: {e}")


def escuchar_respuesta(timeout: int = 30) -> str | None:
    """Escucha una respuesta del usuario. Si detecta eco de Jarvis, descarta y reintenta
    (hasta 3 veces) para capturar la respuesta real del usuario."""
    import speech_recognition as sr
    while _mod._jarvis_hablando:
        time.sleep(0.1)
    eco_restante = _mod._last_hablar_end_time + _mod._ECO_BUFFER - time.time()
    if eco_restante > 0:
        time.sleep(eco_restante)
    recognizer = sr.Recognizer()
    _dev = seleccionar_dispositivo_entrada()
    for intento in range(3):
        try:
            with sr.Microphone(device_index=_dev) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.05)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            resultado = recognizer.recognize_google(audio, language="es-ES").lower()
            if _es_eco_de_jarvis(resultado):
                log(f"[STT] Echo detectado (intento {intento + 1}): '{resultado[:50]}' — reintentando")
                time.sleep(0.4)
                continue
            return resultado
        except sr.WaitTimeoutError:
            # Silencio — el usuario no habló en el tiempo dado
            log(f"[STT] Timeout en intento {intento + 1} — sin audio del usuario.")
            return None
        except sr.UnknownValueError:
            # STT no pudo entender el audio (eco residual o ruido) — reintentar
            log(f"[STT] UnknownValueError en intento {intento + 1} — reintentando.")
            time.sleep(0.3)
            continue
        except sr.RequestError as e:
            log(f"[STT] Error de API en intento {intento + 1}: {e} — abortando.")
            return None
        except Exception as e:
            log(f"[STT] Error inesperado en intento {intento + 1}: {e} — abortando.")
            return None
    log("[STT] 3 intentos sin resultado válido — retornando None")
    return None


# ── Watcher proactivo — handler ───────────────────────────────────────────────

class VaultEventHandler(FileSystemEventHandler):
    _eventos_recientes: list = []  # timestamps de eventos recientes
    _CONCEPTOS_PATH = str(CEREBRO_PATH / "Conocimiento" / "Conceptos")

    def __init__(self, on_nuevo_concepto, on_nueva_correlacion,
                 on_concepto_modificado, lock_interaccion):
        self._on_nuevo_concepto      = on_nuevo_concepto
        self._on_nueva_correlacion   = on_nueva_correlacion
        self._on_concepto_modificado = on_concepto_modificado
        self.lock_interaccion        = lock_interaccion
        self._timers: dict           = {}
        self._conceptos_pendientes: set = set()   # .md acumulados para auto-regenerar el ATLAS
        self._index_timer             = None       # timer compartido (no por-path) del auto-index
        self._index_lock              = threading.Lock()  # serializa ejecuciones de generar_index.py

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".md"):
            return
        self._debounce(event.src_path, self._handle_created)
        self._debounce_auto_index(event.src_path)

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".md"):
            return
        self._debounce(event.src_path, self._handle_modified)
        self._debounce_auto_index(event.src_path)

    def _debounce(self, path, handler):
        if path in self._timers:
            self._timers[path].cancel()
        timer = threading.Timer(3.0, handler, args=[path])
        self._timers[path] = timer
        timer.start()

    def _es_batch(self) -> bool:
        ahora = time.time()
        VaultEventHandler._eventos_recientes.append(ahora)
        VaultEventHandler._eventos_recientes = [
            t for t in VaultEventHandler._eventos_recientes if ahora - t <= 5
        ]
        if len(VaultEventHandler._eventos_recientes) > 3:
            logging.info("[Watcher] Batch detectado, omitiendo")
            return True
        return False

    def _handle_created(self, path):
        if self._es_batch():
            return
        slug = Path(path).stem
        if self.lock_interaccion.locked():
            tipo = "nueva_correlacion" if "Correlaciones" in path else "nuevo_concepto"
            _watcher_queue.put((tipo, slug, path))
            log(f"[Watcher] {Path(path).name} creado — encolado (interacción activa)")
            return
        if "Correlaciones" in path:
            self._on_nueva_correlacion(slug, path)
        elif "Conceptos" in path:
            self._on_nuevo_concepto(slug, path)

    def _handle_modified(self, path):
        if self._es_batch():
            return
        if self.lock_interaccion.locked():
            _watcher_queue.put(("concepto_modificado", Path(path).stem, path))
            return
        if "Conceptos" in path:
            self._on_concepto_modificado(Path(path).stem, path)

    def _debounce_auto_index(self, path: str) -> None:
        """Acumula archivos .md tocados en Conocimiento/Conceptos/ y, tras 3s sin
        actividad nueva, regenera el ATLAS automáticamente (independiente del flujo
        conversacional de _handle_created/_handle_modified — corre siempre, sin
        pedir confirmación por voz)."""
        if not path.startswith(self._CONCEPTOS_PATH):
            return
        self._conceptos_pendientes.add(path)
        if self._index_timer is not None:
            self._index_timer.cancel()
        self._index_timer = threading.Timer(3.0, self._ejecutar_auto_index)
        self._index_timer.start()

    def _ejecutar_auto_index(self) -> None:
        archivos = sorted(self._conceptos_pendientes)
        self._conceptos_pendientes = set()
        if not archivos:
            return
        # Si generar_index.py de un batch anterior sigue corriendo, esperar a que
        # termine antes de lanzar esta ejecución (no se omite, solo se serializa).
        with self._index_lock:
            n = len(archivos)
            if n == 1:
                hablar("Detecté un nuevo concepto en el vault. Ejecutando generar index para actualizar el Atlas.")
            else:
                hablar(f"Detecté {n} nuevos conceptos en el vault. Ejecutando generar index para actualizar el Atlas.")
            try:
                resultado = subprocess.run(
                    ["python3.11", "Prompts/Meta/generar_index.py"],
                    cwd=str(CEREBRO_PATH),
                    capture_output=True, text=True, timeout=60,
                )
                if resultado.returncode == 0:
                    hablar("Atlas actualizado.")
                else:
                    log(f"[Watcher] generar_index.py falló (código {resultado.returncode}): {resultado.stderr[:300]}")
                    hablar("Error al actualizar el Atlas. Revisa el log.")
            except Exception as e:
                log(f"[Watcher] Error ejecutando auto-index: {e}")
                hablar("Error al actualizar el Atlas. Revisa el log.")


# ── Watcher proactivo — callbacks ─────────────────────────────────────────────

_AFIRMACIONES = ("sí", "si", "dale", "claro", "adelante", "ok", "sí por favor")


def _activar_modo_escucha_watcher() -> None:
    """Activa modo escucha 60s después de una notificación del watcher.
    No activa si ya hay una sesión activa (lock tomado) para evitar escuchas paralelas.
    Siempre limpia _pausa_wake_word al salir, incluso en returns tempranos,
    para que el loop de wake word pueda recuperar el micrófono."""
    lock = _lock_interaccion_ref[0]
    if lock is None:
        _pausa_wake_word.clear()
        return
    if lock.locked():
        log("[Watcher] Sesión activa — omitiendo activación de escucha post-notificación.")
        _pausa_wake_word.clear()
        return
    log("[Watcher] Activando modo escucha tras notificación (60s, silencioso).")
    emitir_evento("escuchando", "Di tu comando...")
    _pausa_wake_word.set()  # ya seteado por el callback — no-op
    try:
        # silencioso=True: no habla si no escucha nada → evita que Jarvis se escuche a sí mismo
        modo_escucha_activo(lock, silencioso=True)
    finally:
        _pausa_wake_word.clear()


def _activar_escucha_vision() -> None:
    """Activa modo escucha 30s silencioso tras saludo de presencia.
    Corre en thread propio para no bloquear el loop de visión."""
    lock = _lock_interaccion_ref[0]
    if lock is None or lock.locked():
        return
    def _run():
        time.sleep(2.0)  # el saludo dura ~3s — esperar que el eco físico se disipe
        log("[Vision] Activando modo escucha tras saludo de presencia (30s, silencioso).")
        emitir_evento("escuchando", "Di tu comando...")
        _pausa_wake_word.set()
        try:
            modo_escucha_activo(lock, timeout=30, silencioso=True)
        finally:
            _pausa_wake_word.clear()
    threading.Thread(target=_run, daemon=True).start()


def _drain_watcher_queue(lock_interaccion: threading.Lock) -> None:
    """Procesa eventos del watcher encolados durante la sesión activa."""
    while not _watcher_queue.empty():
        try:
            tipo, slug, path = _watcher_queue.get_nowait()
            log(f"[Watcher] Procesando evento encolado: {tipo} — {slug}")
            if tipo == "nuevo_concepto":
                on_nuevo_concepto(slug, path)
            elif tipo == "nueva_correlacion":
                on_nueva_correlacion(slug, path)
            elif tipo == "concepto_modificado":
                on_concepto_modificado(slug, path)
        except queue.Empty:
            break


def on_nuevo_concepto(slug: str, path: str) -> None:
    titulo = leer_titulo_frontmatter(path) or slug
    log(f"[Watcher] Nuevo concepto detectado: {slug}")
    emitir_evento("watcher", f"Nuevo concepto: {titulo}")
    hablar("Nuevo concepto detectado en el vault.")


def on_nueva_correlacion(slug: str, path: str) -> None:
    log(f"[Watcher] Nueva correlación detectada: {slug}")
    emitir_evento("watcher", f"Nueva correlación: {slug}")
    _pausa_wake_word.set()
    time.sleep(1.5)
    try:
        hablar(f"Identifico una nueva correlación: {slug}. ¿Quieres que la lea?")
        respuesta = escuchar_respuesta(timeout=30)
        if respuesta and any(s in respuesta for s in _AFIRMACIONES):
            _accion_pendiente_watcher[0] = None
            _ejecutar_accion_pendiente_con_lock("leer_correlacion", path)
        else:
            log(f"[Watcher] Lectura de correlación {slug} no capturada — guardando como pendiente.")
            _accion_pendiente_watcher[0] = ("leer_correlacion", path)
    except Exception as e:
        log(f"[Watcher] Error en on_nueva_correlacion: {e}")
    finally:
        _activar_modo_escucha_watcher()


def on_concepto_modificado(slug: str, path: str) -> None:
    log(f"[Watcher] Concepto modificado: {slug}")
    hablar("Concepto modificado detectado en el vault.")


# ── Wake word via STT ─────────────────────────────────────────────────────────

WAKE_WORDS = ("jarvis", "jarvi", "jarvis!", "oye jarvis")

def seleccionar_dispositivo_entrada() -> "int | None":
    """Devuelve el índice del micrófono físico del Mac, ignorando virtual devices.
    Prioriza 'MacBook Pro (micrófono)' sobre Teams Audio, rekordbox Aggregate Device,
    o cualquier otro virtual device que pudiera estar activo como default del sistema.
    Fallback a None si no encuentra el nombre esperado."""
    import speech_recognition as sr
    try:
        nombres = sr.Microphone.list_microphone_names()
        preferidos = ("macbook pro (micrófono)", "built-in microphone", "macbook air (micrófono)")
        for i, nombre in enumerate(nombres):
            if any(p in nombre.lower() for p in preferidos):
                log(f"[Mic] Dispositivo fijado: [{i}] {nombre}")
                return i
    except Exception as e:
        log(f"[Mic] No se pudo seleccionar dispositivo: {e}")
    log("[Mic] Usando dispositivo de entrada por defecto del sistema (None)")
    return None


def esperar_wake_word(device_index: "int | None" = None) -> str:
    """Escucha continuamente hasta detectar la wake word via STT.
    Retorna el texto completo que activó la wake word — puede contener
    un comando adicional (ej. 'chau jarvis') que loop_principal procesará.
    Cuando _pausa_wake_word está activo, CIERRA el micrófono físicamente
    para que otras sesiones (watcher callbacks) puedan abrirlo sin conflicto."""
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    log(f"Esperando wake word {WAKE_WORDS}...")

    while True:
        # No abrir el micrófono mientras otra sesión lo necesita exclusivamente
        if _pausa_wake_word.is_set():
            time.sleep(0.2)
            continue

        try:
            with sr.Microphone(device_index=device_index) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                log("[Wake] Micrófono calibrado. Escuchando de forma continua...")
                while True:
                    try:
                        print("[🎤]", end=" ", flush=True)
                        if _mod._jarvis_hablando:
                            time.sleep(0.1)
                            continue
                        if _pausa_wake_word.is_set():
                            log("[Wake] Pausa solicitada — liberando micrófono.")
                            break  # salir del with → cierra el stream PortAudio
                        if time.time() - _mod._last_hablar_end_time < 1.5:
                            time.sleep(0.2)
                            continue
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=6)
                        if _pausa_wake_word.is_set():
                            log("[Wake] Pausa post-listen — liberando micrófono.")
                            break
                        if _mod._jarvis_hablando:
                            continue
                        if time.time() - _mod._last_hablar_end_time < 1.5:
                            continue
                        texto = recognizer.recognize_google(audio, language="es-ES").lower()
                        log(f"[Wake] Escuchado: '{texto}'")
                        if not any(w in texto for w in WAKE_WORDS):
                            log(f"[Wake] Falso positivo ignorado — sin wake word: '{texto}'")
                            continue
                        return texto
                    except sr.WaitTimeoutError:
                        if _pausa_wake_word.is_set():
                            log("[Wake] Pausa en timeout — liberando micrófono.")
                            break
                        continue
                    except sr.UnknownValueError:
                        continue
                    except Exception as e:
                        log(f"[Wake] Error: {e}")
                        continue
        except Exception as e:
            log(f"[Wake] Error al abrir micrófono: {e}")
            time.sleep(1.0)


# ── Ciclo principal ───────────────────────────────────────────────────────────

_DESPEDIDAS = (
    "te hablo luego", "hasta luego", "bye", "chau", "chao", "adiós", "adios",
    "descansa", "modo espera", "ya terminé", "ya termine", "para jarvis",
    "para ya", "detente", "silencio", "apágate", "apagate",
)

_ABRIR_OJOS = (
    "abre los ojos", "abre ojos",
    "activa la cámara", "activa la camara",
    "activa visión", "activa vision", "activa cámara", "activa camara",
    "enciende la cámara", "enciende la camara", "enciende la vision",
)

_CERRAR_OJOS = (
    "cierra los ojos", "cierra ojos",
    "desactiva la cámara", "desactiva la camara",
    "desactiva visión", "desactiva vision", "apaga la cámara", "apaga la camara",
    "apaga la visión", "apaga la vision", "duerme la camara",
)


def _es_despedida(texto: str) -> bool:
    t = texto.lower()
    return any(d in t for d in _DESPEDIDAS)


def _es_abrir_ojos(texto: str) -> bool:
    t = texto.lower()
    return any(p in t for p in _ABRIR_OJOS)


def _es_cerrar_ojos(texto: str) -> bool:
    t = texto.lower()
    return any(p in t for p in _CERRAR_OJOS)


def procesar_comando(lock_interaccion: threading.Lock) -> bool:
    """Escucha un comando y despacha via jarvis.py. Retorna True si hubo comando."""
    texto = escuchar()
    if texto is None:
        return False
    if _es_eco_de_jarvis(texto):
        log(f"[STT] Echo en procesar_comando descartado: '{texto[:50]}'")
        return False  # cuenta como silencio — no activa ningún intent

    # Acción pendiente del watcher: si el usuario dice una afirmación, ejecutar
    # directamente sin pasar por Groq — Groq no tiene contexto de la pregunta del watcher.
    if _accion_pendiente_watcher[0]:
        if any(s in texto for s in _AFIRMACIONES):
            tipo, param = _accion_pendiente_watcher[0]
            _accion_pendiente_watcher[0] = None
            log(f"[Watcher] Confirmación recibida en modo escucha: ejecutando {tipo}({param})")
            with lock_interaccion:
                _ejecutar_accion_pendiente(tipo, param)
            return True
        else:
            # El usuario dijo otra cosa — la acción pendiente ya no aplica
            log(f"[Watcher] Acción pendiente cancelada — usuario dijo: '{texto[:40]}'")
            _accion_pendiente_watcher[0] = None

    with lock_interaccion:
        if _es_despedida(texto):
            log(f"Despedida detectada: '{texto}'")
            emitir_evento("idle", "Hasta luego...")
            hablar("Hasta luego, Luigui. Di Jarvis cuando me necesites.")
            _vision_solicitar_descanso()
            _mod._salir_escucha[0] = True
            return True

        if _es_abrir_ojos(texto):
            log("[Vision] Activando visión por comando de voz.")
            _vision_activa.set()
            emitir_evento("watcher", "Visión activada — ojos abiertos")
            hablar("Ojos abiertos.")
            return True

        if _es_cerrar_ojos(texto):
            log("[Vision] Desactivando visión por comando de voz.")
            _vision_activa.clear()
            _vision_solicitar_descanso()
            emitir_evento("idle", "Visión desactivada — ojos cerrados")
            hablar("Entendido. Cerrando los ojos.")
            return True

        emitir_evento("procesando", texto[:60])
        intent, params = detectar_intent(texto, historial_sesion)
        log(f"Intent: {intent} | Params: {params}")
        actualizar_historial(texto, (intent, params))
        despachar_intent(intent, params, texto, vision_callback=_vision_callback)
    return True


MAX_SILENCIAS = 3  # fallos STT consecutivos antes de volver al modo wake word


def modo_escucha_activo(lock_interaccion: threading.Lock,
                        timeout: int = MODO_ESCUCHA_TIMEOUT,
                        silencioso: bool = False,
                        forzar: bool = False) -> None:
    """Mantiene Jarvis en escucha activa por `timeout` segundos.
    El timer se reinicia DESPUÉS de que Mónica termina de hablar, via callback.
    Tras MAX_SILENCIAS fallos STT consecutivos duerme automáticamente.
    silencioso=True: sale sin hablar al agotar silencios (activación por presencia/watcher).

    Token de generación de sesión: si loop_principal fuerza una sesión nueva (forzar=True)
    mientras esta sigue bloqueada dentro de escuchar() esperando audio, esta sesión vieja
    puede terminar después de que la nueva ya tomó el control. El finally solo limpia el
    estado global (_response_complete_callback, _escucha_activa) si `my_id` sigue siendo
    la sesión vigente — si no, la sesión nueva ya es la dueña y no debe pisarse."""
    if not forzar and _escucha_activa.is_set():
        log("[Escucha] Ya hay sesión activa — activación ignorada.")
        return

    _session_counter[0] += 1
    my_id = _session_counter[0]
    _current_session_id[0] = my_id

    _escucha_activa.set()
    _deadline = [time.time() + timeout]
    silencias = 0

    def _reset_timer():
        _deadline[0] = time.time() + timeout
        log(f"Timer reiniciado ({timeout}s) tras respuesta completa.")

    _mod._response_complete_callback = _reset_timer
    _mod._salir_escucha[0] = False
    log(f"Modo escucha activo ({MODO_ESCUCHA_TIMEOUT}s). Sin wake word necesario. [sesión {my_id}]")

    try:
        while time.time() < _deadline[0]:
            hubo_comando = procesar_comando(lock_interaccion)

            if hubo_comando:
                silencias = 0
            else:
                silencias += 1
                if silencias >= MAX_SILENCIAS:
                    log(f"[Escucha] {MAX_SILENCIAS} silencios consecutivos — durmiendo.")
                    if not silencioso:
                        hablar("No te escucho, Luigui. Di Jarvis cuando me necesites.")
                    break
                if not silencioso:
                    hablar("No te escuché. Intenta de nuevo." if silencias == 1 else "No te escucho bien. Un intento más.")

            if _mod._salir_escucha[0]:
                log("Modo escucha cerrado por despedida del usuario.")
                break
    finally:
        if my_id == _current_session_id[0]:
            _mod._response_complete_callback = None
            _mod._salir_escucha[0] = False
            _escucha_activa.clear()
            emitir_evento("idle", "Esperando wake word...")
            log(f"Volviendo al loop de wake word. [sesión {my_id}]")
        else:
            log(f"[Escucha] Sesión {my_id} finalizó tardíamente — "
                f"sesión {_current_session_id[0]} ya tomó el control, no piso su estado.")


def loop_principal(lock_interaccion: threading.Lock) -> None:
    """Ciclo infinito: espera wake word via STT, ejecuta flujo de escucha activa."""
    log("Daemon iniciado. Di 'Jarvis' para activar.")

    try:
        while True:
            device_index = seleccionar_dispositivo_entrada()
            texto_wake = esperar_wake_word(device_index)
            if not any(w in texto_wake for w in WAKE_WORDS):
                log(f"[Wake] Guard loop — texto sin wake word descartado: '{texto_wake}'")
                continue
            log(f"Wake word detectado en: '{texto_wake}'")

            # Comandos inline en la frase wake word — procesar sin entrar al modo escucha.
            if _es_despedida(texto_wake):
                log("Despedida detectada en wake word — omitiendo modo escucha.")
                emitir_evento("idle", "Hasta luego...")
                hablar("Hasta luego, Luigui. Di Jarvis cuando me necesites.")
                _vision_solicitar_descanso()
                continue

            if _es_abrir_ojos(texto_wake):
                log("[Vision] Activando visión desde wake word.")
                _vision_activa.set()
                emitir_evento("watcher", "Visión activada — ojos abiertos")
                hablar("Ojos abiertos.")
                continue

            if _es_cerrar_ojos(texto_wake):
                log("[Vision] Desactivando visión desde wake word.")
                _vision_activa.clear()
                _vision_solicitar_descanso()
                emitir_evento("idle", "Visión desactivada — ojos cerrados")
                hablar("Entendido. Cerrando los ojos.")
                continue

            emitir_evento("escuchando", "Di tu comando...")
            _mod._salir_escucha[0] = True   # abortar sesión secundaria activa si existe
            _escucha_activa.clear()          # liberar el flag para la nueva sesión
            hablar("Dime, Luigui.")
            modo_escucha_activo(lock_interaccion, forzar=True)
            _drain_watcher_queue(lock_interaccion)
            log("Volviendo al loop de wake word.")
    except KeyboardInterrupt:
        log("Daemon detenido por KeyboardInterrupt.")


# ── Main ───────────────────────────────────────────────────────────────────────

def diagnosticar_microfono() -> None:
    """Lista los micrófonos disponibles y confirma cuál usa sr.Microphone() por defecto."""
    import speech_recognition as sr
    try:
        nombres = sr.Microphone.list_microphone_names()
        log(f"[Mic] Micrófonos disponibles ({len(nombres)}):")
        for i, nombre in enumerate(nombres):
            log(f"  [{i}] {nombre}")
        with sr.Microphone() as source:
            idx = source.device_index
            if idx is not None and idx < len(nombres):
                nombre_activo = nombres[idx]
            else:
                nombre_activo = "dispositivo por defecto del sistema"
            log(f"[Mic] Dispositivo activo: índice={idx} — {nombre_activo}")
    except Exception as e:
        log(f"[Mic] Error en diagnóstico: {e}")


_pid_lock_fd: "int | None" = None  # mantenido abierto todo el ciclo de vida del proceso


def _acquire_pid_lock() -> bool:
    """Devuelve True si esta instancia puede continuar; False si ya hay otra corriendo.
    Usa flock() sobre un file descriptor que se mantiene abierto durante toda la
    vida del proceso — el kernel libera el lock automáticamente al morir el
    proceso por CUALQUIER motivo (exit limpio, excepción, SIGTERM, SIGKILL,
    crash), sin depender de que el código de cleanup llegue a correr.

    El diseño anterior (crear el archivo con O_CREAT|O_EXCL y comprobar el PID
    leído contra os.kill(pid, 0) en cada arranque) tiene una ventana real: si
    algo borra jarvis.pid mientras el proceso dueño sigue vivo — un `rm` manual,
    otro script, una limpieza mal dirigida — el siguiente arranque encuentra el
    archivo ausente y adquiere el lock igual, aunque el daemon original nunca
    dejó de correr. Se reprodujo exactamente eso en vivo: dos y hasta tres
    procesos jarvis_daemon.py corriendo en simultáneo. flock() no tiene esa
    ventana: la exclusión la garantiza el kernel sobre el file descriptor, no
    un valor de texto que cualquiera puede pisar."""
    global _pid_lock_fd
    fd = os.open(str(PID_FILE), os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        return False
    os.ftruncate(fd, 0)
    os.write(fd, str(os.getpid()).encode())
    os.fsync(fd)
    _pid_lock_fd = fd
    return True


def _release_pid_lock() -> None:
    global _pid_lock_fd
    if _pid_lock_fd is None:
        return
    try:
        fcntl.flock(_pid_lock_fd, fcntl.LOCK_UN)
        os.close(_pid_lock_fd)
    except Exception:
        pass
    _pid_lock_fd = None


def _iniciar_dashboard() -> None:
    """Arranca el dashboard solo si no está ya corriendo.
    Si está vivo, lo deja en paz para preservar la ventana de Chrome existente.

    Detecta "¿está vivo?" intentando tomar el mismo flock() no bloqueante que
    dashboard/server.py mantiene abierto toda su vida — no leyendo un PID de
    texto y probando os.kill(pid, 0), que falla si algo borra dashboard.pid
    mientras el servidor sigue corriendo (ver la misma corrección en
    _acquire_pid_lock más arriba)."""
    _dashboard_path = JARVIS_DIR / "dashboard" / "server.py"
    _dashboard_pid  = JARVIS_DIR / "dashboard" / "dashboard.pid"

    _fd = os.open(str(_dashboard_pid), os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(_fd)
        log("[Dashboard] Ya corriendo — ventana de Chrome preservada.")
        return
    else:
        # Nadie lo tenía tomado → el dashboard no está vivo. Soltar de inmediato:
        # este lock es del servidor, el daemon solo lo usó para verificar.
        fcntl.flock(_fd, fcntl.LOCK_UN)
        os.close(_fd)

    # Libera solo puertos del dashboard (no 8765/8766 que no usa)
    subprocess.run(
        ["bash", "-c", "lsof -ti:7777,7778 | xargs kill -9 2>/dev/null"],
        capture_output=True,
    )
    time.sleep(0.8)

    if not _dashboard_path.exists():
        log("[Dashboard] server.py no encontrado — continuando sin él.")
        return

    try:
        subprocess.Popen(["/usr/local/bin/python3.11", str(_dashboard_path)])
        log("Dashboard iniciado en http://localhost:7777")
        time.sleep(1.2)
    except Exception as e:
        log(f"[Dashboard] Error al arrancar — continuando sin él: {e}")


# ── Saludo proactivo + sync diario al arrancar ────────────────────────────────

_LAST_BOOT_PATH = Path.home() / ".jarvis_last_boot"
_LAST_SYNC_PATH  = Path.home() / ".jarvis_last_sync"


def _leer_timestamp(path: Path) -> str | None:
    """Lee la primera línea de un archivo de timestamp ISO. None si no existe o está vacío
    (primer arranque)."""
    try:
        lineas = path.read_text(encoding="utf-8").strip().splitlines()
        return lineas[0] if lineas else None
    except FileNotFoundError:
        return None
    except Exception as e:
        log(f"[Boot] Error leyendo {path}: {e}")
        return None


def _escribir_timestamp(path: Path) -> None:
    """Formato 'YYYY-MM-DD HH:MM:SS' (no ISO con 'T'/microsegundos) — verificado que
    `git log --since` parsea este formato correctamente; el ISO con 'T' lo ignora
    en silencio y devuelve el historial completo, sin filtrar nada."""
    try:
        path.write_text(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n", encoding="utf-8")
    except Exception as e:
        log(f"[Boot] Error escribiendo {path}: {e}")


def _sync_diario_si_corresponde() -> bool:
    """Si el vault no se sincronizó hoy, hace git pull silencioso (fetch + pull —
    sin diff previo: el saludo usa `git log --since` sobre el repo ya actualizado,
    así que no hace falta reportar los archivos del pull por separado). Nunca
    bloquea el arranque: cualquier falla se loguea y el daemon sigue igual."""
    ultimo_sync = _leer_timestamp(_LAST_SYNC_PATH)
    hoy = datetime.now().date().isoformat()
    if ultimo_sync and ultimo_sync.startswith(hoy):
        return False
    try:
        _git_env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        subprocess.run(
            ["git", "-C", str(CEREBRO_PATH), "fetch", "origin", "main"],
            capture_output=True, text=True, timeout=30,
            stdin=subprocess.DEVNULL, env=_git_env,
        )
        pull = subprocess.run(
            ["git", "-C", str(CEREBRO_PATH), "pull", "origin", "main"],
            capture_output=True, text=True, timeout=30,
            stdin=subprocess.DEVNULL, env=_git_env,
        )
        if pull.returncode != 0:
            log(f"[Boot] Sync diario: pull falló — {pull.stderr[:150]}")
            return False
        _escribir_timestamp(_LAST_SYNC_PATH)
        log("[Boot] Sync diario completado.")
        return True
    except subprocess.TimeoutExpired:
        log("[Boot] Sync diario: timeout.")
        return False
    except Exception as e:
        log(f"[Boot] Sync diario: error {e}")
        return False


def _slugs_nuevos_desde(desde: str) -> list[str]:
    """Slugs de archivos .md agregados en Conocimiento/Conceptos desde `desde`
    (formato aceptado por `git log --since`), filtrados a los que siguen
    existiendo en disco — un concepto agregado y luego borrado dentro del mismo
    rango no debe mencionarse como novedad."""
    resultado = subprocess.run(
        ["git", "-C", str(CEREBRO_PATH), "log", f"--since={desde}",
         "--name-only", "--diff-filter=A", "--pretty=format:",
         "--", "Conocimiento/Conceptos"],
        capture_output=True, text=True, timeout=15,
        stdin=subprocess.DEVNULL,
    )
    if resultado.returncode != 0:
        return []
    candidatos = {f.strip() for f in resultado.stdout.splitlines() if f.strip().endswith(".md")}
    return sorted(
        Path(f).stem for f in candidatos
        if (CEREBRO_PATH / f).exists()
    )


def _saludo_proactivo_y_sync() -> str:
    """Rutina de arranque: sync diario silencioso + saludo mencionando conceptos
    nuevos desde el último boot. Nunca lanza — cualquier error cae al saludo estándar."""
    saludo_estandar = "Jarvis listo. ¿En qué te ayudo?"
    try:
        _sync_diario_si_corresponde()
        ultimo_boot = _leer_timestamp(_LAST_BOOT_PATH)
        desde = ultimo_boot if ultimo_boot else "24 hours ago"
        slugs = _slugs_nuevos_desde(desde)
        _escribir_timestamp(_LAST_BOOT_PATH)
        if not slugs:
            return saludo_estandar
        n = len(slugs)
        lista = ", ".join(slugs[:5]) + ("..." if n > 5 else "")
        return (
            f"Buenos días Luigui. Desde la última vez que hablamos, se agregaron "
            f"{n} concepto{'s' if n != 1 else ''} nuevo{'s' if n != 1 else ''}: {lista}. "
            f"¿Quieres que los revisemos?"
        )
    except Exception as e:
        log(f"[Boot] Saludo proactivo: error {e} — usando saludo estándar.")
        return saludo_estandar


def main():
    if not _acquire_pid_lock():
        print(f"[Jarvis] Instancia ya corriendo. Saliendo.", flush=True)
        sys.exit(0)

    log("=== Jarvis Daemon arrancando ===")
    _iniciar_dashboard()

    observer = None
    try:
        diagnosticar_microfono()
        seleccionar_dispositivo_entrada()
        cargar_rutas_filesystem()
        lock_interaccion = threading.Lock()
        _lock_interaccion_ref[0] = lock_interaccion

        # Habilita "Jarvis, reevalúa este concepto" por voz directa (no solo watcher) —
        # ver _reevaluar_concepto_callback en jarvis.py. No toma el lock: ya se ejecuta
        # desde dentro de procesar_comando(), que lo tiene tomado.
        def _reevaluar_por_voz(slug: str) -> None:
            ruta = _resolver_ruta_concepto(slug)
            if ruta is None:
                hablar(f"No encontré el archivo de {slug}, Luigui.")
                return
            _flujo_evaluacion_conversacional(ruta, ruta.stem)
        _mod._reevaluar_concepto_callback = _reevaluar_por_voz

        _conocimiento_path = CEREBRO_PATH / "Conocimiento"
        if _conocimiento_path.exists():
            handler = VaultEventHandler(
                on_nuevo_concepto=on_nuevo_concepto,
                on_nueva_correlacion=on_nueva_correlacion,
                on_concepto_modificado=on_concepto_modificado,
                lock_interaccion=lock_interaccion,
            )
            observer = Observer()
            observer.schedule(handler, str(_conocimiento_path), recursive=True)
            observer.start()
            log("Watcher activo en Conocimiento/")
        else:
            log(f"[Watcher] '{_conocimiento_path}' no existe — arrancando sin watcher del vault.")

        # Vision loop — no bloquea el arranque si la cámara o las dependencias no están
        try:
            import sys as _sys
            _sys.path.insert(0, str(JARVIS_DIR))
            import jarvis_vision as _vision_mod
            _t_vision = threading.Thread(
                target=_vision_mod.loop_vision,
                args=(_vision_estado, _vision_lock, hablar),
                kwargs={
                    "despedir_fn": _vision_despedir,
                    "emitir_evento_fn": emitir_evento,
                    "activar_escucha_fn": _activar_escucha_vision,
                    "vision_activa_event": _vision_activa,
                },
                daemon=True,
            )
            _t_vision.start()
            log("[Vision] Thread de visión iniciado — ojos cerrados. Di 'Jarvis abre los ojos' para activar.")
        except Exception as _ve:
            log(f"[Vision] No disponible — continuando sin vision: {_ve}")

        try:
            saludo = _saludo_proactivo_y_sync()
        except Exception as _se:
            log(f"[Boot] Saludo proactivo falló por completo — usando estándar: {_se}")
            saludo = "Jarvis listo. ¿En qué te ayudo?"
        hablar(saludo)

        loop_principal(lock_interaccion)
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
        _release_pid_lock()


if __name__ == "__main__":
    main()
