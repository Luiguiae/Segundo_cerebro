---
titulo: El financiamiento circular como señal de techo de demanda
tipo: concepto
familia: economia
tags: [financiamiento, riesgo, infraestructura, demanda, mercado]
relacionado: [presupuesto-ia-como-restriccion, inversion-sesgo-tecnologico, costo-marginal-cero-como-disruptor]
fecha: 2026-08-12
estado: activo
fuentes:
  - titulo: "Nvidia's Risky Business"
    url: "https://stratechery.com/2026/nvidias-risky-business/"
    fecha_acceso: 2026-08-12
  - titulo: "NVIDIA Partners With Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs and KKR"
    url: "https://nvidianews.nvidia.com/news/nvidia-partners-with-apollo-blackrock-blackstone-brookfield-goldman-sachs-and-kkr-to-establish-ai-compute-infrastructure-financing-platforms-to-mobilize-over-500-billion-of-third-party-capital"
    fecha_acceso: 2026-08-12
  - titulo: "Nvidia guarantees its own chips' value to unlock $500 billion in AI infrastructure financing"
    url: "https://the-decoder.com/nvidia-guarantees-its-own-chips-value-to-unlock-500-billion-in-ai-infrastructure-financing/"
    fecha_acceso: 2026-08-12
  - titulo: "Circular Financing: Does Nvidia's $110B Bet Echo the Telecom Bubble?"
    url: "https://tomtunguz.com/nvidia_nortel_vendor_financing_comparison/"
    fecha_acceso: 2026-08-12
  - titulo: "5% GPU utilization: The $401 billion AI infrastructure problem enterprises can't keep ignoring"
    url: "https://venturebeat.com/infrastructure/5-gpu-utilization-the-401-billion-ai-infrastructure-problem-enterprises-cant-keep-ignoring/"
    fecha_acceso: 2026-08-12
  - titulo: "GPU Residual Value Report: 2026 Outlook"
    url: "https://www.amcompute.com/blog/gpu-depreciation-residual-value-report-2026"
    fecha_acceso: 2026-08-12
  - titulo: "AI Capex 2026: The $690B Infrastructure Sprint"
    url: "https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/"
    fecha_acceso: 2026-08-12
---

# El financiamiento circular como señal de techo de demanda

## El concepto

Cuando el proveedor de un activo necesita garantizar el valor de ese activo para que otros lo financien, está admitiendo que el mercado no confía suficientemente en él como colateral. En agosto de 2026, Nvidia anunció asociaciones con Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs y KKR para movilizar más de 500 mil millones de dólares en capital de terceros destinado a la construcción de centros de datos e infraestructura de IA. El mecanismo incluye que Nvidia respalde hasta el 25% del valor residual de cada transacción individual, evaluada caso por caso.

El término "financiamiento circular" captura la paradoja estructural: Nvidia vende los chips, garantiza el valor de los chips como colateral, y el retorno esperado de esos chips (futuros ingresos de los centros de datos) es el activo que respalda el préstamo que permite comprar más chips de Nvidia. El riesgo no desaparece — migra de los balances de los compradores directos hacia fondos de pensiones, aseguradoras y gestores de activos que no marcan el colateral a mercado con la misma frecuencia.

Este patrón tiene nombre en la historia financiera: vendor financing. Lucent Technologies lo usó a gran escala en el boom de telecomunicaciones de finales de los 90. Permitió crecer las ventas mientras el riesgo de crédito se transfería fuera del balance principal — hasta que el valor de los activos subyacentes colapsó y las pérdidas, diferidas durante años, se registraron de golpe.

## Por qué importa

Ben Thompson (Stratechery) argumenta que si la demanda por GPUs fuera genuinamente robusta, Nvidia no necesitaría comprometer sus propios márgenes para garantizar que otros inviertan. La garantía de valor residual no es un favor financiero — es evidencia de que la demanda orgánica ha llegado a un límite donde ya no se sostiene sola. El financiamiento circular no crea demanda; la adelanta y desplaza su riesgo.

Para el vault, esto amplía tres conceptos activos: `presupuesto-ia-como-restriccion` (la restricción económica real que enfrentan compradores sin el balance de los hyperscalers, que ahora Nvidia mitiga artificialmente), `inversion-sesgo-tecnologico` (el sesgo de capital hacia infraestructura antes de que el ROI esté validado — aquí con un proveedor que financia activamente ese sesgo) y `costo-marginal-cero-como-disruptor` (la promesa de que más compute eliminará los costos operativos — promesa que aún no se ha materializado a escala suficiente para justificar el capex).

El riesgo práctico no es solo financiero: es epistémico. Los gestores de activos que suscriben estos vehículos no marcan el colateral a mercado en tiempo real. Cuando los GPUs se deprecian más rápido de lo modelado — y el ciclo Blackwell vs. H100 sugiere que sí lo hacen — la pérdida existe antes de registrarse. La arquitectura oculta el estrés hasta que ya no puede.

## Datos y evidencia

- **$500B**: Capital que Nvidia busca movilizar a través de sus socios financieros (Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs, KKR), anunciado el 10 de agosto de 2026. (Fuente: NVIDIA Newsroom, 2026-08-10)

- **25%**: Porcentaje máximo del valor de cada transacción que Nvidia podría respaldar como garantía de valor residual, evaluado proyecto por proyecto — no sobre el total de $500B. (Fuente: The Decoder, 2026-08-11)

- **$635–690B**: Gasto de capital combinado guiado por los principales hyperscalers (Microsoft, Amazon, Alphabet, Meta, Oracle) para 2026 — aumento del 67–74% respecto a 2025. Aproximadamente el 75% destinado a infraestructura de IA. (Fuente: Futurum Group, 2026)

- **5%**: Tasa promedio de utilización de GPU en empresas que ya poseen infraestructura de IA — contra un stock acumulado de $401B invertido en esa infraestructura. (Fuente: VentureBeat, 2026)

- **10 centavos por dólar**: Relación entre ingresos generados por servicios de IA (~$25B en 2025) y el gasto en infraestructura de IA (>$250B en el mismo período). (Fuente: Long Yield Substack, 2026)

- **$176B**: Estimación de Michael Burry de la depreciación subvalorada de GPUs entre 2026 y 2028, basada en la diferencia entre la vida útil asumida contablemente (5–7 años) y el ciclo de actualización real de Nvidia (2–3 años). (Fuente: GPU Residual Value Report, amcompute.com, 2026)

- **Paralelo Nortel/Lucent**: Tomasz Tunguz documentó que la estrategia de vendor financing de Nvidia (~$110B) replica la de Lucent en el boom de telecomunicaciones, donde el mismo mecanismo extendió ventas mientras el riesgo crediticio migraba fuera del balance — antes del colapso. (Fuente: tomtunguz.com, 2026)

- **210,000 GPUs**: Primer despliegue del modelo de revenue-sharing de Nvidia con Sharon AI y Firmus (Grace Blackwell), lanzado el 1 de julio de 2026 — señal de que el mecanismo de financiamiento Nvidia venía escalando desde antes del anuncio masivo de agosto. (Fuente: TechTimes, 2026-07-04)

## Tensiones y límites

**La diferencia del monopolio**: Nvidia controla >90% del mercado de aceleradores de IA. Lucent competía en un mercado fragmentado donde múltiples vendedores erosionaron márgenes mutuamente. Nvidia puede, en principio, controlar el ritmo de lanzamientos para proteger el valor del colateral — aunque el incentivo de ventas corre exactamente en el sentido contrario: lanzar más rápido es la razón de ser de Nvidia.

**El garantizador crea el riesgo que garantiza**: El mismo actor que respalda el valor residual (Nvidia) es quien lanza el chip de próxima generación que destruye ese valor. La introducción de Blackwell ya colapsó el precio de mercado secundario del H100. No hay equivalente directo a esto en la historia del vendor financing — el fabricante de fibra óptica no lanzaba tecnologías que volvieran obsoleta la fibra ya tendida.

**La demanda puede ser real pero adelantada**: El 5% de utilización promedio no prueba que la infraestructura sea innecesaria en el largo plazo. El argumento del "superciclo de infraestructura" sostiene que la adopción sigue a la disponibilidad con un rezago de 3–5 años. La burbuja de telecomunicaciones construyó fibra oscura que tardó una década en usarse — pero eventualmente se usó. La pregunta es si el financiamiento apalancado puede sostenerse durante ese rezago.

**Lo que este concepto no predice**: No es un indicador de cuándo o si ocurre un colapso. Es un indicador estructural de que la demanda orgánica ha alcanzado un límite relativo — lo suficiente para que Nvidia deba facilitar el acceso al capital para sostener el crecimiento de sus ventas. El límite es real; la forma que toma su resolución no está determinada.

## Ejes investigados

**Eje 1 — Mecánica del financiamiento circular de Nvidia**
Búsquedas sobre el programa de $500B anunciado el 10 de agosto de 2026. Se encontró cobertura en CNBC, The Decoder, NVIDIA Newsroom y TradingKey. Hallazgo principal: la garantía de valor residual es por transacción individual (no sobre el total de $500B), evaluada caso por caso. También se encontró un programa anterior (julio de 2026): Nvidia lanzó un modelo de revenue-sharing con operadores de cloud pequeños (Sharon AI, Firmus — 210,000 GPUs Grace Blackwell) — señal de que el mecanismo viene escalando gradualmente antes del anuncio masivo. 2 fuentes sólidas con autor/institución verificable.

**Eje 2 — El "GPU debt cliff" y el paralelo histórico con infraestructura apalancada**
Búsquedas sobre depreciación de GPUs, riesgo de colateral y comparaciones históricas (Lucent, telecom bubble). Se encontraron: la estimación de Burry sobre depreciación subvalorada ($176B, 2026-2028), el análisis de Tomasz Tunguz del paralelo Nortel/Lucent (~$110B), y la advertencia del Bank of England sobre riesgos de estabilidad financiera vinculados a empresas de IA altamente apalancadas. Hallazgo clave: el colateral (GPU) lo destruye el mismo actor que lo garantiza (Nvidia) — estructura sin equivalente directo en telecomunicaciones. 3 fuentes sólidas con autor/institución verificable.

**Eje 3 — La brecha entre demanda real y la infraestructura construida**
Búsquedas sobre utilización de GPU, ROI de IA y capex vs. ingresos. Se encontró el dato de 5% de utilización promedio (VentureBeat), la relación de 10¢ de ingreso por dólar de capex en 2025, y el gap entre adopción amplia (80–90% de empresas usan IA en alguna función) y adopción profunda (<40% han escalado más allá de pilotos). Hallazgo: la infraestructura se construye antes de que exista la demanda real que la justifique — debate abierto entre "build-ahead racional" y "especulación apalancada" que depende del horizonte temporal y del ritmo de adopción empresarial. 2 fuentes sólidas con datos verificables.
