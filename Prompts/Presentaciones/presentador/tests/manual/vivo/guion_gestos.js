// Guion T14 — gestos, a la distancia real. `dry` = 'derecha'|'izquierda'|'ida_vuelta'|null (ensayo automático con muestras sintéticas).
// Reglas de uso (README): (1) tras un swipe, BAJAR o CERRAR la mano en vez de regresarla horizontal con la palma abierta;
// (2) no saludar ni hacer vaivenes con la palma abierta; M apaga los gestos si hace falta.
(function () {
  const H = (h, f = -1) => ({ h, f });
  const REGLA = 'Sube la mano ABIERTA (palma a la cámara) al centro y déjala QUIETA ~1 s. Al oír el tono: UN swipe rápido y amplio y luego BAJA la mano.';
  const S = (id, lado, dry) => ({ id, tipo: 'cambio', canal: 'gesto', titulo: `Swipe a tu ${lado.toUpperCase()}`, ayuda: REGLA + ' Un solo intento.', preparar: H(lado === 'derecha' ? 5 : 6),
    esperado: (a, d) => d.h === a.h + (lado === 'derecha' ? 1 : -1), dry, timeout: 7000 });
  window.__GUIONES = window.__GUIONES || {};
  window.__GUIONES.gestos = {
    titulo: 'Prueba de GESTOS (T14)',
    activar: ['gestos'],   // están apagados por defecto (experimentales en v1): la guía los enciende
    intro: 'De pie, a la distancia real de la presentación. Cada paso te dice qué hacer; oirás un tono corto al empezar y otro al terminar. Pulsa ESPACIO en la laptop para empezar y luego colócate.',
    cierre: 'Ya guardé todo. Puedes volver a la laptop.',
    pasos: () => {
      const p = [{ id: 'G00', tipo: 'espera', titulo: 'Colócate en tu posición de presentar', ayuda: 'De pie, a la distancia real, con la luz de siempre. Empiezo solo.', timeout: 15000, dry: null }];
      for (let i = 1; i <= 10; i++) p.push(S('G' + String(i).padStart(2, '0'), 'derecha', 'derecha'));
      for (let i = 11; i <= 20; i++) p.push(S('G' + i, 'izquierda', 'izquierda'));
      for (let i = 21; i <= 23; i++) p.push({ id: 'G' + i, tipo: 'cambio', canal: 'gesto', titulo: 'Swipe a la DERECHA e IDA Y VUELTA rápido', ayuda: 'Mal uso a propósito: swipe a tu derecha y regresa la mano al centro rápido, con la palma abierta. Debe contar UN solo cambio (nunca el inverso).', preparar: H(5), esperado: (a, d) => d.h === a.h + 1, dry: 'ida_vuelta', timeout: 7000 });
      p.push({ id: 'G24', tipo: 'nada', titulo: 'Habla y gesticula 20 s', ayuda: 'Cuéntame algo gesticulando normal, con las manos. Sin swipes intencionales y sin decir “Jarvis”. NO debe cambiar nada.', preparar: H(5), ventanaMs: 20000, dry: null });
      p.push({ id: 'G25', tipo: 'nada', titulo: 'Mano abierta QUIETA 8 s, hablando', ayuda: 'Como esperando, mientras cuentas algo. NO debe cambiar nada.', preparar: H(5), ventanaMs: 8000, dry: null });
      p.push({ id: 'G26', tipo: 'nada', titulo: 'Puño o dedo, rápido de lado a lado (6 s)', ayuda: 'NO debe cambiar nada.', preparar: H(5), ventanaMs: 6000, dry: null });
      p.push({ id: 'G27', tipo: 'info', titulo: 'Saluda / vaivén con la palma abierta (6 s)', ayuda: 'Prueba informativa de lo que la regla 2 pide evitar: solo registro cuántos cambios provoca; no cuenta como fallo.', preparar: H(5), timeout: 6000, dry: null });
      p.push({ id: 'G28', tipo: 'cambio', titulo: 'Di “LeIA, siguiente” y AL INSTANTE haz un swipe a la derecha', ayuda: 'Cooldown compartido: debe contar UN solo cambio.', preparar: H(5), esperado: (a, d) => d.h === a.h + 1, dry: null, timeout: 9000 });
      return p;
    },
  };
})();
