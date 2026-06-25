# Contexto del Segundo Cerebro — Luigui Avila

> Archivo actualizado el 2026-06-20 (auditoría completa + skill presentacion-html). Úsalo como contexto en conversaciones de Claude.ai para que el asistente conozca el estado completo del vault.

---

## Quién es Luigui

Diseñador-constructor. Construye el Segundo Cerebro como infraestructura de conocimiento personal para generar presentaciones, propuestas y charlas. Su trabajo orbita en la intersección de diseño, producto e IA. El proyecto central visible es **Wayta IA** — equipo pequeño construyendo con el modelo de diseñador-constructor como principio fundacional.

---

## Qué es el Segundo Cerebro

Un sistema de conocimiento atómico en Obsidian. La lógica: los conceptos se capturan como unidades independientes con frontmatter YAML estricto, se correlacionan explícitamente entre sí, y se activan como insumo para entregables concretos (charlas, propuestas, decks). El sistema no es el vault — es la lógica de estructuración que vive detrás.

**Jarvis** es el agente de mantenimiento del vault (Claude Code) con interfaz de voz. Corre como daemon en macOS vía wake word "Jarvis". Capacidades actuales:

- **Comandos de vault**: agrega conceptos, correlaciona, audita, actualiza ATLAS
- **Watcher proactivo**: detecta cambios en archivos del vault en tiempo real y sugiere acciones (re-evaluar conceptos modificados, evaluar nuevos, leer correlaciones). Si el usuario no confirma inmediatamente, la acción queda pendiente y se ejecuta cuando dice "sí" en el siguiente ciclo de escucha
- **Visión de pantalla** (mejora-007): Jarvis puede ver y describir lo que hay en pantalla, profundizar el contenido o capturarlo como concepto. Usa screenshot + Claude Vision como primario, AppleScript como fallback. Lee el tab activo del browser (no el primero en la lista)
- **Filesystem** (mejora-006): lee, lista y navega archivos del sistema con aliases de rutas conocidas
- **TTS con chunking**: respuestas largas se parten en chunks de ≤200 chars por oración para evitar corte de audio (bug pyttsx3/macOS). `hablar_respuesta()` trunca respuestas de vault a 600 chars con gracia

---

## Estado actual del vault

- **70 conceptos activos** (auditoría 2026-06-20: 11 normalizados, todos aprobados Gate 0 + rúbrica)
- **27 correlaciones documentadas**
- **10 conceptos más recientes (por fecha de frontmatter):**
  - `riesgo-geopolitico-del-modelo` (ia · 2026-06-19) — vulnerabilidad estructural de cualquier sistema construido sobre un modelo frontier cerrado: el acceso puede revocarse por directiva gubernamental en horas, sin falla técnica. Precedente: suspensión global de Fable 5 y Mythos 5 el 12-jun-2026
  - `deuda-cognitiva-organizacional` (organizaciones · 2026-06-19) — costo diferido que se acumula cuando la delegación a la IA pasa del output al pensamiento mismo; erosión de pensamiento crítico, juicio y curiosidad a escala organizacional (BCG 2026: 60% de C-suite ya lo observa)
  - `soberania-epistemica` (diseno · 2026-06-18) — el derecho y capacidad del diseñador de determinar qué herramientas, procesos y marcos conceptuales usa; resistencia activa a la dependencia acrítica de sistemas que definen qué preguntas son válidas
  - `poblaciones-sinteticas` (ia · 2026-06-18) — conjuntos de agentes LLM que simulan la distribución estadística de comportamientos de grupos humanos (silicon sampling); distinción clave con usuarios sintéticos: es fenómeno de distribución, no de perfil individual
  - `impuesto-de-alineacion` (ia · 2026-06-15) — el costo estructural de hacer que los modelos frontier sean seguros y útiles; cada capa de RLHF y filtering consume capacidad y velocidad, creando una brecha entre el potencial del modelo y su comportamiento observable
  - `representacion-agente` (ia · 2026-06-13) — el problema de identidad y autorización cuando un agente actúa en nombre de una persona ante otros agentes: quién habla, con qué mandato, y cómo se verifica esa relación
  - `inteligencia-como-utilidad` (ia · 2026-06-13) — la inferencia de LLMs recorre el mismo ciclo de commoditización que la electricidad y el cómputo en la nube; la inteligencia pasa de ventaja competitiva a infraestructura invisible
  - `ingenieria-agentica` (ia · 2026-06-13) — el paradigma que sucede al vibe coding: diseño de sistemas donde agentes LLM coordinan herramientas y sub-agentes para completar tareas de forma autónoma; el flujo de trabajo como objeto de diseño primario
  - `presupuesto-ia-como-restriccion` (economia · 2026-06-12) — el costo operativo de los LLMs como restricción de diseño de producto; decisiones de arquitectura guiadas por costo de tokens, latencia y disponibilidad de modelo
  - `workforce-de-agentes` (organizaciones · 2026-06-10) — el conjunto de agentes IA que una organización despliega con estructura explícita de empleos, roles y accountability; los agentes como fuerza laboral complementaria, no solo herramienta
- **Correlaciones recientes (2026-06-10):** 10 correlaciones documentadas cubriendo tensiones entre: autoautomatización vs. competencia oculta, conocimiento-LLM vs. metacognición, corrupción silenciosa vs. comprehension debt, cuerpo vs. juicio completo, de-usuario a cliente vs. agencia humana, equipos pequeños vs. comprehension debt, espiral delusional vs. capital de contexto, gobernanza performativa vs. sycophancy, impuesto de verificación vs. pit-stop, inversión sesgo tecnológico vs. filtro de entrada
- **Skill nueva (2026-06-20):** `/presentacion-html [slug] [formato]` — genera una presentación HTML autocontenida y lista para presentar a partir de cualquier concepto del vault. Formato `business-case` implementado. Plantillas en `Plantillas/presentaciones/`
- **Mejora-006 activa:** grafo tipado de relaciones. 21+ conceptos con campo `edges:` (tipos: `contradicts`, `requires`, `enables`, `refines`, `extends`, `exemplifies`, `same_mechanism_as`). ATLAS incluye sección "Grafo tipado de relaciones"
- **Capacidad Remotion activa:** generación de videos animados desde conceptos del vault. Dos composiciones: `ConceptoVideo` y `PresentacionVideo`. Script en `Prompts/Meta/generar_video.py`

---

## Estructura de carpetas

Los conceptos viven en `Conocimiento/Conceptos/` organizados en 6 subcarpetas temáticas:

```
Conocimiento/Conceptos/
├── ia/             (26 conceptos) — tecnología, modelos, agentes IA
├── diseno/         (13 conceptos) — proceso de diseño, rol del diseñador, UX agéntico
├── producto/       (12 conceptos) — construir, medir, iterar productos
├── organizaciones/ (9 conceptos)  — equipos, roles, transformación organizacional
├── economia/       (5 conceptos)  — mercado laboral, impacto económico de la IA
└── filosofia/      (5 conceptos)  — pensamiento abstracto, epistemología, marcos
```

Sistemas adicionales:
- `Backlog/` — pipeline para ideas de proyectos construibles
- `Inbox/` — archivo de entrada para scouts y fuentes sin procesar
- `docs/` — planes de implementación de mejoras del vault
- `Prompts/Meta/jarvis/` — daemon de voz de Jarvis (corre como `Jarvis.app` vía launchd, log en `~/Library/Logs/jarvis.log`)
- `Plantillas/presentaciones/` — sistema de plantillas para generación de presentaciones HTML
  - `html-base.md` — sistema visual compartido (paleta, tipografía, componentes CSS)
  - `business-case.md` — mapa narrativo completo (12 secciones, mapping vault→HTML)
- `.claude/commands/presentacion-html.md` — skill `/presentacion-html [slug] [formato]` para generar HTML desde conceptos del vault

---

## Los 70 conceptos activos

### ia/ (26 conceptos)

| slug | título |
|---|---|
| `agentes-ia` | Equipos de agentes IA |
| `ai-evals-como-disciplina` | AI Evals como disciplina de producto |
| `arnes-del-agente` | Arnés del agente |
| `autoautomatizacion-del-disenador` | La trampa de la autoautomatización |
| `automatizacion-vs-ampliacion` | Automatización vs. amplificación |
| `capital-de-contexto` | Capital de contexto |
| `comprehension-debt` | Comprehension debt |
| `conocimiento-autoorganizado-por-llm` | Conocimiento autoorganizado por LLM |
| `design-system-como-api-para-agentes` | El design system como API para agentes |
| `espectro-autonomia-agente` | Espectro de autonomía del agente |
| `espiral-delusional` | Espiral delusional |
| `fabrica-oscura-de-software` | La fábrica oscura de software |
| `gobernanza-ia-performativa` | Gobernanza de IA performativa |
| `impuesto-de-alineacion` | El impuesto de alineación |
| `impuesto-de-verificacion` | El impuesto de verificación |
| `ingenieria-agentica` | Ingeniería agéntica |
| `inteligencia-como-utilidad` | Inteligencia como utilidad |
| `legibilidad-de-maquina` | Legibilidad de máquina |
| `orquestacion-de-agentes` | Orquestación de agentes |
| `poblaciones-sinteticas` | Poblaciones sintéticas |
| `representacion-agente` | Representación agente |
| `riesgo-geopolitico-del-modelo` | Riesgo geopolítico del modelo IA |
| `spec-driven-development` | Spec-Driven Development |
| `usuarios-sinteticos` | Usuarios sintéticos |
| `vibe-coding` | Vibe coding |
| `web-bifurcada` | Web bifurcada |

### diseno/ (13 conceptos)

| slug | título |
|---|---|
| `agencia-humana-como-imperativo-ux` | Agencia humana como imperativo UX |
| `arquitectura-de-confianza` | Arquitectura de confianza |
| `de-usuario-a-cliente-servido` | De usuario a cliente servido |
| `disenador-a-constructor` | Del diseñador al constructor |
| `diseno-dos-velocidades` | Diseño en dos velocidades |
| `diseno-uxui-y-ia` | Diseño UX/UI con IA |
| `el-moat-del-gusto` | El moat del gusto |
| `fundamentales-vs-flux` | Fundamentales vs. flux |
| `metacognicion-del-disenador` | Metacognición del diseñador |
| `quien-controla-el-prompt` | Quien controla el prompt controla el producto |
| `soberania-epistemica` | Soberanía epistémica |
| `sycophancy-como-riesgo-de-diseno` | Sycophancy como riesgo de diseño |
| `ux-checkpoints` | UX Checkpoints |

### producto/ (12 conceptos)

| slug | título |
|---|---|
| `claridad-antes-de-velocidad` | Claridad antes de velocidad |
| `confianza-a-traves-de-velocidad` | Confianza a través de velocidad |
| `copiloto-de-producto` | Copiloto de producto |
| `corrupcion-silenciosa-por-delegacion` | Corrupción silenciosa por delegación |
| `expertise-de-dominio-en-producto` | Expertise de dominio como infraestructura de producto |
| `feedback-que-escala` | El feedback que escala |
| `las-tres-caras-del-producto-agentico` | Las tres caras del producto agéntico |
| `metricas-post-pantalla` | Métricas post-pantalla |
| `mvp-a-prototipo-en-produccion` | Del MVP al prototipo en producción |
| `pit-stop-cognitivo` | Pit stop cognitivo |
| `pmf-perecedero` | PMF perecedero |
| `restriccion-de-tiempo-como-ventaja` | Restricción de tiempo como ventaja |

### organizaciones/ (9 conceptos)

| slug | título |
|---|---|
| `aprendizaje-vicario-mediado-por-agente` | Aprendizaje vicario mediado por agente |
| `automatizar-mi-propio-trabajo` | Mi trabajo es automatizar mi trabajo |
| `condicion-redespliegue` | La condición del redespliegue |
| `deuda-cognitiva-organizacional` | Deuda cognitiva organizacional |
| `equipos-pequenos-alto-impacto` | Equipos pequeños de alto impacto |
| `ia-sin-ecosistema` | IA sin ecosistema |
| `juicio-como-trabajo-completo` | El juicio como trabajo completo |
| `la-competencia-que-oculta-el-juicio` | La competencia que oculta el juicio |
| `workforce-de-agentes` | Workforce de Agentes |

### economia/ (5 conceptos)

| slug | título |
|---|---|
| `ia-como-filtro-de-entrada` | IA como filtro de entrada al mercado laboral |
| `inversion-sesgo-tecnologico` | La inversión del sesgo tecnológico |
| `marea-creciente-de-automatizacion` | Marea creciente de automatización |
| `presupuesto-ia-como-restriccion` | El presupuesto de IA como restricción operativa |
| `senal-anticipada-mercado-laboral` | Señal anticipada en el mercado laboral |

### filosofia/ (5 conceptos)

| slug | título |
|---|---|
| `arquitectura-de-inteligencia` | Arquitectura de inteligencia |
| `colonialismo-cultural-digital` | Colonialismo cultural digital |
| `cuerpo-como-infraestructura-cognitiva` | El cuerpo como infraestructura cognitiva |
| `lo-ilegible-como-senal` | Lo ilegible como señal |
| `momento-liminal` | El momento liminal |

---

## Las 27 correlaciones documentadas

| archivo | conceptos | descripción breve |
|---|---|---|
| `2026-04-03_vibe-coding--spec-driven-development` | vibe-coding + spec-driven-development | Velocidad sin estructura vs. estructura que habilita velocidad |
| `2026-04-10_claridad-antes-de-velocidad--momento-liminal` | claridad-antes-de-velocidad + momento-liminal | Por qué la pausa reflexiva es condición de la claridad |
| `2026-04-10_fundamentales-vs-flux--disenador-a-constructor` | fundamentales-vs-flux + disenador-a-constructor | Lo que permanece cuando el rol cambia |
| `2026-04-11_automatizar-mi-propio-trabajo--expertise-de-dominio-en-producto` | automatizar-mi-propio-trabajo + expertise-de-dominio | El dominio como condición para automatizar sin perder criterio |
| `2026-04-15_automatizacion-vs-ampliacion--fundamentales-vs-flux` | automatizacion-vs-ampliacion + fundamentales-vs-flux | Qué se amplifica vs. qué se reemplaza |
| `2026-04-15_ia-como-filtro-de-entrada--agentes-ia` | ia-como-filtro-de-entrada + agentes-ia | Los agentes como causa del filtro |
| `2026-04-15_ia-como-filtro-de-entrada--disenador-a-constructor` | ia-como-filtro-de-entrada + disenador-a-constructor | El constructor como ruta alternativa al filtro |
| `2026-04-15_senal-anticipada-mercado-laboral--gobernanza-ia-performativa` | senal-anticipada + gobernanza-performativa | Las señales que la gobernanza ignora |
| `2026-04-18_copiloto-de-producto--quien-controla-el-prompt` | copiloto-de-producto + quien-controla-el-prompt | Quien diseña el copiloto controla la decisión |
| `2026-04-18_espectro-autonomia-agente--capital-de-contexto` | espectro-autonomia + capital-de-contexto | El contexto como determinante del nivel de autonomía viable |
| `2026-04-18_espectro-autonomia-agente--fabrica-oscura-de-software` | espectro-autonomia + fabrica-oscura | Autonomía total = opacidad total |
| `2026-04-18_fabrica-oscura-de-software--capital-de-contexto` | fabrica-oscura + capital-de-contexto | El contexto como antídoto de la oscuridad |
| `2026-04-18_pit-stop-cognitivo--confianza-a-traves-de-velocidad` | pit-stop-cognitivo + confianza-a-traves-de-velocidad | La pausa como generadora de confianza |
| `2026-04-18_pit-stop-cognitivo--feedback-que-escala` | pit-stop-cognitivo + feedback-que-escala | El pit-stop como mecanismo de feedback distribuido |
| `2026-05-13_aprendizaje-vicario-mediado-por-agente--capital-de-contexto` | aprendizaje-vicario + capital-de-contexto | El agente como generador de contexto compartido |
| `2026-05-13_aprendizaje-vicario-mediado-por-agente--feedback-que-escala` | aprendizaje-vicario + feedback-que-escala | El agente público como feedback que escala sin fricción |
| `2026-05-13_aprendizaje-vicario-mediado-por-agente--juicio-como-trabajo-completo` | aprendizaje-vicario + juicio-como-trabajo-completo | Observar el juicio del agente como entrenamiento del propio |
| `2026-06-10_autoautomatizacion-del-disenador--la-competencia-que-oculta-el-juicio` | autoautomatizacion + competencia-oculta | La autoautomatización como forma de enmascarar la ausencia de criterio |
| `2026-06-10_conocimiento-autoorganizado-por-llm--metacognicion-del-disenador` | conocimiento-autoorganizado + metacognicion | Delegar la organización vs. ejercer la metacognición |
| `2026-06-10_corrupcion-silenciosa-por-delegacion--comprehension-debt` | corrupcion-silenciosa + comprehension-debt | Dos formas de perder comprensión del sistema que se construye |
| `2026-06-10_cuerpo-como-infraestructura-cognitiva--juicio-como-trabajo-completo` | cuerpo-infraestructura + juicio-completo | El cuerpo como condición del juicio no delegable |
| `2026-06-10_de-usuario-a-cliente-servido--agencia-humana-como-imperativo-ux` | de-usuario-a-cliente + agencia-humana | El cambio de rol del usuario como colapso de su agencia |
| `2026-06-10_equipos-pequenos-alto-impacto--comprehension-debt` | equipos-pequenos + comprehension-debt | El modelo de éxito lleva el riesgo incorporado |
| `2026-06-10_espiral-delusional--capital-de-contexto` | espiral-delusional + capital-de-contexto | El contexto como escudo contra la espiral |
| `2026-06-10_gobernanza-ia-performativa--sycophancy-como-riesgo-de-diseno` | gobernanza-performativa + sycophancy | La gobernanza que replica el problema que intenta resolver |
| `2026-06-10_impuesto-de-verificacion--pit-stop-cognitivo` | impuesto-de-verificacion + pit-stop | El pit-stop como pago deliberado del impuesto de verificación |
| `2026-06-10_inversion-sesgo-tecnologico--ia-como-filtro-de-entrada` | inversion-sesgo + ia-filtro-entrada | La escalera que se desmonta desde los dos extremos |
