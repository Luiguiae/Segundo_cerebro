---
titulo: "Spec-Driven Development"
tipo: concepto
familia: velocidad-output
tags: [codigo, construccion, ia, iteracion, estrategia]
relacionado: [vibe-coding, agentes-ia, mvp-a-prototipo-en-produccion]
edges:
  - target: vibe-coding
    tipo: contradicts
    why: "spec-driven-development fija el criterio de done antes de ejecutar; vibe-coding lo negocia en tiempo real con el output emergente. La tensión es estructural: el spec presupone que el problema es definible antes de resolverlo, lo que vibe-coding refuta al tratar la ejecución como proceso de descubrimiento."
fecha: 2026-04-07
estado: activo
---

## El concepto

Spec-Driven Development (SDD) es el principio de que todo lo que un agente de IA va a construir debe estar precedido por un documento de especificación que define el criterio de done antes de que el agente empiece. No es documentación — es una decisión sobre qué se está construyendo y por qué, cristalizada antes de delegar la ejecución.

Un spec mínimo define cuatro cosas antes de abrir el editor: el problema (qué situación del usuario estamos resolviendo, no qué feature estamos construyendo), el criterio de done (comportamiento observable, no "que se vea bien"), las restricciones (qué no puede hacer esta solución: stack, tiempo, complejidad aceptable), y el contexto de uso (quién lo usa, cuándo, con qué expectativas). Con ese spec, el agente tiene un ancla; sin él, cada sesión puede reinterpretar el objetivo.

## Por qué importa

Los agentes de IA son excelentes ejecutores pero pésimos definidores de objetivos. Si el criterio de "terminado" no existe antes de la sesión, el agente lo infiere — y puede inferirlo diferente en cada prompt. El resultado es un producto funcionalmente existente pero que nadie puede defender ni mantener, porque no hay contrato con el problema original.

La adopción masiva de vibe coding hizo este problema visible: equipos que iteraban rápido llegaban a versiones que parecían funcionales pero no tenían ningún ancla con lo que querían resolver. El spec es ese ancla. La secuencia sana: vibe coding para explorar → insight sobre qué construir → spec para cristalizarlo → agente para ejecutar.

## Tensiones y límites

El spec crea fricción al inicio: en proyectos exploratorios donde el problema no está claro, forzar un spec prematuro puede limitar el descubrimiento legítimo. Un spec mal escrito es peor que no tener spec: define el problema incorrecto con precisión. Existe tensión directa con vibe coding: la velocidad de exploración se pierde si cada sesión requiere un spec completo. La solución no es elegir uno sino saber cuándo usar cada uno: vibe coding para explorar, SDD para ejecutar lo que ya se sabe que hay que construir.
