#!/usr/local/bin/python3.11
"""
server.py — Jarvis Dashboard Server

HTTP  :7777 — sirve index.html + recibe POST /event de jarvis.py
WebSocket :7778 — push de eventos en tiempo real al browser

Chrome se abre en modo app al arrancar y se mantiene vivo:
- PID lock evita múltiples instancias del servidor.
- Watchdog relanza Chrome si el usuario cierra la ventana.
- Al arrancar, si Chrome ya está abierto no se abre otro.
"""

import atexit
import asyncio
import json
import os
import socket
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import websockets

DASHBOARD_DIR  = Path(__file__).parent
HTTP_PORT      = 7777
WS_PORT        = 7778
PID_FILE       = DASHBOARD_DIR / "dashboard.pid"

_clients: set = set()
_loop: asyncio.AbstractEventLoop | None = None


# ── Singleton del servidor ────────────────────────────────────────────────────

def _acquire_pid_lock() -> bool:
    try:
        fd = os.open(str(PID_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)
            return False
        except (ProcessLookupError, ValueError, OSError):
            PID_FILE.unlink(missing_ok=True)
            return _acquire_pid_lock()


def _release_pid_lock() -> None:
    PID_FILE.unlink(missing_ok=True)


# ── Chrome — ventana única persistente ───────────────────────────────────────

def _launch_chrome() -> None:
    subprocess.Popen([
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--app=http://localhost:7777",
        "--window-size=400,650",
        "--window-position=1400,50",
        "--disable-extensions",
        "--no-first-run",
        "--no-default-browser-check",
    ])


def _launch_chrome_seguro() -> None:
    """Envuelve _launch_chrome() — un binario de Chrome ausente o Popen fallando
    no debe matar en silencio el thread que lo llama (_open_chrome / watchdog)."""
    try:
        _launch_chrome()
    except Exception as e:
        print(f"[Dashboard] No se pudo lanzar Chrome: {e}")


# ── WebSocket ──────────────────────────────────────────────────────────────────

async def _ws_handler(websocket):
    _clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        _clients.discard(websocket)


async def _broadcast(payload: str):
    if not _clients:
        return
    await asyncio.gather(
        *[c.send(payload) for c in list(_clients)],
        return_exceptions=True,
    )


def broadcast_from_thread(data: dict):
    if _loop:
        asyncio.run_coroutine_threadsafe(_broadcast(json.dumps(data)), _loop)


# ── HTTP ───────────────────────────────────────────────────────────────────────

class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # suppress access logs

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            data = (DASHBOARD_DIR / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/event":
            length = int(self.headers.get("Content-Length", 0))
            try:
                data = json.loads(self.rfile.read(length))
                broadcast_from_thread(data)
            except Exception:
                pass
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def _run_http():
    # ThreadingHTTPServer: un GET lento (ej. sirviendo index.html) no debe bloquear
    # los POST /event entrantes de jarvis.py — cada request corre en su propio thread.
    httpd = ThreadingHTTPServer(("localhost", HTTP_PORT), _Handler)
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    httpd.serve_forever()


# ── Chrome ─────────────────────────────────────────────────────────────────────

def _open_chrome():
    """Abre Chrome solo si no hay clientes WebSocket conectados.
    Espera 4s para que Chrome existente reconecte (frontend reintenta cada 2.5s)."""
    time.sleep(4.0)
    if _clients:
        print("[Dashboard] Chrome ya conectado via WebSocket — no se abre otro.")
        return
    print("[Dashboard] Abriendo Chrome...")
    _launch_chrome_seguro()


def _chrome_watchdog():
    """Relanza Chrome si lleva > 12s sin ningún cliente WebSocket conectado."""
    time.sleep(8.0)
    # Arrancar el reloj AHORA — no en 0.0 — para no considerar de entrada que ya
    # pasaron >12s. Con _last_open=0.0, el primer chequeo (a los 8s) siempre lanzaba
    # una segunda ventana de Chrome aunque la primera (_open_chrome, a los 4s) todavía
    # no hubiera tenido tiempo de conectar su WebSocket en un arranque frío.
    _last_open = time.time()
    while True:
        if not _clients and (time.time() - _last_open) > 12.0:
            print("[Dashboard] Sin clientes WS — relanzando Chrome...")
            _launch_chrome_seguro()
            _last_open = time.time()
        time.sleep(3)


# ── Main ───────────────────────────────────────────────────────────────────────

async def _ws_main():
    global _loop
    _loop = asyncio.get_running_loop()
    async with websockets.serve(_ws_handler, "localhost", WS_PORT):
        print(f"[Dashboard] HTTP:{HTTP_PORT}  WS:{WS_PORT} — abriendo Chrome...")
        await asyncio.Future()  # corre indefinidamente


if __name__ == "__main__":
    if not _acquire_pid_lock():
        print("[Dashboard] Servidor ya corriendo. Saliendo.")
        raise SystemExit(0)

    atexit.register(_release_pid_lock)

    threading.Thread(target=_run_http, daemon=True).start()
    threading.Thread(target=_open_chrome, daemon=True).start()
    threading.Thread(target=_chrome_watchdog, daemon=True).start()
    asyncio.run(_ws_main())
