---
titulo: "Métricas post-pantalla"
tipo: concepto
fecha: 2026-04-20
categoria: producto
familia: agencia-ia
estado: activo
tags: [producto, evaluacion, agentes, ia, criterio]
relacionado: [feedback-que-escala, las-tres-caras-del-producto-agentico, arnes-del-agente]
fuentes:
  - titulo: "AI Agent Metrics: How Elite Teams Evaluate"
    url: "https://galileo.ai/blog/ai-agent-metrics"
    fecha_acceso: 2026-04-20
  - titulo: "Evaluating AI agents: Real-world lessons from building agentic systems at Amazon"
    url: "https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/"
    fecha_acceso: 2026-04-20
  - titulo: "La era de los productos agénticos: rediseñando para agentes de inteligencia artificial"
    autor: "Martín Alaimo"
    fecha_acceso: 2026-04-20
---

# Métricas post-pantalla

## El concepto
Las métricas de engagement clásicas — time on site, page views, bounce rate, conversión
por clic, tiempo en pantalla — asumen un humano mirando y tomando decisiones con los ojos
y los dedos. Cuando el usuario es un agente que entra, ejecuta y sale en milisegundos,
esas métricas no solo pierden valor: activamente engañan. Un agente no tiene bounce rate
significativo, no tiene tiempo en pantalla medible, no hace clics. Un sistema optimizado
para esas métricas puede estar perfectamente calibrado para humanos y completamente roto
para agentes — y los dashboards existentes no lo capturan.

Las nuevas métricas relevantes operan en tres niveles: **sesión** (¿el agente completó
todos los objetivos?), **flujo de trabajo** (¿avanzó sin estancarse?, ¿eligió las
herramientas correctas?), y **operación granular** (¿llegó al resultado sin pasos
innecesarios?, ¿su razonamiento fue coherente?). Cada nivel captura un tipo distinto
de falla que el nivel anterior no detecta.

## Por qué importa
Las organizaciones optimizan lo que miden. Si las métricas siguen siendo las de la era
de pantallas, los equipos seguirán optimizando para humanos aunque el tráfico agéntico
crezca. La transición a métricas post-pantalla no es solo técnica — es un cambio en la
definición de éxito del producto.

El problema es más urgente de lo que parece: GA4 y Mixpanel fallan como instrumentos de
medición en contextos agénticos. GA4 aplica bot filtering por defecto usando listas IAB
que no cubren agentes modernos, y no permite auditarlo ni desactivarlo. Mixpanel registra
eventos de agentes como si fueran usuarios — y esos eventos son inmutables, no se pueden
eliminar del historial. El 63% de los sitios web ya recibe tráfico de agentes de IA en
2026 (con ChatGPT generando el 50% de ese tráfico), pero la mayoría de los equipos opera
con dashboards que no distinguen ese tráfico del humano.

## Datos y evidencia
- **Solo el 15% de los equipos** logra cobertura de evaluación de agentes de nivel élite
  (90-100% de comportamientos evaluados); el 72% cree que el testing comprehensivo importa
  — brecha de percepción del 57% (Galileo AI, 2026)
- **Action Advancement score >0.7** indica progreso claro del agente en el flujo de trabajo;
  **<0.3** indica estancamiento — umbrales documentados por Galileo como señales operacionales
  concretas (Galileo AI, 2026)
- **63% de sitios web** ya recibe tráfico de agentes IA en 2026; ChatGPT genera el 50%
  de ese tráfico de agentes (Plausible Analytics / PassionFruit, 2026)
- **GA4** aplica bot filtering vía listas IAB que los agentes modernos eluden fácilmente;
  el filtro no es configurable ni auditable por el usuario (Google Analytics Help, 2026)
- **Quantum Metric** declaró 2025 como año de transición hacia "agentic analytics" —
  dashboards que no solo diagnostican fricción sino que sugieren y ejecutan optimizaciones
  de forma autónoma (Quantum Metric, 2026)

## Framework de métricas post-pantalla (nivel operacional)
El sistema de métricas emergente opera en tres capas:

| capa | métrica | señal de falla |
|------|---------|----------------|
| Sesión | Action Completion | el agente no completó todos los objetivos del usuario |
| Flujo | Action Advancement | score <0.3; Tool Selection Quality bajo |
| Operación | Agent Efficiency | pasos innecesarios para llegar al resultado |

Estas métricas no reemplazan las clásicas para el tráfico humano — coexisten. El reto
de producto es instrumentar ambas capas simultáneamente y distinguir el tráfico.

## Tensiones y límites
No todos los productos tienen tráfico agéntico significativo hoy. Invertir en rediseñar
el sistema de métricas antes de que ese tráfico exista puede ser prematuro. El criterio
de decisión es observacional: ¿hay patrones de tráfico que no corresponden a comportamiento
humano típico? ¿Hay transacciones completadas sin sesión de usuario asociada? El 63% de
sitios ya afectados (2026) sugiere que la pregunta correcta no es "¿cuándo llega el
tráfico agéntico?" sino "¿cuánto ya tengo sin haberlo medido?"

Esta es la misma lógica de `feedback-que-escala`: el problema no es que el feedback sea
incorrecto — es que el sistema de medición produce feedback sobre lo que ya no importa.

## Ejes investigados
1. **Framework de métricas específicas para agentes** — Encontrado: Galileo propone
   6 métricas en 3 niveles con umbrales numéricos concretos. AWS también documenta
   evaluación multidimensional desde producción real.
2. **Falla de herramientas analíticas actuales con tráfico agéntico** — Confirmado:
   GA4 y Mixpanel no distinguen agentes de humanos por diseño; la magnitud del problema
   es mayor de lo esperado (63% de sitios ya afectados).
3. **Adopción de analytics agéntico en empresas** — Confirmado: Quantum Metric como
   caso concreto de pivot hacia "agentic analytics" en 2025-2026.
