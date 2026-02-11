---
titulo: "ADR-000: Inicio del proyecto Wayta IA"
tipo: adr
estado: aceptado
autor: Luigui Avila
fecha: 2026-01-24
updated: 2026-02-10
tags: [wayta-ia, mvp, delivery, ia]
fuentes:
  - Documentos/00-start-here/README.md
---

# ADR-000 — Inicio del proyecto Wayta IA

## Decisión
Iniciar Wayta IA como un proyecto de delivery con el objetivo explícito de
diseñar, implementar y disponibilizar un producto o MVP funcional de forma
individual, utilizando herramientas de IA como soporte principal, sin
dependencia estructural de otros actores humanos.

## Contexto
La proliferación de herramientas de IA promete autonomía individual en diseño,
desarrollo y despliegue de productos. Sin embargo, la mayoría de iniciativas
siguen dependiendo de equipos humanos especializados para ejecución técnica,
operativa o de go-to-market.

Wayta IA surge como una prueba concreta y aplicada: validar hasta qué punto una
persona puede asumir de extremo a extremo el ciclo completo de un producto
(diseño → implementación → disponibilidad) apoyándose en IA como capacidad
extendida, no como simple asistente.

## Problema que se busca aclarar (no resolver aún)
- ¿Dónde realmente se rompe la autonomía individual hoy?
- ¿Qué partes del delivery siguen siendo cuellos de botella humanos?
- ¿Qué tipo de producto es viable bajo esta lógica y cuál no?
- ¿Qué nivel de calidad es alcanzable sin equipo?

## Alcance inicial
Incluye:
- Definición de una propuesta de valor clara.
- Diseño funcional del producto o servicio.
- Implementación técnica del MVP.
- Puesta a disposición (deploy, acceso, uso real).

Excluye (por ahora):
- Escalabilidad masiva.
- Optimización extrema de performance.
- Branding o marketing avanzado.
- Gobierno corporativo o compliance complejo.

## Criterios de éxito tempranos
- Existe un artefacto usable por al menos un usuario externo.
- El producto puede ejecutarse sin intervención manual constante.
- El proceso completo fue diseñado y ejecutado por una sola persona.
- Las decisiones clave quedan documentadas y reproducibles.

## Riesgos asumidos explícitamente
- Calidad subóptima frente a soluciones de equipo.
- Sobre-ingeniería innecesaria.
- Dependencia excesiva de tooling de IA específico.
- Fatiga cognitiva por rol múltiple (diseño + tech + ops).

## Decisión futura abierta
Este ADR se revisará una vez exista un MVP funcional para decidir si:
- Wayta IA escala,
- se convierte en framework,
- o se documenta como experimento cerrado.
