"""Prototipos offline (ronda 2 del spike, T06). Ejecutar: python3 comparar_metodos.py
Contiene los DETECTORES DE PROTOTIPO `detector` (v1: armado por dwell) y `detector2` (v2: mano abierta quieta justo antes del trazo)
que T09 tomará como punto de partida.

Comparación offline de dos formas de detectar 'mano abierta' (ronda 2, con landmarks):
  A) categoría Open_Palm del clasificador
  B) geometría con los 21 landmarks (dedos extendidos)
Mismo detector de swipe para ambas; solo cambia el predicado `abierta(muestra)` de armado."""
import glob, json, math, sys, itertools, collections
from pathlib import Path
D = str(Path(__file__).resolve().parents[2] / "traces") + "/"

def cargar(t): return [json.load(open(f)) for f in sorted(glob.glob(f"{D}r2-{t}-*.json"))]

# ---- predicados de "mano abierta" ------------------------------------------------------------------
def pred_categoria(m): return m.get("cat") == "Open_Palm"

DEDOS = [(8, 5), (12, 9), (16, 13), (20, 17)]          # (punta, MCP) índice, medio, anular, meñique
def d(a, b): return math.dist(a[:2], b[:2])            # distancia en el plano de imagen (x,y normalizados)
def pred_geo(tau=1.5, minimo=4, con_pulgar=False):
    def f(m):
        lm = m.get("lm")
        if not lm: return False
        muneca = lm[0]; n = 0
        for punta, mcp in DEDOS:
            base = d(lm[mcp], muneca)
            if base > 1e-6 and d(lm[punta], muneca) / base >= tau: n += 1
        if con_pulgar and d(lm[4], lm[17]) / max(1e-6, d(lm[5], lm[17])) < 1.2: return False
        return n >= minimo
    return f

# ---- detector de swipe (parametrizado) --------------------------------------------------------------
def detector(ms, abierta, TH=0.10, W=500, A=600, K=3, CD=1500, DY=0.6):
    ev = []; ult = -1e9; hist = []; abiertos = []; esperando = False
    for m in ms:
        if m["x"] is None: continue
        t = m["t"]; hist.append((t, m["x"], m["y"])); hist = [h for h in hist if t - h[0] <= max(W, A)]
        if abierta(m): abiertos.append(t)
        abiertos = [a for a in abiertos if t - a <= A]
        if t - ult < CD: continue
        if esperando:
            if len(abiertos) >= K: esperando = False
            else: continue
        if len(abiertos) < K: continue
        mejor = None
        for h in hist:
            if t - h[0] > W: continue
            dx = m["x"] - h[1]; dy = m["y"] - h[2]
            if abs(dx) >= TH and abs(dy) < DY * abs(dx) and (mejor is None or abs(dx) > abs(mejor)): mejor = dx
        if mejor is not None:
            ev.append((t, "derecha" if mejor < 0 else "izquierda")); ult = t; esperando = True; abiertos = []
    return ev

def evalua(abierta, filtro=lambda t: True, **kw):
    r = {}
    for tipo, esp in (("derecha", "derecha"), ("izquierda", "izquierda"), ("retorno", "derecha")):
        tr = [t for t in cargar(tipo) if filtro(t)]; ok = inv = mudo = extra = pre = 0
        for t in tr:
            ev = detector(t["muestras"], abierta, **kw)
            antes = [e for e in ev if e[0] < t["ya_ms"]]; despues = [e for e in ev if e[0] >= t["ya_ms"]]
            pre += len(antes)
            if not despues: mudo += 1; continue
            if despues[0][1] == esp: ok += 1
            else: inv += 1
            extra += len(despues) - 1
        r[tipo] = dict(n=len(tr), ok=ok, mudo=mudo, inverso=inv, extra=extra, antes_ya=pre)
    fp = {}
    for tipo in ("gesticulacion", "noabierta", "reposo"):
        tr = [t for t in cargar(tipo) if filtro(t)]
        fp[tipo] = [len(detector(t["muestras"], abierta, **kw)) for t in tr]
    return r, fp

def resumen(nombre, r, fp):
    dr, iz = r["derecha"], r["izquierda"]
    tot_fp = sum(sum(v) for v in fp.values()); seg = sum(t["duracion_ms"] for tp in fp for t in cargar(tp)) / 1000
    return f"{nombre:44s} der {dr['ok']:2d}/{dr['n']:2d} ({100*dr['ok']/max(1,dr['n']):3.0f}%)  izq {iz['ok']:2d}/{iz['n']:2d} ({100*iz['ok']/max(1,iz['n']):3.0f}%)  ret {r['retorno']['ok']}/{r['retorno']['n']}  inv {dr['inverso']+iz['inverso']+r['retorno']['inverso']}  extra {dr['extra']+iz['extra']+r['retorno']['extra']}  FP {tot_fp} en {seg:.0f} s (gest {fp['gesticulacion']} puño {fp['noabierta']} reposo {fp['reposo']})"

if __name__ == "__main__":
    print("N trazas:", {t: len(cargar(t)) for t in ("derecha", "izquierda", "retorno", "noabierta", "reposo", "gesticulacion")})

# ---- geometría con orientación --------------------------------------------------------------------
def _cross_z(lm):
    a = (lm[5][0] - lm[0][0], lm[5][1] - lm[0][1]); b = (lm[17][0] - lm[0][0], lm[17][1] - lm[0][1])
    return a[0] * b[1] - a[1] * b[0]
def _angulo(lm):  # grados desde "arriba"
    return abs(math.degrees(math.atan2(lm[9][0] - lm[0][0], -(lm[9][1] - lm[0][1]))))
def pred_geo_ori(tau=1.5, minimo=4, max_ang=45, palma=True):
    ext = pred_geo(tau, minimo)
    def f(m):
        lm = m.get("lm")
        if not lm or not ext(m): return False
        if max_ang is not None and _angulo(lm) > max_ang: return False
        if palma:
            cz = _cross_z(lm)
            if not ((cz < 0) if m.get("h") == "Right" else (cz > 0)): return False   # palma hacia la cámara (regla aprendida por lateralidad)
        return True
    return f

# ---- detector v2: mano abierta QUIETA justo antes del trazo ------------------------------------------
def detector2(ms, abierta, TH=0.10, W=500, AST=300, KST=3, SP=0.04, CD=1500, DY=0.6, FRAC=0.6):
    """Evento si hay un trazo horizontal ≥TH en ≤W ms precedido por AST ms de mano abierta casi quieta
    (≥KST cuadros, ≥FRAC de ellos 'abierta', dispersión x/y ≤SP). La mano no necesita ser 'abierta' durante el trazo."""
    ev = []; ult = -1e9; hist = []
    for m in ms:
        if m["x"] is None: continue
        t = m["t"]
        hist.append((t, m["x"], m["y"], abierta(m)))
        hist = [h for h in hist if t - h[0] <= W + AST + 50]
        if t - ult < CD: continue
        mejor = None
        for a in hist:
            if t - a[0] > W or t - a[0] < 60: continue
            dx = m["x"] - a[1]; dy = m["y"] - a[2]
            if abs(dx) < TH or abs(dy) >= DY * abs(dx): continue
            quieto = [h for h in hist if a[0] - AST <= h[0] <= a[0]]
            if len(quieto) < KST: continue
            xs = [h[1] for h in quieto]; ys = [h[2] for h in quieto]
            if max(xs) - min(xs) > SP or max(ys) - min(ys) > SP: continue
            if sum(1 for h in quieto if h[3]) < FRAC * len(quieto): continue
            if mejor is None or abs(dx) > abs(mejor): mejor = dx
        if mejor is not None:
            ev.append((t, "derecha" if mejor < 0 else "izquierda")); ult = t; hist = []
    return ev
