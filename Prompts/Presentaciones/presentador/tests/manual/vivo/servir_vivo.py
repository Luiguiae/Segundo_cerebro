#!/usr/bin/env python3.11
"""Arnés de DESARROLLO para las pruebas en vivo guiadas (T13–T15). No forma parte de la entrega.

    python3.11 tests/manual/vivo/servir_vivo.py <voz|gestos|degradacion> [--deck demo] [--port 8765] [--no-abrir]

Sirve el deck con el presentador inyectado (modo --debug) y una GUÍA en pantalla (guia.js) que da instrucciones,
emite tonos y verifica cada paso con los eventos reales del presentador. Los resultados se guardan en
tests/manual/vivo/resultados/ (POST /__guia/resultado) y el avance se imprime en la terminal (POST /__guia/evento).
"""
import argparse
import json
import os
import re
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

AQUI = Path(__file__).resolve().parent
PROYECTO = AQUI.parents[2]
sys.path.insert(0, str(PROYECTO))
import presentar  # noqa: E402

RESULTADOS = Path(os.environ.get("VIVO_RESULTADOS") or AQUI / "resultados")  # VIVO_RESULTADOS: solo para ensayar la guía sin ensuciar los resultados reales


class ManejadorVivo(presentar.Manejador):
    def _archivo_para(self, ruta_url):
        if ruta_url.startswith("/__guia/") and self.command in ("GET", "HEAD"):
            return presentar.resolver_segura(AQUI, ruta_url[len("/__guia/"):])
        return super()._archivo_para(ruta_url)

    def _json(self, codigo, obj):
        self._responder(codigo, "application/json; charset=utf-8", json.dumps(obj).encode())

    def do_POST(self):
        largo = int(self.headers.get("Content-Length") or 0)
        if largo <= 0 or largo > 4 * 1024 * 1024:
            return self._json(400, {"ok": False})
        try:
            cuerpo = json.loads(self.rfile.read(largo))
        except ValueError:
            return self._json(400, {"ok": False})
        ruta = self.path.split("?")[0]
        if ruta == "/__guia/evento":
            print("[vivo] " + str(cuerpo.get("linea", ""))[:300], flush=True)
            return self._json(200, {"ok": True})
        if ruta == "/__guia/resultado":
            RESULTADOS.mkdir(exist_ok=True)
            nombre = re.sub(r"[^a-z0-9_-]", "", str(cuerpo.get("guion", "guion")).lower()) or "guion"
            destino = RESULTADOS / f"{nombre}-{time.strftime('%Y%m%d-%H%M%S')}.json"
            destino.write_text(json.dumps(cuerpo, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[vivo] FIN — resultados en {destino}", flush=True)
            return self._json(200, {"ok": True})
        return self._json(404, {"ok": False})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("guion", choices=["voz", "gestos", "degradacion"])
    ap.add_argument("--deck", default=str(PROYECTO / "demo"))
    ap.add_argument("--port", type=int, default=presentar.PUERTO)
    ap.add_argument("--no-abrir", action="store_true")
    ap.add_argument("--variante", default="", help="variante del guion (p. ej. camara, wifi, ininteligible)")
    a = ap.parse_args()
    faltan = presentar.setup_vendor.faltantes(presentar.VENDOR)
    if faltan:
        print("ERROR: vendor/ incompleto. Corre: python3.11 setup_vendor.py", file=sys.stderr)
        return 2
    extra = (f'<script>window.GUION_VIVO={json.dumps(a.guion)};window.GUION_VARIANTE={json.dumps(a.variante)};</script>\n'
             '<script src="/__guia/guia.js"></script>\n').encode()
    srv = presentar.Servidor(("127.0.0.1", a.port), ManejadorVivo)
    srv.cfg = SimpleNamespace(carpeta=Path(a.deck).expanduser(), vendor=presentar.VENDOR, proyecto=PROYECTO,
                              inyectar=True, debug=True, extra=extra)
    url = f"http://localhost:{a.port}/"
    print(f"[vivo] guion '{a.guion}' → {url}", flush=True)
    if not a.no_abrir:
        threading.Timer(0.4, presentar.abrir_chrome, args=[url]).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
