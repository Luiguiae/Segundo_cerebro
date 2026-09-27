#!/usr/bin/env python3.11
"""Servidor de DESARROLLO solo para el spike de gestos (T06). No forma parte de la entrega.

    python3.11 tests/manual/spike/servir_spike.py [--port 8765] [--no-abrir]

Reutiliza el servidor de presentar.py (mismo puerto y origen que el presentador real, así el permiso
de cámara que se conceda aquí sirve después) y le agrega tres cosas que el spike necesita:
  POST /guardar  {nombre, datos}  → escribe tests/traces/<nombre>.json (solo coordenadas; nunca imágenes)
  POST /marca    {fase}           → etiqueta la fase actual para el muestreo de CPU
  POST /fin                       → detiene el muestreo y escribe tests/traces/_cpu.json
y un muestreador de CPU (`top`) que registra, por fase, CPU del sistema, de Chrome y del daemon de Jarvis.
"""

import json
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

AQUI = Path(__file__).resolve().parent
PROYECTO = AQUI.parents[2]
TRAZAS = Path(os.environ.get("SPIKE_TRAZAS") or PROYECTO / "tests" / "traces")  # SPIKE_TRAZAS: solo para probar el spike sin ensuciar las trazas reales
sys.path.insert(0, str(PROYECTO))
import presentar  # noqa: E402

NOMBRE_OK = re.compile(r"^[a-z0-9_-]{1,80}\.json$")
MAX_CUERPO = 8 * 1024 * 1024


def _segundos(cputime: str) -> float:
    """'H:MM:SS.xx' | 'MM:SS.xx' → segundos."""
    partes = cputime.strip().split(":")
    total = 0.0
    for p in partes:
        total = total * 60 + float(p)
    return total


class Muestreador(threading.Thread):
    """Mide CPU sin depender de la lentitud de `top`:
      - Chrome y Jarvis: delta de `cputime` (`ps`) cada ~1 s  → % de UN núcleo (100 = un núcleo completo)
      - Sistema: `top -l 2 -n 0` en un hilo aparte (~4 s por muestra)
    Cada muestra lleva la fase vigente (la marca la página con POST /marca)."""

    def __init__(self):
        super().__init__(daemon=True)
        self.fase = "espera"
        self.parar = threading.Event()
        self.muestras = []      # Chrome + Jarvis (1 Hz)
        self.sistema = []       # CPU total del equipo (~0.25 Hz)
        self.pid_jarvis = self._pid_jarvis()
        self.nucleos_logicos = int(subprocess.run(["sysctl", "-n", "hw.ncpu"], capture_output=True, text=True).stdout or 0)

    @staticmethod
    def _pid_jarvis():
        r = subprocess.run(["pgrep", "-f", "jarvis_daemon.py"], capture_output=True, text=True)
        pids = [int(p) for p in r.stdout.split() if p.isdigit()]
        return pids[0] if pids else None

    def _leer_cputimes(self):
        out = subprocess.run(["ps", "-axo", "pid=,cputime=,command="], capture_output=True, text=True).stdout
        chrome, jarvis = {}, None
        for linea in out.splitlines():
            m = re.match(r"^\s*(\d+)\s+(\S+)\s+(.*)$", linea)
            if not m:
                continue
            pid, cpu, cmd = int(m.group(1)), _segundos(m.group(2)), m.group(3)
            if "Google Chrome" in cmd:
                chrome[pid] = cpu
            if self.pid_jarvis and pid == self.pid_jarvis:
                jarvis = cpu
        return chrome, jarvis

    def _hilo_sistema(self):
        while not self.parar.is_set():
            try:
                out = subprocess.run(["top", "-l", "2", "-n", "0", "-s", "1"], capture_output=True, text=True, timeout=30).stdout
            except Exception:
                continue
            m = re.findall(r"CPU usage:\s*([\d.]+)% user,\s*([\d.]+)% sys,\s*([\d.]+)% idle", out)
            if m:
                self.sistema.append({"t": round(time.time(), 1), "fase": self.fase, "sistema_usado_pct": round(100 - float(m[-1][2]), 1)})

    def run(self):
        threading.Thread(target=self._hilo_sistema, daemon=True).start()
        prev_c, prev_j = self._leer_cputimes()
        prev_t = time.time()
        while not self.parar.wait(1.0):
            c, j = self._leer_cputimes()
            ahora = time.time()
            dt = ahora - prev_t
            d_chrome = sum(max(0.0, c[p] - prev_c[p]) for p in c if p in prev_c)
            d_jarvis = max(0.0, j - prev_j) if (j is not None and prev_j is not None) else 0.0
            self.muestras.append({
                "t": round(ahora, 1), "fase": self.fase,
                "chrome_pct_de_un_nucleo": round(100 * d_chrome / dt, 1),
                "jarvis_pct_de_un_nucleo": round(100 * d_jarvis / dt, 1),
            })
            prev_c, prev_j, prev_t = c, j, ahora


class ManejadorSpike(presentar.Manejador):
    def _json(self, codigo, obj):
        self._responder(codigo, "application/json; charset=utf-8", json.dumps(obj).encode())

    def do_POST(self):
        largo = int(self.headers.get("Content-Length") or 0)
        if largo <= 0 or largo > MAX_CUERPO:
            return self._json(400, {"ok": False, "error": "cuerpo inválido"})
        try:
            cuerpo = json.loads(self.rfile.read(largo))
        except ValueError:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        ruta = self.path.split("?")[0]
        mu = self.server.muestreador
        if ruta == "/guardar":
            nombre = str(cuerpo.get("nombre", ""))
            if not NOMBRE_OK.match(nombre):
                return self._json(400, {"ok": False, "error": "nombre no permitido"})
            TRAZAS.mkdir(parents=True, exist_ok=True)
            destino = TRAZAS / nombre
            if destino.exists():
                return self._json(409, {"ok": False, "error": "ya existe (no se sobrescribe)"})
            destino.write_text(json.dumps(cuerpo.get("datos"), ensure_ascii=False), encoding="utf-8")
            print(f"[spike] guardada {nombre}", flush=True)
            return self._json(200, {"ok": True})
        if ruta == "/marca":
            mu.fase = str(cuerpo.get("fase", ""))[:60]
            print(f"[spike] fase: {mu.fase}", flush=True)
            return self._json(200, {"ok": True})
        if ruta == "/fin":
            mu.parar.set()
            TRAZAS.mkdir(parents=True, exist_ok=True)
            (TRAZAS / "_cpu.json").write_text(json.dumps({"pid_jarvis": mu.pid_jarvis, "nucleos_logicos": mu.nucleos_logicos, "muestras": mu.muestras, "sistema": mu.sistema}), encoding="utf-8")
            print("[spike] FIN — _cpu.json escrito", flush=True)
            return self._json(200, {"ok": True})
        return self._json(404, {"ok": False})


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=presentar.PUERTO)
    ap.add_argument("--no-abrir", action="store_true")
    a = ap.parse_args()
    faltan = presentar.setup_vendor.faltantes(presentar.VENDOR)
    if faltan:
        print("ERROR: vendor/ incompleto. Corre: python3.11 setup_vendor.py", file=sys.stderr)
        return 2
    srv = presentar.Servidor(("127.0.0.1", a.port), ManejadorSpike)
    srv.cfg = SimpleNamespace(carpeta=AQUI, vendor=presentar.VENDOR, proyecto=PROYECTO, inyectar=False, debug=False)
    srv.muestreador = Muestreador()
    srv.muestreador.start()
    url = f"http://localhost:{a.port}/"
    print(f"[spike] sirviendo {AQUI.name} → {url}\n[spike] Jarvis pid: {srv.muestreador.pid_jarvis}", flush=True)
    if not a.no_abrir:
        threading.Timer(0.4, presentar.abrir_chrome, args=[url]).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.muestreador.parar.set()
        srv.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
