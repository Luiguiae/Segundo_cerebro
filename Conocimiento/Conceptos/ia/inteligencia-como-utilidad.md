---
titulo: "Inteligencia como utilidad"
tipo: concepto
fecha: 2026-06-13
familia: agencia-ia
categorias_secundarias: [economia]
tags: [ia, infraestructura, estrategia, poder, sistemas]
estado: activo
relacionado: [ia-sin-ecosistema, capital-de-contexto, arnes-del-agente]
fuentes:
  - titulo: "Gartner Predicts >90% LLM Inference Cost Reduction by 2030"
    url: "https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025"
    fecha_acceso: 2026-06-13
  - titulo: "Why Intuit's CEO thinks the market's wrong on AI — Semafor"
    url: "https://www.semafor.com/article/02/12/2026/why-intuits-ceo-thinks-the-markets-wrong-on-ai"
    fecha_acceso: 2026-06-13
  - titulo: "Own vs Orchestrate: The 2026 Enterprise Guide to Avoiding AI Vendor Lock-In"
    url: "https://expertaiprompts.blog/post/ai-vendor-lock-in"
    fecha_acceso: 2026-06-13
  - titulo: "LLM Inference Price Trends — Epoch AI"
    url: "https://epoch.ai/data-insights/llm-inference-price-trends"
    fecha_acceso: 2026-06-13
---

# Inteligencia como utilidad

## El concepto

La inferencia de modelos de lenguaje de gran escala atraviesa el mismo ciclo que recorrieron la electricidad, el cómputo en la nube y el almacenamiento: de ventaja competitiva a utilidad. Una utilidad es un recurso necesario, confiable y con precio tendiente a cero — cuya disponibilidad deja de ser diferenciadora porque todos la tienen. El LLM como utilidad no significa que la IA deja de ser poderosa. Significa que su potencia se vuelve tan accesible que tener acceso a ella ya no es una ventaja.

El mecanismo opera en dos movimientos simultáneos. Primero, el precio de inferencia colapsa de manera sostenida: de $30 por millón de tokens en 2023 a $0.10 en 2026 — un modelo equivalente cuesta 99.7% menos en tres años. Segundo, los proveedores que construyeron el modelo más capaz descubren que esa capacidad ya no es el activo escaso, porque los competidores alcanzan rendimiento comparable a fracción del precio. El mismo movimiento que garantizaba ventaja ahora la erosiona.

Cuando el modelo se convierte en utilidad, el stack de IA se fractura en capas económicas distintas: la utilidad de inferencia (commodity de precio decreciente), la infraestructura de datos y orquestación (donde vive la lógica de negocio), y la capa del arnés (donde se codifican reglas, criterios y guardrails del dominio). Cada capa empieza a comportarse como la industria que toca, no como la tech company que la construyó.

## Por qué importa

Cuando el modelo es la utilidad, el valor migra hacia las capas que el builder no diseñó para competir: el arnés y el contexto. Sasan Goodarzi, CEO de Intuit, lo formuló en febrero 2026: los LLM son commodities y serán las empresas que los aplican las que capturen el valor — describiendo un stack donde la inferencia es el primer eslabón de una cadena cuyo valor está en el extremo aplicado.

El `capital-de-contexto` del builder — sus datos, su historial, su comprensión del dominio — se vuelve la fuente primaria de diferenciación. El predictor más consistente de calidad de output en 2026 ya no es cuál modelo se usa sino qué calidad de contexto se le provee.

Pero hay un vector menos visible: el arnés como mecanismo de lock-in invertido. El arnés fue diseñado como el artefacto de control del builder sobre el agente. En el contexto de commoditización del modelo, se convierte en el mecanismo por el cual el proveedor mantiene control sobre el builder. Al adoptar el harness de un proveedor, el developer conecta invisiblemente su curva de costos, su elección de modelo y su arquitectura de governance al ecosistema del proveedor. `ia-sin-ecosistema` captura por qué la IA falla sin activos complementarios — este concepto captura el mecanismo inverso: qué ocurre cuando el modelo sí es barato y el activo complementario que genera dependencia es el arnés.

## Datos y evidencia

- GPT-4 API (marzo 2023): $30 por millón de tokens de entrada → Gemini Flash (abril 2026): $0.10 por millón de tokens. Reducción del **99.7%** en 3 años para rendimiento equivalente. (Featherless AI / AI Magicx, 2026)

- Para modelos de rendimiento equivalente, el costo se redujo **10× por año** durante 2021–2025. Proyecciones: 3–5× anuales hasta 2027, luego tapering a 1.5–2× conforme las oportunidades de optimización se agotan. (Epoch AI, 2026)

- Gartner (marzo 2026): para 2030, ejecutar inferencia en un modelo de 1 billón de parámetros costará a los proveedores más del **90% menos** que en 2025. Los LLMs de 2030 serán hasta **100 veces más eficientes en costo** que los primeros modelos de tamaño similar de 2022.

- El costo promedio de migrar de una plataforma de orquestación de agentes a otra es **$315,000 por proyecto**. El lock-in del arnés no es teórico — es fricción medida. (ExpertAIPrompts, 2026)

- El lock-in de orquestación es "la categoría de riesgo de dependencia de IA de mayor crecimiento en 2026". El costo de cambio en el stack no es aditivo sino multiplicativo: acumula dependencia en cinco capas — modelo, orquestación, datos, governance y conocimiento organizacional. (Kai Waehner / ExpertAIPrompts, 2026)

## Tensiones y límites

La commoditización no es uniforme. Los modelos frontier siguen siendo significativamente más capaces para tareas de razonamiento complejo. La utilidad aplica a la franja de tareas que ya se resuelven bien con modelos medianos. Para las tareas donde el frontier es el único que funciona, el proveedor conserva poder de precio.

El arnés abierto como contramedida. MCP (Model Context Protocol), ahora bajo la Linux Foundation, es el estándar abierto que crea una interfaz vendor-agnostic para agentes. Si la industria adopta MCP como base, el harness de un proveedor deja de ser la única vía de integración — lo que reduce el lock-in pero no elimina la dependencia de contexto acumulado.

La paradoja del CEO de Intuit: Goodarzi argumenta que el valor migrará a las empresas aplicadoras, pero Intuit depende de OpenAI o Anthropic para la inferencia. El argumento solo sostiene si las empresas aplicadoras construyen su moat en el arnés propio y no en el arnés del proveedor de modelo.

No toda utilidad tiene precio cero. La electricidad es una utilidad y aún tiene costo. La inferencia LLM seguirá siendo un ítem de presupuesto real — el punto es que deja de ser la fuente de ventaja competitiva, no que desaparezca como gasto.

## Ejes investigados

**Eje 1 — Colapso de precios de inferencia (2023–2026):** Epoch AI, Gartner, Featherless AI, AI Magicx. Datos numéricos robustos: -99.7% en precio para rendimiento equivalente, proyecciones Gartner 2030 confirmadas. 4 fuentes institucionales.

**Eje 2 — Migración de valor al arnés y el contexto:** MindStudio, FourWeekMBA, O'Reilly AI Agents Stack 2026. Argumento "harness > benchmarks" consistente entre fuentes independientes. Cita de Goodarzi (Intuit CEO, Semafor, febrero 2026) verificada. 3 fuentes sólidas.

**Eje 3 — Lock-in del arnés como nuevo riesgo de dependencia:** ExpertAIPrompts, Kai Waehner, Swfte AI, StackAI. Costo de migración ($315K/proyecto) cuantificado. Contraejemplo MCP como mecanismo de mitigación también documentado. 4 fuentes sólidas.
