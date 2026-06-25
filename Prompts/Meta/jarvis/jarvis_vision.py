#!/usr/local/bin/python3.11
"""
jarvis_vision.py — Detección de presencia, reconocimiento facial y gestos para Jarvis.
Usa cv2 (frame differencing + YuNet + SFace) + MediaPipe Hands.
No importa jarvis.py — recibe hablar_fn y estado compartido como parámetros.
"""

import logging
import subprocess
import time
from collections import deque
from pathlib import Path
from typing import Callable

import cv2
import mediapipe as mp

_LOGGER = logging.getLogger("jarvis_vision")

JARVIS_DIR = Path(__file__).parent

# ── Constantes de captura ─────────────────────────────────────────────────────

CAM_WIDTH  = 640
CAM_HEIGHT = 480
FPS_ACTIVO   = 15    # frames/s con presencia detectada
FPS_INACTIVO = 1     # frames/s en modo bajo consumo

# ── Constantes de detección ───────────────────────────────────────────────────

UMBRAL_DIFF        = 25      # 0-255; diferencia mínima de pixel para contar como movimiento
AREA_MIN_PRESENCIA = 5000    # px² — contorno mínimo para confirmar presencia
TIMEOUT_AUSENCIA   = 30      # segundos sin movimiento para bajar a modo bajo consumo
DURACION_MANO      = 2.5     # segundos que la mano abierta debe sostenerse
VENTANA_BARRIDO    = 0.5     # segundos de historial para detectar barrido
DELTA_BARRIDO      = -80     # px a la izquierda en la ventana para confirmar barrido
COOLDOWN_BARRIDO   = 2.0     # segundos mínimos entre barridos consecutivos

VENTANA_OLA   = 1.5    # segundos de historial para detectar ola de despedida
AMPLITUD_OLA  = 30     # px — amplitud mínima de cada media oscilación
CAMBIOS_OLA   = 2      # cambios de dirección mínimos para confirmar ola
COOLDOWN_OLA  = 3.0    # segundos mínimos entre olas consecutivas

# ── Reconocimiento facial — YuNet + SFace ─────────────────────────────────────

MODELO_DETECTOR    = JARVIS_DIR / "yunet.onnx"
MODELO_RECONOCEDOR = JARVIS_DIR / "sface.onnx"
FOTO_REFERENCIA    = JARVIS_DIR / "luigui.jpg"
UMBRAL_COSENO      = 0.363   # umbral oficial de SFace: >= mismo usuario
COOLDOWN_VERIFICACION = 3.0  # segundos mínimos entre intentos de verificación

# Estado del reconocimiento (inicializado en _init_reconocimiento_facial)
_detector_facial    = None
_reconocedor_facial = None
_encoding_referencia = None  # None → modo degradado (cualquier presencia activa)


def _init_reconocimiento_facial() -> bool:
    """
    Inicializa YuNet + SFace y carga el encoding de la foto de referencia.
    Retorna True si el reconocimiento está activo.
    Si falta algún recurso, registra un aviso y retorna False (modo degradado).
    """
    global _detector_facial, _reconocedor_facial, _encoding_referencia

    if not MODELO_DETECTOR.exists() or not MODELO_RECONOCEDOR.exists():
        _LOGGER.warning(
            "[Vision] Modelos de reconocimiento facial no encontrados — "
            "modo degradado (cualquier presencia activa Jarvis). "
            "Para activar: python3 Prompts/Meta/jarvis/jarvis_capturar_foto.py"
        )
        return False

    if not FOTO_REFERENCIA.exists():
        _LOGGER.warning(
            f"[Vision] Foto de referencia no encontrada en {FOTO_REFERENCIA} — "
            "modo degradado. Ejecuta: python3 Prompts/Meta/jarvis/jarvis_capturar_foto.py"
        )
        return False

    try:
        foto = cv2.imread(str(FOTO_REFERENCIA))
        if foto is None:
            _LOGGER.warning("[Vision] No se pudo leer la foto de referencia.")
            return False

        rec = cv2.FaceRecognizerSF.create(str(MODELO_RECONOCEDOR), "")

        # Extraer encoding en la misma resolución que se usará en vivo (320x240)
        # para garantizar alineación consistente entre referencia y frames de cámara
        foto_pequeña = cv2.resize(foto, (320, 240))
        det = cv2.FaceDetectorYN.create(str(MODELO_DETECTOR), "", (320, 240), score_threshold=0.7)

        _, caras = det.detect(foto_pequeña)
        if caras is None or len(caras) == 0:
            _LOGGER.warning("[Vision] No se detectó cara en la foto de referencia (320x240).")
            return False

        cara_alineada = rec.alignCrop(foto_pequeña, caras[0])
        _encoding_referencia = rec.feature(cara_alineada)

        _detector_facial = det
        _reconocedor_facial = rec
        _LOGGER.info("[Vision] Reconocimiento facial activo — solo Luigui activará la presencia.")
        return True

    except Exception as e:
        _LOGGER.warning(f"[Vision] Error inicializando reconocimiento facial: {e}")
        _detector_facial = _reconocedor_facial = _encoding_referencia = None
        return False


def _es_luigui(frame) -> bool:
    """
    True si el frame contiene la cara de Luigui (similitud coseno >= UMBRAL_COSENO).
    Usa frame reducido a 320x240 para mantener CPU bajo.
    Retorna True si el reconocimiento no está disponible (modo degradado).
    """
    if _encoding_referencia is None:
        return True  # modo degradado — aceptar cualquier presencia

    try:
        pequeño = cv2.resize(frame, (320, 240))
        _, caras = _detector_facial.detect(pequeño)
        if caras is None or len(caras) == 0:
            return False

        cara_alineada = _reconocedor_facial.alignCrop(pequeño, caras[0])
        encoding_actual = _reconocedor_facial.feature(cara_alineada)
        similitud = _reconocedor_facial.match(_encoding_referencia, encoding_actual, 0)
        return similitud >= UMBRAL_COSENO

    except Exception as e:
        _LOGGER.warning(f"[Vision] Error en _es_luigui: {e}")
        return True  # en caso de error, no bloquear

# MediaPipe: índices de tip y PIP para los 4 dedos (índice, medio, anular, meñique)
_TIPS = [8, 12, 16, 20]
_PIPS = [6, 10, 14, 18]


# ── Funciones core ────────────────────────────────────────────────────────────

def init_camara():
    """Abre VideoCapture(0) a 640×480. Retorna el objeto o None si la cámara no está disponible."""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        return cap
    except Exception as e:
        _LOGGER.warning(f"[Vision] Error al abrir cámara: {e}")
        return None


def detectar_presencia(frame_anterior, frame_actual) -> bool:
    """
    Frame differencing entre dos frames en escala de grises (ya blureados).
    Retorna True si hay al menos un contorno con área >= AREA_MIN_PRESENCIA.
    """
    diff = cv2.absdiff(frame_anterior, frame_actual)
    _, thresh = cv2.threshold(diff, UMBRAL_DIFF, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return any(cv2.contourArea(c) >= AREA_MIN_PRESENCIA for c in contornos)


def detectar_mano_abierta(hand_landmarks) -> bool:
    """
    Retorna True si los 4 dedos principales están extendidos.
    Criterio: tip.y < pip.y (en coordenadas imagen donde y crece hacia abajo).
    """
    lm = hand_landmarks.landmark
    return all(lm[tip].y < lm[pip].y for tip, pip in zip(_TIPS, _PIPS))


def detectar_barrido_izquierda(historial: deque) -> bool:
    """
    Retorna True si la muñeca se movió > |DELTA_BARRIDO| px a la izquierda
    dentro de la ventana VENTANA_BARRIDO segundos.
    """
    ahora = time.time()
    recientes = [(t, x) for t, x in historial if ahora - t <= VENTANA_BARRIDO]
    if len(recientes) < 3:
        return False
    delta_x = recientes[-1][1] - recientes[0][1]
    return delta_x <= DELTA_BARRIDO


def abrir_en_obsidian(rutas: list) -> list:
    """Abre cada ruta en Obsidian vía 'open -a Obsidian'. Retorna las rutas abiertas exitosamente."""
    abiertas = []
    for ruta in rutas:
        try:
            subprocess.run(
                ["open", "-a", "Obsidian", str(ruta)],
                capture_output=True,
                timeout=5,
            )
            abiertas.append(ruta)
            _LOGGER.info(f"[Vision] Abierto en Obsidian: {ruta}")
        except Exception as e:
            _LOGGER.warning(f"[Vision] Error abriendo {ruta}: {e}")
    return abiertas


def detectar_ola_adios(historial: deque, mano_abierta: bool) -> bool:
    """
    Retorna True si se detecta una ola de despedida con la mano abierta:
    >= CAMBIOS_OLA cambios de dirección horizontal de >= AMPLITUD_OLA px
    dentro de VENTANA_OLA segundos.
    """
    if not mano_abierta:
        return False
    ahora = time.time()
    xs = [x for t, x in historial if ahora - t <= VENTANA_OLA]
    if len(xs) < 6:
        return False

    cambios = 0
    pico = xs[0]
    ultima_dir = None
    for x in xs[1:]:
        diff = x - pico
        if abs(diff) < AMPLITUD_OLA:
            continue
        dir_actual = 1 if diff > 0 else -1
        if ultima_dir is not None and dir_actual != ultima_dir:
            cambios += 1
        ultima_dir = dir_actual
        pico = x

    return cambios >= CAMBIOS_OLA


def cerrar_obsidian() -> bool:
    """Cierra todas las ventanas de Obsidian vía osascript. Retorna True si exitoso."""
    try:
        res = subprocess.run(
            ["osascript", "-e", 'tell application "Obsidian" to close every window'],
            capture_output=True,
            timeout=5,
        )
        return res.returncode == 0
    except Exception as e:
        _LOGGER.warning(f"[Vision] Error cerrando Obsidian: {e}")
        return False


# ── Loop principal ────────────────────────────────────────────────────────────

def loop_vision(
    estado: dict,
    lock,
    hablar_fn: Callable,
    despedir_fn: Callable = None,
    emitir_evento_fn: Callable = None,
    activar_escucha_fn: Callable = None,
    vision_activa_event=None,
) -> None:
    """
    Loop de visión que corre en su propio thread (daemon=True).

    Sin presencia: 1fps, MediaPipe desactivado.
    Con presencia:  15fps, MediaPipe activo en frame reducido (320×240).

    estado: dict compartido con jarvis_daemon.py, protegido por lock.
    hablar_fn: hablar() de jarvis.py.
    despedir_fn: callback para volver a modo wake word.
    emitir_evento_fn: emitir_evento() de jarvis.py para actualizar el dashboard.
    """
    def _emit(tipo: str, msg: str) -> None:
        if emitir_evento_fn:
            try:
                emitir_evento_fn(tipo, msg)
            except Exception:
                pass

    _init_reconocimiento_facial()

    cap = init_camara()
    if cap is None:
        _LOGGER.warning("[Vision] Cámara no disponible — loop_vision no puede arrancar.")
        return

    hands = mp.solutions.hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
        model_complexity=0,
    )

    presencia_activa    = False
    ultimo_movimiento   = None    # None hasta que se detecte el primer movimiento
    frame_anterior      = None
    mano_abierta_desde  = None   # timestamp de inicio del gesto sostenido
    ultimo_barrido      = 0.0    # cooldown entre barridos
    ultimo_ola          = 0.0    # cooldown entre olas de despedida
    ultimo_despedida    = 0.0    # bloquea saludo de presencia tras ola de despedida
    ultimo_saludo       = 0.0    # cooldown entre saludos — evita re-saludar por cada movimiento
    ultimo_verificacion = 0.0    # cooldown entre verificaciones faciales
    historial_muneca: deque = deque(maxlen=60)

    COOLDOWN_SALUDO = 300.0  # 5 minutos entre saludos para no spamear

    _LOGGER.info("[Vision] Loop de visión iniciado.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.5)
                continue

            # Consumir solicitud de descanso del daemon (ej. "chau Jarvis" o "cierra los ojos")
            with lock:
                if estado.get("solicitar_descanso", False):
                    estado["solicitar_descanso"] = False
                    estado["presencia_activa"] = False
                    presencia_activa = False
                    mano_abierta_desde = None
                    historial_muneca.clear()
                    ultimo_despedida = time.time()
                    _LOGGER.info("[Vision] Descanso por voz — presencia desactivada.")
                    _emit("idle", "Esperando wake word...")

            # Gate de visión — solo procesar si los ojos están abiertos
            if vision_activa_event is not None and not vision_activa_event.is_set():
                time.sleep(1.0 / FPS_INACTIVO)
                continue

            frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gris = cv2.GaussianBlur(frame_gris, (21, 21), 0)

            # Detección de movimiento / presencia
            if frame_anterior is not None:
                if detectar_presencia(frame_anterior, frame_gris):
                    ultimo_movimiento = time.time()
                    if not presencia_activa:
                        # Verificar identidad con cooldown para no spamear el reconocedor
                        ahora = time.time()
                        if ahora - ultimo_verificacion >= COOLDOWN_VERIFICACION:
                            ultimo_verificacion = ahora
                            if _es_luigui(frame):
                                presencia_activa = True
                                with lock:
                                    estado["presencia_activa"] = True
                                _LOGGER.info("[Vision] Luigui identificado — presencia activa.")
                                if ahora - ultimo_despedida > 8.0 and ahora - ultimo_saludo > COOLDOWN_SALUDO:
                                    ultimo_saludo = ahora
                                    _emit("watcher", "Luigui detectado")
                                    hablar_fn("Hola Luigui, ¿en qué trabajamos?")
                                    if activar_escucha_fn:
                                        activar_escucha_fn()
                            else:
                                _LOGGER.debug("[Vision] Movimiento detectado — cara no reconocida, ignorando.")

            frame_anterior = frame_gris

            if presencia_activa:
                # Timeout de ausencia
                if ultimo_movimiento and time.time() - ultimo_movimiento > TIMEOUT_AUSENCIA:
                    presencia_activa = False
                    mano_abierta_desde = None
                    historial_muneca.clear()
                    with lock:
                        estado["presencia_activa"] = False
                    _LOGGER.info("[Vision] Ausencia prolongada — modo bajo consumo.")
                    _emit("idle", "Esperando wake word...")
                    time.sleep(1.0 / FPS_INACTIVO)
                    continue

                # MediaPipe en frame reducido para mantener CPU bajo
                frame_peq = cv2.resize(frame, (320, 240))
                frame_rgb = cv2.cvtColor(frame_peq, cv2.COLOR_BGR2RGB)
                frame_rgb.flags.writeable = False
                resultados = hands.process(frame_rgb)
                frame_rgb.flags.writeable = True

                if resultados.multi_hand_landmarks:
                    hand_lm = resultados.multi_hand_landmarks[0]

                    # Registrar posición X de la muñeca (escala del frame 320px)
                    wrist_x = int(hand_lm.landmark[0].x * 320)
                    historial_muneca.append((time.time(), wrist_x))

                    # Gesto: mano abierta sostenida → abrir archivos del vault
                    if detectar_mano_abierta(hand_lm):
                        if mano_abierta_desde is None:
                            mano_abierta_desde = time.time()
                        elif time.time() - mano_abierta_desde >= DURACION_MANO:
                            with lock:
                                rutas = list(estado["archivos_mencionados"])
                                estado["archivos_mencionados"] = []
                            if rutas:
                                abiertas = abrir_en_obsidian(rutas)
                                with lock:
                                    estado["archivos_abiertos_por_jarvis"].extend(abiertas)
                                n = len(abiertas)
                                _emit("watcher", f"Mano abierta — {n} archivo{'s' if n != 1 else ''} en Obsidian")
                                hablar_fn(f"Abriendo {n} archivo{'s' if n != 1 else ''} en Obsidian.")
                                _LOGGER.info(f"[Vision] Mano abierta — {n} archivos abiertos.")
                            else:
                                _emit("watcher", "Mano abierta — sin archivos pendientes")
                                hablar_fn("No hay archivos pendientes de abrir.")
                            mano_abierta_desde = None
                            if activar_escucha_fn:
                                activar_escucha_fn()
                    else:
                        mano_abierta_desde = None

                    # Gesto: barrido izquierda → cerrar ventanas de Obsidian
                    if (time.time() - ultimo_barrido > COOLDOWN_BARRIDO
                            and detectar_barrido_izquierda(historial_muneca)):
                        ultimo_barrido = time.time()
                        historial_muneca.clear()
                        with lock:
                            habia_abiertos = bool(estado["archivos_abiertos_por_jarvis"])
                            estado["archivos_abiertos_por_jarvis"] = []
                        if habia_abiertos:
                            cerrar_obsidian()
                            _emit("watcher", "Barrido izquierda — Obsidian cerrado")
                            hablar_fn("Archivos cerrados.")
                            _LOGGER.info("[Vision] Barrido izquierda — Obsidian cerrado.")
                            if activar_escucha_fn:
                                activar_escucha_fn()

                    # Gesto: ola de despedida → modo wake word
                    es_mano_abierta = detectar_mano_abierta(hand_lm)
                    if (time.time() - ultimo_ola > COOLDOWN_OLA
                            and detectar_ola_adios(historial_muneca, es_mano_abierta)):
                        ultimo_ola = time.time()
                        ultimo_despedida = time.time()
                        historial_muneca.clear()
                        presencia_activa = False
                        mano_abierta_desde = None
                        with lock:
                            estado["presencia_activa"] = False
                        _LOGGER.info("[Vision] Ola de despedida — volviendo a modo wake word.")
                        _emit("idle", "Ola de despedida — hasta luego Luigui")
                        hablar_fn("Hasta luego, Luigui. Di Jarvis cuando me necesites.")
                        if despedir_fn:
                            despedir_fn()
                else:
                    mano_abierta_desde = None

                time.sleep(1.0 / FPS_ACTIVO)

            else:
                time.sleep(1.0 / FPS_INACTIVO)

    finally:
        hands.close()
        cap.release()
        _LOGGER.info("[Vision] Loop de visión terminado — recursos liberados.")
