// Spike de gestos (T06) — SOLO desarrollo. Mide MediaPipe GestureRecognizer en este Mac/Chrome y graba
// trazas {t, x, y, cat} (solo coordenadas del centro de palma; nunca imágenes) guiando a Luigui en pantalla.
//
// Flujo: ESPACIO → permiso de cámara → cuenta atrás para que te alejes → benchmark (≈50 s) →
//        protocolo de grabación guiado (25 swipes + 3 no-abierta + 3 gesticulación) → resumen.
// Con ?prueba=1 los tiempos se acortan y no se exige mano (para probar el flujo con una cámara falsa).

import { FilesetResolver, GestureRecognizer } from '/vendor/tasks-vision/vision_bundle.mjs';

const QS = new URLSearchParams(location.search);
const PRUEBA = QS.has('prueba');
const RONDA2 = QS.get('ronda') === '2';   // ronda 2: 640×480 fijo, 21 landmarks por cuadro, protocolo corto, archivos con prefijo r2-
const PREFIJO = RONDA2 ? 'r2-' : '';
const $ = (id) => document.getElementById(id);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const post = (ruta, cuerpo) => fetch(ruta, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(cuerpo) })
  .then((r) => r.json()).catch((e) => ({ ok: false, error: String(e) }));
const marca = (fase) => post('/marca', { fase });
const redondea = (v, d = 4) => (v === null || v === undefined ? null : Math.round(v * 10 ** d) / 10 ** d);
const pct = (arr, p) => { if (!arr.length) return null; const s = [...arr].sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
const media = (arr) => (arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : null);

const video = $('video'), punto = $('punto');
const coach = (t, s = '', c = '') => { $('coach').textContent = t; $('sub').textContent = s; $('cuenta').textContent = c; };

// ── Audio (avisos para quien está de pie a distancia) ───────────────────────────────────────────────
let ac = null;
function beep(freq = 660, ms = 120, vol = 0.25) {
  if (!ac) return;
  const o = ac.createOscillator(), g = ac.createGain();
  o.frequency.value = freq; g.gain.value = vol; o.connect(g); g.connect(ac.destination);
  o.start(); o.stop(ac.currentTime + ms / 1000);
}

// ── Estado global ───────────────────────────────────────────────────────────────────────────────────
let vision = null;
const reconocedores = {};        // 'GPU' | 'CPU' → GestureRecognizer
const cargaMs = {}, errores = {};
let stream = null, ajustesCamara = null;
let ultimoTs = 0;
let pausado = false, abortar = false;
const resumen = { version: 1, prueba: PRUEBA, inicio: new Date().toISOString(), baseline: {}, configs: [], elegida: null, protocolo: {}, trazas: [], red: null, entorno: {} };

// ── Cámara y bucle de detección ─────────────────────────────────────────────────────────────────────
async function abrirCamara(w, h) {
  if (stream) stream.getTracks().forEach((t) => t.stop());
  stream = await navigator.mediaDevices.getUserMedia({ video: { width: { ideal: w }, height: { ideal: h }, frameRate: { ideal: 30 } }, audio: false });
  video.srcObject = stream;
  await video.play();
  await sleep(300);
  const s = stream.getVideoTracks()[0].getSettings();
  ajustesCamara = { ancho: s.width, alto: s.height, fps_declarados: s.frameRate };
  punto.width = 160; punto.height = 120;
  return ajustesCamara;
}

const CENTRO_PALMA = [0, 5, 9, 13, 17]; // muñeca + base de los 4 dedos
function muestraDe(res, ts, t0, t1, meta, now) {
  const m = { t: ts, infer: t1 - t0, lat: t1 - (meta.captureTime ?? meta.presentationTime ?? now), x: null, y: null, cat: null, s: null };
  const lm = res && res.landmarks && res.landmarks[0];
  if (lm) {
    m.x = CENTRO_PALMA.reduce((a, i) => a + lm[i].x, 0) / CENTRO_PALMA.length;
    m.y = CENTRO_PALMA.reduce((a, i) => a + lm[i].y, 0) / CENTRO_PALMA.length;
    const g = res.gestures && res.gestures[0] && res.gestures[0][0];
    if (g) { m.cat = g.categoryName; m.s = g.score; }
    m.lm = lm.map((q) => [q.x, q.y, q.z]);   // los 21 landmarks (existen aunque la categoría sea "ninguna")
    const hd = res.handedness && res.handedness[0] && res.handedness[0][0];
    if (hd) m.h = hd.categoryName;
  }
  return m;
}

// Bucle: procesa cada cuadro de vídeo con `rec` (o solo cuenta cuadros si rec es null) hasta que `hasta()` sea true.
function bucle(rec, hasta, alMuestra) {
  return new Promise((resolve) => {
    const out = [];
    const paso = (now, meta) => {
      if (hasta()) return resolve(out);
      ultimoTs = Math.max(ultimoTs + 1, Math.round(now));
      const t0 = performance.now();
      const res = rec ? rec.recognizeForVideo(video, ultimoTs) : null;
      const t1 = performance.now();
      const m = muestraDe(res, now, t0, t1, meta, now);
      out.push(m);
      if (alMuestra) alMuestra(m);
      video.requestVideoFrameCallback(paso);
    };
    video.requestVideoFrameCallback(paso);
  });
}

let vivoUlt = 0;
function actualizaVivo(m) {
  const ahora = performance.now();
  if (ahora - vivoUlt < 100) return;
  vivoUlt = ahora;
  const el = $('live');
  if (m.cat === 'Open_Palm') { el.className = 'palma'; el.textContent = 'palma abierta ✓'; }
  else if (m.x !== null) { el.className = 'mano'; el.textContent = `mano: ${m.cat || '?'}`; }
  else { el.className = ''; el.textContent = 'sin mano'; }
  const c = punto.getContext('2d'); c.clearRect(0, 0, punto.width, punto.height);
  if (m.x !== null) { c.fillStyle = m.cat === 'Open_Palm' ? '#7ee787' : '#ffd166'; c.beginPath(); c.arc(m.x * punto.width, m.y * punto.height, 7, 0, 7); c.fill(); }
}

// ── Benchmark ───────────────────────────────────────────────────────────────────────────────────────
function estadisticas(muestras, ventanaIniMs, ventanaMs) {
  const t0 = muestras.length ? muestras[0].t : 0;
  const utiles = muestras.filter((m) => m.t - t0 >= ventanaIniMs); // descarta el calentamiento
  const dur = utiles.length ? (utiles[utiles.length - 1].t - utiles[0].t) / 1000 : 0;
  const porSeg = {};
  utiles.forEach((m) => { const b = Math.floor((m.t - utiles[0].t) / 1000); porSeg[b] = (porSeg[b] || 0) + 1; });
  const segs = Object.entries(porSeg).filter(([b]) => Number(b) < Math.floor(dur)).map(([, v]) => v); // solo segundos completos
  return {
    cuadros: utiles.length, segundos: redondea(dur, 1),
    fps_medio: redondea(dur ? utiles.length / dur : 0, 1),
    fps_min_por_seg: segs.length ? Math.min(...segs) : null,
    fps_p5_por_seg: segs.length ? pct(segs, 0.05) : null,
    pct_segundos_ge15: segs.length ? redondea(100 * segs.filter((v) => v >= 15).length / segs.length, 0) : null,
    infer_ms_medio: redondea(media(utiles.map((m) => m.infer)), 1), infer_ms_p95: redondea(pct(utiles.map((m) => m.infer), 0.95), 1),
    latencia_ms_medio: redondea(media(utiles.map((m) => m.lat)), 1), latencia_ms_p95: redondea(pct(utiles.map((m) => m.lat), 0.95), 1),
    pct_con_mano: redondea(100 * utiles.filter((m) => m.x !== null).length / Math.max(1, utiles.length), 0),
    pct_palma_abierta: redondea(100 * utiles.filter((m) => m.cat === 'Open_Palm').length / Math.max(1, utiles.length), 0),
  };
}

async function benchmark() {
  const RES = { '640x480': [640, 480], '320x240': [320, 240] };
  const durBase = PRUEBA ? 1500 : 3000, durCfg = PRUEBA ? 5000 : 13000, calienta = PRUEBA ? 1500 : 3000; // 3 s de calentamiento (compila shaders GPU) + 10 s medidos
  for (const [nombre, [w, h]] of Object.entries(RES)) {
    await marca(`baseline-${nombre}`);
    coach('Midiendo la cámara…', `Resolución ${nombre} — sin detección, solo cuántos cuadros entrega la cámara.`);
    const aj = await abrirCamara(w, h);
    const t0 = performance.now();
    const cu = await bucle(null, () => performance.now() - t0 >= durBase);
    resumen.baseline[nombre] = { ajustes: aj, fps_camara_medidos: redondea(cu.length / (durBase / 1000), 1) };
  }
  const CFGS = [['GPU', '640x480'], ['CPU', '640x480'], ['GPU', '320x240'], ['CPU', '320x240']];
  let n = 0;
  for (const [delegado, nombre] of CFGS) {
    n++;
    if (!reconocedores[delegado]) { resumen.configs.push({ delegado, resolucion: nombre, omitida: true, error: errores[delegado] }); continue; }
    await marca(`bench-${delegado}-${nombre}`);
    coach(`Prueba ${n}/4 · ${delegado} ${nombre}`, 'Mantén la MANO ABIERTA frente a la cámara, palma hacia ella, y muévela despacio de lado a lado.', '');
    const aj = await abrirCamara(...RES[nombre]);
    const t0 = performance.now();
    const cu = await bucle(reconocedores[delegado], () => performance.now() - t0 >= durCfg, actualizaVivo);
    resumen.configs.push({ delegado, resolucion: nombre, ajustes: aj, ...estadisticas(cu, calienta) });
    coach(`Prueba ${n}/4 lista`, `${delegado} ${nombre}: ${resumen.configs.at(-1).fps_medio} fps`, '');
    await sleep(600);
  }
  // Config elegida: mayor fps medio con mano vista; en empate, la de mayor resolución.
  const validas = resumen.configs.filter((c) => !c.omitida && c.fps_medio);
  validas.sort((a, b) => b.fps_medio - a.fps_medio || (b.resolucion === '640x480') - (a.resolucion === '640x480'));
  resumen.elegida = validas[0] ? { delegado: validas[0].delegado, resolucion: validas[0].resolucion } : null;
}

// ── Análisis de una traza (informativo; el detector real se diseña en T09) ────────────────────────────
// x,y en coordenadas SIN espejar. Presentador: mueve la mano a SU derecha ⇒ x DISMINUYE en la imagen cruda.
function ventanaMaxDx(palma) {
  let mejor = { dx: 0, dy: 0, ms: 0, t: 0 };
  for (let i = 0; i < palma.length; i++) {
    for (let j = i + 1; j < palma.length && palma[j].t - palma[i].t <= 500; j++) {
      const dx = palma[j].x - palma[i].x;
      if (Math.abs(dx) > Math.abs(mejor.dx)) mejor = { dx, dy: palma[j].y - palma[i].y, ms: palma[j].t - palma[i].t, t: palma[j].t };
    }
  }
  return mejor;
}
// Detector ingenuo (solo umbral) para saber cuántos disparos daría sin re-armado: útil para T09.
function eventosIngenuos(palma) {
  const ev = []; let bloqueadoHasta = -1;
  for (let i = 0; i < palma.length; i++) {
    if (palma[i].t < bloqueadoHasta) continue;
    for (let j = i + 1; j < palma.length && palma[j].t - palma[i].t <= 400; j++) {
      const dx = palma[j].x - palma[i].x, dy = palma[j].y - palma[i].y;
      if (Math.abs(dx) >= 0.25 && Math.abs(dy) < 0.5 * Math.abs(dx)) {
        ev.push({ t_ms: Math.round(palma[j].t), dir: dx < 0 ? 'derecha' : 'izquierda' });
        bloqueadoHasta = palma[j].t + 1500; break;
      }
    }
  }
  return ev;
}
function analiza(muestras, yaMs) {
  const post = muestras.filter((m) => m.t >= yaMs);
  const palma = post.filter((m) => m.cat === 'Open_Palm' && m.x !== null);
  const mano = post.filter((m) => m.x !== null);
  const w = ventanaMaxDx(palma);
  const wCualquiera = ventanaMaxDx(mano);
  return {
    cuadros: post.length, cuadros_con_mano: mano.length, cuadros_palma_abierta: palma.length,
    pct_palma_abierta: redondea(100 * palma.length / Math.max(1, post.length), 0),
    dx_max_palma: redondea(Math.abs(w.dx), 3), dx_max_con_signo_crudo: redondea(w.dx, 3), dy_en_esa_ventana: redondea(w.dy, 3), ms_de_esa_ventana: Math.round(w.ms),
    direccion_presentador: w.dx === 0 ? null : (w.dx < 0 ? 'derecha' : 'izquierda'),
    dx_max_cualquier_gesto: redondea(Math.abs(wCualquiera.dx), 3),
    eventos_ingenuos: eventosIngenuos(palma),
  };
}

// ── Protocolo de grabación ──────────────────────────────────────────────────────────────────────────
const PASOS1 = [
  { tipo: 'derecha', nombre: 'SWIPE A TU DERECHA', n: 10, dur: 3500, ayuda: 'Mano ABIERTA, palma hacia la cámara, al centro. Al oír el tono largo: un swipe rápido hacia TU DERECHA y deja que la mano vuelva sola, sin frenarla.' },
  { tipo: 'izquierda', nombre: 'SWIPE A TU IZQUIERDA', n: 10, dur: 3500, ayuda: 'Mano ABIERTA al centro. Al oír el tono largo: un swipe rápido hacia TU IZQUIERDA y deja que la mano vuelva sola, sin frenarla.' },
  { tipo: 'retorno', nombre: 'IDA Y VUELTA RÁPIDO', n: 5, dur: 4000, ayuda: 'Mano ABIERTA al centro. Al oír el tono largo: swipe a tu DERECHA y regresa la mano al centro lo MÁS RÁPIDO que puedas (el peor caso). Luego baja la mano.' },
  { tipo: 'noabierta', nombre: 'PUÑO O DEDO — RÁPIDO', n: 3, dur: 3500, ayuda: 'Cierra el puño (o señala con un dedo). Al oír el tono largo: muévelo rápido de lado a lado varias veces. NO debe contar como swipe.' },
  { tipo: 'gesticulacion', nombre: 'HABLA Y GESTICULA', n: 3, dur: 20000, ayuda: 'Cuéntame en voz alta qué hiciste hoy, gesticulando normal — la mano abierta a ratos, moviéndola como al explicar. SIN swipes intencionales. Dura 20 s.' },
];

// Ronda 2: más corta (~10 min) y con "reposo" (mano abierta quieta hablando) para medir falsos positivos del armado.
const PASOS2 = [
  { tipo: 'derecha', nombre: 'SWIPE A TU DERECHA', n: 10, dur: 3000, ayuda: 'Mano ABIERTA, dedos bien separados, palma hacia la cámara, al centro. Al tono largo: un swipe rápido y amplio hacia TU DERECHA; deja que la mano vuelva sola.' },
  { tipo: 'izquierda', nombre: 'SWIPE A TU IZQUIERDA', n: 10, dur: 3000, ayuda: 'Mano ABIERTA, dedos bien separados, palma hacia la cámara, al centro. Al tono largo: un swipe rápido y amplio hacia TU IZQUIERDA; deja que la mano vuelva sola.' },
  { tipo: 'retorno', nombre: 'IDA Y VUELTA RÁPIDO', n: 4, dur: 3500, ayuda: 'Mano ABIERTA al centro. Al tono largo: swipe a tu DERECHA y regresa la mano al centro lo MÁS RÁPIDO posible. Luego baja la mano.' },
  { tipo: 'noabierta', nombre: 'PUÑO O DEDO — RÁPIDO', n: 2, dur: 3000, ayuda: 'Puño cerrado o señalando con un dedo; al tono largo, muévelo rápido de lado a lado. NO debe contar como swipe.' },
  { tipo: 'reposo', nombre: 'MANO ABIERTA QUIETA', n: 2, dur: 10000, ayuda: 'Al tono largo: mano ABIERTA frente a la cámara, casi quieta (como esperando), mientras cuentas algo en voz alta. Sin swipes. Dura 10 s.' },
  { tipo: 'gesticulacion', nombre: 'HABLA Y GESTICULA', n: 4, dur: 20000, ayuda: 'Cuéntame en voz alta qué hiciste hoy, gesticulando normal, con la mano abierta a ratos. SIN swipes intencionales. Dura 20 s. (No digas "Jarvis")' },
];
const PASOS = RONDA2 ? PASOS2 : PASOS1;

function contadores(validas) {
  return PASOS.map((p) => `${p.tipo === 'noabierta' ? 'Puño' : p.tipo === 'reposo' ? 'Reposo' : p.tipo === 'gesticulacion' ? 'Gesticulación' : p.tipo[0].toUpperCase() + p.tipo.slice(1)} ${validas[p.tipo] || 0}/${PRUEBA ? 1 : p.n}`).join('  ·  ');
}

async function esperaPausa() { while (pausado && !abortar) { coach('PAUSA', 'Pulsa ESPACIO para continuar.'); await sleep(200); } }

async function protocolo(rec) {
  pausado = false;
  const validas = {}, intentos = {};
  const total = PASOS.reduce((a, p) => a + (PRUEBA ? 1 : p.n), 0);
  let hechas = 0;
  let muestras = [];
  let grabando = false, tGrab = 0;
  // Bucle continuo en segundo plano: llena `muestras` mientras `grabando`.
  let activo = true;
  const fondo = bucle(rec, () => !activo, (m) => { actualizaVivo(m); if (grabando) muestras.push(m); });

  for (const paso of PASOS) {
    const objetivo = PRUEBA ? 1 : paso.n;
    validas[paso.tipo] = 0; intentos[paso.tipo] = 0;
    while (validas[paso.tipo] < objetivo && intentos[paso.tipo] < objetivo * 2 && !abortar) {
      await esperaPausa(); if (abortar) break;
      intentos[paso.tipo]++;
      const k = intentos[paso.tipo];
      await marca(`grabando-${paso.tipo}`);
      document.body.className = '';
      $('cont').textContent = `${contadores(validas)}\nFaltan ${total - hechas} de ${total} · intento ${k}${k > objetivo ? ' (repetición)' : ''}`;
      coach(`${paso.nombre}  ${validas[paso.tipo] + 1}/${objetivo}`, paso.ayuda, '');
      await sleep(PRUEBA ? 400 : RONDA2 ? 2200 : 3200);          // tiempo para leer y colocarse
      for (const n of PRUEBA ? [1] : RONDA2 ? [2, 1] : [3, 2, 1]) {              // cuenta atrás; la grabación empieza en el "1"
        $('cuenta').textContent = String(n); beep(520, 110);
        if (n === 1) { muestras = []; tGrab = performance.now(); grabando = true; }
        await sleep(PRUEBA ? 200 : RONDA2 ? 850 : 1000);
      }
      const yaMs = performance.now();
      beep(1040, 450, 0.35); document.body.className = 'ya'; coach('¡YA!', paso.ayuda, '');
      await sleep(PRUEBA ? Math.min(paso.dur, 1200) : paso.dur);
      grabando = false; document.body.className = ''; beep(440, 120);

      const rel = muestras.map((m) => ({ ...m, t: m.t - tGrab }));
      const an = analiza(rel, yaMs - tGrab);
      let valida;
      if (PRUEBA) valida = true;
      else if (paso.tipo === 'gesticulacion') valida = an.cuadros_con_mano >= 40;
      else if (paso.tipo === 'reposo') valida = an.cuadros_con_mano >= 0.6 * an.cuadros;
      else if (RONDA2 && ['derecha', 'izquierda', 'retorno'].includes(paso.tipo)) valida = an.cuadros_con_mano >= 0.5 * an.cuadros && an.dx_max_cualquier_gesto >= 0.08;  // criterio laxo: la comparación de métodos se hace offline
      else if (paso.tipo === 'noabierta') valida = an.cuadros_con_mano >= 10;
      else valida = an.cuadros_palma_abierta >= 6 && an.dx_max_palma >= 0.15;
      if (valida) { validas[paso.tipo]++; hechas++; }

      const nn = String(k).padStart(2, '0');
      const nombre = `${PREFIJO}${paso.tipo}-${nn}-${valida ? 'ok' : 'x'}.json`;
      const datos = {
        version: 1, ronda: RONDA2 ? 2 : 1, tipo: paso.tipo, intento: k, valida, ya_ms: redondea(yaMs - tGrab, 0), duracion_ms: paso.dur,
        config: resumen.elegida, camara: ajustesCamara,
        esperado: ['gesticulacion', 'noabierta', 'reposo'].includes(paso.tipo) ? { eventos: 0 } : { primer_evento: paso.tipo === 'izquierda' ? 'izquierda' : 'derecha', eventos: 1 },
        analisis: an,
        muestras: rel.map((m) => {
          const o = { t: Math.round(m.t), x: redondea(m.x), y: redondea(m.y), cat: m.cat, s: redondea(m.s, 2) };
          if (RONDA2) { o.h = m.h || null; o.lm = m.lm ? m.lm.map((q) => [redondea(q[0], 3), redondea(q[1], 3), redondea(q[2], 3)]) : null; }
          return o;
        }),
      };
      const r = await post('/guardar', { nombre, datos });
      resumen.trazas.push({ nombre, tipo: paso.tipo, valida, guardada: !!r.ok, analisis: an });

      // Retroalimentación breve
      let msg;
      if (paso.tipo === 'gesticulacion') msg = valida ? `✔ ${an.cuadros_con_mano} cuadros con mano · ${an.pct_palma_abierta}% palma abierta · ${an.eventos_ingenuos.length} disparos "ingenuos"` : '✗ casi no te vi la mano; repetimos';
      else if (paso.tipo === 'noabierta') msg = valida ? `✔ registrado (${an.pct_palma_abierta}% clasificado como palma abierta)` : '✗ no vi la mano; repetimos';
      else msg = valida ? `✔ Δx ${Math.round(an.dx_max_palma * 100)}% en ${an.ms_de_esa_ventana} ms → detectado hacia tu ${an.direccion_presentador}` : `✗ ${an.cuadros_palma_abierta < 6 ? 'no vi la PALMA ABIERTA' : 'movimiento demasiado corto (' + Math.round(an.dx_max_palma * 100) + '%)'}; repetimos`;
      coach(msg, '', ''); beep(valida ? 880 : 300, 150);
      await sleep(PRUEBA ? 200 : RONDA2 ? 1100 : 1800);
    }
    resumen.protocolo[paso.tipo] = { validas: validas[paso.tipo], intentos: intentos[paso.tipo], objetivo };
  }
  activo = false; await fondo;
  $('cont').textContent = contadores(validas);
}

// ── Resumen final y red ─────────────────────────────────────────────────────────────────────────────
function auditaRed() {
  const rt = performance.getEntriesByType('resource').map((r) => { let h = ''; try { h = new URL(r.name).origin; } catch (e) { h = r.name; } return h; });
  const externosRT = rt.filter((o) => o !== location.origin);
  const intentos = window.__red.intentos;
  return {
    peticiones_de_recursos: rt.length,
    recursos_externos: externosRT.length,
    intentos_fetch_xhr_beacon_ws: intentos.length,
    intentos_externos: intentos.filter((i) => i.externa).length,
    violaciones_csp: window.__red.violaciones.length,
    detalle_externos: intentos.filter((i) => i.externa).slice(0, 10),
    detalle_violaciones: window.__red.violaciones.slice(0, 10),
  };
}

function entorno() {
  let gl = null; try { const c = document.createElement('canvas').getContext('webgl2'); const e = c.getExtension('WEBGL_debug_renderer_info'); gl = e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'sin info'; } catch (e) { gl = 'error'; }
  return { userAgent: navigator.userAgent, nucleos: navigator.hardwareConcurrency, webgl_renderer: gl, carga_modelo_ms: cargaMs, errores_delegados: errores, camara_final: ajustesCamara };
}

async function finalizar() {
  resumen.red = auditaRed(); resumen.entorno = entorno(); resumen.fin = new Date().toISOString();
  await post('/guardar', { nombre: RONDA2 ? 'r2-resumen.json' : '_resumen.json', datos: resumen });
  await post('/fin', { prefijo: RONDA2 ? 'r2' : '' });
  if (stream) stream.getTracks().forEach((t) => t.stop());
  document.body.className = ''; beep(880, 300);
  coach('Listo ✔  Gracias', 'Ya guardé todo. Puedes volver a la laptop.', '');
  $('vista').style.display = 'none'; $('live').style.display = 'none';
  const c = resumen.configs.filter((x) => !x.omitida).map((x) => `${x.delegado} ${x.resolucion}: ${x.fps_medio} fps (mín/seg ${x.fps_min_por_seg}) · inferencia ${x.infer_ms_medio} ms · latencia p95 ${x.latencia_ms_p95} ms`).join('\n');
  $('cont').textContent = `${c}\n\nRed: ${resumen.red.intentos_externos} intentos externos · ${resumen.red.violaciones_csp} bloqueos CSP · ${resumen.red.recursos_externos} recursos externos\nElegida: ${resumen.elegida ? resumen.elegida.delegado + ' ' + resumen.elegida.resolucion : 'ninguna'}`;
}

// ── Arranque ────────────────────────────────────────────────────────────────────────────────────────
async function cargarMediaPipe() {
  coach('Cargando MediaPipe…', 'Modelo y WASM desde /vendor/ (sin internet).');
  vision = await FilesetResolver.forVisionTasks('/vendor/tasks-vision/wasm');
  for (const delegate of ['GPU', 'CPU']) {
    const t0 = performance.now();
    try {
      reconocedores[delegate] = await GestureRecognizer.createFromOptions(vision, {
        baseOptions: { modelAssetPath: '/vendor/models/gesture_recognizer.task', delegate },
        runningMode: 'VIDEO', numHands: 1,
      });
      cargaMs[delegate] = Math.round(performance.now() - t0);
    } catch (e) { errores[delegate] = String(e && e.message || e).slice(0, 300); }
  }
}

async function iniciar() {
  try {
    ac = new (window.AudioContext || window.webkitAudioContext)(); ac.resume().catch(() => {}); beep(660, 120);
    await cargarMediaPipe();
    if (!Object.keys(reconocedores).length) throw new Error('Ningún delegado (GPU/CPU) cargó: ' + JSON.stringify(errores));
    coach('Permiso de cámara', 'Acepta el permiso de cámara en Chrome si te lo pide.');
    await abrirCamara(640, 480);
    coach('Todo cargado ✔', `Modelo cargado (${Object.entries(cargaMs).map(([k, v]) => k + ' ' + v + ' ms').join(', ')}).`);
    const espera = PRUEBA ? 2 : RONDA2 ? 15 : 20;
    for (let s = espera; s > 0 && !abortar; s--) {
      coach('Aléjate a tu posición de presentar', 'De pie, a la distancia real de la presentación, con la luz de siempre. El benchmark y la grabación empiezan solos. (ESPACIO = pausa · ESC = cancelar)', String(s));
      await sleep(1000);
    }
    if (abortar) return finalizar();
    if (RONDA2) resumen.elegida = { delegado: reconocedores.GPU ? 'GPU' : 'CPU', resolucion: '640x480' };
    else await benchmark();
    if (!resumen.elegida) throw new Error('Ninguna configuración produjo mediciones.');
    await abrirCamara(...resumen.elegida.resolucion.split('x').map(Number));
    coach('Ahora las grabaciones', `Usaré ${resumen.elegida.delegado} ${resumen.elegida.resolucion}. Sigue las instrucciones en pantalla: oirás una cuenta atrás y un tono largo.`, '');
    await sleep(PRUEBA ? 500 : 4000);
    await protocolo(reconocedores[resumen.elegida.delegado]);
    await finalizar();
  } catch (e) {
    console.error(e);
    resumen.error = String(e && e.message || e);
    coach('Error en el spike', resumen.error, '');
    await finalizar().catch(() => {});
  }
}

addEventListener('keydown', (e) => {
  if (e.code === 'Space') {
    e.preventDefault();
    if (!ac) { $('cont').textContent = ''; iniciar(); } else { pausado = !pausado; }
  }
  if (e.code === 'Escape') abortar = true;
});
coach(RONDA2 ? 'Spike de gestos — RONDA 2 (640×480)' : 'Spike de gestos (T06)', RONDA2 ? 'Pulsa ESPACIO para empezar. Cargar → permiso de cámara → te alejas (15 s) → 32 grabaciones guiadas (~10 min). Sin benchmark: 640×480 fijo.' : 'Pulsa ESPACIO para empezar. Pasos: cargar → permiso de cámara → te alejas → benchmark (~50 s) → 31 grabaciones guiadas (~6 min).');
$('cont').textContent = PRUEBA ? 'MODO PRUEBA (?prueba=1): tiempos cortos, sin exigir mano.' : '';
if (PRUEBA) setTimeout(() => { if (!ac) iniciar(); }, 300);
