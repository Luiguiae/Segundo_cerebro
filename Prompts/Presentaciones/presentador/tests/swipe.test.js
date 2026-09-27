// Tests del detector de swipe v2 (swipe.js). Ejecutar: node --test tests/swipe.test.js
//  - Sintéticos: cada regla del detector por separado.
//  - Trazas reales (tests/traces/, rondas 1 y 2 del spike T06): 0 falsos positivos, 0 disparos inversos,
//    y la tasa de acierto en intentos válidos no puede empeorar (piso de regresión).
// Prioridad del proyecto: ante conflicto entre tasa de acierto y falsos positivos, gana 0 falsos positivos.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { crearDetector, CONFIG_POR_DEFECTO } = require('../swipe.js');

// ── Generadores de muestras (cuadro SIN espejar: x decreciente = derecha del presentador) ───────────
const DT = 1000 / 30;
function quieta(t0, ms, x, { cat = 'Open_Palm', y = 0.5, ruido = 0, dt = DT } = {}) {
  const m = [];
  for (let t = t0, i = 0; t <= t0 + ms; t += dt, i++) m.push({ t, x: x + (ruido ? ruido * (i % 2 ? 1 : -1) : 0), y, categoria: cat });
  return m;
}
function trazo(t0, ms, x0, x1, { cat = 'None', y0 = 0.5, y1 = 0.5, dt = DT } = {}) {
  const m = [];
  for (let t = t0; t <= t0 + ms; t += dt) { const f = (t - t0) / ms; m.push({ t, x: x0 + (x1 - x0) * f, y: y0 + (y1 - y0) * f, categoria: cat }); }
  return m;
}
const fin = (m) => m[m.length - 1].t;
function correr(det, muestras) {
  const ev = [];
  for (const m of muestras) { const r = det.procesar(m); if (r) ev.push({ t: m.t, dir: r }); }
  return ev;
}
const dirs = (ev) => ev.map((e) => e.dir);

test.describe('dirección y espejo', () => {
  test('mano abierta quieta y trazo con x decreciente → derecha', () => {
    const s = [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4)];
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha']);
  });
  test('x creciente → izquierda (verifica el espejo)', () => {
    const s = [...quieta(0, 400, 0.4), ...trazo(400, 300, 0.4, 0.6)];
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['izquierda']);
  });
  test('espejo:false invierte las direcciones', () => {
    const s = [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4)];
    assert.deepEqual(dirs(correr(crearDetector({ espejo: false }), s)), ['izquierda']);
  });
  test('cada dirección dispara exactamente una vez', () => {
    for (const [x0, x1, esp] of [[0.6, 0.4, 'derecha'], [0.4, 0.6, 'izquierda']]) {
      const ev = correr(crearDetector(), [...quieta(0, 400, x0), ...trazo(400, 300, x0, x1), ...quieta(700, 800, x1, { cat: 'None' })]);
      assert.deepEqual(dirs(ev), [esp]);
    }
  });
});

test.describe('lo que NO debe disparar', () => {
  test('trazo lento (Δ0.2 en 2 s)', () => {
    assert.deepEqual(correr(crearDetector(), [...quieta(0, 400, 0.6), ...trazo(400, 2000, 0.6, 0.4)]), []);
  });
  test('trazo corto (5 % del ancho)', () => {
    assert.deepEqual(correr(crearDetector(), [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.55)]), []);
  });
  test('desplazamiento vertical dominante', () => {
    assert.deepEqual(correr(crearDetector(), [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.5, { y0: 0.5, y1: 0.65 })]), []);
  });
  test('mano NO abierta antes del trazo (puño / dedo / sin categoría)', () => {
    for (const cat of ['Closed_Fist', 'Pointing_Up', 'None', null]) {
      assert.deepEqual(correr(crearDetector(), [...quieta(0, 600, 0.6, { cat }), ...trazo(600, 300, 0.6, 0.4)]), [], String(cat));
    }
  });
  test('mano abierta en movimiento continuo (0.5 anchos/s), sin quietud previa', () => {
    const s = trazo(0, 1400, 0.85, 0.15, { cat: 'Open_Palm' });
    assert.deepEqual(correr(crearDetector(), s), []);
  });
  test('3 cuadros quietos que abarcan solo ~66 ms no bastan (la quietud debe abarcar ≥150 ms)', () => {
    const s = [...quieta(0, 66, 0.6), ...trazo(100, 300, 0.6, 0.4)];
    assert.deepEqual(correr(crearDetector(), s), []);
    // con 200 ms de quietud sí dispara
    assert.deepEqual(dirs(correr(crearDetector(), [...quieta(0, 200, 0.6), ...trazo(233, 300, 0.6, 0.4)])), ['derecha']);
  });
  test('vaivén rápido con la palma abierta (2–3 Hz): sin eventos pasado el primer segundo', () => {
    for (const [hz, A] of [[2, 0.12], [2, 0.08]]) {
      const det = crearDetector(); const ev = [];
      for (let t = 0; t < 5000; t += DT) { const r = det.procesar({ t, x: 0.5 + A * Math.sin(2 * Math.PI * hz * t / 1000), y: 0.5, categoria: 'Open_Palm' }); if (r && t >= 1000) ev.push(t); }
      assert.deepEqual(ev, [], `${hz} Hz ±${A}`);
    }
  });
  test('temblor de ±2 % con la mano abierta quieta', () => {
    assert.deepEqual(correr(crearDetector(), quieta(0, 4000, 0.5, { ruido: 0.02 })), []);
  });
  test('mano que sale y entra en otro lugar (hueco de 500 ms)', () => {
    const s = [...quieta(0, 500, 0.6), ...quieta(1000, 500, 0.4)];
    assert.deepEqual(correr(crearDetector(), s), []);
  });
  test('hueco de detección de 450 ms (>400) con reaparición desplazada: se descarta como salto de seguimiento', () => {
    const s = [...quieta(0, 500, 0.6), { t: 950, x: 0.4, y: 0.5, categoria: 'Open_Palm' }, { t: 983, x: 0.4, y: 0.5, categoria: 'Open_Palm' }];
    assert.deepEqual(correr(crearDetector(), s), []);
  });
  test('cuadros sin mano (x nulo) no rompen ni disparan', () => {
    const det = crearDetector();
    assert.equal(det.procesar({ t: 0, x: null, y: null, categoria: null }), null);
    assert.equal(det.procesar(null), null);
    assert.equal(det.procesar(undefined), null);
    assert.equal(det.procesar({ t: 'x', x: 0.5, y: 0.5 }), null);
  });
});

test.describe('lo que SÍ debe disparar aunque sea imperfecto', () => {
  test('la categoría se pierde DURANTE el trazo (solo hace falta abierta y quieta antes)', () => {
    const s = [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4, { cat: null })];
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha']);
  });
  test('muestreo irregular (66–100 ms)', () => {
    const s = []; let t = 0, k = 0;
    while (t < 700) { s.push({ t, x: 0.6, y: 0.5, categoria: 'Open_Palm' }); t += (k++ % 2 ? 66 : 100); }
    let x = 0.6; while (x > 0.38) { x -= 0.07; s.push({ t, x, y: 0.5, categoria: 'None' }); t += (k++ % 2 ? 66 : 100); }
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha']);
  });
  test('hueco de 300 ms (<400) a mitad del trazo: es desenfoque de movimiento, sí cuenta', () => {
    const s = [...quieta(0, 500, 0.6), { t: 800, x: 0.4, y: 0.5, categoria: 'Open_Palm' }];
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha']);
  });
  test('la mano se pierde 250 ms a mitad del trazo (desenfoque) y reaparece en el destino', () => {
    const s = [...quieta(0, 400, 0.6), { t: 433, x: 0.58, y: 0.5, categoria: 'Open_Palm' }, { t: 700, x: 0.37, y: 0.5, categoria: 'Open_Palm' }];
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha']);
  });
  test('dos cuadros seguidos moviéndose tras el disparo: un solo evento', () => {
    const ev = correr(crearDetector(), [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.35), ...trazo(700, 100, 0.35, 0.3)]);
    assert.equal(ev.length, 1);
  });
});

test.describe('retorno de la mano y cooldown', () => {
  test('swipe + retorno rápido dentro de 1500 ms = 1 solo evento', () => {
    const ev = correr(crearDetector(), [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4), ...trazo(700, 300, 0.4, 0.6, { cat: 'Open_Palm' })]);
    assert.deepEqual(dirs(ev), ['derecha']);
  });
  test('retorno a los 1600 ms sin haber quedado abierta y quieta = ninguno', () => {
    const ev = correr(crearDetector(), [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4), ...trazo(700, 900, 0.4, 0.45, { cat: 'None' }), ...trazo(1600, 300, 0.45, 0.65)]);
    assert.deepEqual(dirs(ev), ['derecha']);
  });
  test('tras quedarse abierta y quieta 300 ms, un nuevo swipe en el MISMO sentido sí dispara', () => {
    const s = [...quieta(0, 400, 0.7), ...trazo(400, 300, 0.7, 0.5), ...quieta(1700, 400, 0.7), ...trazo(2100, 300, 0.7, 0.5)];
    // la mano vuelve a su sitio sin trazo detectable (salto de cuadros) y queda abierta y quieta antes del segundo swipe
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha', 'derecha']);
  });
  test('sentido CONTRARIO bloqueado 3 s tras un evento (retorno con pausa) y se consume el trazo', () => {
    // derecha en 700 ms; la mano reposa abierta 2 s en el destino y vuelve rápido a los 2.7 s (2 s después) → bloqueado
    const s = [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4), ...quieta(700, 2000, 0.4), ...trazo(2700, 300, 0.4, 0.6), ...quieta(3000, 1500, 0.6, { cat: 'None' })];
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha'], 'el retorno no debe disparar ni siquiera al vencer el bloqueo');
  });
  test('el sentido contrario SÍ dispara pasado el bloqueo (swipe deliberado a la izquierda)', () => {
    const s = [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4), ...quieta(700, 3500, 0.4), ...trazo(4200, 300, 0.4, 0.6)];
    assert.deepEqual(dirs(correr(crearDetector(), s)), ['derecha', 'izquierda']);
  });
  test('notificarCambio (otro canal): ignora 1500 ms y exige nueva quietud', () => {
    const det = crearDetector();
    const antes = quieta(0, 400, 0.6);
    correr(det, antes);
    det.notificarCambio(fin(antes));
    assert.deepEqual(correr(det, trazo(450, 300, 0.6, 0.4)), [], 'dentro del cooldown');
    assert.deepEqual(dirs(correr(det, [...quieta(1800, 400, 0.6), ...trazo(2200, 300, 0.6, 0.4)])), ['derecha'], 'con nueva quietud dispara');
  });
  test('notificarCambio limpia el historial: la quietud previa al cambio no cuenta', () => {
    const det = crearDetector();
    const a = quieta(0, 600, 0.6); correr(det, a);
    det.notificarCambio(fin(a));
    assert.deepEqual(correr(det, trazo(fin(a) + 1600, 300, 0.6, 0.4)), []);
  });
  test('reiniciar() vuelve al estado inicial', () => {
    const det = crearDetector();
    correr(det, [...quieta(0, 400, 0.6), ...trazo(400, 300, 0.6, 0.4)]);
    det.reiniciar();
    assert.deepEqual(dirs(correr(det, [...quieta(800, 400, 0.6), ...trazo(1200, 300, 0.6, 0.4)])), ['derecha']);
  });
  test('el reloj que retrocede no rompe nada', () => {
    const det = crearDetector();
    correr(det, quieta(1000, 300, 0.5));
    assert.doesNotThrow(() => correr(det, quieta(0, 300, 0.5)));
  });
});

test('la configuración por defecto es la aprobada (plan.md §12)', () => {
  assert.equal(CONFIG_POR_DEFECTO.umbral, 0.08);
  assert.equal(CONFIG_POR_DEFECTO.ventanaMs, 500);
  assert.equal(CONFIG_POR_DEFECTO.quietoMs, 200);
  assert.equal(CONFIG_POR_DEFECTO.cooldownMs, 1500);
  assert.equal(CONFIG_POR_DEFECTO.categoriaAbierta, 'Open_Palm');
});

// ── Trazas reales (rondas 1 y 2 del spike) ───────────────────────────────────────────────────────────
const DIR_TRAZAS = path.join(__dirname, 'traces');
const trazas = fs.readdirSync(DIR_TRAZAS)
  .filter((f) => f.endsWith('.json') && !/resumen|cpu/.test(f))
  .map((f) => ({ archivo: f, ronda: f.startsWith('r2-') ? 2 : 1, ...JSON.parse(fs.readFileSync(path.join(DIR_TRAZAS, f), 'utf8')) }));
const eventosDe = (t) => { const d = crearDetector(); return correr(d, t.muestras.map((m) => ({ t: m.t, x: m.x, y: m.y, categoria: m.cat }))); };
const ESPERADO = { derecha: 'derecha', izquierda: 'izquierda', retorno: 'derecha' };

test('hay trazas reales de las dos rondas para probar', () => {
  assert.ok(trazas.filter((t) => t.ronda === 1).length >= 50, 'ronda 1');
  assert.ok(trazas.filter((t) => t.ronda === 2).length >= 45, 'ronda 2');
});

test.describe('trazas reales — 0 falsos positivos', () => {
  for (const t of trazas.filter((x) => ['gesticulacion', 'reposo', 'noabierta'].includes(x.tipo))) {
    test(`${t.archivo}: ningún evento (${t.tipo})`, () => assert.deepEqual(eventosDe(t), []));
  }
});

test.describe('trazas reales — swipes', () => {
  const swipes = trazas.filter((x) => ESPERADO[x.tipo]);
  test('0 eventos antes del YA', () => {
    for (const t of swipes) assert.deepEqual(eventosDe(t).filter((e) => e.t < t.ya_ms), [], t.archivo);
  });
  test('0 disparos inversos (en cualquier posición) ni eventos extra', () => {
    for (const t of swipes) {
      const d = eventosDe(t).filter((e) => e.t >= t.ya_ms);
      assert.ok(d.length <= 1, `${t.archivo}: ${d.length} eventos`);
      for (const e of d) assert.equal(e.dir, ESPERADO[t.tipo], `${t.archivo}: dirección inversa`);
    }
  });
  const tasa = (lista, tipo) => { const v = lista.filter((x) => x.tipo === tipo && x.valida); return [v.filter((t) => eventosDe(t).some((e) => e.t >= t.ya_ms && e.dir === tipo)).length, v.length]; };
  test('ronda 2 — intentos válidos: ≥8/10 derecha y ≥8/10 izquierda (meta del proyecto)', () => {
    const r2 = trazas.filter((t) => t.ronda === 2);
    for (const tipo of ['derecha', 'izquierda']) { const [ok, n] = tasa(r2, tipo); assert.equal(n, 10); assert.ok(ok >= 8, `${tipo}: ${ok}/${n}`); }
  });
  test('rondas 1+2 — intentos válidos: piso de regresión (15/18 derecha, 15/17 izquierda)', () => {
    const [okd, nd] = tasa(trazas, 'derecha'), [oki, ni] = tasa(trazas, 'izquierda');
    assert.ok(okd >= 15, `derecha ${okd}/${nd}`); assert.ok(oki >= 15, `izquierda ${oki}/${ni}`);
  });
});
