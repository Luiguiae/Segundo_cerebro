#!/usr/bin/env python3.11
"""Descarga las dependencias del presentador a vendor/ (sin CDN en runtime).

    python3.11 setup_vendor.py            # descarga lo que falte (idempotente)
    python3.11 setup_vendor.py --forzar   # vuelve a descargar todo

Qué descarga (versiones y hashes fijos; aborta si algo no coincide):
  - reveal.js 6.0.2            → vendor/reveal/dist/...
  - @mediapipe/tasks-vision 1.0.1 → vendor/tasks-vision/vision_bundle.mjs + wasm/
  - gesture_recognizer.task (float16, v1) → vendor/models/

Solo librería estándar. Correrlo con internet ANTES de la charla, no el día de la charla.
"""

import argparse
import base64
import hashlib
import io
import json
import shutil
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

PROYECTO = Path(__file__).resolve().parent
VENDOR = PROYECTO / "vendor"
MARCA = ".setup-ok"  # manifiesto que escribe este script al terminar bien

REVEAL_VERSION = "6.0.2"
REVEAL_URL = "https://registry.npmjs.org/reveal.js/-/reveal.js-6.0.2.tgz"
REVEAL_INTEGRITY = "sha512-JYIg5D9aoxoaLeb84O+OvAwsKWdIavVgEDScxtYEXFCT6t6TQrhNtSgogcjdCpdLsWglhJn3zyE3fUOwiH5KEg=="

MP_VERSION = "1.0.1"
MP_URL = "https://registry.npmjs.org/@mediapipe/tasks-vision/-/tasks-vision-1.0.1.tgz"
MP_INTEGRITY = "sha512-rvRE2FmAZ6ZxKSw7wq+e+jQDpN3t1B/tD2mJz9SmAzb1msoDkd4dMoE4wAh8Z30Um0PQwLiHr9QtomhmXk3aUQ=="

MODELO_URL = ("https://storage.googleapis.com/mediapipe-models/gesture_recognizer/"
              "gesture_recognizer/float16/1/gesture_recognizer.task")
MODELO_SHA256 = "97952348cf6a6a4915c2ea1496b4b37ebabc50cbbf80571435643c455f2b0482"
MODELO_BYTES = 8_373_440

# Fuente única de verdad de "vendor completo": presentar.py importa esta lista.
# Rutas relativas a vendor/.
ARCHIVOS_REQUERIDOS = (
    "reveal/dist/reveal.js",
    "reveal/dist/reveal.css",
    "reveal/dist/reset.css",
    "reveal/dist/theme/black.css",
    "tasks-vision/vision_bundle.mjs",
    "tasks-vision/wasm/vision_wasm_internal.js",
    "tasks-vision/wasm/vision_wasm_internal.wasm",
    "tasks-vision/wasm/vision_wasm_nosimd_internal.js",
    "tasks-vision/wasm/vision_wasm_nosimd_internal.wasm",
    "models/gesture_recognizer.task",
)


class ErrorIntegridad(Exception):
    pass


def verificar_sha512_npm(datos: bytes, integrity: str) -> None:
    """`integrity` con el formato de npm: 'sha512-<base64>'."""
    algoritmo, _, esperado = integrity.partition("-")
    if algoritmo != "sha512":
        raise ErrorIntegridad(f"algoritmo no soportado: {algoritmo}")
    obtenido = base64.b64encode(hashlib.sha512(datos).digest()).decode()
    if obtenido != esperado:
        raise ErrorIntegridad("sha512 no coincide con el de npm (descarga corrupta o alterada)")


def verificar_sha256(datos: bytes, esperado: str) -> None:
    obtenido = hashlib.sha256(datos).hexdigest()
    if obtenido != esperado:
        raise ErrorIntegridad(f"sha256 no coincide (esperado {esperado[:12]}…, obtenido {obtenido[:12]}…)")


def faltantes(vendor: Path = VENDOR) -> list:
    """Archivos requeridos que no existen o están vacíos."""
    return [r for r in ARCHIVOS_REQUERIDOS
            if not (vendor / r).is_file() or (vendor / r).stat().st_size == 0]


def descargar(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "presentador-setup/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def _extraer_seguro(datos_tgz: bytes, destino: Path) -> None:
    """Extrae el .tgz rechazando rutas absolutas, '..' y enlaces."""
    destino.mkdir(parents=True, exist_ok=True)
    raiz = destino.resolve()
    with tarfile.open(fileobj=io.BytesIO(datos_tgz), mode="r:gz") as tar:
        for m in tar.getmembers():
            objetivo = (destino / m.name).resolve()
            if m.issym() or m.islnk() or not objetivo.is_relative_to(raiz):
                raise ErrorIntegridad(f"entrada sospechosa en el tarball: {m.name}")
        tar.extractall(destino)


def instalar_reveal(datos_tgz: bytes, vendor: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        _extraer_seguro(datos_tgz, Path(tmp))
        origen = Path(tmp) / "package"
        destino = vendor / "reveal"
        if destino.exists():
            shutil.rmtree(destino)
        shutil.copytree(origen / "dist", destino / "dist")
        for extra in ("LICENSE", "package.json"):
            if (origen / extra).exists():
                shutil.copy2(origen / extra, destino / extra)


def instalar_mediapipe(datos_tgz: bytes, vendor: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        _extraer_seguro(datos_tgz, Path(tmp))
        origen = Path(tmp) / "package"
        destino = vendor / "tasks-vision"
        if destino.exists():
            shutil.rmtree(destino)
        destino.mkdir(parents=True)
        shutil.copy2(origen / "vision_bundle.mjs", destino / "vision_bundle.mjs")
        shutil.copytree(origen / "wasm", destino / "wasm")
        shutil.copy2(origen / "package.json", destino / "package.json")


def instalar_modelo(datos: bytes, vendor: Path) -> None:
    destino = vendor / "models"
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "gesture_recognizer.task").write_bytes(datos)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Descarga reveal.js, MediaPipe Tasks Vision y el modelo a vendor/.")
    ap.add_argument("--forzar", action="store_true", help="vuelve a descargar aunque vendor/ esté completo")
    args = ap.parse_args(argv)

    if not args.forzar and not faltantes() and (VENDOR / MARCA).exists():
        print(f"vendor/ ya está completo ({len(ARCHIVOS_REQUERIDOS)} archivos requeridos). Nada que descargar.")
        return 0

    VENDOR.mkdir(exist_ok=True)
    try:
        print(f"[1/3] reveal.js {REVEAL_VERSION} …", flush=True)
        datos = descargar(REVEAL_URL)
        verificar_sha512_npm(datos, REVEAL_INTEGRITY)
        instalar_reveal(datos, VENDOR)

        print(f"[2/3] @mediapipe/tasks-vision {MP_VERSION} …", flush=True)
        datos = descargar(MP_URL)
        verificar_sha512_npm(datos, MP_INTEGRITY)
        instalar_mediapipe(datos, VENDOR)

        print("[3/3] gesture_recognizer.task …", flush=True)
        datos = descargar(MODELO_URL)
        if len(datos) != MODELO_BYTES:
            raise ErrorIntegridad(f"tamaño inesperado del modelo: {len(datos)} bytes (esperado {MODELO_BYTES})")
        verificar_sha256(datos, MODELO_SHA256)
        instalar_modelo(datos, VENDOR)
    except ErrorIntegridad as e:
        print(f"\nERROR de integridad: {e}\nNo se instaló nada de lo que falló la verificación.", file=sys.stderr)
        return 1
    except OSError as e:  # sin internet, DNS, timeout…
        print(f"\nERROR de red: {e}\nRevisa tu conexión y vuelve a correr este script.", file=sys.stderr)
        return 1

    pendientes = faltantes()
    if pendientes:
        print("\nERROR: tras instalar faltan archivos requeridos:\n  " + "\n  ".join(pendientes), file=sys.stderr)
        return 1
    (VENDOR / MARCA).write_text(json.dumps({
        "reveal.js": REVEAL_VERSION, "tasks-vision": MP_VERSION,
        "modelo_sha256": MODELO_SHA256,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"\nListo: vendor/ completo ({len(ARCHIVOS_REQUERIDOS)} archivos requeridos verificados).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
