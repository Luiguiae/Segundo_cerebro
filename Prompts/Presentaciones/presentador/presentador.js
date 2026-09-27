// presentador.js — presentador por gestos y voz para decks Reveal.js (se inyecta al servir; ver presentar.py).
// T11: bloqueo de telemetría, espera a Reveal, navegación con la semántica del SPEC y cooldown compartido.
// T14: gestos (MediaPipe GestureRecognizer + detector v2 de swipe.js).
// T13: voz (Web Speech API + parser de comandos.js).
// T12: teclas M (gestos) / E (voz) / I (indicador) e indicador en pantalla. `V` es la pausa de Reveal y `G`/`H` también
//      chocan con atajos suyos (ver SPEC, revisión 2026-09-26), por eso M/E/I.
//
// Semántica de navegación (SPEC §4):
//   paso   → Reveal.next() / prev()         (respeta fragments)
//   salto  → Reveal.slide(h ± N, 0)         (N slides horizontales completos; tope en el primero / último)
//   inicio → Reveal.slide(0, 0)
// Cooldown compartido: tras CUALQUIER cambio de slide o fragment (voz, gesto, teclado, clicker) se ignora todo
// comando de voz o gesto durante 1500 ms. Las teclas nativas de Reveal nunca se bloquean.
(function () {
  'use strict';
  if (window.Presentador) return; // idempotente: una sola instancia por página

  const CONFIG = Object.assign({ debug: false }, window.PRESENTADOR_CONFIG || {});
  const COOLDOWN_MS = 1500;
  const ESPERA_REVEAL_MS = 15000;
  const HOSTS_BLOQUEADOS = ['odml.pa.googleapis.com'];

  const estado = {
    reveal: 'esperando',            // 'esperando' | 'listo' | 'sin-reveal'
    ultimoCambioMs: -Infinity,      // performance.now() del último cambio de slide o fragment, venga de donde venga
    ultimoComando: null,            // { texto, canal, h, total }
    bloqueadas: [],                 // peticiones de telemetría bloqueadas
    // Lo que Luigui quiere (M, E, I); los motores (T13/T14) reportan lo que pasa. GESTOS APAGADOS POR DEFECTO: el swipe es
    // experimental en v1 (2 disparos inversos en 10 swipes a la izquierda en la prueba en vivo de T14; plan.md §13–14). Se activan con M.
    control: { gestos: false, voz: true, indicador: true },
    debugTexto: '',                 // última transcripción cruda (solo con --debug)
    debugGestos: '',                // estado de la mano (solo con --debug)
  };
  const motores = {};               // { gestos, voz } → { iniciar(), detener(), estado() → { estado, detalle } }
  let reveal = null;
  const suscriptores = [];          // callbacks para "cambió el slide": f(t, origen) (p. ej. swipe.notificarCambio en T14)
  const oyentes = [];               // bus de eventos (comandos, transcripciones…): f(evento) — lo usan las guías de prueba y T17
  let origenActual = null;          // canal que está moviendo Reveal en este instante ('voz' | 'gesto' | 'consola'), null si es teclado/clicker/otro
  const contadores = { voz: { acciones: 0, reinicios: 0, errores: 0 }, gestos: { acciones: 0 } };
  function emitir(ev) { ev.t = Math.round(performance.now()); for (const f of oyentes) { try { f(ev); } catch (e) { console.warn('[presentador] oyente:', e); } } }

  // ── 1. Bloqueo de telemetría ────────────────────────────────────────────────────────────────────
  // MediaPipe Tasks Vision 1.0.1 crea SIEMPRE un registrador de uso que envía métricas a Google cada 60 s
  // (POST protobuf a odml.pa.googleapis.com/v1/log; sin opción para desactivarlo). Se bloquea aquí, ANTES
  // de que se cargue MediaPipe. El registrador se apaga solo tras el primer fallo. (plan.md §9–10)
  function esBloqueada(url) {
    try { return HOSTS_BLOQUEADOS.includes(new URL(String(url), location.href).hostname); } catch (e) { return false; }
  }
  function registrarBloqueo(tipo, url) {
    estado.bloqueadas.push({ tipo, url: String(url).slice(0, 120), t: Math.round(performance.now()) });
    if (CONFIG.debug) console.info('[presentador] telemetría bloqueada:', tipo, url);
  }
  (function instalarBloqueoTelemetria() {
    try {
      const fetchOriginal = window.fetch;
      if (typeof fetchOriginal === 'function') {
        window.fetch = function (entrada) {
          const url = entrada && typeof entrada === 'object' && 'url' in entrada ? entrada.url : entrada;
          if (esBloqueada(url)) { registrarBloqueo('fetch', url); return Promise.reject(new TypeError('Failed to fetch (bloqueado por el presentador)')); }
          return fetchOriginal.apply(this, arguments);
        };
      }
      const open = XMLHttpRequest.prototype.open, send = XMLHttpRequest.prototype.send;
      XMLHttpRequest.prototype.open = function (metodo, url) {
        this.__presentadorBloqueada = esBloqueada(url);
        if (this.__presentadorBloqueada) registrarBloqueo('xhr', url);
        return open.apply(this, arguments);
      };
      XMLHttpRequest.prototype.send = function () {
        if (this.__presentadorBloqueada) { setTimeout(() => this.dispatchEvent(new ProgressEvent('error')), 0); return; }
        return send.apply(this, arguments);
      };
      if (typeof navigator.sendBeacon === 'function') {
        const beacon = navigator.sendBeacon.bind(navigator);
        navigator.sendBeacon = function (url, datos) {
          if (esBloqueada(url)) { registrarBloqueo('beacon', url); return false; }
          return beacon(url, datos);
        };
      }
    } catch (e) { console.warn('[presentador] no se pudo instalar el bloqueo de telemetría:', e); }
  })();

  // ── 2. Indicador en pantalla ─────────────────────────────────────────────────────────────────────
  // Shadow DOM (no lo afecta el CSS del deck), position:fixed en una esquina, pointer-events:none y colgado de
  // <html>, fuera del flujo del deck: no altera su layout ni bloquea clics. Se oculta/muestra con la tecla I.
  let host = null, raizSombra = null, avisoTexto = '';
  const CSS = ':host{all:initial}.caja{font:12px/1.45 -apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif;color:#e8eaed;' +
    'background:rgba(20,22,26,.80);padding:6px 10px;border-radius:8px;min-width:150px;max-width:280px}' +
    '.k{color:#9aa4b2}.on{color:#7ee787}.off{color:#8a93a0}.err{color:#ffb4a9}.ult{margin-top:3px;color:#ffd166}.dbg{margin-top:3px;color:#9aa4b2;font-size:11px}.av{color:#ffd166;margin-bottom:3px}';
  function sombra() {
    if (raizSombra) return raizSombra;
    host = document.createElement('div');
    host.id = 'presentador-indicador';
    host.style.cssText = 'all:initial;position:fixed;right:10px;bottom:10px;z-index:2147483647;pointer-events:none;';
    raizSombra = host.attachShadow({ mode: 'open' });
    raizSombra.innerHTML = `<style>${CSS}</style><div class="caja" id="caja"></div>`;
    (document.documentElement || document.body).appendChild(host);
    return raizSombra;
  }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function linea(nombre, etiqueta, tecla) {
    const quiere = estado.control[nombre];
    const m = motores[nombre];
    let clase = 'off', txt;
    if (!quiere) txt = 'apagado';
    else if (!m) txt = '—';
    else {
      const e = m.estado ? m.estado() : { estado: 'activo' };
      if (e.estado === 'activo') { clase = 'on'; txt = e.detalle || 'activo'; }
      else if (e.estado === 'error') { clase = 'err'; txt = e.detalle || 'error'; }
      else txt = e.detalle || 'iniciando…';
    }
    return `<span class="k">${etiqueta} (${tecla})</span> <span class="${clase}">${esc(txt)}</span>`;
  }
  function dibujar() {
    try {
      const caja = sombra().getElementById('caja');
      host.style.display = estado.control.indicador ? '' : 'none';
      const partes = [];
      if (avisoTexto) partes.push(`<div class="av">${esc(avisoTexto)}</div>`);
      partes.push(`<div>${linea('gestos', 'Cámara', 'M')}</div>`, `<div>${linea('voz', 'Micrófono', 'E')}</div>`);
      if (estado.ultimoComando) partes.push(`<div class="ult">${esc(estado.ultimoComando.texto)} <span class="k">${esc(estado.ultimoComando.canal)}</span></div>`);
      if (CONFIG.debug && estado.debugTexto) partes.push(`<div class="dbg">oyó: “${esc(estado.debugTexto)}”</div>`);
      if (CONFIG.debug && estado.debugGestos) partes.push(`<div class="dbg">${esc(estado.debugGestos)}</div>`);
      caja.innerHTML = partes.join('');
    } catch (e) { /* sin UI no pasa nada: la presentación sigue */ }
  }
  function aviso(texto) {
    avisoTexto = texto; dibujar();
    if (CONFIG.debug) console.info('[presentador]', texto);
  }

  // ── Control (teclas M / E / I) y motores ─────────────────────────────────────────────────────────
  // Un motor (voz en T13, gestos en T14) se registra con { iniciar(), detener(), estado() }.
  function registrarMotor(nombre, motor) {
    motores[nombre] = motor;
    if (estado.control[nombre] && reveal && typeof motor.iniciar === 'function') Promise.resolve().then(() => motor.iniciar()).catch((e) => console.warn('[presentador] motor', nombre, e));
    dibujar();
  }
  function alternar(nombre) {
    if (!(nombre in estado.control)) return null;
    estado.control[nombre] = !estado.control[nombre];
    const m = motores[nombre];
    if (m && nombre !== 'indicador') {
      try {
        if (estado.control[nombre]) { if (typeof m.iniciar === 'function') Promise.resolve(m.iniciar()).catch((e) => console.warn('[presentador]', nombre, e)); }
        else if (typeof m.detener === 'function') m.detener();
      } catch (e) { console.warn('[presentador]', nombre, e); }
    }
    dibujar();
    return estado.control[nombre];
  }
  const TECLAS = { KeyM: 'gestos', KeyE: 'voz', KeyI: 'indicador' };
  function esCampoDeTexto(el) {
    if (!el) return false;
    const tag = (el.tagName || '').toUpperCase();
    return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || el.isContentEditable === true;
  }
  window.addEventListener('keydown', (e) => {
    if (e.repeat || e.ctrlKey || e.metaKey || e.altKey || e.shiftKey) return;   // ni combinaciones ni autorrepetición
    const que = TECLAS[e.code];
    if (!que || esCampoDeTexto(e.target)) return;
    alternar(que);                                   // no se cancela el evento: M/E/I no son teclas de Reveal
  });
  setInterval(dibujar, 1000);                         // refleja el estado de los motores sin que tengan que avisar

  // ── 3. Espera a Reveal ───────────────────────────────────────────────────────────────────────────
  // Reveal puede inicializarse antes o después de este script, y si el deck lo carga como módulo ESM no hay
  // window.Reveal. Se comprueba isReady() Y el evento ready (que pudo haber ocurrido ya), con tiempo límite.
  function esperarReveal() {
    return new Promise((resolver) => {
      let hecho = false, enganchado = false;
      const t0 = Date.now();
      const fin = (R) => { if (!hecho) { hecho = true; resolver(R); } };
      (function sondear() {
        const R = window.Reveal;
        if (R && typeof R.isReady === 'function') {
          if (R.isReady()) return fin(R);
          if (!enganchado && typeof R.on === 'function') { enganchado = true; R.on('ready', () => fin(R)); }
        }
        if (Date.now() - t0 > ESPERA_REVEAL_MS) return fin(null);
        setTimeout(sondear, 100);
      })();
    });
  }

  // ── 4. Navegación ────────────────────────────────────────────────────────────────────────────────
  const firma = (R) => { const i = R.getIndices(); return `${i.h}/${i.v}/${i.f === undefined ? '' : i.f}`; };
  const tope = (n, a, b) => Math.max(a, Math.min(b, n));
  const menos = (n) => (n < 0 ? '−' + Math.abs(n) : '+' + n);

  // Texto del último comando para el indicador: `→ 4/12` (paso), `+3 → 7/12` (salto), `inicio → 1/12`.
  function textoComando(cmd, h, total) {
    if (cmd.accion === 'paso') return `${cmd.delta > 0 ? '→' : '←'} ${h}/${total}`;
    if (cmd.accion === 'salto') return `${menos(cmd.delta)} → ${h}/${total}`;
    return `inicio → ${h}/${total}`;
  }

  // cmd: { accion: 'paso'|'salto'|'inicio', delta } · canal: 'voz' | 'gesto' | 'consola'
  // Devuelve { cambio, motivo?, texto?, h?, total? }
  function navegar(cmd, canal) {
    const R = reveal;
    if (!R) return { cambio: false, motivo: 'sin-reveal' };
    if (!cmd || !['paso', 'salto', 'inicio'].includes(cmd.accion)) return { cambio: false, motivo: 'accion-desconocida' };
    const ahora = performance.now();
    const base = { tipo: 'comando', canal: canal || 'consola', accion: cmd.accion, delta: cmd.delta };
    if (ahora - estado.ultimoCambioMs < COOLDOWN_MS) { emitir({ ...base, ejecutado: false, motivo: 'cooldown' }); return { cambio: false, motivo: 'cooldown' }; }

    const antes = firma(R);
    origenActual = canal || 'consola';
    try {
      if (cmd.accion === 'paso') { if (cmd.delta > 0) R.next(); else R.prev(); }
      else if (cmd.accion === 'salto') {
        const n = R.getHorizontalSlides().length;
        R.slide(tope(R.getIndices().h + cmd.delta, 0, n - 1), 0);
      } else R.slide(0, 0);
    } finally { origenActual = null; }

    if (firma(R) === antes) { emitir({ ...base, ejecutado: false, motivo: 'sin-cambio' }); return { cambio: false, motivo: 'sin-cambio' }; } // p. ej. "siguiente" en el último slide
    const total = R.getHorizontalSlides().length, h = R.getIndices().h;
    const texto = textoComando(cmd, h + 1, total);
    estado.ultimoComando = { texto, canal: canal || 'consola', h: h + 1, total };
    marcarCambio(canal || 'consola'); // por si el evento de Reveal llega después
    dibujar();
    emitir({ ...base, ejecutado: true, texto, h: h + 1, total });
    return { cambio: true, texto, h: h + 1, total };
  }

  function marcarCambio(origen) {
    estado.ultimoCambioMs = performance.now();
    const o = typeof origen === 'string' ? origen : (origenActual || 'otro'); // 'otro' = teclado, clicker…
    for (const f of suscriptores) { try { f(estado.ultimoCambioMs, o); } catch (e) { console.warn('[presentador] suscriptor:', e); } }
  }

  // ── 5. Arranque ──────────────────────────────────────────────────────────────────────────────────
  dibujar();
  esperarReveal().then((R) => {
    if (!R) {
      estado.reveal = 'sin-reveal';
      aviso('Presentador: esta página no usa Reveal.js — inactivo');
      return;
    }
    reveal = R;
    estado.reveal = 'listo';
    // Cooldown compartido con cualquier canal (teclado y clicker incluidos); sus teclas NUNCA se bloquean.
    for (const ev of ['slidechanged', 'fragmentshown', 'fragmenthidden']) R.on(ev, () => marcarCambio());
    estado.ultimoCambioMs = -Infinity; // el cambio inicial de Reveal al arrancar no cuenta
    if (CONFIG.debug) console.info('[presentador] Reveal listo');
    for (const [nombre, m] of Object.entries(motores)) if (estado.control[nombre] && typeof m.iniciar === 'function') Promise.resolve(m.iniciar()).catch((e) => console.warn('[presentador]', nombre, e));
    dibujar();
  }).catch((e) => { estado.reveal = 'error'; aviso('Presentador: error al iniciar (' + (e && e.message || e) + ')'); });

  // ── 6. Voz (T13) ─────────────────────────────────────────────────────────────────────────────────
  // Web Speech API de Chrome (continuous + interimResults) + parser de comandos.js (probado en tests/comandos.test.js).
  //  · Un mismo enunciado dispara UNA acción: cada resultado se identifica por su índice y, al dispararse, ese índice
  //    queda consumido (sus siguientes actualizaciones, incluido el resultado final, se ignoran).
  //  · D5: "avanza" puede ser el inicio de "avanza 3": esos interinos esperan ~500 ms de texto estable (o el final).
  //  · Chrome corta el reconocimiento continuo tras silencios: se reinicia solo en onend/onerror, con espera creciente
  //    si el error persiste (red); 'not-allowed' y 'service-not-allowed' son permanentes (no se reintenta).
  const motorVoz = (function () {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    const LANG = CONFIG.lang || 'es-PE';
    const ESTABLE_MS = 500;
    let rec = null, activo = false, permanente = false, reinicio = null;
    let fallos = 0, inicioSesion = 0, huboError = false, ultimoError = '';
    let consumidos = new Set(), pendientes = new Map(); // índice → { texto, timer }
    let st = { estado: 'inactivo', detalle: '' };
    const fijar = (e, d) => { st = { estado: e, detalle: d }; dibujar(); };

    function limpiarPendientes() { for (const p of pendientes.values()) clearTimeout(p.timer); pendientes.clear(); }

    function ejecutar(r, texto, indice) {
      consumidos.add(indice);
      const p = pendientes.get(indice); if (p) { clearTimeout(p.timer); pendientes.delete(indice); }
      contadores.voz.acciones++;
      emitir({ tipo: 'voz-comando', texto, indice, accion: r.accion, delta: r.delta, conPrefijo: r.conPrefijo });
      navegar({ accion: r.accion, delta: r.delta }, 'voz');
    }

    function alResultado(e) {
      fallos = 0;
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const res = e.results[i];
        const texto = (res[0] && res[0].transcript) || '';
        const esFinal = !!res.isFinal;
        estado.debugTexto = texto + (esFinal ? '' : ' …');
        emitir({ tipo: 'transcripcion', texto, final: esFinal, indice: i });
        if (consumidos.has(i)) continue;
        const r = window.Comandos.interpretar(texto, esFinal);
        if (!r) { const p = pendientes.get(i); if (p) { clearTimeout(p.timer); pendientes.delete(i); } continue; }
        if (r.definitivo) { ejecutar(r, texto, i); continue; }
        // interino ambiguo (D5): esperar a que el texto se estabilice; el resultado final lo resuelve antes
        const previo = pendientes.get(i); if (previo) clearTimeout(previo.timer);
        pendientes.set(i, { texto, timer: setTimeout(() => {
          if (consumidos.has(i)) return;
          const r2 = window.Comandos.interpretar(texto, false);
          if (r2) ejecutar(r2, texto, i);
        }, ESTABLE_MS) });
      }
      dibujar();
    }

    function programar(ms) {
      clearTimeout(reinicio);
      reinicio = setTimeout(arrancar, ms);
    }

    function arrancar() {
      if (!activo || permanente) return;
      try {
        rec = new SR();
        rec.lang = LANG; rec.continuous = true; rec.interimResults = true; rec.maxAlternatives = 1;
        rec.onstart = () => { consumidos.clear(); limpiarPendientes(); inicioSesion = Date.now(); huboError = false; fijar('iniciando', 'conectando…'); };
        rec.onaudiostart = () => fijar('activo', 'escuchando');
        rec.onresult = alResultado;
        rec.onerror = (e) => {
          huboError = true; ultimoError = e.error; contadores.voz.errores++;
          emitir({ tipo: 'voz-error', error: e.error });
          if (e.error === 'not-allowed' || e.error === 'service-not-allowed') { permanente = true; fijar('error', 'sin permiso de micrófono'); }
          else if (e.error === 'network') { fallos++; fijar('error', 'sin internet — reintentando'); }
          else if (e.error === 'audio-capture') { fallos++; fijar('error', 'sin micrófono'); }
          else if (e.error !== 'no-speech' && e.error !== 'aborted') { fallos++; fijar('error', 'error: ' + e.error); }
        };
        rec.onend = () => {
          limpiarPendientes();
          if (!activo || permanente) return;
          contadores.voz.reinicios++;
          const benigno = !huboError || ultimoError === 'no-speech' || ultimoError === 'aborted';
          if (benigno && Date.now() - inicioSesion > 3000) fallos = 0;
          programar(benigno ? 200 : Math.min(5000, 300 * 2 ** Math.min(fallos, 5)));
        };
        rec.start();
      } catch (e) { fallos++; fijar('error', 'no arranca: ' + (e && e.message || e)); programar(Math.min(5000, 300 * 2 ** Math.min(fallos, 5))); }
    }

    return {
      iniciar() {
        if (activo) return;
        if (!SR) { fijar('error', 'este Chrome no tiene reconocimiento de voz'); return; }
        if (!window.Comandos) { fijar('error', 'falta comandos.js'); return; }
        activo = true; permanente = false; fallos = 0; fijar('iniciando', 'conectando…'); arrancar();
      },
      detener() {
        activo = false; clearTimeout(reinicio); limpiarPendientes();
        try { if (rec) { rec.onend = null; rec.abort(); } } catch (e) { /* ya estaba parado */ }
        fijar('inactivo', 'apagado');
      },
      estado: () => st,
    };
  })();

  // ── 7. Gestos (T14) ──────────────────────────────────────────────────────────────────────────────
  // MediaPipe Tasks Vision GestureRecognizer (JS/WASM, desde /vendor/, sin CDN) → centro de palma + categoría →
  // detector v2 de swipe.js. Cámara 640×480. El swipe es un canal SECUNDARIO en v1 (plan.md §12): voz y teclado cubren
  // los fallos, y ante conflicto gana 0 falsos positivos. La telemetría de MediaPipe ya está bloqueada (sección 1).
  const motorGestos = (function () {
    const CENTRO_PALMA = [0, 5, 9, 13, 17];   // muñeca + base de los 4 dedos
    let activo = false, cargando = null, recognizer = null, delegado = '';
    let stream = null, video = null, vfc = null, ultimoTs = 0, det = null;
    let st = { estado: 'inactivo', detalle: '' };
    let cuadros = 0, t0Cuadros = 0, fps = 0, fallosInferencia = 0, ultimoDebug = 0;
    const fijar = (e, d) => { st = { estado: e, detalle: d }; dibujar(); };

    async function cargarModelo() {
      if (recognizer) return recognizer;
      if (!cargando) {
        cargando = (async () => {
          const mod = await import('/vendor/tasks-vision/vision_bundle.mjs');
          const vision = await mod.FilesetResolver.forVisionTasks('/vendor/tasks-vision/wasm');
          let ultimo = null;
          for (const d of ['GPU', 'CPU']) {
            try {
              recognizer = await mod.GestureRecognizer.createFromOptions(vision, {
                baseOptions: { modelAssetPath: '/vendor/models/gesture_recognizer.task', delegate: d }, runningMode: 'VIDEO', numHands: 1 });
              delegado = d; return recognizer;
            } catch (e) { ultimo = e; }
          }
          throw ultimo;
        })().catch((e) => { cargando = null; throw e; });
      }
      return cargando;
    }

    // Una muestra por cuadro: { t, x, y, categoria } (x, y = centro de palma normalizado, cuadro SIN espejar).
    function alMuestra(m) {
      if (!det) return null;
      const dir = det.procesar(m);
      if (dir) {
        contadores.gestos.acciones++;
        emitir({ tipo: 'gesto', dir });
        navegar({ accion: 'paso', delta: dir === 'derecha' ? 1 : -1 }, 'gesto');
      }
      return dir;
    }

    function paso(now) {
      if (!activo || !recognizer || !video) return;
      vfc = video.requestVideoFrameCallback(paso);
      ultimoTs = Math.max(ultimoTs + 1, Math.round(now));
      let res = null;
      try { res = recognizer.recognizeForVideo(video, ultimoTs); fallosInferencia = 0; }
      catch (e) { if (++fallosInferencia > 30) { fijar('error', 'error del modelo: ' + (e && e.message || e)); } return; }
      const m = { t: now, x: null, y: null, categoria: null };
      const lm = res && res.landmarks && res.landmarks[0];
      if (lm) {
        m.x = CENTRO_PALMA.reduce((a, i) => a + lm[i].x, 0) / CENTRO_PALMA.length;
        m.y = CENTRO_PALMA.reduce((a, i) => a + lm[i].y, 0) / CENTRO_PALMA.length;
        const g = res.gestures && res.gestures[0] && res.gestures[0][0];
        m.categoria = g ? g.categoryName : null;
      }
      cuadros++;
      if (now - t0Cuadros >= 2000) { fps = Math.round(cuadros * 1000 / (now - t0Cuadros)); cuadros = 0; t0Cuadros = now; if (st.estado === 'activo') fijar('activo', `activa · ${fps} fps`); }
      alMuestra(m);
      if (CONFIG.debug && now - ultimoDebug > 200) {
        ultimoDebug = now;
        estado.debugGestos = m.x === null ? 'mano: —' : `mano: ${m.categoria || 'ninguna'} · x=${m.x.toFixed(2)}`;
        dibujar();
      }
    }

    function liberar() {
      try { if (video && vfc !== null && video.cancelVideoFrameCallback) video.cancelVideoFrameCallback(vfc); } catch (e) { /* nada */ }
      vfc = null;
      if (stream) { stream.getTracks().forEach((tr) => { tr.onended = null; tr.stop(); }); stream = null; }
      if (video) { video.srcObject = null; video.remove(); video = null; }
      estado.debugGestos = '';
    }

    return {
      async iniciar() {
        if (activo) return;
        if (!window.Swipe) { fijar('error', 'falta swipe.js'); return; }
        activo = true; fijar('iniciando', 'cargando modelo…');
        try {
          await cargarModelo();
          if (!activo) return;
          fijar('iniciando', 'abriendo cámara…');
          stream = await navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 640 }, height: { ideal: 480 }, frameRate: { ideal: 30 } }, audio: false });
          if (!activo) { liberar(); return; }
          video = document.createElement('video');
          video.muted = true; video.playsInline = true; video.srcObject = stream;
          video.style.cssText = 'position:fixed;width:1px;height:1px;opacity:0;pointer-events:none;left:0;top:0';
          sombra().appendChild(video);
          await video.play();
          if (!activo) { liberar(); return; }
          stream.getVideoTracks()[0].onended = () => { if (activo) fijar('error', 'cámara desconectada'); };
          det = window.Swipe.crearDetector();
          cuadros = 0; t0Cuadros = performance.now(); fps = 0;
          fijar('activo', 'activa');
          vfc = video.requestVideoFrameCallback(paso);
        } catch (e) {
          const n = e && e.name;
          if (n === 'NotAllowedError' || n === 'SecurityError') fijar('error', 'sin permiso de cámara');
          else if (n === 'NotFoundError' || n === 'OverconstrainedError') fijar('error', 'sin cámara');
          else if (n === 'NotReadableError') fijar('error', 'cámara en uso por otra app');
          else fijar('error', 'gestos no disponibles: ' + (e && e.message || e));
          liberar(); activo = false;    // los errores de permiso no se reintentan solos: M vuelve a intentarlo
        }
      },
      detener() { activo = false; liberar(); if (det) det.reiniciar(); fijar('inactivo', 'apagado'); },
      estado: () => st,
      // interno (pruebas): inyectar una muestra sin cámara
      _alMuestra: (m) => alMuestra(m),
      _detector: () => det,
      _crearDetectorDePrueba: () => { det = window.Swipe.crearDetector(); return det; },
      info: () => ({ activo, delegado, fps }),
    };
  })();
  // Un cambio de slide que NO viene del propio gesto (voz, teclado, clicker) inicia el cooldown del detector y exige
  // nueva quietud; los cambios propios no, porque borrarían su bloqueo del sentido contrario.
  suscriptores.push((t, origen) => { const d = motorGestos._detector(); if (d && origen !== 'gesto') d.notificarCambio(t); });

  window.Presentador = {
    version: '0.4-T14',
    config: CONFIG,
    COOLDOWN_MS,
    navegar,
    estado: () => ({ reveal: estado.reveal, ultimoCambioMs: estado.ultimoCambioMs, ultimoComando: estado.ultimoComando }),
    bloqueadas: () => estado.bloqueadas.slice(),
    alCambiar: (f) => { suscriptores.push(f); },
    alEvento: (f) => { oyentes.push(f); },
    estadisticas: () => JSON.parse(JSON.stringify(contadores)),
    motores: () => Object.fromEntries(Object.entries(motores).map(([n, m]) => [n, m.estado ? m.estado() : { estado: 'activo' }])),
    aviso,
    control: () => Object.assign({}, estado.control),
    alternar,
    registrarMotor,
    debug: (texto) => { estado.debugTexto = String(texto); if (CONFIG.debug) dibujar(); },
    actualizarIndicador: dibujar,
    _interno: { sombra, gestos: motorGestos },
  };
  window.Presentador.registrarMotor('voz', motorVoz);
  window.Presentador.registrarMotor('gestos', motorGestos);
})();
