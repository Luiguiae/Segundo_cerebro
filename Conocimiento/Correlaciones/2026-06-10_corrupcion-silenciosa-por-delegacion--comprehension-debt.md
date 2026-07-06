---
titulo: "El modo de supervisión que hace invisible la degradación"
tipo: correlacion
conceptos: [corrupcion-silenciosa-por-delegacion, comprehension-debt]
fecha: 2026-06-10
tags: [ia, criterio, velocidad, control, no-leido]
estado: borrador
---

# El modo de supervisión que hace invisible la degradación

## La tensión

`corrupcion-silenciosa-por-delegacion` describe cómo un LLM editando documentos en nombre del usuario introduce errores que se acumulan turno a turno mientras cada cambio individual parece correcto. `comprehension-debt` describe la brecha creciente entre el volumen de código que existe en un repositorio y lo que el equipo genuinamente entiende de él.

Son fenómenos de acumulación invisible en dominios distintos: uno en la fidelidad de los artefactos de texto, otro en la comprensión del sistema técnico.

## El insight no obvio

La superficie diferencia los dominios (documentos vs. código) pero el mecanismo es idéntico: en ambos casos el output de IA pasa el gate de aprobación turno a turno mientras la degradación se acumula entre turnos.

La corrupción silenciosa crece porque nadie compara el documento actual con el original — solo se revisa el último cambio. La comprehension debt crece porque nadie revisa la arquitectura del sistema — solo se revisa el diff inmediato. Ambas requieren una ventana temporal larga para volverse visibles, y la velocidad de la IA naturalmente induce el modo de supervisión local e incremental que hace imposible esa ventana larga.

El hallazgo central: el modo de supervisión que optimiza para velocidad es exactamente el que hace invisibles ambas formas de degradación. No es un problema de herramienta ni de disciplina individual — es una consecuencia del marco temporal que la IA impone sobre el trabajo.

## La consecuencia para el equipo

Ambas deudas requieren el mismo tipo de práctica: revisión con ventana larga y sin el contexto inmediato del último cambio. Leer el documento original cada cierta cantidad de ediciones delegadas. Revisar la arquitectura del sistema cada cierta cantidad de PRs de agentes. El pit-stop con perspectiva histórica, no solo de lo inmediato.

La señal de que ambas deudas se están acumulando simultáneamente: el equipo puede describir cada cambio individual pero no puede describir coherentemente el estado actual del sistema o el documento como totalidad.

## El límite

El problema de la ventana corta no es exclusivo de la IA — los equipos sin IA también acumulan comprehension debt y corrupción silenciosa. Lo que la IA cambia es la velocidad de acumulación: más outputs por unidad de tiempo significa que el ciclo de degradación se completa más rápido. La práctica correctiva (revisión con ventana larga) no es nueva — lo que cambia es la frecuencia con que debe ejecutarse.
