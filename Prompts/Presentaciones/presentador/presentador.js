// presentador.js — presentador por gestos y voz para decks Reveal.js (se inyecta al servir; ver presentar.py).
// T11: bloqueo de telemetría, espera a Reveal, navegación con la semántica del SPEC y cooldown compartido.
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
    control: { gestos: true, voz: true, indicador: true }, // lo que Luigui quiere (M, E, I); los motores (T13/T14) reportan lo que pasa
    debugTexto: '',                 // última transcripción cruda (solo con --debug)
  };
  const motores = {};               // { gestos, voz } → { iniciar(), detener(), estado() → { estado, detalle } }
  let reveal = null;
  const suscriptores = [];          // callbacks para "cambió el slide" (p. ej. swipe.notificarCambio en T14)

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
    if (ahora - estado.ultimoCambioMs < COOLDOWN_MS) return { cambio: false, motivo: 'cooldown' };

    const antes = firma(R);
    if (cmd.accion === 'paso') { if (cmd.delta > 0) R.next(); else R.prev(); }
    else if (cmd.accion === 'salto') {
      const n = R.getHorizontalSlides().length;
      R.slide(tope(R.getIndices().h + cmd.delta, 0, n - 1), 0);
    } else R.slide(0, 0);

    if (firma(R) === antes) return { cambio: false, motivo: 'sin-cambio' }; // p. ej. "siguiente" en el último slide
    const total = R.getHorizontalSlides().length, h = R.getIndices().h;
    const texto = textoComando(cmd, h + 1, total);
    estado.ultimoComando = { texto, canal: canal || 'consola', h: h + 1, total };
    marcarCambio(); // por si el evento de Reveal llega después
    dibujar();
    return { cambio: true, texto, h: h + 1, total };
  }

  function marcarCambio() {
    estado.ultimoCambioMs = performance.now();
    for (const f of suscriptores) { try { f(estado.ultimoCambioMs); } catch (e) { console.warn('[presentador] suscriptor:', e); } }
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
    for (const ev of ['slidechanged', 'fragmentshown', 'fragmenthidden']) R.on(ev, marcarCambio);
    estado.ultimoCambioMs = -Infinity; // el cambio inicial de Reveal al arrancar no cuenta
    if (CONFIG.debug) console.info('[presentador] Reveal listo');
    for (const [nombre, m] of Object.entries(motores)) if (estado.control[nombre] && typeof m.iniciar === 'function') Promise.resolve(m.iniciar()).catch((e) => console.warn('[presentador]', nombre, e));
    dibujar();
  }).catch((e) => { estado.reveal = 'error'; aviso('Presentador: error al iniciar (' + (e && e.message || e) + ')'); });

  window.Presentador = {
    version: '0.2-T12',
    config: CONFIG,
    COOLDOWN_MS,
    navegar,
    estado: () => ({ reveal: estado.reveal, ultimoCambioMs: estado.ultimoCambioMs, ultimoComando: estado.ultimoComando }),
    bloqueadas: () => estado.bloqueadas.slice(),
    alCambiar: (f) => { suscriptores.push(f); },
    aviso,
    control: () => Object.assign({}, estado.control),
    alternar,
    registrarMotor,
    debug: (texto) => { estado.debugTexto = String(texto); if (CONFIG.debug) dibujar(); },
    actualizarIndicador: dibujar,
    _interno: { sombra },
  };
})();
