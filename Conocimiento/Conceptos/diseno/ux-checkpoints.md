---
titulo: "UX Checkpoints"
tipo: concepto
fecha: 2026-04-21
familia: agencia-ia
estado: activo
tags: [diseño, ux, agentes, confianza, control]
relacionado: [pit-stop-cognitivo, arnes-del-agente, arquitectura-de-confianza]
fuentes:
  - titulo: "The checkpoints of the AI User Experience"
    autor: "Gianluca Brugnoli"
    url: "https://medium.com/@lowresolution/the-checkpoints-of-the-ai-user-experience-421c7ecfcf5a"
    fecha_acceso: 2026-04-21
---

# UX Checkpoints

## El concepto
En la era de agentes, la filosofía del diseño se invierte: la fricción deliberada es el
mecanismo que mantiene al humano en control. Un UX checkpoint es un momento explícito en
el flujo donde el agente pausa para obtener validación, confirmación o corrección humana
antes de continuar. No son interrupciones al flujo — son la arquitectura que hace al flujo
confiable. Brugnoli identifica tres funciones que un checkpoint bien diseñado cumple:
control (crear puntos de decisión antes de acciones irreversibles), transparencia (exponer
el razonamiento del agente en términos humanos) y consistencia (establecer patrones
predecibles que permiten al usuario construir un modelo mental del sistema). El diseño ya
no pregunta "¿dónde está la fricción y cómo la elimino?" sino "¿dónde está la decisión
humana y cómo la preservo?"

## Por qué importa
Durante dos décadas, el objetivo central del diseño UX fue el "frictionless journey":
eliminar pasos innecesarios, reducir clics, acortar el camino entre intención y resultado.
Esa aspiración era correcta para software operado por humanos. En sistemas agénticos, ese
mismo principio aplicado sin distinción produce sistemas opacos donde el usuario va de
intención a resultado sin haber sido consultado. Ejemplos bien ejecutados: Klarna hace
handoff explícito cuando detecta problemas; Duolingo ofrece "Explain My Answer" después
de cada pregunta. Ninguno es una interrupción ad-hoc — son momentos planificados con
propósito. Cuando los checkpoints están ausentes, la investigación muestra un patrón
consistente: ante un resultado incorrecto, los usuarios no intentan corregirlo de forma
incremental. Reinician la conversación desde cero. El costo de no tener checkpoints no
es solo de experiencia — es de confianza estructural.

## Tensiones y límites
Un checkpoint mal diseñado produce el efecto opuesto: fricción sin valor, que erosiona
la confianza en lugar de construirla. El criterio de calidad es que el checkpoint debe
sentirse como una oportunidad para el usuario — para orientar, confirmar, corregir —
no como un obstáculo burocrático. La frecuencia óptima varía por contexto: en B2C
(e-commerce, viajes) los usuarios esperan velocidad con checkpoints solo en decisiones
de alto impacto; en B2B (finanzas, salud, legal) se esperan más puntos de control y
trazabilidad. El diseño del checkpoint no es universal — es una calibración caso a caso
entre autonomía del agente y control humano requerido.
