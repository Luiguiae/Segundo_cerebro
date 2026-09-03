---
titulo: "El umbral \"Crítico\" que no frena el lanzamiento"
tipo: concepto
familia: agencia-ia
tags: [ia, gobernanza-ia, autonomia, tension, etica]
relacionado: [gobernanza-ia-performativa, riesgo-geopolitico-del-modelo, impuesto-de-alineacion]
fecha: 2026-09-03
estado: borrador
fuentes:
  - titulo: "OpenAI's Astra Crosses 'Critical' Cyber Threshold After Finding Zero-Days"
    url: "https://www.securityweek.com/openais-astra-becomes-first-model-to-cross-critical-cybersecurity-threshold/"
    fecha_acceso: 2026-09-03
  - titulo: "Responding to the next frontier of critical cyber capabilities"
    url: "https://openai.com/index/responding-next-frontier-critical-cyber-capabilities/"
    fecha_acceso: 2026-09-03
  - titulo: "OpenAI blinks first in AI safety standoff"
    url: "https://www.axios.com/2026/08/19/openai-astra-safety-altman-anthropic"
    fecha_acceso: 2026-09-03
  - titulo: "Anthropic Drops Hard Safety Limits From its AI Scaling Policy"
    url: "https://winbuzzer.com/2026/02/25/anthropic-drops-hard-safety-limit-responsible-scaling-policy-xcxwbn/"
    fecha_acceso: 2026-09-03
  - titulo: "AI Safety Index — Summer 2026"
    url: "https://futureoflife.org/ai-safety-index-summer-2026/"
    fecha_acceso: 2026-09-03
  - titulo: "OpenAI Rates Astra 'Critical' Under Preparedness Framework"
    url: "https://www.gncrypto.news/news/openai-rates-astra-critical-preparedness-framework/"
    fecha_acceso: 2026-09-03
---

## El concepto

El Preparedness Framework de OpenAI define el nivel "Crítico" como la capacidad de un modelo para identificar y desarrollar exploits funcionales zero-day en muchos sistemas reales endurecidos sin intervención humana, o diseñar y ejecutar estrategias end-to-end de ciberataques contra objetivos endurecidos dado solo un objetivo de alto nivel. Es el umbral más alto del framework — diseñado, en su concepción original, como línea roja de no-lanzamiento.

El 1 de septiembre de 2026, OpenAI confirmó que Astra es el primer modelo de su historia clasificado en nivel Crítico para ciberseguridad. Astra logró el 100% en ExploitBench (desarrollo de exploits desde vulnerabilidades conocidas), encontró 2 vulnerabilidades zero-day reales en una batería de 20 vulnerabilidades V8 de alta severidad de mediados de 2026, construyó una cadena completa de compromiso de browser, escapó de un sandbox aislado, y escaló privilegios de usuario estándar a root en un sistema operativo endurecido — todo sin supervisión humana paso a paso.

OpenAI decidió lanzarlo.

## Por qué importa

El umbral "Crítico" fue diseñado para detener. En la práctica funcionó como criterio de "suficientes salvaguardas para continuar": training adicional para rechazar solicitudes dañinas (Astra declina el 91.5% de intentos de jailbreak, frente al 59% de GPT-5.6 Sol), monitoreo de actividad no autorizada, y un programa de acceso restringido (Daybreak Blue) para testers seleccionados antes de disponibilidad amplia.

La asimetría es estructural: el modelo que alcanza el 100% de efectividad explotando vulnerabilidades y el que rechaza el 91.5% de solicitudes de abuso son el mismo modelo. El 8.5% restante no es una brecha técnica — es la superficie de ataque que el lanzamiento habilita públicamente. Nadie externo al laboratorio decidió si ese umbral de riesgo residual es aceptable.

Esto es cualitativamente distinto del patrón documentado en `gobernanza-ia-performativa` (donde los marcos existen como señal hacia reguladores, pero sin enforcement real). Aquí el mecanismo es más granular: el laboratorio publica el umbral, evalúa el modelo contra ese umbral, certifica que lo cruzó, y luego decide unilateralmente que sus propias salvaguardas son suficientes para lanzar de todos modos. La función de detención se convirtió en función de habilitación.

## Datos y evidencia

- **100%** en ExploitBench — Astra desarrolla exploits de vulnerabilidades conocidas con éxito completo (OpenAI, septiembre 2026).
- **2 vulnerabilidades zero-day reales** encontradas de 20 vulnerabilidades V8 de alta severidad testeadas (mid-2026). OpenAI las notificó a los maintainers del software afectado (OpenAI, septiembre 2026).
- **91.5%** de solicitudes de jailbreak rechazadas vs. **59%** de GPT-5.6 Sol — la mejora de robustez coexiste con capacidad ofensiva sin precedentes (SecurityWeek, septiembre 2026).
- **Anthropic** eliminó en febrero 2026 la promesa central de su RSP de no lanzar modelos más capaces sin medidas de seguridad probadas en advance, citando "zona de ambigüedad", clima político anti-regulatorio, y requisitos difíciles de cumplir sin coordinación industria-wide (WinBuzzer, febrero 2026).
- **Future of Life Institute AI Safety Index — Summer 2026**: Anthropic, OpenAI, Google DeepMind y Meta han debilitado o anulado compromisos de pausa unilateral si se acercan líneas rojas. "El sistema voluntario de seguridad creado por los labs ha comenzado a erosionarse antes de que los gobiernos pongan una alternativa duradera" (FLI, 2026).

## Tensiones y límites

**La paradoja de la certificación propia.** El que escribe el umbral es el mismo que evalúa si el modelo lo cruzó y el mismo que decide si cruzarlo justifica no lanzar. Sin auditoría independiente con autoridad de veto, el framework es autoregulación pura — su valor como señal de confianza y su valor como mecanismo de control son inversamente proporcionales: cuanto más útil para el marketing de responsabilidad, menos creíble como línea roja real.

**El límite Daybreak Blue.** El argumento de acceso restringido asume que la distinción ofensivo/defensivo en ciberseguridad se puede mantener en el tiempo. Los programas de "testers defensivos" no garantizan que las capacidades no lleguen a actores ofensivos — la historia de la seguridad informática es la historia de capacidades que migraron de contextos controlados a ecosistemas abiertos.

**Cuándo no aplica.** Este concepto no describe el caso general de "labs que ignoran sus propios frameworks" — Astra pausó desarrollo en agosto 2026 para agregar salvaguardas antes de lanzar, lo que muestra que el proceso tuvo efecto. El límite específico es que el resultado final del proceso sigue siendo el laboratorio decidiendo unilateralmente, sin un árbitro externo con poder real de detención.

## Ejes investigados

**Eje 1 — Definición operacional del umbral Crítico y evidencia de Astra.** Consultadas: SecurityWeek, OpenAI (vía search), gncrypto.news. Datos confirmados: ExploitBench 100%, 2 zero-days reales de 20 testeados, capacidades de ataque detalladas, resistencia a jailbreak 91.5% vs 59%. 3 fuentes sólidas.

**Eje 2 — Las salvaguardas que justifican el lanzamiento y su asimetría.** Consultadas: SecurityWeek, gncrypto.news. El argumento de OpenAI: training + monitoreo + Daybreak Blue — sin árbitro externo ni mecanismo verificable por terceros. 2 fuentes sólidas.

**Eje 3 — El patrón de erosión en la autoregulación de labs.** Consultadas: Axios, WinBuzzer, Future of Life Institute AI Safety Index Summer 2026. El caso Astra no es aislado: sistema completo de compromisos voluntarios muestra erosión documentada. Anthropic eliminó su hard limit en febrero 2026; múltiples labs debilitaron compromisos de pausa unilateral. 3 fuentes sólidas.
