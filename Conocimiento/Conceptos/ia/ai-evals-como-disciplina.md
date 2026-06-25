---
titulo: "AI Evals como disciplina de producto"
tipo: concepto
familia: epistemologia-practica
fecha: 2026-05-18
estado: activo
tags: [ia, producto, validacion, evaluacion, criterio]
relacionado:
  - fabrica-oscura-de-software
  - spec-driven-development
  - vibe-coding
fuentes:
  - titulo: "Evals: El nuevo testing de productos IA — Vamos Por Partes (Martín Alaimo)"
    url: "https://www.youtube.com/watch?v=QCUi7pmPUxY"
    fecha_acceso: 2026-05-18
  - titulo: "LLM-as-a-Judge Simply Explained — Confident AI"
    url: "https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method"
    fecha_acceso: 2026-05-18
  - titulo: "Golden datasets: Creating evaluation standards — Statsig"
    url: "https://www.statsig.com/perspectives/golden-datasets-evaluation-standards"
    fecha_acceso: 2026-05-18
  - titulo: "LLM Monitoring & Evaluation for Real-World Production Use — Langwatch"
    url: "https://langwatch.ai/blog/llm-monitoring-evaluation-for-real-world-production-use"
    fecha_acceso: 2026-05-18
  - titulo: "LLM Evaluation Frameworks 2025 vs 2026 — ML AI Digital"
    url: "https://www.mlaidigital.com/blogs/llm-evaluation-frameworks-2025-vs-2026-what-matters-now-2026"
    fecha_acceso: 2026-05-18
---

# AI Evals como disciplina de producto

## El concepto

AI Evals (evaluaciones de IA) es el conjunto de metodologías estructuradas para medir si un sistema basado en LLMs hace lo que se supone que debe hacer — no de forma subjetiva, sino sistemática y reproducible. A diferencia del testing clásico que verifica resultados determinísticos, los evals trabajan con outputs probabilísticos: el mismo input puede producir respuestas distintas, igualmente válidas o igualmente incorrectas, sin que ningún assert tradicional lo detecte.

El núcleo de la disciplina son tres tipos de jueces: el **evaluador determinístico** (reglas exactas: ¿mencionó la palabra prohibida?, ¿el JSON tiene el campo requerido?), el **LLM-as-judge** (un modelo evalúa el output de otro modelo usando rúbricas definidas), y el **evaluador humano** (criterio experto para casos donde la calidad no se puede codificar). Ninguno funciona solo — la arquitectura de madurez es por capas: se automatiza lo determinístico, se escala con LLM-as-judge, y se calibra con humanos en los bordes.

El segundo pilar son los **golden datasets**: conjuntos de casos de prueba con respuestas verificadas por humanos que sirven como ground truth. Un golden dataset no es estático — cada fallo en producción es un candidato a entrar al dataset. La taxonomía de fallos importa tanto como los casos en sí: distinguir si el modelo alucinó datos, siguió instrucciones incorrectamente, o ignoró contexto relevante define acciones de corrección distintas.

## Por qué importa

El vault ya documenta el problema en `fabrica-oscura-de-software` ("vibe testing no alcanza") pero no tiene el concepto solución. Los evals son la respuesta estructural: sin ellos, el ciclo de desarrollo de productos IA opera en un loop donde se percibe que el sistema funciona hasta que falla de una forma que nadie anticipó — y nadie sabe cuándo va a volver a fallar.

La tensión fundacional es de epistemología del producto: el vibe testing optimiza para que *parezca* que funciona; los evals prueban que *falla* de formas específicas. Esta distinción define dos culturas de producto completamente distintas. Además, los LLMs cambian cada semana — un modelo que pasó evals en enero puede fallar en marzo porque el proveedor actualizó los pesos. Los evals en producción (online evaluation) son el único mecanismo que detecta ese drift antes de que afecte a usuarios reales.

La razón por la que esto es trabajo de Producto y no solo de Engineering: la pregunta central de los evals ("¿qué cuenta como correcto?") no se puede programar. Requiere criterio sobre el dominio, el usuario, y las consecuencias del error. Definir la rúbrica de un eval es tomar una decisión de producto.

## Datos y evidencia

- **85%** de acuerdo entre GPT-4 como juez y anotadores humanos — superior al 81% de acuerdo promedio entre dos humanos en las mismas tareas (MT-Bench benchmark, Lmsys.org, 2024).
- **>50%** de error en tests de bias avanzados para modelos frontier usados como jueces, según JudgeBiasBench (Hongli Zhou et al., EMNLP Findings 2025) — el LLM-as-judge no es neutral.
- **43%** de los fallos en sistemas IA en producción se originan en evaluación pre-despliegue insuficiente (Berkeley AI Research, 2025).
- Organizaciones con workflows estructurados de evaluación reportan hasta **60% menos incidentes en producción** frente a equipos sin procesos de eval (Stanford Center for Research on Foundation Models, Stanford HAI AI Index 2025).
- El criterio más ejecutado en G-Eval es "answer correctness" — corrió más de **8 millones de veces** solo en marzo 2025 (Confident AI, 2025).
- Las tasas de alucinación van del **10% al 82%** dependiendo del modelo y el método de prompting; los 5 modelos top en 2025 se agrupan entre 10% y 20% (LLM Hallucination Leaderboard, 2025).

## Tensiones y límites

**El juez también es un LLM.** LLM-as-judge introduce sesgos propios: preferencia por respuestas más largas, por respuestas que imitan el estilo del evaluador, por outputs que suenan seguros aunque sean incorrectos. Un eval con LLM-as-judge que no ha sido calibrado con humanos puede reproducir sistemáticamente los mismos errores que intenta detectar.

**El golden dataset se vuelve obsoleto.** Un dataset construido con casos de hace seis meses puede no reflejar los patrones de fallo actuales del modelo si el proveedor actualizó los pesos. Los evals requieren mantenimiento continuo — no son un artefacto que se construye una vez.

**El coverage es asintótico.** Los evals cubren los fallos que ya conoces. Los fallos más costosos en producción suelen ser los que ningún golden dataset anticipó — el "unknown unknown" del LLM. La disciplina de evals reduce frecuencia e impacto de los fallos conocidos, pero no puede garantizar ausencia de sorpresas.

**Costo de implementación.** Construir un eval framework robusto requiere tiempo de ingeniería y criterio de producto que equipos pequeños raramente tienen al mismo tiempo. El riesgo: evals con cobertura baja que dan confianza falsa, o sobre-instrumentación que frena el ciclo de iteración.

## Ejes investigados

**Eje 1 — Tipos de evaluadores y LLM-as-judge**
Busqué los tres tipos de jueces en eval frameworks 2025-2026: determinístico, LLM-as-judge, y humano. Fuentes: Confident AI, Evidently AI, Arize. La arquitectura de capas es consenso: automatizar lo determinístico, escalar con LLM, calibrar con humanos en los bordes. Hallazgo clave: GPT-4 como juez alcanza 85% de acuerdo con humanos, pero >50% de error en tests de bias avanzados — el rango de confiabilidad tiene límites documentados (JudgeBiasBench, EMNLP 2025). 3 fuentes sólidas encontradas.

**Eje 2 — Golden datasets y taxonomía de fallos**
Busqué cómo se construyen datasets de referencia y qué tipos de fallos se categorizan. Convergencia en tres fuentes (Statsig, Arize, Microsoft PromptFlow) sobre el principio: tratar cada fallo en producción como candidato a golden dataset. La taxonomía de fallos más extendida distingue: alucinación factual, seguimiento incorrecto de instrucciones, e ignorar contexto relevante. 3 fuentes sólidas encontradas.

**Eje 3 — Evals en producción (online evaluation)**
Busqué el estado del arte en monitoreo post-release. Distinción clave: offline evaluation (pre-release, dataset curado, gate de calidad) vs. online evaluation (post-release, tráfico real, safety net). Stanford HAI (2025 AI Index) y Berkeley AI Research (2025) cuantifican el impacto: 43% de fallos vienen de evaluación pre-despliegue insuficiente; equipos con eval estructurado tienen 60% menos incidentes. 4 fuentes sólidas encontradas.