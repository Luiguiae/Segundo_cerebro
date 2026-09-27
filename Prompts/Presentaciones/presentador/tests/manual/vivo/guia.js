// Guía en pantalla para las pruebas en vivo (T13–T15). SOLO desarrollo. La carga servir_vivo.py tras el presentador.
// Da instrucciones grandes, emite tonos y verifica cada paso con los eventos reales de `Presentador`.
// Los guiones viven en guion_<nombre>.js y definen: { titulo, pasos: [...] } (ver guion_voz.js).
(function () {
  'use strict';
  const GUION = window.GUION_VIVO, VARIANTE = window.GUION_VARIANTE || '';
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const post = (ruta, cuerpo) => fetch(ruta, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(cuerpo) }).catch(() => {});
  const log = (linea) => { console.info('[guia]', linea); post('/__guia/evento', { linea }); };
  const G = window.__guia = { guion: GUION, paso: null, buf: [], resultados: [], fin: false, listo: false };

  // ── audio ──
  let ac = null;
  function beep(freq = 660, ms = 110, vol = 0.25) {
    if (!ac) return;
    const o = ac.createOscillator(), g = ac.createGain();
    o.frequency.value = freq; g.gain.value = vol; o.connect(g); g.connect(ac.destination); o.start(); o.stop(ac.currentTime + ms / 1000);
  }

  // ── UI ──
  const host = document.createElement('div');
  host.style.cssText = 'all:initial;position:fixed;left:2vw;top:2vh;width:62vw;z-index:2147483646;pointer-events:none;';
  const sr = host.attachShadow({ mode: 'open' });
  sr.innerHTML = `<style>
    .p{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif;color:#fff;background:rgba(8,10,14,.86);border-radius:18px;padding:1.6vw 2vw}
    .t{font-size:3.6vw;font-weight:800;line-height:1.1;letter-spacing:-.02em}.s{font-size:1.7vw;line-height:1.35;color:#c5ccd6;margin-top:.7vw}
    .c{font-size:1.5vw;color:#ffd166;margin-top:.8vw}.ok{color:#7ee787}.mal{color:#ff8a8a}.n{font-size:6vw;font-weight:900;color:#ffd166;line-height:1}
    .b{height:.6vw;background:#2a2f37;border-radius:9px;margin-top:1vw;overflow:hidden}.b>i{display:block;height:100%;background:#ffd166;width:0}
  </style><div class="p"><div class="t" id="t"></div><div class="s" id="s"></div><div class="n" id="n"></div><div class="b"><i id="b"></i></div><div class="c" id="c"></div></div>`;
  document.documentElement.appendChild(host);
  const $ = (id) => sr.getElementById(id);
  const mostrar = (t, s = '', n = '', cls = '') => { $('t').textContent = t; $('t').className = 't ' + cls; $('s').textContent = s; $('n').textContent = n; };
  const barra = (f) => { $('b').style.width = Math.max(0, Math.min(1, f)) * 100 + '%'; };

  // ── observación ──
  const idx = () => { const i = Reveal.getIndices(); return { h: i.h, f: i.f === undefined ? -1 : i.f }; };
  const cooldownRestante = () => Math.max(0, 1600 - (performance.now() - (window.Presentador.estado().ultimoCambioMs || -1e9)));
  function esperar(cond, timeoutMs, alTick) {
    return new Promise((resolver) => {
      const t0 = performance.now();
      (function tick() {
        const r = cond();
        if (r) return resolver(r);
        const dt = performance.now() - t0;
        if (alTick) alTick(dt);
        if (dt >= timeoutMs) return resolver(null);
        setTimeout(tick, 50);
      })();
    });
  }
  const ejecutados = () => G.buf.filter((e) => e.tipo === 'comando' && e.ejecutado);

  async function correrPaso(p, i, n, resumenTxt) {
    G.buf = [];
    if (p.preparar) { Reveal.slide(p.preparar.h, 0, p.preparar.f === undefined ? -1 : p.preparar.f); await sleep(300); }
    if (p.antes) await p.antes();
    mostrar('Un momento…', p.titulo, '');
    // dejar pasar el cooldown del cambio de preparación para que la primera orden no se descarte
    await sleep(cooldownRestante() + 250);
    G.buf = [];
    const ini = idx(); const t0 = performance.now();
    G.paso = { id: p.id, tipo: p.tipo, titulo: p.titulo, dry: p.dry, ini, t0 };
    beep(520, 90);
    mostrar(p.titulo, p.ayuda || '', '', '');
    $('c').textContent = `Paso ${i + 1}/${n}  ·  ${resumenTxt()}`;
    const tim = p.timeout || p.ventanaMs || 12000;
    const alTick = (dt) => { barra(dt / tim); };
    let ok = false, obs = '', extra = {};

    if (p.tipo === 'cambio' || p.tipo === 'uno') {
      const c = await esperar(() => ejecutados()[0] || null, tim, alTick);
      if (!c) { obs = 'no reaccionó en ' + Math.round(tim / 1000) + ' s'; }
      else {
        await sleep(1700);                                   // ventana para detectar un doble disparo
        const todos = ejecutados(); const fin = idx();
        const canalOk = !p.canal || todos[0].canal === p.canal;
        const esp = p.esperado ? p.esperado(ini, fin, todos[0]) : true;
        if (todos.length > 1) obs = `doble disparo (${todos.length} acciones)`;
        else if (!canalOk) obs = 'canal inesperado: ' + todos[0].canal;
        else if (!esp) obs = `resultado inesperado: ${JSON.stringify(ini)} → ${JSON.stringify(fin)}`;
        else { ok = true; obs = `${todos[0].texto} (${Math.round(todos[0].t - t0)} ms tras el aviso)`; }
        extra = { latencia_desde_aviso_ms: Math.round(todos[0].t - t0), n_acciones: todos.length };
      }
    } else if (p.tipo === 'nada') {
      await esperar(() => ejecutados()[0] || null, tim, alTick);
      const d = ejecutados();
      ok = d.length === 0 && JSON.stringify(idx()) === JSON.stringify(ini);
      obs = ok ? 'sin cambios (correcto)' : `cambió sin querer: ${d.map((e) => e.texto).join(', ')}`;
    } else if (p.tipo === 'espera') {
      await esperar(() => false, tim, (dt) => { barra(dt / tim); $('n').textContent = Math.ceil((tim - dt) / 1000); });
      ok = true; obs = 'ok';
    } else if (p.tipo === 'info') {
      await esperar(() => false, tim, (dt) => { barra(dt / tim); $('n').textContent = Math.ceil((tim - dt) / 1000); });
      ok = true; obs = `informativo: ${ejecutados().length} cambios`; extra = { cambios: ejecutados().map((e) => e.texto) };
    } else if (p.tipo === 'condicion') {
      const r = await esperar(() => { try { return p.cond(); } catch (e) { return false; } }, tim, (dt) => { barra(dt / tim); $('n').textContent = Math.ceil((tim - dt) / 1000); });
      ok = !!r; obs = ok ? (p.obsOk || 'ok') : (p.obsMal || 'no se cumplió a tiempo');
    }
    const trans = G.buf.filter((e) => e.tipo === 'transcripcion' && e.final).map((e) => e.texto);
    const r = { id: p.id, titulo: p.titulo, tipo: p.tipo, ok: p.tipo === 'info' || p.tipo === 'espera' ? null : ok, obs, transcripciones: trans, ...extra };
    G.resultados.push(r); G.paso = null;
    beep(ok ? 880 : 280, 160);
    mostrar((ok ? '✔ ' : '✗ ') + (p.tipo === 'espera' ? 'Listo' : obs), trans.length ? 'Chrome entendió: “' + trans.join('” · “') + '”' : '', '', ok ? 'ok' : 'mal');
    barra(0);
    log(`${p.id} ${ok ? 'OK' : 'FALLA'} — ${obs}${trans.length ? ' · oyó: ' + trans.join(' | ') : ''}`);
    await sleep(p.pausaTrasMs || 1400);
    return r;
  }

  async function principal() {
    const cargar = await new Promise((res) => { const s = document.createElement('script'); s.src = `/__guia/guion_${GUION}.js`; s.onload = () => res(true); s.onerror = () => res(false); document.head.appendChild(s); });
    const def = window.__GUIONES && window.__GUIONES[GUION];
    if (!cargar || !def) { mostrar('No encontré el guion ' + GUION, ''); return; }
    await esperar(() => window.Presentador && window.Presentador.estado().reveal !== 'esperando', 30000);
    window.Presentador.alEvento((e) => G.buf.push(e));
    for (const n of (def.activar || [])) if (!window.Presentador.control()[n]) window.Presentador.alternar(n);   // p. ej. gestos, que están apagados por defecto
    const pasos = typeof def.pasos === 'function' ? def.pasos(VARIANTE) : def.pasos;
    G.listo = true;
    mostrar(def.titulo, def.intro || 'Pulsa ESPACIO para empezar.', '', '');
    const iniciar = () => { if (!ac) { ac = new (window.AudioContext || window.webkitAudioContext)(); ac.resume().catch(() => {}); } };
    await new Promise((res) => {
      const f = (e) => { if (e.code === 'Space' || window.__guiaDry) { removeEventListener('keydown', f); iniciar(); res(); } };
      addEventListener('keydown', f);
      if (new URLSearchParams(location.search).has('auto')) { window.__guiaDry = true; res(); }
    });
    beep(660, 120);
    log(`INICIO guion ${GUION}${VARIANTE ? ' (' + VARIANTE + ')' : ''}`);
    const t_ini = new Date().toISOString();
    const resumenTxt = () => { const v = G.resultados.filter((r) => r.ok !== null); return `✔ ${v.filter((r) => r.ok).length}  ✗ ${v.filter((r) => !r.ok).length}`; };
    for (let i = 0; i < pasos.length; i++) await correrPaso(pasos[i], i, pasos.length, resumenTxt);
    const v = G.resultados.filter((r) => r.ok !== null);
    const resumen = { total: v.length, ok: v.filter((r) => r.ok).length, fallos: v.filter((r) => !r.ok).length };
    const salida = { guion: GUION, variante: VARIANTE, inicio: t_ini, fin: new Date().toISOString(), resumen, estadisticas: window.Presentador.estadisticas(),
      motores: window.Presentador.motores(), bloqueadas: window.Presentador.bloqueadas(), userAgent: navigator.userAgent, pasos: G.resultados };
    await post('/__guia/resultado', salida);
    G.fin = true; G.salida = salida;
    beep(880, 300);
    mostrar(`Listo — ${resumen.ok}/${resumen.total} pasos correctos`, def.cierre || 'Ya guardé todo. Puedes volver a la laptop.', '', resumen.fallos ? 'mal' : 'ok');
    log(`FIN — ${resumen.ok}/${resumen.total} OK`);
  }
  principal().catch((e) => { console.error(e); mostrar('Error en la guía', String(e && e.message || e)); log('ERROR ' + (e && e.message || e)); });
})();
