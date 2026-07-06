# Contexto del Segundo Cerebro — Luigui Avila

> Archivo actualizado el 2026-07-06 (auditoría completa del vault + mejora-006 de Jarvis completa: memoria personal, saludo proactivo, watcher conversacional con profundización externa, auto-regeneración del ATLAS — ver JARVIS_LOG.md). Úsalo como contexto en conversaciones de Claude.ai para que el asistente conozca el estado completo del vault.

---

## Quién es Luigui

Diseñador-constructor. Construye el Segundo Cerebro como infraestructura de conocimiento personal para generar presentaciones, propuestas y charlas. Su trabajo orbita en la intersección de diseño, producto e IA. El proyecto central visible es **Wayta IA** — equipo pequeño construyendo con el modelo de diseñador-constructor como principio fundacional.

---

## Qué es el Segundo Cerebro

Un sistema de conocimiento atómico en Obsidian. La lógica: los conceptos se capturan como unidades independientes con frontmatter YAML estricto, se correlacionan explícitamente entre sí, y se activan como insumo para entregables concretos (charlas, propuestas, decks). El sistema no es el vault — es la lógica de estructuración que vive detrás.

**Jarvis** es el agente de mantenimiento del vault (Claude Code) con interfaz de voz. Corre como daemon en macOS vía wake word "Jarvis". Capacidades actuales:

- **Comandos de vault**: agrega conceptos, correlaciona, audita, actualiza ATLAS, sube cambios a GitHub por voz
- **Memoria personal**: recuerda hechos que Luigui le pide guardar ("recuerda que...") en `memoria.md` y los carga como contexto en toda conversación futura
- **Conciencia temporal**: responde "qué hicimos ayer / hoy / esta semana" filtrando `JARVIS_LOG.md` por período real, en vez de mostrar ciegamente las últimas líneas
- **Saludo proactivo al arrancar**: sincroniza el vault con GitHub y reporta qué conceptos nuevos aparecieron desde la última vez que habló con Luigui
- **Watcher proactivo**: detecta cambios en `Conocimiento/Conceptos/` en tiempo real. Anuncia la detección por voz sin pedir confirmación (evita que el daemon quede colgado esperando una respuesta que no puede capturar fuera del loop de wake word) y regenera el ATLAS automáticamente (debounce de 3s, agrupa múltiples archivos en un solo anuncio, serializa ejecuciones si `generar_index.py` ya está corriendo)
- **Reevaluación conversacional por voz**: "Jarvis, reevalúa este concepto" evalúa contra la rúbrica real (Groq, sin pasar por Claude Code), reporta hallazgos, pregunta si guardar, y pregunta si profundizar con fuentes externas vía el VPS (`POST /evaluar`, nunca `/confirmar` — ver nota de mejora-006 abajo)
- **Visión de pantalla** (mejora-007): Jarvis puede ver y describir lo que hay en pantalla, profundizar el contenido o capturarlo como concepto. Usa screenshot + Claude Vision como primario, AppleScript como fallback. Lee el tab activo del browser (no el primero en la lista)
- **Filesystem** (mejora-006 · filesystem): lee, lista y navega archivos del sistema con aliases de rutas conocidas
- **TTS con chunking**: respuestas largas se parten en chunks de ≤200 chars por oración para evitar corte de audio. `hablar_respuesta()` trunca respuestas de vault a 600 chars con gracia

---

## Estado actual del vault

- **80 conceptos** (71 activos, 9 borrador) — última auditoría completa: 2026-07-06
- **29 correlaciones documentadas** (18 activas, 11 borrador — la misma auditoría bajó el estado de varias por no plantear tensión real, solo convergencia o co-ocurrencia)
- **Auditoría 2026-07-06:** revisión de los 109 archivos contra Gate 0 (estructura) y Gate 1+2 (rúbrica). 4 archivos normalizados estructuralmente (campo `slug` prohibido, `estado` ausente, `tags`/`relacionado` sobre el límite). 17 archivos bajados de `activo` a `borrador` por contenido (tensión débil, dato sin fuente, o correlación que el propio texto admite como no-contradictoria). Detalle completo en `JARVIS_LOG.md`.
- **6 conceptos más recientes (por fecha de frontmatter):**
  - `cambio-como-estado-permanente` (organizaciones · 2026-07-05) — el cambio dejó de ser un evento episódico para ser el modo normal de operación en la era agéntica; las competencias de gestión de transición se vuelven competencias de operación continua
  - `presencia-como-condicion-del-valor` (filosofia · 2026-07-05) — el valor de algo hecho a mano viene del tiempo de vida invertido, no de la técnica; la IA hace fácil producir sin presencia ("el Dalí tardío")
  - `costo-marginal-cero-como-disruptor` (economia · 2026-07-05) — moats construidos sobre fricción de proceso colapsan cuando los agentes eliminan esa fricción
  - `problema-del-referente-para-la-ia` (ia · 2026-07-03) — a quién beneficia una IA cuando "beneficio" no tiene un referente único ni estable. Estado borrador (fuente única).
  - `alineacion-de-cuatro-partes` (ia · 2026-07-03) — marco de 4 capas para diagnosticar a quién sirve realmente un sistema de IA
  - `supuestos-importados-por-ia` (filosofia · 2026-06-25) — marco propio de tres capas (ontológica, epistemológica, ética) para los supuestos filosóficos que la IA importa sin declarar
- **Jarvis Server (VPS):** desplegado en `https://jarvis-luigui.duckdns.org`. Corre código anterior a la corrección de seguridad del 2026-07-04 (el `/health` en vivo todavía expone `conceptos`/`vault_commit` en el body) — redespliegue pendiente, no bloqueante. Endpoints: `/health`, `/comando`, `/audio`, `/evaluar` (Tavily+DeepSeek, usado por la reevaluación conversacional de Jarvis), `/confirmar` (solo para conceptos nuevos — rechaza con 409 si el slug ya existe).
- **mejora-006 de Jarvis (Memoria y Conciencia Contextual) — completa, las 6 fases:** memoria personal, "qué hicimos" con filtro de período, subir cambios por voz, saludo proactivo + sync diario, watcher conversacional (evaluar/reportar/confirmar/guardar), profundización externa vía VPS. Detalle de diseño en `docs/plan-006.md` / `docs/tasks-006.md` (ambos `estado: completado`). Nota: el número "mejora-006" también se usa para la feature de Filesystem del daemon de voz — son dos iniciativas distintas que comparten numeración por casualidad, sin colisión real.
- **Auto-index del watcher (2026-07-06):** el watcher ya no pide confirmación al detectar un concepto nuevo o modificado — anuncia la detección y regenera el ATLAS automáticamente sin intervención. La reevaluación completa contra la rúbrica sigue disponible, pero solo por voz directa ("Jarvis, reevalúa este concepto"), no disparada automáticamente por el watcher.
- **Skill `/presentacion-html [slug] [formato]`** — genera una presentación HTML autocontenida desde cualquier concepto del vault. Formato `business-case` implementado. Plantillas en `Plantillas/presentaciones/`.
- **Grafo tipado de relaciones:** 24 conceptos con campo `edges:` (37 edges tipados en total; tipos: `contradicts`, `requires`, `enables`, `refines`, `extends`, `exemplifies`, `same_mechanism_as`, `analogous_to`, `precedes`). ATLAS incluye sección "Grafo tipado de relaciones".
- **Remotion (generación de video):** NO funcional — `remotion/src` está vacío/perdido (nunca se trackeó en git). `generar_video.py` falla con error claro en vez de crashear, pero no genera videos hasta reconstruir el proyecto. Para presentaciones, usar `/presentacion-html`.

---

## Estructura de carpetas

Los conceptos viven en `Conocimiento/Conceptos/` organizados en 6 subcarpetas temáticas:

```
Conocimiento/Conceptos/
├── ia/             (30 conceptos) — tecnología, modelos, agentes IA
├── diseno/         (13 conceptos) — proceso de diseño, rol del diseñador, UX agéntico
├── producto/       (12 conceptos) — construir, medir, iterar productos
├── organizaciones/ (12 conceptos) — equipos, roles, transformación organizacional
├── economia/       (6 conceptos)  — mercado laboral, impacto económico de la IA
└── filosofia/      (7 conceptos)  — pensamiento abstracto, epistemología, marcos
```

Sistemas adicionales:
- `Backlog/` — pipeline para ideas de proyectos construibles
- `Inbox/` — archivo de entrada para scouts y fuentes sin procesar
- `docs/` — planes de implementación de mejoras del vault (incluye `plan-006.md`/`tasks-006.md`, completos)
- `Prompts/Meta/jarvis/` — daemon de voz de Jarvis (corre como `Jarvis.app` vía launchd, log en `~/Library/Logs/jarvis.log`)
- `Plantillas/presentaciones/` — sistema de plantillas para generación de presentaciones HTML
  - `html-base.md` — sistema visual compartido (paleta, tipografía, componentes CSS)
  - `business-case.md` — mapa narrativo completo (12 secciones, mapping vault→HTML)
- `.claude/commands/presentacion-html.md` — skill `/presentacion-html [slug] [formato]` para generar HTML desde conceptos del vault

---

## Los 80 conceptos (71 activos, 9 borrador)

### ia/ (30 conceptos)

| slug | título | estado |
|---|---|---|
| `agentes-ia` | Equipos de agentes IA | activo |
| `ai-evals-como-disciplina` | AI Evals como disciplina de producto | activo |
| `alineacion-de-cuatro-partes` | Alineación de cuatro partes | activo |
| `arnes-del-agente` | Arnés del agente | activo |
| `autoautomatizacion-del-disenador` | La trampa de la autoautomatización | activo |
| `automatizacion-vs-ampliacion` | Automatización vs. amplificación | activo |
| `capital-de-contexto` | Capital de contexto | activo |
| `comprehension-debt` | Comprehension debt | activo |
| `conocimiento-autoorganizado-por-llm` | Conocimiento autoorganizado por LLM | activo |
| `design-system-como-api-para-agentes` | El design system como API para agentes | activo |
| `el-agente-que-no-para` | El agente que no para | activo |
| `espectro-autonomia-agente` | Espectro de autonomía del agente | activo |
| `espiral-delusional` | Espiral delusional | **borrador** |
| `fabrica-oscura-de-software` | La fábrica oscura de software | activo |
| `gestion-del-tiempo` | Gestión efectiva del tiempo | **borrador** |
| `gobernanza-ia-performativa` | Gobernanza de IA performativa | activo |
| `impuesto-de-alineacion` | El impuesto de alineación | activo |
| `impuesto-de-verificacion` | El impuesto de verificación | activo |
| `ingenieria-agentica` | Ingeniería agéntica | activo |
| `inteligencia-como-utilidad` | Inteligencia como utilidad | activo |
| `legibilidad-de-maquina` | Legibilidad de máquina | activo |
| `orquestacion-de-agentes` | Orquestación de agentes | activo |
| `poblaciones-sinteticas` | Poblaciones sintéticas | activo |
| `problema-del-referente-para-la-ia` | El problema del referente para la IA | **borrador** |
| `representacion-agente` | Representación agente | activo |
| `riesgo-geopolitico-del-modelo` | Riesgo geopolítico del modelo IA | activo |
| `spec-driven-development` | Spec-Driven Development | activo |
| `usuarios-sinteticos` | Usuarios sintéticos | **borrador** |
| `vibe-coding` | Vibe coding | activo |
| `web-bifurcada` | Web bifurcada | activo |

### diseno/ (13 conceptos)

| slug | título | estado |
|---|---|---|
| `agencia-humana-como-imperativo-ux` | Agencia humana como imperativo UX | activo |
| `arquitectura-de-confianza` | Arquitectura de confianza | activo |
| `de-usuario-a-cliente-servido` | De usuario a cliente servido | activo |
| `disenador-a-constructor` | Del diseñador al constructor | activo |
| `diseno-dos-velocidades` | Diseño en dos velocidades | activo |
| `diseno-uxui-y-ia` | Diseño UX/UI con IA | activo |
| `el-moat-del-gusto` | El moat del gusto | activo |
| `fundamentales-vs-flux` | Fundamentales vs. flux | **borrador** |
| `metacognicion-del-disenador` | Metacognición del diseñador | activo |
| `quien-controla-el-prompt` | Quien controla el prompt controla el producto | activo |
| `soberania-epistemica` | Soberanía epistémica | activo |
| `sycophancy-como-riesgo-de-diseno` | Sycophancy como riesgo de diseño | activo |
| `ux-checkpoints` | UX Checkpoints | activo |

### producto/ (12 conceptos)

| slug | título | estado |
|---|---|---|
| `claridad-antes-de-velocidad` | Claridad antes de velocidad | activo |
| `confianza-a-traves-de-velocidad` | Confianza a través de velocidad | activo |
| `copiloto-de-producto` | Copiloto de producto | activo |
| `corrupcion-silenciosa-por-delegacion` | Corrupción silenciosa por delegación | activo |
| `expertise-de-dominio-en-producto` | Expertise de dominio como infraestructura de producto | **borrador** |
| `feedback-que-escala` | El feedback que escala | activo |
| `las-tres-caras-del-producto-agentico` | Las tres caras del producto agéntico | activo |
| `metricas-post-pantalla` | Métricas post-pantalla | activo |
| `mvp-a-prototipo-en-produccion` | Del MVP al prototipo en producción | activo |
| `pit-stop-cognitivo` | Pit stop cognitivo | activo |
| `pmf-perecedero` | PMF perecedero | activo |
| `restriccion-de-tiempo-como-ventaja` | Restricción de tiempo como ventaja | activo |

### organizaciones/ (12 conceptos)

| slug | título | estado |
|---|---|---|
| `aprendizaje-vicario-mediado-por-agente` | Aprendizaje vicario mediado por agente | activo |
| `automatizar-mi-propio-trabajo` | Mi trabajo es automatizar mi trabajo | activo |
| `cambio-como-estado-permanente` | El cambio como estado permanente | activo |
| `condicion-redespliegue` | La condición del redespliegue | activo |
| `cultura-de-tinkering` | Cultura de tinkering como ventaja competitiva | activo |
| `deuda-cognitiva-organizacional` | Deuda cognitiva organizacional | activo |
| `equipos-pequenos-alto-impacto` | Equipos pequeños de alto impacto | **borrador** |
| `ia-sin-ecosistema` | IA sin ecosistema | activo |
| `juicio-como-trabajo-completo` | El juicio como trabajo completo | activo |
| `la-competencia-que-oculta-el-juicio` | La competencia que oculta el juicio | activo |
| `rutina-trabajo-enfocada` | Rutina de trabajo enfocada | **borrador** |
| `workforce-de-agentes` | Workforce de Agentes | activo |

### economia/ (6 conceptos)

| slug | título | estado |
|---|---|---|
| `costo-marginal-cero-como-disruptor` | Costo marginal cero como disruptor de moats | activo |
| `ia-como-filtro-de-entrada` | IA como filtro de entrada al mercado laboral | activo |
| `inversion-sesgo-tecnologico` | La inversión del sesgo tecnológico | activo |
| `marea-creciente-de-automatizacion` | Marea creciente de automatización | activo |
| `presupuesto-ia-como-restriccion` | El presupuesto de IA como restricción operativa | activo |
| `senal-anticipada-mercado-laboral` | Señal anticipada en el mercado laboral | activo |

### filosofia/ (7 conceptos)

| slug | título | estado |
|---|---|---|
| `arquitectura-de-inteligencia` | Arquitectura de inteligencia | activo |
| `colonialismo-cultural-digital` | Colonialismo cultural digital | activo |
| `cuerpo-como-infraestructura-cognitiva` | El cuerpo como infraestructura cognitiva | **borrador** |
| `lo-ilegible-como-senal` | Lo ilegible como señal | activo |
| `momento-liminal` | El momento liminal | activo |
| `presencia-como-condicion-del-valor` | La presencia como condición del valor | activo |
| `supuestos-importados-por-ia` | Supuestos importados por IA | activo |

---

## Las 29 correlaciones documentadas (18 activas, 11 borrador)

| archivo | título | estado |
|---|---|---|
| `2026-04-03_vibe-coding--spec-driven-development` | La trampa de construir sin saber qué estás construyendo | activo |
| `2026-04-10_claridad-antes-de-velocidad--momento-liminal` | La claridad que pides no existe todavía | activo |
| `2026-04-10_fundamentales-vs-flux--disenador-a-constructor` | ¿Construir es un fundamental o una habilidad que se depreca? | activo |
| `2026-04-11_automatizar-mi-propio-trabajo--expertise-de-dominio-en-producto` | El experto que intenta reemplazarse a sí mismo se descubre a sí mismo | activo |
| `2026-04-15_automatizacion-vs-ampliacion--fundamentales-vs-flux` | La misma línea divisoria, dos mapas | **borrador** |
| `2026-04-15_ia-como-filtro-de-entrada--agentes-ia` | El multiplicador que cierra la puerta | **borrador** |
| `2026-04-15_ia-como-filtro-de-entrada--disenador-a-constructor` | La salida de emergencia también se cierra | activo |
| `2026-04-15_senal-anticipada-mercado-laboral--gobernanza-ia-performativa` | Gobernar la señal sin verla | activo |
| `2026-04-18_copiloto-de-producto--quien-controla-el-prompt` | El mapa y el volante | activo |
| `2026-04-18_espectro-autonomia-agente--capital-de-contexto` | El precio de entrada para cada posición | **borrador** |
| `2026-04-18_espectro-autonomia-agente--fabrica-oscura-de-software` | El operador que no está | activo |
| `2026-04-18_fabrica-oscura-de-software--capital-de-contexto` | El único activo que queda | **borrador** |
| `2026-04-18_pit-stop-cognitivo--confianza-a-traves-de-velocidad` | La pausa que sostiene la velocidad | activo |
| `2026-04-18_pit-stop-cognitivo--feedback-que-escala` | Lo que el sistema no puede enseñarse a sí mismo | activo |
| `2026-05-13_aprendizaje-vicario-mediado-por-agente--capital-de-contexto` | Cómo el contexto aprende de sí mismo | activo |
| `2026-05-13_aprendizaje-vicario-mediado-por-agente--feedback-que-escala` | El aprendizaje que no se codifica desaparece | **borrador** |
| `2026-05-13_aprendizaje-vicario-mediado-por-agente--juicio-como-trabajo-completo` | El agente que destruye la rampa también puede reconstruirla | activo |
| `2026-06-10_autoautomatizacion-del-disenador--la-competencia-que-oculta-el-juicio` | La trampa sin señal de alarma | **borrador** |
| `2026-06-10_conocimiento-autoorganizado-por-llm--metacognicion-del-disenador` | ¿Tu vault es el producto o el ejercicio de tu conocimiento? | activo |
| `2026-06-10_corrupcion-silenciosa-por-delegacion--comprehension-debt` | El modo de supervisión que hace invisible la degradación | **borrador** |
| `2026-06-10_cuerpo-como-infraestructura-cognitiva--juicio-como-trabajo-completo` | La ironía estructural de la era agéntica | activo |
| `2026-06-10_de-usuario-a-cliente-servido--agencia-humana-como-imperativo-ux` | La comodidad como camino de menor resistencia del diseño | activo |
| `2026-06-10_equipos-pequenos-alto-impacto--comprehension-debt` | El modelo de éxito lleva el riesgo incorporado | **borrador** |
| `2026-06-10_espiral-delusional--capital-de-contexto` | La espiral del experto | activo |
| `2026-06-10_gobernanza-ia-performativa--sycophancy-como-riesgo-de-diseno` | Dos capas de apariencia, cero de enforcement | **borrador** |
| `2026-06-10_impuesto-de-verificacion--pit-stop-cognitivo` | El mismo acto, diagnósticos opuestos | activo |
| `2026-06-10_inversion-sesgo-tecnologico--ia-como-filtro-de-entrada` | La escalera que se desmonta desde los dos extremos | activo |
| `2026-06-25_agentes-ia--capital-de-contexto` | La Tensión entre Equipos de Agentes IA y Capital de Contexto | **borrador** |
| `2026-06-25_gestion-del-tiempo--capital-de-contexto` | La Tensión entre Gestión del Tiempo y Capital de Contexto | **borrador** |

Las 2 correlaciones del 2026-06-25 (`agentes-ia--capital-de-contexto`, `gestion-del-tiempo--capital-de-contexto`) tienen una estructura y voz claramente distintas al resto del corpus (secciones genéricas en vez del patrón `## La tensión`/`## El insight no obvio`/`## El límite`, título literal "La Tensión entre A y B") — candidatas a reescritura completa, no solo a advertencia.
