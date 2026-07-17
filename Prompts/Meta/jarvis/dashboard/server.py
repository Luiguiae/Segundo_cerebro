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
import fcntl
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
# flock() sobre un fd mantenido abierto toda la vida del proceso — el kernel
# libera el lock automáticamente al morir el proceso por cualquier motivo, sin
# depender de que jarvis_daemon.py's_iniciar_dashboard() lea un PID en un
# archivo que alguien pudo borrar mientras el dueño seguía vivo (ver el mismo
# fix, con la misma justificación, en jarvis_daemon.py::_acquire_pid_lock).

_pid_lock_fd: "int | None" = None


def _acquire_pid_lock() -> bool:
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


# ── Chrome — ventana única persistente ───────────────────────────────────────
#
# La verificación de "¿ya hay una ventana de Jarvis abierta?" NO puede basarse en
# si hay un cliente WebSocket conectado (heurística anterior): una ventana puede
# seguir abierta con el WS momentáneamente caído (Mac que durmió, el servidor de
# dashboard se reinició pero Chrome no) y el chequeo la daba por "cerrada",
# abriendo una segunda ventana. Tampoco alcanza con trackear el PID del proceso
# que lanza `--app=...`: si Chrome ya estaba corriendo, ese proceso solo reenvía
# la apertura a la instancia existente y puede salir casi de inmediato, sin que
# su PID represente la ventana real. La fuente de verdad es el propio Chrome,
# consultado vía AppleScript — mismo mecanismo que ya usa mejora_007_vision.py.

_VENTANA_JARVIS_SCRIPT = '''
set chromeRunning to false
tell application "System Events"
    if exists (application process "Google Chrome") then set chromeRunning to true
end tell
if not chromeRunning then return "0"
tell application "Google Chrome"
    set ventanasJarvis to {}
    repeat with w in windows
        try
            if URL of active tab of w contains "localhost:7777" then
                set end of ventanasJarvis to w
            end if
        end try
    end repeat
    set n to count of ventanasJarvis
    if n > 1 then
        repeat with i from 2 to n
            try
                close (item i of ventanasJarvis)
            end try
        end repeat
    end if
    return (n as string)
end tell
'''


def _normalizar_ventanas_jarvis() -> int:
    """Cuenta las ventanas de Chrome que muestran el dashboard de Jarvis
    (URL localhost:7777) y cierra cualquier duplicado, dejando como máximo una.
    Retorna cuántas había ANTES de cerrar duplicados (0 si Chrome ni siquiera
    está corriendo, -1 si no se pudo verificar — ej. permiso de automatización
    no otorgado). El caller debe tratar -1 como "no abrir, por las dudas": es
    preferible quedarse sin ventana temporalmente a arriesgar un duplicado."""
    try:
        resultado = subprocess.run(
            ["osascript", "-e", _VENTANA_JARVIS_SCRIPT],
            capture_output=True, text=True, timeout=10,
        )
        if resultado.returncode != 0:
            print(f"[Dashboard] No pude verificar ventanas de Chrome: {resultado.stderr.strip()[:200]}")
            return -1
        return int(resultado.stdout.strip())
    except Exception as e:
        print(f"[Dashboard] Error verificando ventanas de Chrome: {e}")
        return -1


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
    """Abre Chrome solo si no hay ya una ventana del dashboard — verificado contra
    las ventanas reales de Chrome (_normalizar_ventanas_jarvis), no contra si el
    WebSocket ya reconectó. Si -1 (no se pudo verificar), no abre — prefiere
    quedarse sin ventana a arriesgar un duplicado."""
    time.sleep(1.5)  # margen para que HTTP/WS estén arriba antes de la primera consulta
    n = _normalizar_ventanas_jarvis()
    if n != 0:
        print(f"[Dashboard] Ventana de Jarvis ya existe (n={n}, normalizado a máx. 1) — no se abre otra.")
        return
    print("[Dashboard] Abriendo Chrome...")
    _launch_chrome_seguro()


def _chrome_watchdog():
    """Cada 10s verifica cuántas ventanas de Jarvis hay realmente abiertas en
    Chrome: si hay 0, relanza; si hay más de 1 (ej. tras un reinicio del backend
    mientras una ventana huérfana seguía abierta), _normalizar_ventanas_jarvis ya
    las cerró y deja como máximo una — acá no hace falta acción adicional."""
    time.sleep(6.0)
    while True:
        n = _normalizar_ventanas_jarvis()
        if n == 0:
            print("[Dashboard] Ninguna ventana de Jarvis abierta — relanzando Chrome...")
            _launch_chrome_seguro()
        time.sleep(10)


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
