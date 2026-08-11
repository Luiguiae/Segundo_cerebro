---
titulo: economia-de-la-intencion
tipo: concepto
fecha: 2026-08-11
familia: diseno
tags: [intencion, atencion, ux-agentica, metricas, kpi]
relacionado: [agencia-humana-como-imperativo-ux, de-usuario-a-cliente-servido, quien-controla-el-prompt]
estado: activo
fuentes:
  - titulo: "We spent a decade designing to capture attention. Now the best products are designed to give it back."
    url: "https://newsletter.uxuniversity.io/p/we-spent-a-decade-designing-to-capture"
    fecha_acceso: 2026-08-11
  - titulo: "Gartner Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026, Up from Less Than 5% in 2025"
    url: "https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025"
    fecha_acceso: 2026-08-11
  - titulo: "The Intention Economy: When Customers Take Charge (Doc Searls, HBR Press, 2012)"
    url: "https://en.wikipedia.org/wiki/The_Intention_Economy"
    fecha_acceso: 2026-08-11
  - titulo: "User Engagement in 2026: Human + Agent Signals"
    url: "https://userpilot.com/blog/user-engagement/"
    fecha_acceso: 2026-08-11
  - titulo: "Growth Metrics Evolution: From Attention to Intention in 2026"
    url: "https://www.influencers-time.com/evolving-growth-metrics-from-attention-to-intention/"
    fecha_acceso: 2026-08-11
---

# De la economía de la atención a la economía de la intención

## El concepto

La economía de la intención es la inversión del principio de diseño que dominó la industria durante la última década. Donde la economía de la atención —popularizada por redes sociales y plataformas de streaming— optimizó para maximizar el tiempo que el usuario pasa dentro del producto, la economía de la intención optimiza para minimizarlo: el producto de mayor calidad es el que resuelve la intención del usuario más rápido y lo deja ir.

El término tiene raíces en el trabajo de Doc Searls, quien acuñó "intention economy" en marzo de 2006 en Linux Journal y lo desarrolló en su libro "The Intention Economy: When Customers Take Charge" (Harvard Business Review Press, 2012). Searls lo planteó desde el lado del mercado: en vez de que las empresas compitan por la atención del consumidor, los consumidores expresan directamente sus intenciones y son los vendedores quienes deben responder. Lo que cambia en 2025-2026 es que la UX agéntica convierte ese marco teórico en un imperativo de diseño operacional: los productos dejan de ser destinos donde el usuario habita y se vuelven canales por donde pasa su intención.

La transición está siendo acelerada por la irrupción de interfaces agénticas —productos que no esperan que el usuario navegue hacia su objetivo, sino que capturan la intención, la procesan de forma autónoma y reportan el resultado. Cuando el flujo central muta de navegar → seleccionar → ejecutar a expresar intención → delegar → verificar resultado, el tiempo de sesión pasa de ser señal de éxito a señal de fricción.

## Por qué importa

El argumento invierte el KPI más arraigado del diseño de producto de la última década. "Tiempo en la app" fue la métrica proxy que unificó equipos de producto, crecimiento y diseño bajo una misma dirección: más tiempo = más valor capturado. La economía de la intención desmonta esa ecuación: si el usuario pasa más tiempo en el producto para resolver algo que podría delegarse a un agente, ese tiempo es costo, no valor.

Las consecuencias son prácticas e inmediatas. Un producto agéntico requiere un marco de métricas distinto al de un producto de atención: los KPIs tradicionales de engagement (DAU/MAU, session length, pages per session) empiezan a actuar como señales invertidas — alta sesión puede significar fricción, no satisfacción. El diseño pasa a medir completion rate, time-to-first-value y resolution velocity: cuánto tarda el sistema en cerrar la intención del usuario desde que la expresa.

Para el diseñador, el cambio estructural es profundo: ya no se diseña para retener al usuario dentro de una interfaz bien construida. Se diseña para que la interfaz sea tan efectiva que el usuario no necesite quedarse.

## Datos y evidencia

- **Gartner (agosto 2025):** 40% de las aplicaciones enterprise integrarán agentes de IA específicos para tareas al finalizar 2026, vs. menos del 5% en 2025. El mercado global de agentes de IA proyecta alcanzar $10.9–12.06 mil millones en 2026, con CAGR de 44–46% hasta 2030. Esta adopción masiva convierte el diseño de intención en presión estructural de mercado, no en tendencia de vanguardia.

- **Userpilot (2026):** En productos asistidos por IA, las sesiones largas señalan fricción, no engagement: "Someone who spends 45 minutes in your product daily because the workflow is confusing isn't the same as someone who spends 45 minutes because they're getting work done." Las métricas de actividad (DAU/MAU, session length, page views) "start to break in agent-heavy accounts."

- **Framework de 3 capas para productos agénticos (2026):** Task metrics (¿funcionó la tarea?), trajectory metrics (¿cómo fue el camino?), business metrics (¿creó valor medible?). "Session length and thumbs-up/thumbs-down tell you almost nothing about whether your agent is actually completing tasks."

- **Doc Searls (2006 / 2012):** El término fue acuñado en marzo de 2006 en Linux Journal. La premisa original: los consumidores expresan sus intenciones directamente al mercado en lugar de ser capturados por campañas de atención. La versión 2026 amplifica esa premisa desde el diseño de interfaz: los productos deben recibir intenciones delegadas, no generar deseo de quedarse.

- **Métricas de primera sesión (2025):** Usuarios que completan una acción core en su primer día retienen al 33.42% al día 30, vs. 20.36% para quienes no lo hacen. El gap de retención se crea en la primera sesión, no se cierra con notificaciones de reactivación — evidencia de que la velocidad de entrega de valor importa más que la frecuencia de visitas.

- **Empresa que diseña para dar de vuelta la atención (2025–2026):** Resolution velocity emerge como el nuevo KPI central en interfaces agénticas, definido como el tiempo entre la expresión de la intención del usuario y el cierre de esa intención por el sistema.

## Tensiones y límites

El concepto tiene una tensión de modelo de negocio no resuelta: la mayoría de los productos de atención se financian vía publicidad, que requiere tiempo de exposición para generar valor. Un producto que resuelve en 30 segundos tiene un inventario publicitario de 30 segundos, no de 30 minutos. La economía de la intención asume implícitamente un modelo de monetización por resultado —suscripción, comisión, outcome-based pricing— en lugar de por tiempo de exposición. No es un argumento universal; es un argumento condicionado al modelo de negocio.

La segunda tensión es de alcance: el argumento aplica claramente a productos de servicio y herramientas de productividad (agentes de IA, banca digital, logística, soporte técnico), pero se debilita en categorías donde el tiempo es el producto mismo —entretenimiento, juegos, redes sociales de exploración. Un servicio de streaming que "te da de vuelta" 30 minutos de tu tarde no es mejor; simplemente falló en su propuesta de valor. El error de aplicación indiscriminada puede llevar a simplificar productos que requieren profundidad real (herramientas creativas, plataformas de aprendizaje, espacios de colaboración).

El tercer límite es de madurez del sector: el 40% de enterprise apps con agentes proyectado por Gartner para 2026 implica también que más del 40% de organizaciones aún no tiene un modelo maduro de gobernanza de IA autónoma —solo el 21% lo tiene hoy. La economía de la intención requiere infraestructura de confianza que el mercado todavía está construyendo.

## Ejes investigados

**Eje 1 — Inversión del KPI de tiempo en pantalla:** Se buscó evidencia de que el sector de producto está abandonando "time-on-app" como métrica de éxito. Hallazgo: no hay abandono formal, sino bifurcación. Los productos de atención (redes sociales, streaming) mantienen la métrica; los productos de servicio y herramientas agénticas la están reemplazando por task completion, resolution velocity y time-to-first-value. La señal más sólida: para productos con IA agéntica, sesiones largas se interpretan como fricción. 2 fuentes sólidas encontradas.

**Eje 2 — UX agéntica y delegación de intención:** Se buscó qué cambios de diseño concretos trae la UX agéntica y cuál es su adopción real. Hallazgo: el flujo central muta de navegar→seleccionar→ejecutar a expresar intención→delegar→verificar resultado. Gartner proyecta 40% de enterprise apps con agentes para fines de 2026 (vs. <5% en 2025) — dato empírico de adopción, no proyección teórica. El mercado proyecta $10.9–12.06 mil millones en 2026. 3 fuentes sólidas encontradas.

**Eje 3 — Economía de la intención como marco conceptual:** Se buscó el origen del término y su evolución. Hallazgo: Doc Searls acuñó "intention economy" en 2006 con una lectura de mercado (el cliente expresa intenciones, las empresas responden). La versión 2026 lo reconvierte en principio de diseño de interfaz. Las dos lecturas coexisten: la original (empoderamiento del consumidor vía VRM) y la nueva (diseño de productos agénticos que reciben intenciones delegadas). 2 fuentes sólidas encontradas.
