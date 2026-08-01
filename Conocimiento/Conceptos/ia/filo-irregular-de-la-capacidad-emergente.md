---
titulo: "El filo irregular de la capacidad emergente del modelo"
tipo: concepto
familia: agencia-ia
tags: [ia, evaluacion, incertidumbre, producto, escala]
relacionado: [espectro-autonomia-agente, capital-de-contexto, impuesto-de-verificacion]
fecha: 2026-08-01
estado: borrador
fuentes:
  - titulo: "Anthropic's first technical PM on token maxing, the jagged edge, and living in the future | Dianne Penn"
    autor: "Dianne Penn (Lenny's Podcast)"
    url: "https://www.lennysnewsletter.com/p/anthropics-first-technical-pm-on"
    fecha_acceso: 2026-08-01
  - titulo: "Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of AI on Knowledge Worker Productivity and Quality"
    autor: "Dell'Acqua, McFowland, Mollick et al. (HBS / BCG)"
    url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321"
    fecha_acceso: 2026-08-01
  - titulo: "Predicting Emergent Capabilities by Finetuning"
    autor: "Snell, Wallace et al. (COLM 2024)"
    url: "https://arxiv.org/abs/2411.16035"
    fecha_acceso: 2026-08-01
  - titulo: "Large language models and emergence: a complex systems perspective"
    url: "https://royalsocietypublishing.org/rsta/article/384/2320/20250014/481676/Large-language-models-and-emergence-a-complex"
    fecha_acceso: 2026-08-01
  - titulo: "Evals are the new PRD"
    url: "https://www.braintrust.dev/blog/evals-are-the-new-prd"
    fecha_acceso: 2026-08-01
---

## El concepto

Las curvas de pérdida (loss) de los modelos de lenguaje siguen leyes de escala suaves y predecibles: cada duplicación de parámetros o datos produce ganancias proporcionales en perplexity. Pero las capacidades que emergen de esa pérdida no se comportan así. Un modelo puede fallar por completo una tarea en un checkpoint y dominarla con precisión en el siguiente, sin ninguna transición gradual visible desde el exterior.

Este fenómeno es el "filo irregular" (jagged edge o jagged frontier): la frontera entre lo que un modelo puede y no puede hacer no es una línea recta ni una curva predecible — es un contorno accidentado e incoherente con las intuiciones humanas sobre dificultad de tarea. Una operación aparentemente simple puede quedar fuera del filo; una que parece compleja puede estar profundamente dentro.

La causa subyacente es lo que la teoría del escalado llama "quantización": los modelos aprenden habilidades discretas (quanta) de forma abrupta, pero el agregado de miles de esas microemergencias produce curvas de loss lisas. Lo que parece suave a nivel de la función objetivo es, en realidad, la superposición estadística de incontables saltos invisibles.

## Por qué importa

La consecuencia directa es que cualquier roadmap de producto construido sobre mejora incremental de modelos es estructuralmente frágil. Si las capacidades saltan en vez de deslizarse, el plan que hoy tiene sentido puede quedar obsoleto en el próximo checkpoint — no por una decisión estratégica, sino por un salto emergente que nadie podía anticipar con los datos disponibles.

Dianne Penn, primera PM técnica de Anthropic y responsable de lanzar cada modelo desde Claude 2 hasta Fable 5, articula la respuesta operativa que esto genera: su equipo "sweats the tokens as much as the pixels" — lee transcripciones de fallas del modelo con el mismo rigor que antes se aplicaba a mockups pixel-perfect. La razón es exactamente el filo: sin métricas de evaluación continua, los saltos de capacidad quedan como "overhang" no aprovechado durante semanas o meses.

El corolario organizacional: planear sobre modelos de frontera exige experimentación constante y un sistema de detección (evals) que funcione como radar de capacidad, no como validación puntual. La unidad de trabajo ya no es el PRD trimestral — es el suite de evaluación que puede correr contra cada nuevo checkpoint y detectar cuándo un umbral fue cruzado.

## Datos y evidencia

- **HBS / BCG, experimento de campo 2023 → publicado en Organization Science 2025:** 758 consultores de BCG asignados aleatoriamente a tareas con y sin GPT-4. Para tareas *dentro* del filo: +12.2% de tareas completadas, +25.1% de velocidad, calidad evaluada +40% superior por evaluadores humanos. Para tareas *fuera* del filo: los usuarios con IA rindieron **19 puntos porcentuales peor** que los que trabajaron sin ella. El mismo modelo, según qué lado del filo estaba la tarea. Fuente: [Dell'Acqua, Mollick et al., SSRN 4573321](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321)

- **COLM 2024 (arXiv 2411.16035):** "Predicting Emergent Capabilities by Finetuning" (Snell, Wallace et al.) propone "emergence laws" — funciones paramétricas ajustadas sobre modelos pequeños que predicen cuándo emergerá una capacidad en modelos con hasta **4x más compute**, con un error menor a **0.1 nats**. Validado sobre MMLU, GSM8K, CommonsenseQA y CoLA. Fuente: [arXiv:2411.16035](https://arxiv.org/abs/2411.16035)

- **Anthropic, julio 2026:** Dianne Penn declara que su equipo escribe **30-40 ejemplos representativos por feature** (cada uno: prompt + respuesta ideal "golden answer") como artefacto primario de producto. Los PRDs persisten para alinear ingeniería, legal y seguridad, pero el eval es el núcleo del trabajo de definición de producto. Fuente: [Lenny's Podcast, 2026-07-26](https://www.lennysnewsletter.com/p/anthropics-first-technical-pm-on)

- **Royal Society, 2025:** los LLMs son sistemas dinámicos complejos; las capacidades emergentes resultan de interacciones cooperativas no lineales entre unidades — análogas a transiciones de fase en sistemas de materia condensada, no extrapolables linealmente de parámetros individuales. Fuente: [Philosophical Transactions of the Royal Society A, 384(2320)](https://royalsocietypublishing.org/rsta/article/384/2320/20250014/481676/Large-language-models-and-emergence-a-complex)

## Tensiones y límites

**El filo puede ser un artefacto de métrica, no de capacidad.** Schaeffer et al. (2023) argumentan que los saltos aparentes en capacidad desaparecen cuando se reemplazan métricas discretas (acierto/fallo) por métricas continuas como Brier score o Token Edit Distance. Bajo esas métricas, el mismo modelo mejora de forma suave y predecible a través de los checkpoints. Esto no invalida el fenómeno operativo — las métricas discretas son las que los equipos de producto usan en producción — pero obliga a ser preciso: el filo es real como experiencia de gestión de producto, aunque su base física sea más continua de lo que aparenta.

**La predicción parcial ya es posible.** El trabajo de COLM 2024 erosiona parcialmente la afirmación de que "los saltos son impredecibles": son anticipables si inviertes en construir emergence laws antes de escalar, usando modelos de finetuning a pequeña escala. El problema práctico es que esa inversión requiere infraestructura de evaluación que pocos equipos de producto tienen, lo que convierte la predictibilidad en un privilegio de los labs grandes, no una herramienta disponible para equipos de producto medianos.

**El filo se mueve, pero no en la dirección que el equipo necesita.** Lo que estaba fuera del filo hace seis meses puede estar profundamente dentro hoy — pero también lo contrario: un modelo de frontera puede retroceder en una capacidad específica al ser fine-tuneado para otra. Tratar "la IA no puede hacer X" como conclusión permanente es un error estructural; pero asumir que el filo siempre avanzará hacia donde el equipo necesita también es riesgo de planning. La incertidumbre es bidireccional.

## Ejes investigados

**Eje 1 — Evidencia empírica del fenómeno (¿el filo es real y cuantificable?):** búsqueda en literatura de scaling laws, papers sobre emergencia en LLMs, y estudios de campo con usuarios reales. 4 fuentes sólidas: estudio HBS/BCG (758 consultores, datos de campo cuantificados), Royal Society 2025 (marco de sistemas complejos), arXiv 2411.16035 (emergence laws con predicción experimental), debate de métrica de Schaeffer et al.

**Eje 2 — Consecuencias para product planning (¿cómo cambia el roadmap?):** búsqueda en artículos de producto, estrategia y gestión de equipos sobre planificación bajo incertidumbre de capacidad de IA. 3 fuentes sólidas: análisis "Roadmaps After Frontier Models" (Medium, jun 2026), Digital Economy Dispatch sobre bottlenecks y jagged edges, oneusefulthing.org sobre jaggedness y salients. Eje central: el filo convierte el planning determinístico en planning experimental con ciclos cortos de detección.

**Eje 3 — Evals como metodología de respuesta operativa (¿qué hace un equipo con esto?):** búsqueda sobre eval-driven development, reemplazo del PRD por evals, y metodología pública de Anthropic. 3 fuentes sólidas: Dianne Penn en Lenny's Podcast (jul 2026), Braintrust "Evals are the new PRD", Arize AI sobre construcción de evals confiables para agentes.
