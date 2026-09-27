// Guion T15 — las 4 pruebas manuales de degradación (SPEC §4 "Errores"). Variante = qué prueba:
//   sinreveal | camara | wifi | ininteligible
(function () {
  const H = (h, f = -1) => ({ h, f });
  const est = (n) => (window.Presentador.motores()[n] || {});
  const ctl = () => window.Presentador.control();
  const humano = (id, titulo, ayuda, timeout = 60000) => ({ id, tipo: 'humano', titulo, ayuda: (ayuda || '') + '   Pulsa 1 = SÍ  ·  0 = NO', timeout });
  const cond = (id, titulo, ayuda, cond, timeout, obsMal) => ({ id, tipo: 'condicion', titulo, ayuda, cond, timeout, obsMal, dry: null });
  const voz = (id, frase, ayuda) => ({ id, tipo: 'cambio', canal: 'voz', titulo: `Di:  “${frase}”`, ayuda: ayuda || '', preparar: H(5), esperado: (a, d) => d.h === a.h + 1, timeout: 12000, dry: null });
  const tecla = (id, titulo) => ({ id, tipo: 'condicion', titulo, ayuda: 'Debe moverse el slide (la tecla nativa nunca se bloquea).', preparar: H(5), cond: (ini) => window.Reveal && Reveal.getIndices().h !== ini.h, timeout: 20000, obsOk: 'la flecha movió el slide', obsMal: 'la flecha no movió el slide', dry: null });
  const nada = (id, titulo, ayuda, ms, dry) => ({ id, tipo: 'nada', canal: 'voz', titulo, ayuda: (ayuda || '') + ' NO debe cambiar nada.', preparar: H(5), ventanaMs: ms, dry });
  window.__GUIONES = window.__GUIONES || {};
  window.__GUIONES.degradacion = {
    titulo: 'Prueba de DEGRADACIÓN (T15)',
    intro: 'Pulsa ESPACIO para empezar. Los pasos te dicen qué hacer; algunos piden que confirmes con la tecla 1 (sí) o 0 (no).',
    cierre: 'Ya guardé todo. Puedes volver a la laptop.',
    pasos: (v) => ({
      // 1) Página sin Reveal.js: se ve igual, el presentador no se activa y el indicador lo avisa
      sinreveal: [
        cond('D1a', 'Espera unos segundos…', 'El presentador comprueba durante 15 s si la página usa Reveal.js.', () => window.Presentador.estado().reveal === 'sin-reveal', 30000, 'no llegó a "sin-reveal"'),
        humano('D1b', '¿La página se ve NORMAL (título y lista) y abajo a la derecha dice “no usa Reveal.js — inactivo”?', 'Fíjate en que no cambió nada de la página.'),
        cond('D1c', 'Pulsa  M  y luego  E', 'Con la página sin Reveal no debe pasar nada malo.', () => ctl().gestos === true && ctl().voz === false, 40000, 'no pulsaste M y E'),
        { id: 'D1d', tipo: 'condicion', titulo: 'Comprobando…', ayuda: '', cond: () => est('gestos').estado !== 'activo' && est('voz').estado !== 'activo' && window.__guia.errores === 0, timeout: 4000, obsOk: 'motores inactivos y 0 errores en la página', obsMal: 'algún motor se activó o hubo errores', dry: null },
        humano('D1e', '¿La página SIGUE viéndose normal, sin mensajes ni ventanas nuevas?'),
      ],
      // 2) Sin permiso de cámara (gestos apagados por defecto: se activan con M y se BLOQUEA la cámara)
      camara: [
        cond('C1', 'Si Chrome pide el MICRÓFONO, pulsa PERMITIR', 'Es un origen nuevo (puerto distinto), así que lo pedirá.', () => est('voz').estado === 'activo', 60000, 'la voz no llegó a activarse'),
        cond('C2', 'Pulsa  M  UNA vez y espera; cuando Chrome pida la CÁMARA, pulsa BLOQUEAR', 'Tarda unos segundos en cargar el modelo antes de pedir la cámara: no pulses M otra vez. Debe aparecer “sin permiso de cámara”.', () => est('gestos').estado === 'error' && /permiso/.test(est('gestos').detalle || ''), 60000, 'no apareció “sin permiso de cámara” (¿permitiste la cámara?)'),
        voz('C3', 'LeIA, siguiente', 'Sin cámara, la voz debe seguir funcionando.'),
        tecla('C4', 'Pulsa la flecha →  del teclado'),
        humano('C5', '¿El indicador dice “Cámara (M) sin permiso de cámara” y NO hay ningún mensaje intrusivo en pantalla?'),
      ],
      // 3) Sin internet: la voz avisa; gestos y teclado siguen
      wifi: [
        cond('W1', 'Pulsa  M  para encender los gestos', 'Este origen ya tiene permiso de cámara.', () => est('gestos').estado === 'activo', 40000, 'los gestos no se activaron'),
        cond('W2', 'APAGA el Wi-Fi ahora (icono de Wi-Fi arriba a la derecha)', 'Mi conexión también se corta un rato; la guía sigue sola.', () => !navigator.onLine, 120000, 'no detecté que el Wi-Fi estuviera apagado'),
        cond('W3', 'Sin internet: di varias veces  “LeIA, siguiente”', 'Ahí no debe cambiar nada y el indicador debe avisar “sin internet”.', () => /internet/.test(est('voz').detalle || ''), 90000, 'la voz no avisó de que no hay internet'),
        { id: 'W4', tipo: 'cambio', canal: 'gesto', titulo: 'Swipe con la mano abierta (sin internet)', ayuda: 'Los gestos no necesitan internet. Tienes 15 s; puedes reintentar. (Los gestos son experimentales: no cuenta como fallo grave.)', preparar: H(5), esperado: (a, d) => d.h !== a.h, timeout: 15000, dry: null },
        tecla('W5', 'Pulsa la flecha →  del teclado'),
        cond('W6', 'ENCIENDE el Wi-Fi ahora', 'Espera a que vuelva la conexión.', () => navigator.onLine, 120000, 'no volvió el Wi-Fi'),
        cond('W7', 'Espera: la voz debe recuperarse sola', 'Sin tocar nada; puede tardar unos segundos.', () => est('voz').estado === 'activo' && /escuchando/.test(est('voz').detalle || ''), 90000, 'la voz no se recuperó tras volver el internet'),
        voz('W8', 'LeIA, siguiente', 'Con internet de vuelta debe funcionar.'),
      ],
      // 4) Comando de voz no reconocido: no pasa nada y no hay mensajes intrusivos
      ininteligible: [
        nada('I1', 'Di:  “LeIA, bailemos un vals”', '', 9000, 'leia bailemos un vals'),
        nada('I2', 'Di:  “LeIA, qué hora es”', '', 9000, 'leia que hora es'),
        nada('I3', 'Murmura algo incomprensible (“blablabla…”) 8 s', '', 8000, 'blablabla'),
        nada('I4', 'Di:  “LeIA”  y nada más', 'Solo la palabra de activación.', 8000, 'leia'),
        humano('I5', '¿La pantalla se mantuvo LIMPIA (solo el indicador discreto, ningún aviso ni error)?'),
      ],
    }[v] || []),
  };
})();
