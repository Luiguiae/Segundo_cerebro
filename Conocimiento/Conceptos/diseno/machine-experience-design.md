---
titulo: machine-experience-design
tipo: concepto
fecha: 2026-04-27
categoria: diseno
tags: [mx-design, machine-readable, ai-agents, legibilidad-semantica, human-centered-design]
estado: activo
relacionado: [colonialismo-cultural-digital, arquitectura-de-inteligencia, quien-controla-el-prompt, diseno-uxui-y-ia, disenador-a-constructor, capital-de-contexto]
fuentes:
  - titulo: "2026 State of AI Traffic & Cyberthreat Benchmark Report"
    url: "https://www.humansecurity.com/learn/resources/2026-state-of-ai-traffic-cyberthreat-benchmarks/"
    fecha_acceso: 2026-04-27
  - titulo: "Inside AI Traffic's 796% Growth"
    url: "https://www.webfx.com/blog/seo/gen-ai-search-trends/"
    fecha_acceso: 2026-04-27
  - titulo: "The Rise of Machine Experience (MX): Designing for AI Agents"
    url: "https://strategichumanist.substack.com/p/machine-experience-mx-design-ai-agents"
    fecha_acceso: 2026-04-27
  - titulo: "Is your website ready for AI agents in 2026?"
    url: "https://www.dwmedia.com/blog/is-your-website-ready-for-ai-agents-in-2026/"
    fecha_acceso: 2026-04-27
  - titulo: "Machine Experience (MX): Designing experiences for a new type of user"
    url: "https://excopartners.com/2025/10/15/machine-experience-mx-designing-experiences-for-a-new-type-of-user"
    fecha_acceso: 2026-04-27
---

# Machine Experience Design

## El concepto

Machine Experience Design (MX Design) es la disciplina que diseña artefactos digitales
para ser legibles y utilizables por agentes de inteligencia artificial, que actúan como
el primer decoder del contenido antes de que ningún usuario humano llegue a él. Así como
el UX Design lleva décadas refinando artefactos para necesidades humanas —percepción
visual, respuesta emocional, intuición navegacional— MX Design construye el equivalente
para audiencias algorítmicas: estructura semántica, datos estructurados, jerarquía de
encabezados predecible, y metadatos que comunican intención.

El cambio estructural no es de herramientas sino de orden de audiencia. Hasta 2023, el
humano era el primer y único decoder de cualquier artefacto digital. Desde 2024, los
agentes IA (ChatGPT, Perplexity, Gemini, los agentic browsers de OpenAI y Perplexity)
interceptan, interpretan y resumen contenido antes de entregarlo —o no entregarlo— al
usuario humano. El diseñador que sigue produciendo solo para percepción humana está
diseñando para la segunda audiencia que lee su trabajo.

La pila técnica de MX Design incluye capas que evolucionaron en paralelo al diseño visual
sin integrarse: JSON-LD y vocabularios de Schema.org para datos estructurados, HTML
semántico con jerarquía de encabezados clara, llms.txt (el equivalente de robots.txt para
modelos de lenguaje), y el Model Context Protocol (MCP, Anthropic, 2024) como estándar
emergente de interoperabilidad entre fuentes de datos y agentes. Cada capa responde a la
misma pregunta: ¿puede una máquina entender esto lo suficientemente bien como para
representarlo con precisión?

## Por qué importa

La audiencia dual —humanos + máquinas— no es una evolución gradual del diseño: es un
cambio en el orden de llegada. Los agentes IA actúan como gatekeepers antes de que
cualquier usuario humano tome una decisión de navegación. Las marcas que no diseñan para
esta primera capa de legibilidad son invisibles antes de que ningún humano llegue a verlas.

Para el diseñador-constructor, esto convierte la legibilidad semántica en una competencia
de primer orden disfrazada durante años de competencia técnica de SEO. No es
optimización: es diseño de la estructura que comunica intención a un decoder que no tiene
ojos, no sigue flujos emocionales, y no hace inferencias visuales. El diseñador que no
incorpora esta capa en su workflow está construyendo para una audiencia que ya no es la
primera.

## Datos y evidencia

- El tráfico de agentes IA creció **7,851% año a año** entre 2024 y 2025. HUMAN Security,
  "2026 State of AI Traffic & Cyberthreat Benchmark Report" (marzo 2026), análisis de
  tráfico global de 2025. El tráfico de training crawlers representa el 67.5% del total
  de tráfico IA, pero su participación cayó mientras el tráfico agéntico creció.

- El tráfico referido por plataformas de IA generativa creció **796% de enero 2024 a
  diciembre 2025**, con conversiones creciendo **6,432% YoY** en el mismo período. WebFX,
  análisis sobre 2.3 billion sesiones de sitios web (2025-2026).

- **ChatGPT concentra el 77.97%** de todo el tráfico referido por IA; Perplexity
  representa el 15.10% (19.73% en EEUU). El tráfico referido por Gemini creció 388%
  entre septiembre y noviembre de 2025. SE Ranking AI Traffic Research Study, 2025.

- El tráfico referido por IA era solo **1.08% del tráfico web total** a noviembre 2025,
  pero convierte **1.2x mejor que búsqueda orgánica** y genera el 19% del pipeline inbound
  cualificado en firmas donde representa apenas el 4% de sesiones.

- El tráfico de referencia de Google a publishers cayó **38% año a año** en EEUU durante
  2025 (Press Gazette, Trends Report 2026). El CTR en queries con AI Overviews cayó
  **61%** entre junio 2024 y septiembre 2025 (DataSlayer, 2025).

- Google AI Overviews aparece en **2 billion consultas por mes** (Google, 2025). Las
  marcas citadas en AI Overviews reciben **35% más de CTR orgánico** que las no citadas.

- A abril 2026, ninguna plataforma IA mayor ha comprometido oficialmente leer `llms.txt`
  como input de primer nivel, pero frameworks RAG y herramientas de desarrollo (Cursor,
  Continue, Aider) sí lo procesan cuando está presente. El Model Context Protocol (MCP),
  introducido por Anthropic a finales de 2024, se está convirtiendo en el estándar por
  defecto para conectar datos y herramientas a agentes IA.

## Tensiones y límites

**La tensión con `colonialismo-cultural-digital` es directa y no resuelta.** El vault ya
documenta que los filtros de legibilidad algorítmica reproducen asimetría cultural: lo que
no es legible para el sistema simplemente no existe. MX Design no resuelve esa asimetría;
propone optimizar para ella. Un diseñador del Sur Global que sigue las guías de MX Design
está optimizando sus artefactos para los estándares de legibilidad definidos por
infraestructura de IA entrenada predominantemente en inglés y normas occidentales. La
legibilidad machine-readable hereda los sesgos del corpus de entrenamiento. Optimizar para
MX Design sin criticar el sistema que define qué es "legible" es aceptar la colonización
como condición de visibilidad.

**La paradoja del diseño human-centered**: La definición fundacional de HCD asume que el
artefacto se diseña y evalúa desde las necesidades del usuario humano. MX Design no
reemplaza HCD —propone una capa previa obligatoria: si el artefacto no supera el filtro
algorítmico, el usuario humano nunca llega a evaluarlo. El diseñador opera en dos etapas
secuenciales: legibilidad para máquinas primero, experiencia para humanos segundo. La
pregunta que MX Design no responde: cuando los requisitos de legibilidad algorítmica
contradicen los requisitos de experiencia humana, ¿cuál cede?

**El riesgo de sobre-optimización**: Diseñar primariamente para legibilidad algorítmica
puede producir contenido semánticamente correcto pero humanamente estéril. La estructura
que los modelos prefieren —jerarquía clara, entidades bien definidas, datos explícitos—
puede entrar en conflicto con las formas narrativas, visuales o no lineales que comunican
mejor para ciertas audiencias o culturas humanas.

**El límite del estándar llms.txt**: A diferencia de robots.txt, no hay consenso de
adopción entre plataformas. Es una señal de intención, no un mecanismo de garantía. El
campo de estándares MX está en formación, no en madurez.

## Ejes investigados

**Eje 1 — Estándares técnicos de legibilidad machine-readable**
Qué estándares están emergiendo para hacer contenido procesable por agentes IA. Encontré
tres capas activas: llms.txt (en adopción comunitaria pero sin compromiso oficial de
plataformas mayores a abril 2026), JSON-LD (recomendado oficialmente por Google desde mayo
2025), y MCP de Anthropic (2024) como estándar de interoperabilidad para agentes. El
ecosistema de estándares existe pero no está consolidado — campo en formación. Fuentes:
documentación de Google Search Central, ALLMO.ai reporte llms.txt 2026, ExcoPartners
(oct 2025).

**Eje 2 — AI agents como primer decoder: escala y evidencia**
Qué datos existen sobre el volumen e impacto real del tráfico de agentes IA. Datos
convergentes de tres fuentes independientes: HUMAN Security (7,851% crecimiento YoY de
tráfico agéntico, marzo 2026), WebFX (796% crecimiento en tráfico referido por IA
generativa, 2.3B sesiones), SE Ranking (distribución de cuota por plataforma, 2025). El
dato crítico: este tráfico convierte mejor que el orgánico — los agentes IA ya son filtros
de decisión pre-humanos con impacto comercial medible, no solo intermediarios informativos.

**Eje 3 — Tensión con diseño human-centered y framework dual-audience**
Cómo la comunidad de diseño está resolviendo la coexistencia de HCD y MX Design. El campo
está fragmentado: Strategic Humanist Substack ("Human Patterns in the Machine Age", 2025)
propone MX como disciplina paralela a UX; marcos de Human-AI Co-Creation (CHI 2024)
intentany absorber MX dentro de HCD extendido. La tensión con `colonialismo-cultural-digital`
no aparece resuelta en la literatura — es un gap que el vault puede ocupar de forma única.
