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
    dispersionMax: 0.08,       // …y dispersión x/y (máx − mín) ≤ esto
    cooldownMs: 1500,          // tras un evento (o un cambio de otro canal) se ignora todo este tiempo
    huecoMaxMs: 400,           // un hueco de detección mayor limpia el historial (mano que sale y entra ≠ swipe). 250 ms costaba swipes reales; 400 no
    categoriaAbierta: 'Open_Palm',
    espejo: true,              // true: x decreciente en la imagen cruda = 'derecha' del presentador
  };

  function crearDetector(cfgUsuario) {
    const cfg = Object.assign({}, CONFIG_POR_DEFECTO, cfgUsuario || {});
    let hist = [];                 // { t, x, y, abierta }
    let ultimoEvento = -Infinity;

    function procesar(m) {
      if (!m || typeof m.t !== 'number' || m.x === null || m.x === undefined || m.y === null || m.y === undefined) return null;
      const t = m.t;
      if (hist.length) {
        const previo = hist[hist.length - 1].t;
        if (t < previo || t - previo > cfg.huecoMaxMs) hist = []; // reloj retrocedió o hueco largo: empezar de cero
      }
      hist.push({ t, x: m.x, y: m.y, abierta: m.categoria === cfg.categoriaAbierta });
      const corte = t - (cfg.ventanaMs + cfg.quietoMs + 50);
      hist = hist.filter((h) => h.t >= corte);

      if (t - ultimoEvento < cfg.cooldownMs) return null;

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

        if (mejor === null || Math.abs(dx) > Math.abs(mejor)) mejor = dx;
      }
      if (mejor === null) return null;

      ultimoEvento = t;
      hist = [];
      const haciaDerechaEnImagen = mejor > 0;
      const derechaDelPresentador = cfg.espejo ? !haciaDerechaEnImagen : haciaDerechaEnImagen;
      return derechaDelPresentador ? 'derecha' : 'izquierda';
    }

    // Un cambio de slide ocurrido por OTRO canal (voz, teclado): mismo cooldown y historial limpio,
    // así el movimiento posterior no puede disparar hasta que la mano vuelva a quedar abierta y quieta.
    function notificarCambio(t) { ultimoEvento = t; hist = []; }

    function reiniciar() { hist = []; ultimoEvento = -Infinity; }

    return { procesar, notificarCambio, reiniciar, config: cfg };
  }

  return { crearDetector, CONFIG_POR_DEFECTO };
});
