#!/usr/bin/env python3.11
"""Servidor local del presentador por gestos y voz.

    python3.11 presentar.py ~/Presentaciones/<carpeta> [--port 8765] [--debug] [--sin-inyeccion] [--no-abrir]

Sirve la carpeta de la presentación en `/`, las librerías de `vendor/` en `/vendor/` y los
scripts del presentador (lista blanca) en `/presentador/`. Solo escucha en 127.0.0.1
(`localhost` es contexto seguro, requisito de getUserMedia). Solo librería estándar.

Nunca escribe nada en la carpeta de la presentación.
"""

import argparse
import errno
import mimetypes
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setup_vendor  # noqa: E402  (fuente única de la lista de archivos requeridos de vendor/)

PROYECTO = Path(__file__).resolve().parent
VENDOR = PROYECTO / "vendor"
PUERTO = 8765

# Solo estos archivos del proyecto se sirven en /presentador/ (nada de docs/, tests/, presentar.py…).
ARCHIVOS_PRESENTADOR = ("presentador.js", "comandos.js", "swipe.js")

# Tipos fijos: no dependen de los mime.types del sistema. `.task` no tiene tipo estándar.
TIPOS = {
    ".html": "text/html",  # sin charset: se respeta el <meta charset> del deck
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".map": "application/json; charset=utf-8",
    ".wasm": "application/wasm",
    ".task": "application/octet-stream",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
}


# ── Inyección del presentador en index.html (solo al servir; el HTML en disco no se toca) ──────────

MARCA_INYECCION = b"presentador:inyectado"
_RE_CIERRE_BODY = re.compile(rb"</body\s*>", re.IGNORECASE)


def bloque_inyeccion(debug: bool = False, extra: bytes = b"") -> bytes:
    return (
        "\n<!-- presentador:inyectado -->\n"
        f"<script>window.PRESENTADOR_CONFIG = {{\"debug\": {'true' if debug else 'false'}}};</script>\n"
        '<script src="/presentador/comandos.js"></script>\n'
        '<script src="/presentador/swipe.js"></script>\n'
        '<script src="/presentador/presentador.js"></script>\n'
    ).encode("ascii") + extra


def inyectar(html: bytes, debug: bool = False, extra: bytes = b"") -> bytes:
    """Agrega los scripts del presentador antes del ÚLTIMO </body> (sin distinguir mayúsculas;
    si no hay, al final). Trabaja sobre bytes (no decodifica: cualquier codificación queda intacta)
    y es idempotente. `extra`: bytes que se añaden tras los scripts (solo lo usan los arneses de prueba en vivo)."""
    if MARCA_INYECCION in html:
        return html
    bloque = bloque_inyeccion(debug, extra)
    ultimo = None
    for ultimo in _RE_CIERRE_BODY.finditer(html):
        pass
    if ultimo is None:
        return html + bloque
    return html[:ultimo.start()] + bloque + html[ultimo.start():]


def tipo_de(ruta: Path) -> str:
    t = TIPOS.get(ruta.suffix.lower())
    if t:
        return t
    return mimetypes.guess_type(str(ruta))[0] or "application/octet-stream"


def resolver_segura(raiz: Path, relativa: str):
    """Ruta absoluta dentro de `raiz`, o None. Rechaza '..', enlaces que escapan y dotfiles."""
    if "\x00" in relativa:
        return None
    partes = [p for p in relativa.split("/") if p not in ("", ".")]
    if any(p.startswith(".") for p in partes):  # incluye '..' y ocultos (.git, .env…)
        return None
    raiz_real = raiz.resolve()
    objetivo = (raiz_real.joinpath(*partes)).resolve() if partes else raiz_real
    if not objetivo.is_relative_to(raiz_real):
        return None
    if objetivo.is_dir():
        objetivo = objetivo / "index.html"
    return objetivo if objetivo.is_file() else None


class Manejador(BaseHTTPRequestHandler):
    server_version = "presentador/1.0"

    def log_message(self, fmt, *args):  # silencio: la consola es para errores y avisos
        pass

    def do_GET(self):
        self._servir(con_cuerpo=True)

    def do_HEAD(self):
        self._servir(con_cuerpo=False)

    def _responder(self, codigo, tipo, cuerpo: bytes, con_cuerpo=True):
        try:
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(cuerpo)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if con_cuerpo:
                self.wfile.write(cuerpo)
        except (BrokenPipeError, ConnectionResetError):
            pass  # el navegador cortó la conexión (p. ej. al recargar)

    def _no_encontrado(self, con_cuerpo=True):
        self._responder(404, "text/plain; charset=utf-8", b"404 no encontrado\n", con_cuerpo)

    def _archivo_para(self, ruta_url: str):
        cfg = self.server.cfg
        if ruta_url.startswith("/vendor/"):
            return resolver_segura(cfg.vendor, ruta_url[len("/vendor/"):])
        if ruta_url.startswith("/presentador/"):
            nombre = ruta_url[len("/presentador/"):]
            if nombre not in ARCHIVOS_PRESENTADOR:
                return None
            return resolver_segura(cfg.proyecto, nombre)
        return resolver_segura(cfg.carpeta, ruta_url)

    def _servir(self, con_cuerpo=True):
        ruta_url = unquote(urlsplit(self.path).path)
        archivo = self._archivo_para(ruta_url)
        if archivo is None:
            return self._no_encontrado(con_cuerpo)
        cfg = self.server.cfg
        if cfg.inyectar and ruta_url in ("/", "/index.html"):
            try:
                cuerpo = inyectar(archivo.read_bytes(), cfg.debug, getattr(cfg, "extra", b""))
            except OSError:
                return self._no_encontrado(con_cuerpo)
            return self._responder(200, tipo_de(archivo), cuerpo, con_cuerpo)
        try:
            tamano = archivo.stat().st_size
            self.send_response(200)
            self.send_header("Content-Type", tipo_de(archivo))
            self.send_header("Content-Length", str(tamano))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if con_cuerpo:
                with archivo.open("rb") as f:
                    shutil.copyfileobj(f, self.wfile)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except OSError:
            self._no_encontrado(con_cuerpo)


class Servidor(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def crear_servidor(carpeta: Path, puerto=PUERTO, vendor=None, proyecto=None,
                   inyectar=True, debug=False, extra=b"") -> Servidor:
    srv = Servidor(("127.0.0.1", puerto), Manejador)
    srv.cfg = SimpleNamespace(
        carpeta=Path(carpeta), vendor=Path(vendor or VENDOR), proyecto=Path(proyecto or PROYECTO),
        inyectar=inyectar, debug=debug, extra=extra,
    )
    return srv


def abrir_chrome(url: str) -> None:
    r = subprocess.run(["open", "-a", "Google Chrome", url], capture_output=True)
    if r.returncode != 0:
        webbrowser.open(url)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Sirve una presentación Reveal.js con el presentador por gestos y voz.")
    ap.add_argument("carpeta", help="carpeta de la presentación (con index.html), p. ej. ~/Presentaciones/2026-09-28")
    ap.add_argument("--port", "--puerto", dest="puerto", type=int, default=PUERTO)
    ap.add_argument("--debug", action="store_true", help="muestra la transcripción cruda de la voz en el indicador")
    ap.add_argument("--sin-inyeccion", action="store_true", help="sirve la carpeta tal cual, sin inyectar el presentador")
    ap.add_argument("--no-abrir", action="store_true", help="no abre Chrome (para pruebas)")
    args = ap.parse_args(argv)

    carpeta = Path(args.carpeta).expanduser()
    if not carpeta.is_dir():
        print(f"ERROR: la carpeta no existe: {carpeta}", file=sys.stderr)
        return 1
    if not (carpeta / "index.html").is_file():
        print(f"ERROR: {carpeta} no tiene index.html.", file=sys.stderr)
        return 1

    faltan = setup_vendor.faltantes(VENDOR)
    if faltan:
        ejemplo = ", ".join(faltan[:3]) + (f" … (+{len(faltan) - 3})" if len(faltan) > 3 else "")
        print(f"ERROR: vendor/ falta o está incompleto ({len(faltan)} archivos: {ejemplo}).\n"
              f"Corre primero (con internet):\n\n    python3.11 setup_vendor.py\n", file=sys.stderr)
        return 2

    try:
        srv = crear_servidor(carpeta, args.puerto, inyectar=not args.sin_inyeccion, debug=args.debug)
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print(f"ERROR: el puerto {args.puerto} está ocupado (¿otra instancia de presentar.py?). "
                  f"Ciérrala o usa --port N (ojo: los permisos de cámara y micrófono son por puerto).", file=sys.stderr)
            return 1
        raise

    url = f"http://localhost:{args.puerto}"
    print(f"Presentador sirviendo {carpeta}\n  → {url}   (Ctrl+C para salir)", flush=True)
    if not args.no_abrir:
        threading.Timer(0.4, abrir_chrome, args=[url]).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando.")
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
