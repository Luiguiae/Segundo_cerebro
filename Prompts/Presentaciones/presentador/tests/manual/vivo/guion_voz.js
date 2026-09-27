// Guion T13 — voz. `dry` = lo que diría un usuario (lo usa el ensayo automático con un reconocedor simulado).
(function () {
  const H = (h, f = -1) => ({ h, f });
  const C = (id, titulo, ayuda, prep, esperado, dry, extra = {}) => ({ id, tipo: 'cambio', canal: 'voz', titulo, ayuda, preparar: prep, esperado, dry, timeout: 12000, ...extra });
  window.__GUIONES = window.__GUIONES || {};
  window.__GUIONES.voz = {
    titulo: 'Prueba de VOZ (T13)',
    intro: 'Habla con naturalidad, como en la charla. Cada paso te dice qué frase decir; oirás un tono corto al empezar y otro al terminar. Pulsa ESPACIO para empezar.',
    cierre: 'Ya guardé todo. Puedes volver a la laptop.',
    pasos: (variante) => {
      const todos = [
      C('V01', 'Di:  “LeIA, siguiente”', 'Avanza un slide.', H(5), (a, d) => d.h === a.h + 1, 'leia siguiente'),
      C('V02', 'Di:  “LeIA, retrocede”', 'Vuelve un slide.', H(6), (a, d) => d.h === a.h - 1, 'leia retrocede'),
      C('V03', 'Di:  “Siguiente”   (a secas, y haz una pausa)', 'Sin “LeIA”: solo funciona si es la frase completa.', H(5), (a, d) => d.h === a.h + 1, 'siguiente'),
      C('V04', 'Di:  “Retrocede”   (a secas, y haz una pausa)', '', H(6), (a, d) => d.h === a.h - 1, 'retrocede'),
      C('V05', 'Di:  “Avanza tres slides”', 'Salta 3 slides.', H(4), (a, d) => d.h === a.h + 3, 'avanza tres slides'),
      C('V06', 'Di:  “LeIA, retrocede dos slides”', 'Salta 2 hacia atrás.', H(8), (a, d) => d.h === a.h - 2, 'leia retrocede dos slides'),
      C('V07', 'Di:  “Vuelve al inicio”', 'Va al primer slide.', H(7), (a, d) => d.h === 0, 'vuelve al inicio'),
      C('V08', 'Di:  “LeIA, siguiente”', 'Este slide tiene fragments: debe mostrar el PRIMER fragment, sin cambiar de slide.', H(2), (a, d) => d.h === 2 && d.f === a.f + 1, 'leia siguiente'),
      C('V09', 'Di:  “LeIA, avanza una diapositiva”', 'Salta el slide completo aunque queden fragments.', H(2), (a, d) => d.h === 3, 'leia avanza una diapositiva'),
      { id: 'V10', tipo: 'nada', canal: 'voz', titulo: 'Di la frase:  “veamos el siguiente punto”', ayuda: 'NO debe cambiar nada.', preparar: H(5), ventanaMs: 8000, dry: 'veamos el siguiente punto' },
      { id: 'V11', tipo: 'nada', canal: 'voz', titulo: 'Habla con normalidad 12 s', ayuda: 'Cuéntame qué hiciste hoy. Evita las palabras “siguiente”, “avanza”, “retrocede” y “Jarvis”. NO debe cambiar nada.', preparar: H(5), ventanaMs: 12000, dry: 'hoy estuve trabajando en la presentacion de la semana' },
      { id: 'V12', tipo: 'espera', titulo: 'No digas nada durante 30 s', ayuda: 'Prueba que el reconocimiento sigue vivo después de un silencio largo.', preparar: H(5), timeout: 30000, dry: null },
      C('V13', 'Ahora di:  “LeIA, siguiente”', 'Tras 30 s de silencio debe funcionar igual.', H(5), (a, d) => d.h === a.h + 1, 'leia siguiente'),
      C('V14', 'Di:  “LeIA, siguiente”', 'Calibración: veremos cómo transcribe Chrome “LeIA”.', H(5), (a, d) => d.h === a.h + 1, 'leia siguiente'),
      C('V15', 'Di:  “LeIA, siguiente”', 'Otra vez.', H(5), (a, d) => d.h === a.h + 1, 'leia siguiente'),
      C('V16', 'Di:  “LeIA, atrás”', '', H(6), (a, d) => d.h === a.h - 1, 'leia atras'),
      C('V17', 'Di:  “LeIA, siguiente”', 'Última.', H(5), (a, d) => d.h === a.h + 1, 'leia siguiente'),
      ];
      if (variante === 'rapida') {   // repetición corta: primer paso tras cargar + la frase que falló
        const g = (id) => todos.find((p) => p.id === id);
        return [g('V01'), g('V09'), { ...g('V09'), id: 'V09b' }, { ...g('V02'), id: 'V02b' }];
      }
      return todos;
    },
  };
})();
