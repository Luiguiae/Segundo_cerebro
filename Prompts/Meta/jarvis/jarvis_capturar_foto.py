#!/usr/local/bin/python3.11
"""
jarvis_capturar_foto.py — Captura la foto de referencia para reconocimiento facial.

Uso:
    python3 Prompts/Meta/jarvis/jarvis_capturar_foto.py

Colócate frente a la cámara, bien iluminado, mirando de frente.
Después de 3 segundos captura la foto y la guarda como luigui.jpg.
"""

import sys
import time
from pathlib import Path

import cv2

JARVIS_DIR    = Path(__file__).parent
FOTO_SALIDA   = JARVIS_DIR / "luigui.jpg"
MODELO_YUNET  = JARVIS_DIR / "yunet.onnx"


def main():
    if not MODELO_YUNET.exists():
        print(f"[ERROR] Modelo YuNet no encontrado en {MODELO_YUNET}")
        print("Ejecuta primero:")
        print("  curl -L -o Prompts/Meta/jarvis/yunet.onnx \\")
        print("    https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx")
        sys.exit(1)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] No se pudo abrir la cámara.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = cv2.FaceDetectorYN.create(str(MODELO_YUNET), "", (640, 480), score_threshold=0.7)

    print("Preparando cámara... colócate frente a ella, bien iluminado.")
    time.sleep(1.5)

    print("Capturando en 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("¡Capturando!")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("[ERROR] No se pudo leer frame de la cámara.")
        sys.exit(1)

    # Verificar que hay una cara visible
    _, caras = detector.detect(frame)
    if caras is None or len(caras) == 0:
        print("[ERROR] No se detectó ninguna cara en el frame.")
        print("Intenta de nuevo: mejor iluminación, mira de frente a la cámara.")
        sys.exit(1)

    n = len(caras)
    if n > 1:
        print(f"[AVISO] Se detectaron {n} caras — se usará la de mayor confianza.")

    cv2.imwrite(str(FOTO_SALIDA), frame)
    print(f"\n✓ Foto guardada en: {FOTO_SALIDA}")
    print(f"  Caras detectadas: {n}")
    print(f"  Confianza de la cara principal: {caras[0][-1]:.2f}")
    print("\nReinicia Jarvis para activar el reconocimiento facial.")


if __name__ == "__main__":
    main()
