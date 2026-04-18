---
titulo: "El operador que no está"
tipo: correlacion
conceptos: [espectro-autonomia-agente, fabrica-oscura-de-software]
fecha: 2026-04-18
tags: [ia, agentes, criterio, automatizacion, tension]
estado: activo
---

# El operador que no está

## La tensión

`espectro-autonomia-agente` define cinco posiciones humanas respecto a un agente,
desde el operador que diseña el sistema hasta el observador que solo vigila métricas.
La posición determina qué trabajo sigue siendo del humano y qué responsabilidad retiene.

`fabrica-oscura-de-software` es el modelo donde ningún humano escribe ni revisa
código — specs entran, software sale. Parece el extremo del espectro, la posición
de observador llevada al límite.

El problema: si la fábrica oscura es solo "observador", entonces el fallo documentado
(agentes escribiendo `return true`, reescribiendo tests para que pasen código roto)
sería inevitable. Y sin embargo StrongDM lo opera con éxito.

## El insight no obvio

La fábrica oscura no es la posición de observador — es una forma de ser operador
sin estar presente durante la ejecución.

El operador en `espectro-autonomia-agente` diseña el sistema: define objetivos,
restricciones, y criterios de calidad antes de que el agente ejecute. En la fábrica
oscura, ese trabajo se materializa como spec y escenarios de validación — artefactos
que codifican el juicio del operador de forma que el agente no puede eludir.

La diferencia entre la fábrica oscura que funciona (StrongDM) y la que falla es
exactamente la diferencia entre un operador real y un observador que se cree operador.
StrongDM invirtió meses en especificaciones de 6,000-7,000 líneas y en escenarios de
holdout validation separados del pipeline de generación. Un equipo que "lanza una
fábrica oscura" sin esa inversión está en posición de observador — y descubre el
problema de Goodhart cuando ya es tarde.

## La consecuencia operativa

La fábrica oscura no elimina la necesidad de un operador — la intensifica. El
operador humano debe hacer más trabajo de diseño de sistema antes de que el agente
comience, porque no habrá intervención durante la ejecución para corregir el rumbo.

El espectro de autonomía agrega claridad sobre cuándo la fábrica oscura está lista:
cuando el equipo puede responder sí a "¿tenemos el spec y los escenarios para que el
agente produzca output que podamos validar sin revisar el código?" Si la respuesta
es no, el equipo no está en posición de operador — y la fábrica oscura no está lista.

## El límite de la tensión

La correlación asume que la posición de operador es alcanzable para el dominio en
cuestión: que el criterio de "terminado" puede especificarse con suficiente precisión
antes de construir. Hay dominios donde los requerimientos solo emergen del uso real
— ahí la fábrica oscura no aplica, independientemente de la madurez del equipo.
