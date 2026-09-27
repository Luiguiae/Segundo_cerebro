// Casos de prueba del parser de voz (SPEC §4 CU2/CU3/CU4). Ejecutar: node --test tests/comandos.test.js
// Contrato: interpretar(texto, esFinal) → null | { accion: 'paso'|'salto'|'inicio', delta, definitivo, conPrefijo }
//   paso   = Reveal.next()/prev()   (delta ±1, respeta fragments)
//   salto  = Reveal.slide(h ± N)    (ignora fragments; "un/una" = 1)
//   inicio = Reveal.slide(0, 0)     (delta 0)
//   definitivo:false (D5) = con prefijo, resultado NO final y comando que admite número ("avanza" puede
//   ser el inicio de "avanza 3"): quien llama espera ~500 ms de texto estable o el resultado final.
const test = require('node:test');
const assert = require('node:assert/strict');
const { normalizar, interpretar } = require('../comandos.js');

// esperado: null | [accion, delta, definitivo, conPrefijo]
function caso(texto, esFinal, esperado, nombre) {
  test(`${nombre ? nombre + ' — ' : ''}${JSON.stringify(texto)} (${esFinal ? 'final' : 'interino'}) → ${esperado ? esperado.slice(0, 3).join(' ') : 'null'}`, () => {
    const r = interpretar(texto, esFinal);
    if (esperado === null) return assert.equal(r, null);
    assert.notEqual(r, null, 'debería interpretarse como comando');
    const [accion, delta, definitivo, conPrefijo] = esperado;
    assert.equal(r.accion, accion, 'accion');
    assert.equal(r.delta, delta, 'delta');
    assert.equal(r.definitivo, definitivo, 'definitivo');
    assert.equal(r.conPrefijo, conPrefijo, 'conPrefijo');
  });
}
const SIN = (a, d) => [a, d, true, false];          // sin prefijo (solo finales), definitivo
const CON = (a, d, def = true) => [a, d, def, true]; // con prefijo

test('la API existe', () => {
  assert.equal(typeof interpretar, 'function');
  assert.equal(typeof normalizar, 'function');
});

test.describe('normalizar', () => {
  test('tildes, mayúsculas, puntuación y espacios', () => {
    assert.equal(normalizar('¡Leía, ATRÁS!'), 'leia atras');
    assert.equal(normalizar('  Avanza   3. '), 'avanza 3');
    assert.equal(normalizar('Lámina'), 'lamina');
    assert.equal(normalizar(''), '');
    assert.equal(normalizar('¿¡...!?'), '');
  });
});

test.describe('robustez de entrada', () => {
  caso(null, true, null); caso(undefined, true, null); caso('', true, null); caso('   ', true, null); caso('...', true, null);
});

test.describe('sin prefijo — paso (solo resultado final)', () => {
  for (const t of ['siguiente', 'Siguiente.', '  SIGUIENTE  ', 'avanza', 'adelante', 'AVANZA'])
    caso(t, true, SIN('paso', +1));
  for (const t of ['retrocede', 'atrás', 'atras', 'anterior', 'regresa', 'Retrocede.'])
    caso(t, true, SIN('paso', -1));
});

test.describe('sin prefijo — salto de N slides', () => {
  caso('avanza 3', true, SIN('salto', +3));
  caso('AVANZA 3', true, SIN('salto', +3));
  caso('avanza tres slides', true, SIN('salto', +3));
  caso('avanza 3 diapositivas', true, SIN('salto', +3));
  caso('avanza 3 slide', true, SIN('salto', +3));
  caso('adelanta 2', true, SIN('salto', +2));
  caso('adelanta dos láminas', true, SIN('salto', +2));
  caso('adelanta dos laminas', true, SIN('salto', +2));
  caso('retrocede 2 slides', true, SIN('salto', -2));
  caso('retrocede dos slides', true, SIN('salto', -2));
  caso('regresa cinco', true, SIN('salto', -5));
  caso('regresa 4 diapositivas', true, SIN('salto', -4));
  caso('retrocede un slide', true, SIN('salto', -1));
  caso('retrocede una lámina', true, SIN('salto', -1));
  caso('avanza una diapositiva', true, SIN('salto', +1));
  caso('avanza 12', true, SIN('salto', +12));
  caso('avanza dieciséis', true, SIN('salto', +16));
  caso('avanza diecisiete', true, SIN('salto', +17));
  caso('avanza veinte', true, SIN('salto', +20));
  caso('avanza 20', true, SIN('salto', +20));
  caso('avanza 1', true, SIN('salto', +1));
  // Todos los números en palabras, de 1 a 20
  const PAL = ['un', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciseis', 'diecisiete', 'dieciocho', 'diecinueve', 'veinte'];
  PAL.forEach((p, i) => caso(`avanza ${p} slides`, true, SIN('salto', i + 1), `palabra ${i + 1}`));
});

test.describe('sin prefijo — fuera de rango 1–20 no dispara (ni cae a "paso")', () => {
  for (const t of ['avanza 21', 'avanza 0', 'avanza 25', 'retrocede 100', 'regresa 21 slides']) caso(t, true, null);
});

test.describe('sin prefijo — inicio', () => {
  for (const t of ['vuelve al inicio', 'al inicio', 'primer slide', 'Vuelve al inicio.', 'VUELVE AL INICIO'])
    caso(t, true, SIN('inicio', 0));
});

test.describe('sin prefijo — rechazos: el enunciado completo debe ser exactamente un comando', () => {
  for (const t of ['veamos el siguiente punto', 'el siguiente', 'siguiente por favor', 'adelante con el tema',
    'avanza y retrocede', 'hola', 'atrás de eso', 'siguiente siguiente', 'avanza tres cuatro',
    'no avanza', 'avanza tres por favor', 'vamos al inicio de la charla', 'gracias'])
    caso(t, true, null);
});

test.describe('sin prefijo — los resultados intermedios NUNCA disparan', () => {
  for (const t of ['siguiente', 'avanza 3', 'vuelve al inicio', 'atrás', 'adelante', 'primer slide']) caso(t, false, null);
});

test.describe('con prefijo LeIA — paso, interino y final', () => {
  caso('leia siguiente', false, CON('paso', +1));
  caso('leia siguiente', true, CON('paso', +1));
  caso('LeIA, siguiente', true, CON('paso', +1));
  caso('LEÍA ATRÁS', true, CON('paso', -1));
  caso('leía retrocede', true, CON('paso', -1));
  caso('leia anterior', false, CON('paso', -1));
  caso('leia regresa', true, CON('paso', -1));
  caso('leia atrás', false, CON('paso', -1));
});

test.describe('con prefijo — variantes de transcripción de "LeIA"', () => {
  caso('lea siguiente', true, CON('paso', +1));
  caso('le ia siguiente', true, CON('paso', +1));
  caso('lelia atrás', true, CON('paso', -1));
  caso('leya vuelve al inicio', true, CON('inicio', 0));
  caso('leia siguiente', true, CON('paso', +1));
});

test.describe('con prefijo — dentro de un enunciado más largo', () => {
  caso('bueno leia siguiente gracias', false, CON('paso', +1));
  caso('bueno leia siguiente gracias', true, CON('paso', +1));
  caso('ok leia avanza tres', false, CON('salto', +3, false));
  caso('ok leia avanza tres', true, CON('salto', +3, true));
  caso('pasemos a lo siguiente leia atrás', false, CON('paso', -1));
  caso('leia avanza 3 slides por favor', true, CON('salto', +3));
});

test.describe('D5 — interinos ambiguos: "avanza" puede ser el inicio de "avanza 3"', () => {
  caso('leia avanza', false, CON('paso', +1, false));
  caso('leia retrocede', false, CON('paso', -1, false));
  caso('leia avanza 3', false, CON('salto', +3, false));
  caso('leia regresa 2', false, CON('salto', -2, false));
  caso('leia adelanta dos', false, CON('salto', +2, false));
  caso('leia avanza', true, CON('paso', +1, true));
  caso('leia avanza 3 slides', true, CON('salto', +3, true));
  caso('leia retrocede dos slides', true, CON('salto', -2, true));
  // sin número posible: disparo inmediato incluso en interino
  caso('leia adelante', false, CON('paso', +1, true));
  caso('leia siguiente', false, CON('paso', +1, true));
  caso('leia atrás', false, CON('paso', -1, true));
  caso('leia vuelve al inicio', false, CON('inicio', 0, true));
  caso('leia primer slide', false, CON('inicio', 0, true));
});

test.describe('D5 — "un/una" solo cuenta como número si va seguido de la unidad (o al final)', () => {
  caso('leia avanza un poco', true, CON('paso', +1));       // "un" aquí es un artículo, no N
  caso('leia avanza una diapositiva', true, CON('salto', +1));
  caso('leia retrocede un slide', true, CON('salto', -1));
  caso('leia avanza un', true, CON('salto', +1));
});

test.describe('D4 — el prefijo debe ir pegado al comando ("lea" también es un verbo)', () => {
  for (const t of ['leia', 'leia qué hora es', 'lea el siguiente párrafo', 'que lea el siguiente',
    'leia el siguiente punto', 'leia me pasas el siguiente', 'lea usted el anterior', 'y leia'])
    caso(t, true, null);
  caso('leia', false, null);
});

test.describe('con prefijo — números fuera de rango tampoco disparan', () => {
  caso('leia avanza 25', true, null);
  caso('leia avanza 0', true, null);
  caso('leia retrocede 21 slides', true, null);
});

test.describe('un mismo enunciado dispara una sola acción (la primera)', () => {
  caso('leia siguiente leia siguiente', true, CON('paso', +1));
  caso('leia siguiente, retrocede', true, CON('paso', +1));
  caso('leia atrás leia siguiente', true, CON('paso', -1));
  caso('leia siguiente leia siguiente', false, CON('paso', +1));
});

test.describe('sufijo opcional (slide, diapositiva, lámina)', () => {
  caso('leia siguiente slide', true, CON('paso', +1));
  caso('leia retrocede una lámina', true, CON('salto', -1));
  caso('leia vuelve al inicio', true, CON('inicio', 0));
});

test.describe('con prefijo pero sin comando reconocible', () => {
  for (const t of ['leia hola', 'leia gracias por venir', 'leia abre el menú']) caso(t, true, null);
});

test.describe('calibración en vivo (2026-09-26): así transcribió Chrome "LeIA"', () => {
  caso('de ella avanza una diapositiva', true, CON('salto', +1));
  caso('de ella siguiente', false, CON('paso', +1));
  caso('leía siguiente', true, CON('paso', +1));
  caso('de ella hablaremos luego', true, null);            // "de ella" sin comando pegado no dispara
  caso('hablamos de ella y luego veremos el siguiente punto', true, null);
  caso('según la ley siguiente', true, null);              // 'ley' NO es variante: evita un falso positivo real
  caso('ley siguiente', true, null);
});
