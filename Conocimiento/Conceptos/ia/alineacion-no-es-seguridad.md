---
titulo: "Alineación ≠ Seguridad"
tipo: concepto
familia: ia
fecha: 2026-06-23
tags: [seguridad, alineacion, agentes, ia-safety, prompt-injection]
relacionado:
  - arnes-del-agente
  - gobernanza-ia-performativa
  - espectro-autonomia-agente
estado: activo
fuentes:
  - titulo: "Securing internal systems against increasingly capable and imperfectly aligned AI"
    url: "https://deepmind.google/blog/securing-the-future-of-ai-agents/"
    fecha_acceso: 2026-06-23
  - titulo: "Google DeepMind AI Control Roadmap: When Alignment Fails, Defense-in-Depth Takes Over"
    url: "https://www.techtimes.com/articles/318758/20260620/google-deepmind-ai-control-roadmap-when-alignment-fails-defense-depth-takes-over.htm"
    fecha_acceso: 2026-06-23
  - titulo: "Prompt injection still drives most agentic AI security failures in production"
    url: "https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/"
    fecha_acceso: 2026-06-23
  - titulo: "Prompt Injection Attacks in Large Language Models and AI Agent Systems"
    url: "https://www.mdpi.com/2078-2489/17/1/54"
    fecha_acceso: 2026-06-23
  - titulo: "International AI Safety Report 2026"
    url: "https://arxiv.org/pdf/2602.21012"
    fecha_acceso: 2026-06-23
---

# Alineación ≠ Seguridad

## El concepto

La narrativa dominante en IA safety asume que un agente bien alineado es un agente seguro. Esta equivalencia es falsa. La alineación y la seguridad son capas independientes que operan sobre objetos distintos: la alineación opera sobre las *intenciones del modelo* — qué quiere hacer, qué objetivos persigue. La seguridad opera sobre el *sistema que contiene al modelo* — qué puede hacer, con qué puede interactuar, cómo se monitorea y se detiene.

El AI Control Roadmap de Google DeepMind (18 jun 2026) hace esta distinción explícita. El framework trata a los propios agentes de DeepMind como *insider threats* — amenazas internas que podrían comprometerse — y construye 15 controles de sistema sobre esa hipótesis, independientemente de cuán bien alineados estén los modelos subyacentes. La premisa es directa: la alineación perfecta es una condición *insuficiente* para la seguridad en sistemas agénticos, y diseñar como si fuera suficiente es una apuesta que no se puede ganar.

El cambio filosófico que introduce: la seguridad de un agente deja de ser un problema de mejora del modelo y se convierte en un problema de arquitectura del sistema que lo contiene. Lo que antes se delegaba a la alineación ahora requiere infraestructura: Supervisor Agent para monitoreo en tiempo real, firma criptográfica de acciones del agente, kill switch, y controles mapeados en cuatro tiers de detección (D1–D4) y tres tiers de respuesta (R1–R3).

## Por qué importa

Un modelo perfectamente alineado puede ser manipulado vía prompt injection para actuar contra sus propias intenciones — y esto no constituye un fallo de alineación. El ataque opera en una capa anterior: instrucciones y datos externos comparten el mismo stream de tokens, y el modelo no puede distinguir confiablemente entre ambos. La alineación le dice qué *quiere* hacer; la arquitectura no le permite saber qué es instrucción legítima y qué es payload malicioso. Este es el "alignment paradox" que la literatura de seguridad lleva documentando desde 2024.

El análisis de más de un millón de tareas de codificación de agentes (DeepMind, jun 2026) añade un hallazgo contraintuitivo: la mayoría de eventos problemáticos no fueron ataques adversariales — fueron *over-diligence*, modelos persiguiendo los objetivos del usuario con demasiada agresividad, malinterpretando el alcance de sus permisos. Esto desacopla el diseño del arnés (`arnes-del-agente`) del diseño de la alineación: son capas que deben diseñarse separadamente aunque interactúen.

Para quien construye productos con agentes, la consecuencia es directa: no basta elegir un modelo "seguro" o "bien alineado". El diseño del arnés — permisos, sandboxing, monitoreo, límites de acción irreversible — es responsabilidad del producto, no del proveedor del modelo.

## Datos y evidencia

- **1M+ tareas de agentes analizadas (DeepMind, jun 2026):** la mayoría de eventos problemáticos correspondieron a "overzealous agents" — over-diligence, no ataques adversariales. Los modelos perseguían los objetivos del usuario con demasiada agresividad. Fuente: AI Control Roadmap, Google DeepMind, 2026-06-18.

- **Prompt injection = #1 vulnerabilidad, OWASP Top 10 LLM Applications 2025:** presente en más del 73% de deployments de producción evaluados en auditorías de seguridad. Fuente: OWASP 2025 / Help Net Security, jun 2026.

- **Tasa de éxito >85%** de ataques de prompt injection contra defensas de estado del arte cuando se emplean estrategias adaptativas, según meta-análisis de 78 estudios recientes. Solo 5 documentos diseñados específicamente pueden manipular respuestas de IA el 90% del tiempo vía RAG poisoning. Fuente: MDPI Information 17(1):54, ene 2026.

- **+32% de payloads maliciosos** embebidos en contenido web entre noviembre 2025 y febrero 2026 (Google researchers). Fuente: Help Net Security, jun 2026.

- **15 controles de sistema (DeepMind, jun 2026):** mapeados en D1–D4 (detección) y R1–R3 (respuesta y prevención). D1: monitoreo de chain-of-thought visible. D4: inspección de representaciones internas del modelo. R1: revisión asíncrona post-facto para acciones reversibles. R3: bloqueo sincrónico en tiempo real para acciones de alto riesgo. Controles de infraestructura, no ajustes al modelo. Fuente: AI Control Roadmap, Google DeepMind, 2026-06-18.

- **International AI Safety Report 2026 (arXiv 2602.21012):** la brecha entre capacidades de IA y técnicas de alineación se está *ampliando*, no cerrando. Alinear agentes individuales no garantiza seguridad a nivel de sistema.

## Tensiones y límites

La distinción alineación/seguridad como capas separadas es operacionalmente útil pero conceptualmente parcial. Un modelo con alineación suficientemente fuerte podría resistir prompt injection reconociendo la naturaleza del ataque — lo que la literatura llama "alignment-based defenses" (StruQ, SecAlign vía preference optimization). El argumento de DeepMind no es que la alineación no contribuye, sino que no es suficiente sola.

Segundo límite: la arquitectura de controles de DeepMind fue diseñada para sus propios sistemas internos, con capacidad plena de instrumentar el entorno de ejecución. En sistemas con arquitecturas heterogéneas — multi-tenant, APIs de terceros, pipelines de MCP — los mismos controles son significativamente más difíciles de implementar. La promesa de defense-in-depth no escala automáticamente.

Tercer límite: si la mayoría de incidentes son over-diligence y no ataques adversariales, el problema central de la seguridad agéntica tiene más en común con el diseño de permisos y la `gobernanza-ia-performativa` que con la seguridad ofensiva clásica. La terminología de "insider threat" puede llevar a sobreinvertir en detección de ataques y subinvertir en claridad de objetivos y alcance de acción.

## Ejes investigados

**Eje 1 — Prompt injection como paradoja de la alineación:**
Búsquedas sobre ataques de prompt injection en agentes alineados 2025-2026. Hallazgo central: el ataque opera en la capa arquitectónica (instrucciones y datos comparten token stream), no en la capa de intenciones del modelo. Tasa de éxito >85% contra defensas de estado del arte. OWASP confirma como vulnerabilidad #1 en 73% de deployments. Fuentes encontradas: 4 (OWASP/Help Net Security, MDPI ene 2026, Zylos Research abr 2026, Obsidian Security).

**Eje 2 — DeepMind AI Control Roadmap: 15 controles más allá de la alineación:**
Búsquedas sobre el AI Control Roadmap (18 jun 2026). Resultado: framework de defense-in-depth con 15 controles de infraestructura basados en 1M+ tareas de agentes. Hallazgo clave confirmado: over-diligence predomina sobre ataques adversariales. Arquitectura D1-D4 / R1-R3. Incluye Supervisor Agent, firma criptográfica y kill switch basados en MITRE ATT&CK adaptado. Fuentes encontradas: 5 (eWeek, Tech Jacks Solutions, TechTimes, Axios, Fortune jun 2026).

**Eje 3 — Brecha sistémica entre alineación y control:**
Búsquedas sobre la distinción formal alineación/seguridad y arquitecturas en capas para sistemas agénticos. Resultado: consenso emergente en industria y academia de que alinear agentes individuales no garantiza seguridad de sistema. International AI Safety Report 2026 (arXiv 2602.21012) confirma que la brecha se amplía. AWS, Bain y ARMO documentan patrones de defense-in-depth en producción. Fuentes encontradas: 4 (arXiv 2602.21012, AWS Security Blog, Bain & Company, ARMO).
