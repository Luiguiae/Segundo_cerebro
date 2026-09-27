// swipe.js — detector de swipe del presentador (SPEC §4 CU1). Sin dependencias, puro y testeable.
// Módulo dual: en el navegador expone `Swipe`; en Node, `module.exports`.
//
// Detector v2 (aprobado tras la ronda 2 del spike; ver docs/plan.md §11–12):
//   Hay evento cuando existe un trazo horizontal de ≥ `umbral` (fracción del ancho del cuadro) en ≤ `ventanaMs`,
//   con poco desplazamiento vertical, PRECEDIDO de `quietoMs` de mano abierta (categoría Open_Palm) casi quieta.
//   La mano NO tiene que ser Open_Palm durante el trazo (con el movimiento la categoría se pierde ~50 % de los cuadros).
//   Por qué así: sin la quietud previa, el retorno de la mano (a veces más amplio que el propio swipe) dispara el
//   sentido contrario, y colocar la mano al empezar dispara un falso positivo. Prioridad: 0 falsos positivos.
//
// Entrada:  { t (ms), x, y (0–1, centro de palma, cuadro SIN espejar; null = sin mano), categoria }
// Salida de procesar(): null | 'derecha' | 'izquierda'  (perspectiva del presentador: la webcam viene en espejo,
//   así que una mano que se mueve a SU derecha hace DISMINUIR x en la imagen cruda).
(function (raiz, fabrica) {
  const api = fabrica();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else raiz.Swipe = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const CONFIG_POR_DEFECTO = {
    umbral: 0.08,              // desplazamiento horizontal mínimo (fracción del ancho). Rango de trabajo 0.08–0.12
    ventanaMs: 500,            // el trazo debe completarse en ≤ ventanaMs
    minTrazoMs: 60,            // trazos más cortos que esto son saltos de landmarks, no movimiento
    relacionVerticalMax: 0.6,  // |dy| < relacionVerticalMax · |dx|
    quietoMs: 200,             // mano abierta casi quieta justo antes del trazo…
    minCuadrosQuieto: 3,       // …con al menos este número de cuadros,
    fraccionAbierta: 0.6,      // …de los cuales esta fracción son Open_Palm,
    dispersionMax: 0.08,       // …y dispersión x/y (máx − mín) ≤ esto,
    quietoSpanFrac: 0.75,      // …y que la quietud ABARQUE al menos esta fracción de quietoMs (3 cuadros pueden ser solo 66 ms).
    vaivenVentanaMs: 1000,     // Vaivén (saludar / gesticular con la palma abierta): si en esta ventana la mano invierte su sentido
    vaivenAmplitud: 0.04,      //   al menos vaivenMinInversiones veces con amplitud ≥ vaivenAmplitud, no se arma (una ola invierte ~4 veces/s;
    vaivenMinInversiones: 3,   //   swipe + retorno, 1–2).
    cooldownMs: 1500,          // tras un evento (o un cambio de otro canal) se ignora todo este tiempo
    bloqueoInversoMs: 3000,    // tras un evento, el sentido CONTRARIO se ignora este tiempo: es casi siempre el retorno de la mano (ver abajo)
    huecoMaxMs: 400,           // un hueco de detección mayor limpia el historial (mano que sale y entra ≠ swipe). 250 ms costaba swipes reales; 400 no
    categoriaAbierta: 'Open_Palm',
    espejo: true,              // true: x decreciente en la imagen cruda = 'derecha' del presentador
  };

  // Inversiones de sentido con histéresis: cuenta cuántas veces la mano "da la vuelta" retrocediendo ≥ amp desde su extremo.
  function inversiones(pts, amp) {
    if (pts.length < 3) return 0;
    let dir = 0, ext = pts[0].x, n = 0;
    for (const p of pts) {
      if (dir === 0) {
        if (p.x - ext >= amp) { dir = 1; ext = p.x; } else if (ext - p.x >= amp) { dir = -1; ext = p.x; }
      } else if (dir === 1) {
        if (p.x > ext) ext = p.x; else if (ext - p.x >= amp) { dir = -1; ext = p.x; n++; }
      } else if (p.x < ext) ext = p.x; else if (p.x - ext >= amp) { dir = 1; ext = p.x; n++; }
    }
    return n;
  }

  function crearDetector(cfgUsuario) {
    const cfg = Object.assign({}, CONFIG_POR_DEFECTO, cfgUsuario || {});
    let hist = [];                 // { t, x, y, abierta }
    let trayectoria = [];          // { t, x } de los últimos vaivenVentanaMs (solo para detectar vaivén)
    let ultimoEvento = -Infinity;
    let ultimaDireccion = null;    // dirección del último evento propio (null tras un cambio de otro canal)

    function procesar(m) {
      if (!m || typeof m.t !== 'number' || m.x === null || m.x === undefined || m.y === null || m.y === undefined) return null;
      const t = m.t;
      if (hist.length) {
        const previo = hist[hist.length - 1].t;
        if (t < previo || t - previo > cfg.huecoMaxMs) { hist = []; trayectoria = []; } // reloj retrocedió o hueco largo: empezar de cero
      }
      hist.push({ t, x: m.x, y: m.y, abierta: m.categoria === cfg.categoriaAbierta });
      trayectoria.push({ t, x: m.x });
      trayectoria = trayectoria.filter((h) => t - h.t <= cfg.vaivenVentanaMs);
      const corte = t - (cfg.ventanaMs + cfg.quietoMs + 50);
      hist = hist.filter((h) => h.t >= corte);

      if (t - ultimoEvento < cfg.cooldownMs) return null;
      if (inversiones(trayectoria, cfg.vaivenAmplitud) >= cfg.vaivenMinInversiones) { hist = []; return null; } // vaivén: no armar

      let mejor = null; // dx (con signo) del mejor trazo válido
      for (const a of hist) {
        const dt = t - a.t;
        if (dt > cfg.ventanaMs || dt < cfg.minTrazoMs) continue;
        const dx = m.x - a.x;
        const dy = m.y - a.y;
        if (Math.abs(dx) < cfg.umbral || Math.abs(dy) >= cfg.relacionVerticalMax * Math.abs(dx)) continue;

        // Quietud previa: cuadros en [a.t − quietoMs, a.t]
        const quieto = hist.filter((h) => h.t >= a.t - cfg.quietoMs && h.t <= a.t);
        if (quieto.length < cfg.minCuadrosQuieto) continue;
        let xMin = Infinity, xMax = -Infinity, yMin = Infinity, yMax = -Infinity, abiertos = 0;
        for (const h of quieto) {
          if (h.x < xMin) xMin = h.x; if (h.x > xMax) xMax = h.x;
          if (h.y < yMin) yMin = h.y; if (h.y > yMax) yMax = h.y;
          if (h.abierta) abiertos++;
        }
        if (xMax - xMin > cfg.dispersionMax || yMax - yMin > cfg.dispersionMax) continue;
        if (abiertos < cfg.fraccionAbierta * quieto.length) continue;
        if (a.t - quieto[0].t < cfg.quietoSpanFrac * cfg.quietoMs) continue;

        if (mejor === null || Math.abs(dx) > Math.abs(mejor)) mejor = dx;
      }
      if (mejor === null) return null;

      const haciaDerechaEnImagen = mejor > 0;
      const derechaDelPresentador = cfg.espejo ? !haciaDerechaEnImagen : haciaDerechaEnImagen;
      const direccion = derechaDelPresentador ? 'derecha' : 'izquierda';

      // Bloqueo del sentido contrario: en la ronda 1 una mano que descansó abierta 2.3 s en el destino y luego
      // volvió rápido al centro disparó el sentido inverso. No se puede distinguir de un swipe deliberado a la
      // izquierda, así que se prioriza 0 disparos inversos: el contrario espera bloqueoInversoMs (la voz y el
      // teclado cubren el 'retrocede' inmediato).
      if (ultimaDireccion !== null && direccion !== ultimaDireccion && t - ultimoEvento < cfg.bloqueoInversoMs) {
        hist = [];   // el trazo bloqueado se CONSUME: si no, dispararía apenas venciera el bloqueo
        return null;
      }

      ultimoEvento = t;
      ultimaDireccion = direccion;
      hist = [];
      return direccion;
    }

    // Un cambio de slide ocurrido por OTRO canal (voz, teclado): mismo cooldown y historial limpio,
    // así el movimiento posterior no puede disparar hasta que la mano vuelva a quedar abierta y quieta.
    function notificarCambio(t) { ultimoEvento = t; ultimaDireccion = null; hist = []; trayectoria = []; }

    function reiniciar() { hist = []; trayectoria = []; ultimoEvento = -Infinity; ultimaDireccion = null; }

    return { procesar, notificarCambio, reiniciar, config: cfg };
  }

  return { crearDetector, CONFIG_POR_DEFECTO };
});
