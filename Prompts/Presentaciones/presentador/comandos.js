// comandos.js — parser de voz del presentador (SPEC §4 CU2/CU3/CU4). Sin dependencias.
// Módulo dual: en el navegador expone `Comandos`; en Node, `module.exports`.
//
//   interpretar(texto, esFinal) → null | { accion, delta, definitivo, conPrefijo }
//     accion 'paso'   → Reveal.next()/prev()  (delta ±1; respeta fragments)
//     accion 'salto'  → Reveal.slide(h ± N)   (delta ±N; ignora fragments)
//     accion 'inicio' → Reveal.slide(0, 0)    (delta 0)
//
// Reglas (ver docs/plan.md, D4 y D5):
//  - Con prefijo "LeIA": el prefijo debe ir PEGADO al comando (D4: "lea" también es un verbo);
//    vale dentro de un enunciado más largo y sobre resultados intermedios. Un enunciado dispara
//    una sola acción: la del primer prefijo con comando válido.
//  - Sin prefijo: solo si el enunciado COMPLETO, como resultado final, es exactamente un comando.
//  - D5: en un resultado intermedio, los comandos que admiten número (avanza/adelanta/retrocede/
//    regresa) devuelven definitivo:false ("avanza" puede ser el inicio de "avanza 3"); quien llama
//    espera ~500 ms de texto estable o el resultado final. Los demás disparan de inmediato.
(function (raiz, fabrica) {
  const api = fabrica();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else raiz.Comandos = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Variantes de transcripción de "LeIA" (normalizadas). Se ajusta en el ensayo con lo que
  // realmente transcriba Chrome; se lee en cada llamada, así que puede editarse en caliente.
  const VARIANTES_LEIA = ['leia', 'lea', 'le ia', 'lelia', 'leya'];

  const UNIDADES = new Set(['slide', 'slides', 'diapositiva', 'diapositivas', 'lamina', 'laminas']);

  const NUMEROS = {
    un: 1, una: 1, dos: 2, tres: 3, cuatro: 4, cinco: 5, seis: 6, siete: 7, ocho: 8, nueve: 9, diez: 10,
    once: 11, doce: 12, trece: 13, catorce: 14, quince: 15, dieciseis: 16, diecisiete: 17, dieciocho: 18,
    diecinueve: 19, veinte: 20,
  };
  const MIN_N = 1, MAX_N = 20;

  // Verbos que admiten número: signo del movimiento y si la forma sin número es válida.
  const VERBOS_N = {
    avanza: { signo: +1, sinNumero: true },
    adelanta: { signo: +1, sinNumero: false }, // "adelanta" solo, sin número, no es comando del SPEC
    retrocede: { signo: -1, sinNumero: true },
    regresa: { signo: -1, sinNumero: true },
  };
  // Comandos de una palabra que no admiten número (disparan al instante incluso en interinos).
  const PASOS = { siguiente: +1, adelante: +1, anterior: -1, atras: -1 };

  function normalizar(texto) {
    if (texto === null || texto === undefined) return '';
    return String(texto)
      .normalize('NFD').replace(/[̀-ͯ]/g, '') // sin tildes
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, ' ')                       // puntuación → espacio
      .trim();
  }

  // Intenta leer un comando que empiece en tokens[i]. Devuelve:
  //   null                       → no hay comando aquí
  //   { invalido: true }         → hay un verbo con número fuera de 1–20
  //   { accion, delta, admiteNumero, siguiente }  → comando; `siguiente` = índice tras consumirlo
  function leerComando(tokens, i) {
    const t = tokens[i];
    if (t === undefined) return null;

    let cmd = null;
    if (Object.prototype.hasOwnProperty.call(PASOS, t)) {
      cmd = { accion: 'paso', delta: PASOS[t], admiteNumero: false, siguiente: i + 1 };
    } else if (t === 'vuelve' && tokens[i + 1] === 'al' && tokens[i + 2] === 'inicio') {
      cmd = { accion: 'inicio', delta: 0, admiteNumero: false, siguiente: i + 3 };
    } else if (t === 'al' && tokens[i + 1] === 'inicio') {
      cmd = { accion: 'inicio', delta: 0, admiteNumero: false, siguiente: i + 2 };
    } else if (t === 'primer' && UNIDADES.has(tokens[i + 1])) {
      return { accion: 'inicio', delta: 0, admiteNumero: false, siguiente: i + 2 }; // la unidad ya es parte del comando
    } else if (Object.prototype.hasOwnProperty.call(VERBOS_N, t)) {
      const v = VERBOS_N[t];
      const n = leerNumero(tokens, i + 1);
      if (n && n.invalido) return { invalido: true };
      if (n) {
        cmd = { accion: 'salto', delta: v.signo * n.valor, admiteNumero: true, siguiente: n.siguiente };
      } else if (v.sinNumero) {
        cmd = { accion: 'paso', delta: v.signo, admiteNumero: true, siguiente: i + 1 };
      } else {
        return null;
      }
    }
    if (!cmd) return null;
    if (UNIDADES.has(tokens[cmd.siguiente])) cmd.siguiente += 1; // "slide", "diapositiva"… opcional al final
    return cmd;
  }

  // Número en tokens[j]: dígitos o palabras 1–20. "un"/"una" solo cuentan como número si les sigue
  // la unidad o el fin del enunciado ("avanza un poco": ahí "un" es un artículo).
  function leerNumero(tokens, j) {
    const t = tokens[j];
    if (t === undefined) return null;
    if (/^\d+$/.test(t)) {
      const v = parseInt(t, 10);
      return v >= MIN_N && v <= MAX_N ? { valor: v, siguiente: j + 1 } : { invalido: true };
    }
    if (Object.prototype.hasOwnProperty.call(NUMEROS, t)) {
      if ((t === 'un' || t === 'una') && tokens[j + 1] !== undefined && !UNIDADES.has(tokens[j + 1])) return null;
      return { valor: NUMEROS[t], siguiente: j + 1 };
    }
    return null;
  }

  function posicionesDePrefijo(tokens) {
    const variantes = VARIANTES_LEIA.map((v) => normalizar(v).split(' ')).filter((v) => v[0]);
    const res = [];
    for (let i = 0; i < tokens.length; i++) {
      for (const v of variantes) {
        if (v.every((w, k) => tokens[i + k] === w)) { res.push({ inicio: i, largo: v.length }); break; }
      }
    }
    return res;
  }

  function interpretar(texto, esFinal) {
    const tokens = normalizar(texto).split(' ').filter(Boolean);
    if (tokens.length === 0) return null;
    const final = esFinal === true;

    // 1) Con prefijo: el primer prefijo con un comando válido pegado a él.
    for (const p of posicionesDePrefijo(tokens)) {
      const c = leerComando(tokens, p.inicio + p.largo);
      if (c && c.invalido) return null;
      if (c) {
        return {
          accion: c.accion, delta: c.delta, conPrefijo: true,
          definitivo: final || !c.admiteNumero,
        };
      }
    }

    // 2) Sin prefijo: solo resultado final, y el enunciado completo debe ser exactamente un comando.
    if (!final) return null;
    const c = leerComando(tokens, 0);
    if (!c || c.invalido || c.siguiente !== tokens.length) return null;
    return { accion: c.accion, delta: c.delta, conPrefijo: false, definitivo: true };
  }

  return { normalizar, interpretar, VARIANTES_LEIA };
});
