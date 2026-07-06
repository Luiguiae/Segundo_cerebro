---
titulo: "El aprendizaje que no se codifica desaparece"
tipo: correlacion
conceptos: [aprendizaje-vicario-mediado-por-agente, feedback-que-escala]
fecha: 2026-05-13
tags: [ia, sistemas, aprendizaje, organizacion, criterio]
estado: borrador
---

# El aprendizaje que no se codifica desaparece

## La tensión

`feedback-que-escala` tiene una premisa clara: el criterio que vive en la cabeza de
una persona no escala. Si el mismo error requiere corrección manual cada vez, el
problema no es la persona — es que ese criterio todavía no está codificado en el
sistema. El criterio que no se codifica en prompts, procesos o design systems
desaparece cuando cambia quien lo lleva.

`aprendizaje-vicario-mediado-por-agente` describe un fenómeno de escala aparente: en
Shopify, 5,938 empleados desarrollaron criterio observando los errores públicos de
River. El aprendizaje se distribuyó masivamente — pero en las cabezas de las personas,
no en el sistema. Quien observó los patrones de error, los incorporó como intuición.
No queda registro de qué aprendió quién ni cómo.

Aplicar `feedback-que-escala` al resultado: ese aprendizaje vicario es exactamente
el tipo de criterio que el sistema todavía no tiene codificado.

## El insight no obvio

El aprendizaje vicario y el feedback sistémico son dos fases consecutivas del mismo
ciclo de mejora — no alternativas.

La observación pública del agente genera insight tácito: los miembros del equipo
internalizan patrones, desarrollan intuiciones sobre cuándo el agente va a fallar,
identifican instrucciones que funcionan. Esto es el insumo, no el producto. El
producto es cuando esas observaciones se convierten en correcciones a los prompts,
actualizaciones a las instrucciones, o patrones documentados.

En el caso Shopify, los dos mecanismos operaron juntos: los empleados observaban los
errores de River (vicario) Y corregían colectivamente las instrucciones (sistémico).
El merge rate mejoró de 36% a 77% porque el insight tácito se convirtió en contexto
mejorado del sistema. Sin el segundo paso, la mejora habría existido en 5,938 cabezas
y no en el agente.

La síntesis: el aprendizaje vicario sin codificación produce capital humano volátil.
El feedback sistémico sin observación vicaria previa solo puede codificar errores ya
definidos, no los que el sistema todavía no reconoce como errores. Uno nutre al otro.

## La consecuencia operativa

Desplegar un agente en público no es suficiente si no hay un proceso explícito para
convertir las observaciones en mejoras del sistema. Las organizaciones que hacen
solo visibilidad crean aprendizaje que desaparece con la rotación de personal.

El diseño completo tiene dos capas:
- Visibilidad: el agente trabaja en público y sus errores son observables
- Captura: hay un mecanismo para que las observaciones se conviertan en instrucciones,
  prompts o procesos actualizados

Sin la segunda capa, el aprendizaje vicario es una mejora temporal. Con ambas capas,
el aprendizaje vicario se convierte en el mecanismo por el cual el capital de contexto
del sistema crece a través de inteligencia distribuida.

## El límite de la tensión

No todo el aprendizaje vicario es codificable. El juicio sobre cuándo overrridear al
agente, la intuición de que un output correcto "se siente mal", la meta-comprensión
del comportamiento del agente en casos borde — estos resisten la formalización. El
`feedback-que-escala` cubre la capa codificable; el aprendizaje vicario puede ser el
único mecanismo para desarrollar la capa no codificable.

La correlación también asume que hay alguien con criterio suficiente para arbitrar
qué observaciones vicarias merecen codificarse. En equipos con poco criterio
acumulado, la codificación prematura puede cristalizar errores en lugar de soluciones.
