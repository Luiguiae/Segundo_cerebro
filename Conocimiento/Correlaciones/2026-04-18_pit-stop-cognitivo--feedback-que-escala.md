---
titulo: "Lo que el sistema no puede enseñarse a sí mismo"
tipo: correlacion
conceptos: [pit-stop-cognitivo, feedback-que-escala]
fecha: 2026-04-18
tags: [ia, sistemas, criterio, conocimiento, tension]
estado: activo
---

# Lo que el sistema no puede enseñarse a sí mismo

## La tensión

`feedback-que-escala` dice que el criterio de calidad debe codificarse en el
sistema — prompts, design systems, procesos de revisión — para no depender de
intervención humana en cada instancia. Si el criterio está en la cabeza de una
persona y no en el sistema, desaparece cuando cambia la persona.

`pit-stop-cognitivo` dice que el humano debe recuperar activamente el modelo
mental del sistema en cada iteración — que delegar comprensión al agente produce
comprehension-debt irreversible.

La tensión parece fundamental: uno pide que el criterio viva en el sistema, el
otro pide que viva en la cabeza del humano.

## El insight no obvio

No operan sobre el mismo objeto. La confusión desaparece cuando se distingue
qué tipo de conocimiento puede codificarse y cuál no.

`feedback-que-escala` codifica **criterio sobre outputs conocidos**: qué es un
buen botón, dónde va el CTA, cómo se nombra una variable, qué constituye un
buen componente. Son decisiones que se pueden especificar, ejemplificar y
verificar automáticamente. El sistema puede aprenderlas y aplicarlas sin
intervención humana.

`pit-stop-cognitivo` mantiene **comprensión del sistema como totalidad**: cómo
se conectan las piezas, qué emerge del conjunto que no es visible en ninguna
parte individual, qué decisiones tomadas en la iteración 3 tienen consecuencias
no obvias en la iteración 17. Esto no puede codificarse en un prompt — requiere
un humano que haya visto el sistema evolucionar.

El límite de `feedback-que-escala` es preciso: el sistema solo puede enseñarse
a detectar errores que alguien ya definió como errores. Los problemas sistémicos
— los que emergen de la interacción de decisiones individualmente correctas —
no tienen representación en ningún prompt ni design system. Solo son visibles
para quien mantiene el modelo mental completo.

## La consecuencia operativa

Los dos conceptos son complementarios en capas distintas del proceso de calidad:

- `feedback-que-escala` previene la re-ocurrencia de errores **ya conocidos**
- `pit-stop-cognitivo` detecta problemas que el sistema **todavía no sabe que tiene**

Un equipo que tiene solo feedback sistémico sin pit stops cognitivos produce
outputs correctos según criterios viejos mientras el sistema acumula deuda
estructural invisible. Un equipo que hace pit stops sin feedback sistémico
corrige los mismos errores puntuales una y otra vez.

La madurez de un equipo AI-native se puede leer en si tiene ambos: criterio
codificado para lo conocido, y práctica deliberada de comprensión para lo
desconocido.

## El límite de la tensión

La correlación pierde fuerza si el sistema es suficientemente simple como para
que todo su comportamiento sea especificable. En productos pequeños y acotados,
el feedback sistémico puede cubrir casi todo. La tensión es más aguda en sistemas
que evolucionan rápido — donde la distancia entre "lo que el sistema sabe hacer"
y "lo que el sistema realmente hace" crece más rápido de lo que el equipo puede
codificar criterio.
