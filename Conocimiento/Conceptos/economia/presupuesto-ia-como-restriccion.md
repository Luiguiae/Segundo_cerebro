---
titulo: El presupuesto de IA como restricción operativa
tipo: concepto
familia: transicion-ia
tags: [ia, infraestructura, organizacion, estrategia, trabajo]
relacionado: [ia-sin-ecosistema, impuesto-de-verificacion, capital-de-contexto]
fecha: 2026-06-12
estado: activo
fuentes:
  - titulo: "The token bill comes due: Inside the industry scramble to manage AI's runaway costs"
    url: "https://www.google.com/url?q=https://techcrunch.com/2026/06/05/the-token-bill-comes-due-inside-the-industry-scramble-to-manage-ais-runaway-costs/&source=gmail&ust=1781334351936000&sa=E"
    fecha_acceso: 2026-06-12
  - titulo: "AI Spending Per Employee: The $2,068 Benchmark Your CFO Needs"
    url: "https://www.google.com/url?q=https://rize.io/blog/ai-spending-per-employee-benchmark&source=gmail&ust=1781334351936000&sa=E"
    fecha_acceso: 2026-06-12
  - titulo: "Uber caps employee AI spending after blowing through budget in four months"
    url: "https://www.google.com/url?q=https://techcrunch.com/2026/06/02/uber-caps-employee-ai-spending-after-blowing-through-budget-in-four-months/&source=gmail&ust=1781334351936000&sa=E"
    fecha_acceso: 2026-06-12
  - titulo: "AI tokens: How to navigate AI's new spend dynamics | Deloitte Insights"
    url: "https://www.google.com/url?q=https://www.deloitte.com/us/en/insights/topics/emerging-technologies/ai-tokens-how-to-navigate-spend-dynamics.html&source=gmail&ust=1781334351936000&sa=E"
    fecha_acceso: 2026-06-12
  - titulo: "Botanu Emerges from Stealth, Reveals Enterprises Spend $186M Annually on AI With Little Proof of ROI"
    url: "https://www.google.com/url?q=https://www.globenewswire.com/news-release/2026/06/11/3310447/0/en/Botanu-Emerges-from-Stealth-Reveals-Enterprises-Spend-186M-Annually-on-AI-With-Little-Proof-of-ROI.html&source=gmail&ust=1781334351936000&sa=E"
    fecha_acceso: 2026-06-12
  - titulo: "LLM Cost Optimization and Multi-Model Routing — How to Cut AI Costs by 60%"
    url: "https://www.google.com/url?q=https://atlosz.hu/en/blog/llm-koltsegoptimalizalas-routing-strategia/&source=gmail&ust=1781334351936000&sa=E"
    fecha_acceso: 2026-06-12
---

# El presupuesto de IA como restricción operativa

## El concepto

La IA fue adoptada como multiplicador de productividad que se pagaría a sí misma. En 2026 se convirtió en el principal problema de presupuesto de muchas organizaciones — y la productividad correspondiente no aparece en los estados financieros.

La economía del token invirtió la lógica que la industria usó para justificar la adopción. El precio por token cayó un 98% desde 2022 (GPT-4 equivalente: de $20 a $0.40 por millón de tokens). Sin embargo, el gasto empresarial en IA creció un 320% en el mismo período, pasando de $1.2M promedio anual por empresa en 2024 a $7M en 2026. Más barato por unidad no significa menos costo total: los equipos simplemente consumen más tokens, y los agentes los consumen a escala automáticamente.

El resultado es una nueva categoría de restricción operativa: no tecnológica sino económica. El presupuesto de IA dejó de ser una partida invisible del budget de TI y se convirtió en un ítem de board que requiere gobernanza activa. Uber agotó su presupuesto anual de AI coding en cuatro meses (a abril 2026). Sam Altman reconoció en junio 2026: "El tema nunca había surgido. La gente estaba totalmente contenta con lo que gastaba. Ahora es un issue enorme."

## Por qué importa

Cuando el presupuesto de IA se convierte en restricción operativa, diseñar cómo se usa la IA pasa de ser una decisión técnica a una decisión económica. Esto tiene tres consecuencias directas.

La primera es la aparición del model routing como disciplina de diseño: usar modelos más baratos para tareas simples, los más capaces para las complejas. Un equipo de desarrollo encontró que el 70% de sus requests (formateo, sintaxis, completions básicos) funcionaban perfectamente con modelos de $0.50–2/millón de tokens, y solo el 30% requería modelos de $30–60/millón. El ahorro resultante fue del 60–80% con impacto mínimo en calidad. Esto introduce una capa de decisión nueva: ¿qué tarea merece qué modelo?

La segunda consecuencia es que el capital de contexto adquiere retorno económico directo y medible. Prompts más precisos generan outputs correctos en menos tokens. Lo que antes era una ventaja competitiva abstracta ("el contexto es el activo") ahora tiene una línea de factura concreta. El diseñador-constructor que invierte en estructurar su contexto no solo mejora la calidad de los outputs — reduce el costo de producirlos.

La tercera transforma la estructura organizacional: emerge un nuevo perfil de gobernanza ("AI budget owner"). Deloitte publicó en abril 2026 la primera guía para CFOs sobre "token economics" — un concepto que no existía en el vocabulario financiero 18 meses antes. El token se convierte en la unidad atómica de medición del valor de la IA.

## Datos y evidencia

- $2,068/empleado/año: gasto promedio en IA en 2026 — 50% más que en 2025 ($1,358). El top 10% de empresas gasta $2,800+/empleado; el 50% del mercado gasta menos de $200. (Rize, 2026)
- $46/empleado/mes: mediana real de Ramp (abril 2026). Rango percentil 25–75: $3–$352 PEPM — diferencia de 100x entre empresas de la misma distribución.
- $186M: gasto anual promedio de enterprise en IA, con solo el 27% de ejecutivos reportando que cumplió expectativas de ROI. (Botanu, junio 2026)
- 13x: incremento en token spend desde enero 2025. (Deloitte, 2026)
- Uber: agotó su presupuesto anual de AI coding en 4 meses. (TechCrunch, junio 2026)
- 93% / 7%: del presupuesto de IA, el 93% va a tecnología (licencias, compute, tokens), solo el 7% a personas y workflows que generan el valor. 20% de las empresas capturan 74% de los retornos. (Deloitte State of AI 2026)
- $0.40 vs $30–60 por millón de tokens: rango actual de precios entre modelos pequeños (Llama, Mistral: $0.10–0.50) y premium (Claude Opus, GPT-4: $30–60). Model routing entre niveles → 60–80% ahorro para workloads mixtos.
- $20M → $2B en 36 meses: proyección de escala de costos para organizaciones con transformación agéntica completa. (Celonis Field CTO, 2026)

## Tensiones y límites

La tensión central es estructural: la misma IA que prometía pagar su propio costo al liberar tiempo humano generó una nueva categoría de gasto que no existía antes, sin que la productividad correspondiente sea visible en los libros. ia-sin-ecosistema ya captura que el ROI de la IA requiere activos complementarios; este concepto agrega que uno de esos activos complementarios es ahora la gobernanza del propio gasto en IA — un meta-problema que la IA creó para sí misma.

La segunda tensión afecta directamente al diseñador-constructor. Model routing resuelve el costo pero introduce una nueva capa de juicio: ¿qué tarea merece qué modelo? Esta decisión no puede delegarse fácilmente al agente, porque sería el agente decidiendo en qué modelo ejecutar sus propias tareas — un loop circular. El impuesto-de-verificacion se extiende aquí: no solo verificas el output, también debes verificar el modelo que lo produjo.

Límites del concepto: la restricción presupuestaria aplica principalmente a organizaciones con adopción a escala. Para el diseñador-constructor individual, el costo suele ser marginal y absorbible. La restricción se vuelve operativa cuando los agentes se convierten en productores autónomos de tokens sin supervisión humana sobre el volumen generado.

## Ejes investigados

Eje 1 — El shock real de gasto en IA empresarial (2026)
Búsqueda: datos concretos de cuánto gastan empresas, crecimiento YoY, casos documentados de presupuestos agotados. Encontrado: datos de Rize, Ramp, Botanu (junio 2026), TechCrunch (Uber), Deloitte, y declaración pública de Sam Altman. Mínimo 4 fuentes independientes confirmando el fenómeno. 6 fuentes sólidas totales.

Eje 2 — Model routing como respuesta técnica emergente
Búsqueda: qué están haciendo las organizaciones técnicamente para controlar costos. Encontrado: ecosistema de model routing madurando (MindStudio, Swfte, Atlosz). Datos de precios verificables: diferencia de 60–300x entre modelos premium y pequeños. Dato validado por múltiples fuentes: 70% de requests son simples, 30% requieren razonamiento. Ahorro realista: 60–80% en workloads mixtos. 4 fuentes sólidas.

Eje 3 — Cambio en la gobernanza organizacional del gasto en IA
Búsqueda: qué está cambiando estructuralmente en cómo las organizaciones gestionan el gasto. Encontrado: guía Deloitte para CFOs en abril 2026 (concepto inexistente 18 meses antes); Linux Foundation lanzando estándares de token usage en julio 2026; nuevo vocabulario: "token economics", "AI budget owner", "FinOps for AI". Dato estructural: 93% del presupuesto en tecnología, 7% en personas — exactamente el patrón de ia-sin-ecosistema. 3 fuentes sólidas.

Eje 7 — Cambio en la gobernanza organizacional del gasto en IA
Búsqueda: qué está cambiando estructuralmente en cómo las organizaciones gestionan el gasto. Encontrado: guía Deloitte para CFOs en abril 2026 (concepto inexistente 18 meses antes); Linux Foundation lanzando estándares de token usage en julio 2026; nuevo vocabulario: "token economics", "AI budget owner", "FinOps for AI". Dato estructural: 93% del presupuesto en tecnología, 7% en personas — exactamente el patrón de ia-sin-ecosistema. 3 fuentes sólidas.