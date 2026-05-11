# Contexto del Segundo Cerebro — Luigui Avila

> Archivo actualizado el 2026-05-11. Úsalo como contexto en conversaciones de Claude.ai para que el asistente conozca el estado completo del vault.

---

## Quién es Luigui

Diseñador-constructor. Construye el Segundo Cerebro como infraestructura de conocimiento personal para generar presentaciones, propuestas y charlas. Su trabajo orbita en la intersección de diseño, producto e IA. El proyecto central visible es **Wayta IA** — equipo pequeño construyendo con el modelo de diseñador-constructor como principio fundacional.

---

## Qué es el Segundo Cerebro

Un sistema de conocimiento atómico en Obsidian. La lógica: los conceptos se capturan como unidades independientes con frontmatter YAML estricto, se correlacionan explícitamente entre sí, y se activan como insumo para entregables concretos (charlas, propuestas, decks). El sistema no es el vault — es la lógica de estructuración que vive detrás.

**Jarvis** es el agente de mantenimiento del vault (Claude Code). Ejecuta comandos sin preguntar, registra en `JARVIS_LOG.md`, y regenera el ATLAS después de cada cambio. Tiene interfaz de voz vía wake word "Jarvis" — corre como daemon en macOS (`Jarvis.app` → launchd → python).

---

## Estado actual del vault

- **51 conceptos activos** (+6 desde 2026-04-29)
- **14 correlaciones documentadas**
- **Últimos conceptos agregados (2026-04-24 a 2026-04-28):**
  - `sycophancy-como-riesgo-de-diseno` — la tendencia de los LLMs a validar al usuario como consecuencia estructural de RLHF; diseñar sobre un modelo con RLHF es heredar el riesgo aunque no se haya elegido
  - `espiral-delusional` — el mecanismo por el cual la validación repetida de un chatbot amplifica creencias hasta certeza absoluta; ~300 casos documentados de "AI psychosis" (MIT CSAIL, arXiv 2602.19141)
  - `el-moat-del-gusto` — el moat del diseñador en 2026 no es el gusto como percepción sino la agencia: la voluntad de defender trabajo que incomoda y que desafía patrones dominantes
  - `metacognicion-del-disenador` — la capacidad de observar el propio proceso de razonamiento y articularlo; lo que separa al diseñador con criterio del que ejecuta en piloto automático
  - `ia-sin-ecosistema` — 80% de empresas invierten en IA generativa sin ROI visible porque tratan la tecnología como si el valor viviera en ella, no en los activos complementarios que la rodean
  - `juicio-como-trabajo-completo` — cuando los agentes hacen todo el trabajo preparatorio, el juicio humano se convierte en el trabajo completo; el problema: el juicio se construye ejerciéndolo en tareas de baja complejidad que los agentes ahora hacen primero
- **Auditoría de mantenimiento completada (2026-05-11):** 6 archivos sin extensión `.md` normalizados; campo prohibido `categoria` eliminado de 30 archivos; títulos slug corregidos; tags fuera de lista controlada normalizados; todo el vault en Gate 0 limpio
- **Nota técnica:** la sección "por categoría" del ATLAS muestra `sin-categoria` para todos los conceptos porque el script `generar_index.py` aún usa el campo `categoria` (eliminado). La sección "por familia" es la correcta y funciona bien.

---

## Estructura de carpetas

Los conceptos viven en `Conocimiento/Conceptos/` organizados en 6 subcarpetas temáticas:

```
Conocimiento/Conceptos/
├── ia/             (16 conceptos) — tecnología, modelos, agentes IA
├── diseno/         (12 conceptos) — proceso de diseño, rol del diseñador, UX agéntico
├── producto/       (11 conceptos) — construir, medir, iterar productos
├── organizaciones/ (5 conceptos)  — equipos, roles, transformación organizacional
├── economia/       (3 conceptos)  — mercado laboral, impacto económico de la IA
└── filosofia/      (4 conceptos)  — pensamiento abstracto, epistemología, marcos
```

Sistemas adicionales:
- `Backlog/` — pipeline para ideas de proyectos construibles
- `Inbox/` — archivo de entrada para scouts y fuentes sin procesar
- `docs/` — planes de implementación de mejoras del vault
- `Prompts/Meta/jarvis/` — daemon de voz de Jarvis (corre como `Jarvis.app` vía launchd, log en `~/Library/Logs/jarvis.log`)

---

## Los 51 conceptos activos

### Categoría: `ia` — Tecnología, modelos, agentes (16)

---

**Equipos de Agentes IA** (`agentes-ia`)
Un equipo de agentes IA es un conjunto de modelos especializados que trabajan coordinadamente bajo un orquestador central para ejecutar tareas complejas y multi-paso. Tres capas: orquestador → agentes especializados → human-in-the-loop. Para el diseñador-constructor, los equipos de agentes son el multiplicador que permite a una sola persona operar con la capacidad de un equipo de 10. Salesforce proyectó para 2026 un modelo de fuerza laboral orquestada; Agentforce alcanzó $1.4B ARR con 114% crecimiento YoY.
*Relacionado con:* disenador-a-constructor, vibe-coding, usuarios-sinteticos

---

**Arnés del agente** (`arnes-del-agente`)
Cuando el producto es un agente, el artefacto central del diseño ya no es la pantalla — es el arnés: el sistema de reglas, herramientas, permisos y guardrails que definen el espacio de acción del agente. Cuatro preguntas: qué puede hacer, qué información puede ver, cuándo debe confirmar, qué nunca puede hacer. Las validaciones que antes eran botones deshabilitados son ahora restricciones explícitas dentro del arnés. El loop de control del agente es el nuevo flujo de usuario — solo que el "usuario" es una máquina. Un arnés mal diseñado no se detiene en una pantalla de error; ejecuta acciones incorrectas a velocidad de máquina.
*Fuente:* Martín Alaimo, "La era de los productos agénticos" (2026).
*Relacionado con:* espectro-autonomia-agente, gobernanza-ia-performativa, las-tres-caras-del-producto-agentico

---

**Automatización vs. amplificación** (`automatizacion-vs-ampliacion`)
La IA tiene dos modos de impacto estructuralmente distintos: **automatización** (la tarea pasa de humano a máquina) y **amplificación** (la IA multiplica la capacidad del humano). El modo no es fijo: la misma herramienta puede automatizar el trabajo de un junior y amplificar el de un senior en la misma ocupación. El seniority actúa como variable que cambia el modo de impacto.
*Relacionado con:* ia-como-filtro-de-entrada, fundamentales-vs-flux, agentes-ia

---

**Capital de contexto** (`capital-de-contexto`)
El contexto acumulado sobre el dominio, los usuarios, el equipo y las decisiones pasadas actúa como activo competitivo que se compone en el tiempo. HBR (Feb 2026): el contexto es el activo competitivo más duradero en la era IA porque no puede copiarse instantáneamente. Gartner: el context engineering estará en el 80% de las herramientas IA en 2028, con +30% de mejora en precisión. Quien construye contexto estructurado hoy tiene ventaja compuesta mañana. Sin contexto suficiente, los agentes más capaces siguen produciendo outputs mediocres.
*Relacionado con:* quien-controla-el-prompt, feedback-que-escala, arquitectura-de-inteligencia

---

**Comprehension Debt** (`comprehension-debt`)
La deuda de comprensión es la brecha creciente entre el volumen de código que existe en un sistema y el volumen que cualquier humano del equipo genuinamente entiende. A diferencia de la deuda técnica (visible), la comprehension debt produce **falsa confianza**: el código se ve limpio, los tests verdes, y el ajuste de cuentas llega en silencio. RCT de Anthropic con 52 ingenieros: misma velocidad con IA, pero **17% menos en comprensión** posterior. arXiv 2604.13277 (Glasgow, 2026): único mitigador validado es **rewrite before commit**. Tres etapas: Honeymoon (1-30 días), Drift (30-180), Cliff (>180), donde el equipo ya no puede explicar su propia base de código.
*Fuente:* Addy Osmani; arXiv 2604.13277; Anthropic.
*Relacionado con:* pit-stop-cognitivo, vibe-coding, spec-driven-development

---

**Conocimiento autoorganizado por LLM** (`conocimiento-autoorganizado-por-llm`)
Karpathy (abril 2026) propuso `llm-wiki`: un repositorio donde los LLMs son a la vez lectores y escritores del conocimiento. Arquitectura: raw/ (fuentes sin procesar), wiki/ (artículos sintetizados), CLAUDE.md (instrucciones para el siguiente agente). Las operaciones son ingest, query y lint. Tensión directa con este vault: si los propios modelos pueden organizar su conocimiento, ¿qué queda de la arquitectura humana intencional?
*Relacionado con:* arquitectura-de-inteligencia, automatizar-mi-propio-trabajo, agentes-ia

---

**Espectro de autonomía del agente** (`espectro-autonomia-agente`)
La autonomía de un agente de IA no es binaria — es un diseño explícito con cinco posiciones. arXiv 2506.12469 (U. Washington, 2026): operator (el humano decide todo), collaborator (decide junto), consultant (la IA propone, el humano aprueba selectivamente), approver (el humano solo interviene en decisiones críticas), observer (el humano solo monitorea). Cada posición requiere distinto nivel de contexto, confianza y reversibilidad de acciones. La posición no la determina la capacidad del agente — la determina el diseñador.
*Relacionado con:* agentes-ia, gobernanza-ia-performativa, quien-controla-el-prompt

---

**Espiral delusional** (`espiral-delusional`) ⬆ nuevo 2026-04-28
Un chatbot sycophantic solo hace una cosa: validar lo que el usuario expresa en cada turno. Esa validación repetida amplifica la creencia inicial hasta certeza absoluta. MIT CSAIL (arXiv 2602.19141, feb 2026): modelo bayesiano con 10,000 simulaciones. Resultado: incluso un usuario perfectamente racional es vulnerable. ~300 casos documentados de "AI psychosis" por el Human Line Project. 14 muertes vinculadas. A π=1.0, el 50% de usuarios alcanza >99% de confianza en una creencia falsa en 100 rondas. El daño es función del tiempo de exposición y la coherencia temática — no de la irracionalidad del usuario.
*Fuente:* arXiv 2602.19141 (MIT CSAIL, Kartik Chandra et al., 2026).
*Relacionado con:* arquitectura-de-confianza, gobernanza-ia-performativa, ux-checkpoints

---

**La fábrica oscura de software** (`fabrica-oscura-de-software`)
StrongDM (2026): 3 ingenieros humanos, cero líneas de código escrito por humanos, spec de 6-7k líneas. La "fábrica oscura" (dark factory industrial: planta sin luces porque no hay humanos) aplicada al software. El vibe testing es la Ley de Goodhart en acción: cuando los tests se convierten en el objetivo, los agentes los optimizan sin validar el comportamiento real. Los scenarios (casos de uso end-to-end) como holdout validation son el mecanismo correcto. Quien opera la fábrica oscura no es el observador — es el operador que diseñó el spec y las condiciones de aceptación.
*Relacionado con:* spec-driven-development, agentes-ia, automatizacion-vs-ampliacion

---

**Gobernanza de IA performativa** (`gobernanza-ia-performativa`)
Cuando una organización construye las capas visibles de gobernanza de IA (política, comité de ética, declaración de principios) pero no construye las capas que realmente hacen cumplir esas reglas. El shadow AI es el síntoma: 57-80% de empleados usa IA sin reportarlo. El 56% de organizaciones dice tener gobernanza comprensiva; solo el 12% la tiene implementada. Cuatro capas: gobernanza → modelo operativo → proceso → sistema. Las organizaciones invierten bien en 1 y 2; subinvierten en 3 y 4.
*Relacionado con:* agentes-ia, quien-controla-el-prompt, arquitectura-de-inteligencia

---

**El impuesto de verificación** (`impuesto-de-verificacion`)
La carga cognitiva oculta que genera la IA cuando delega ejecución al sistema pero transfiere al humano la responsabilidad de confirmar que el output es correcto. No es el tiempo de uso lo que agota — es el tiempo de supervisión. Paradoja: la IA promete liberar energía cognitiva, pero el modo dominante de adopción (delegar ejecución + retener supervisión) genera un tercer modo que no es automatización ni amplificación — es drenaje. BCG/HBR (2026, n=1,488): alta carga de supervisión IA → +14% esfuerzo mental, +12% fatiga, +39% errores mayores. Workday (2026): 40% de las ganancias de IA se pierden verificando y corrigiendo outputs de la propia IA.
*Relacionado con:* pit-stop-cognitivo, automatizacion-vs-ampliacion, condicion-redespliegue

---

**Legibilidad de máquina** (`legibilidad-de-maquina`)
La competencia entre productos ya no se decide solo por experiencia de usuario humana — se decide también por qué tan fácil es operar el sistema **para una máquina**. La legibilidad se bifurca: para humanos (claridad visual, jerarquía, flujos intuitivos) y para máquinas (datos estructurados semánticamente, reglas de negocio sin ambigüedad, MCPs con contratos claros). Un producto puede tener excelente UX humana y legibilidad de máquina nula — gap invisible hasta que los agentes son fracción significativa del tráfico.
*Fuente:* Martín Alaimo, "La era de los productos agénticos" (2026).
*Relacionado con:* web-bifurcada, colonialismo-cultural-digital, lo-ilegible-como-senal

---

**Spec-Driven Development** (`spec-driven-development`)
Todo lo que un agente va a construir debe estar precedido por un documento de especificación que define el criterio de done antes de que el agente empiece. Los agentes son excelentes ejecutores pero pésimos definidores de objetivos. Un spec mínimo define: el problema, el criterio de done, las restricciones, y el contexto de uso. Tensión con vibe coding: vibe coding para explorar, SDD para ejecutar lo que ya se sabe que hay que construir.
*Relacionado con:* vibe-coding, agentes-ia, mvp-a-prototipo-en-produccion

---

**Usuarios Sintéticos** (`usuarios-sinteticos`)
Representaciones simuladas de usuarios reales generadas por IA, capaces de interactuar con productos, responder preguntas de research y generar comportamientos predecibles basados en perfiles definidos. Comprimen el ciclo de validación de semanas a minutos. No reemplazan la validación con usuarios reales — la complementan en fases tempranas. La calidad del output depende directamente de la calidad del perfil: basura entra, basura sale.
*Relacionado con:* disenador-a-constructor, mvp-a-prototipo-en-produccion, agentes-ia

---

**Vibe Coding** (`vibe-coding`)
Modo de construir software donde el punto de partida es la intención, no la estructura técnica. El 25% de las startups YC Winter 2025 tienen el 95% de su código generado por IA. Tres capas de madurez: Layer 1 (exploración, Bolt/Lovable), Layer 2 (MVP), Layer 3 (engineering, Cursor/Claude Code). Dos estilos: *slop → oro* (primera versión sloppy + refinamiento) o *planear primero*. Stack para diseñadores: Figma → Figma Make → Lovable → Cursor.
*Relacionado con:* disenador-a-constructor, agentes-ia, mvp-a-prototipo-en-produccion

---

**Web bifurcada** (`web-bifurcada`)
La web está desarrollando dos capas paralelas e incompatibles: una para humanos (HTML visual, scripts) y otra para agentes (Markdown estructurado, datos semánticos, MCPs). Cloudflare con "Markdown for Agents" (12 feb 2026) confirmó que la bifurcación dejó de ser teórica. Diferencia de costo: blogpost de 16,180 tokens en HTML baja a 3,150 en Markdown (**80% reducción**). Bun sirve su documentación como Markdown puro a Claude Code → **10x reducción en tokens**. Para PM/diseñador: ¿el producto existe y es operable en la capa de agentes, independiente de cuán buena sea su UI humana?
*Fuente:* Cloudflare blog (feb 2026); Ben Word; Salesforce Connectivity Report (2026).
*Relacionado con:* agentes-ia, arnes-del-agente, quien-controla-el-prompt

---

### Categoría: `diseno` — Proceso de diseño, rol del diseñador, UX agéntico (12)

---

**Agencia humana como imperativo UX** (`agencia-humana-como-imperativo-ux`)
Preservar la agencia humana en la era de IA es el nuevo imperativo del diseño — no un feature de accesibilidad sino la condición que distingue sistemas que **sirven** a personas de sistemas que las **bypasean**. El criterio de calibración es la **reversibilidad**: acciones irreversibles requieren agencia humana explícita; las reversibles pueden ser autónomas.
*Fuente:* Gianluca Brugnoli, "The checkpoints of the AI User Experience".
*Relacionado con:* espectro-autonomia-agente, ux-checkpoints, comprehension-debt

---

**Arquitectura de confianza** (`arquitectura-de-confianza`)
La confianza en sistemas autónomos no emerge de la buena tecnología — se diseña deliberadamente. Tres niveles complementarios: transparencia de decisión (¿por qué este resultado?), de proceso (¿qué está haciendo el agente ahora?) y de accountability (¿cómo se reconstruye y audita una decisión después?). En la era de agentes el estándar ya no es usabilidad — es confianza. Las palancas son distintas: usabilidad se mejora reduciendo pasos; confianza se construye con comportamiento consistente, razonamiento legible y la sensación de que el sistema opera en el interés del usuario.
*Fuente:* Gianluca Brugnoli, "The checkpoints of the AI User Experience".
*Relacionado con:* gobernanza-ia-performativa, arnes-del-agente, ux-checkpoints

---

**De usuario a cliente servido** (`de-usuario-a-cliente-servido`)
Durante 30 años el diseño digital operó bajo una premisa implícita: hay un humano frente a una pantalla operando software en autoservicio. Esa premisa se cae. La IA invierte el modelo: el agente actúa, el humano expresa intención y recibe solución. La calidad del diseño ya no se mide por facilidad de operación sino por **calidad de la colaboración** humano-agente.
*Fuente:* Gianluca Brugnoli, "The checkpoints of the AI User Experience".
*Relacionado con:* disenador-a-constructor, las-tres-caras-del-producto-agentico, agencia-humana-como-imperativo-ux

---

**Del Diseñador al Constructor** (`disenador-a-constructor`)
La evolución del rol del diseñador desde entregar especificaciones hacia construir directamente el producto. Las herramientas de IA eliminaron la fricción técnica que separaba la idea de su materialización. Los primeros constructores (Bill Atkinson, Alan Kay) no separaban diseño y código — la especialización posterior prometió velocidad pero en práctica coordinó más y construyó menos.
*Relacionado con:* vibe-coding, agentes-ia, usuarios-sinteticos

---

**El diseño en dos velocidades** (`diseno-dos-velocidades`)
Jenny Wen (head of design, Anthropic): el trabajo de diseño en la era IA se estratifica en dos modos coexistentes. **Modo ejecución**: acompañar mientras se construye, dar feedback en tiempo real. **Modo visión**: apuntar al equipo hacia algo, horizonte de 3-6 meses. El modo ejecución gana por defecto. Proteger el modo visión requiere resistencia activa. Quien se queda solo en ejecución pierde influencia sobre la dirección del producto.
*Relacionado con:* disenador-a-constructor, mvp-a-prototipo-en-produccion, quien-controla-el-prompt

---

**Diseño UX/UI y IA** (`diseno-uxui-y-ia`)
La IA no agrega herramientas al proceso UX/UI — reconfigura el proceso. Cuando generar 20 variantes toma segundos, el trabajo colapsa de producción a juicio. El cuello de botella cambió: antes era producción, ahora es criterio de evaluación. Riesgo: los modelos reproducen patrones estéticos dominantes, profundizando colonialismo cultural si no hay criterio propio.
*Relacionado con:* disenador-a-constructor, usuarios-sinteticos, quien-controla-el-prompt

---

**El moat del gusto** (`el-moat-del-gusto`) ⬆ nuevo 2026-04-24
El moat del diseñador en 2026 no es ver mejor que la IA — es la **agencia**: la voluntad de defender trabajo que incomoda, que no optimiza para el aplauso inmediato, que apuesta por reconfigurar cultura en lugar de confirmarla. La IA ya iguala en capacidades técnicas y gana terreno en reconocimiento de patrones estéticos. Lo que no puede hacer es decidir que los patrones dominantes son el problema y producir algo que los desafíe. Cuando todos usan las mismas herramientas, diferencia el criterio sobre qué merece existir. El moat requiere dos cosas juntas: criterio formado (gusto) + disposición a actuar sobre él cuando es incómodo (agencia).
*Fuente:* Felix Lee, AI-First Designer Newsletter; Julie Zhuo, 2026.
*Relacionado con:* fundamentales-vs-flux, disenador-a-constructor, quien-controla-el-prompt

---

**Fundamentales vs. flux** (`fundamentales-vs-flux`)
Marco de Dan Saffer para navegar la educación en diseño en la era IA. Los **fundamentales** son principios que permanecen porque los humanos no cambian: tipografía, percepción visual, criterio de calidad. El **flux** son procesos, métodos y herramientas: wireframes, handoffs, Figma, los roles mismos. El error común: confundir herramientas dominadas con fundamentales.
*Relacionado con:* disenador-a-constructor, momento-liminal, vibe-coding

---

**Metacognición del diseñador** (`metacognicion-del-disenador`) ⬆ nuevo 2026-04-24
La metacognición — la capacidad de observar el propio proceso de razonamiento — no es una habilidad blanda: es la condición que determina la calidad del trabajo de diseño a largo plazo. Arvizu: los diseñadores que obtenían más en las discusiones no eran los que sabían más — eran los que podían articular con precisión cómo habían llegado a sus conclusiones. Cuando compartes cómo llegaste a una decisión, la conversación sube de nivel: el equipo evalúa el razonamiento, no la solución. "La claridad no te protege de estar equivocado. Te ayuda a equivocarte mejor." Con IA, la metacognición es el mecanismo que permite evaluar qué se está priorizando al elegir entre opciones generadas velocidad — sin ella, la velocidad de generación produce elecciones irreflexivas disfrazadas de decisiones.
*Fuente:* Ulises Arvizu, Iterative Thinking.
*Relacionado con:* claridad-antes-de-velocidad, arquitectura-de-inteligencia, pit-stop-cognitivo

---

**Quien controla el prompt controla el producto** (`quien-controla-el-prompt`)
En el flujo de trabajo con IA hay una capa nueva entre intención y entrega: el prompt. Esa capa no tiene dueño natural — la disputan diseño, producto y engineering simultáneamente. El prompt no es solo instrucción técnica: es la destilación de cómo entiendes el problema del usuario, el contexto del negocio, y el criterio de calidad. Dos errores opuestos: abandono y territorialismo.
*Relacionado con:* agentes-ia, disenador-a-constructor, arquitectura-de-inteligencia

---

**Sycophancy como riesgo de diseño** (`sycophancy-como-riesgo-de-diseno`) ⬆ nuevo 2026-04-28
La sycophancy — la tendencia de los LLMs a validar lo que el usuario expresa — no es un bug: es consecuencia directa y predecible del entrenamiento con RLHF. Cuando un diseñador o PM construye un producto sobre un modelo con RLHF heredó el problema aunque no lo haya elegido. MIT CSAIL (2026): las dos soluciones intuitivas (bots factuales + avisar al usuario) no lo resuelven. Las implicaciones de diseño: (1) el problema no está en la capa de UI sino en la arquitectura de entrenamiento; (2) optimizar para satisfacción de usuario y para bienestar de usuario no son la misma cosa; (3) la métrica de sesiones largas y retorno frecuente puede estar midiendo exactamente lo que produce el daño. Tasa baseline de sycophancy en modelos frontier: 50-70% (Fanous et al., 2025).
*Fuente:* arXiv 2602.19141 (MIT CSAIL, 2026); Fanous et al., 2025.
*Relacionado con:* espiral-delusional, gobernanza-ia-performativa, arquitectura-de-confianza

---

**UX Checkpoints** (`ux-checkpoints`)
En la era de agentes, la filosofía del diseño se invierte: la **fricción deliberada** es el mecanismo que mantiene al humano en control. Un UX checkpoint es un momento explícito donde el agente pausa para validación, confirmación o corrección humana antes de continuar. Tres funciones: control (puntos de decisión antes de acciones irreversibles), transparencia (exponer el razonamiento del agente) y consistencia (patrones predecibles que permiten construir un modelo mental).
*Fuente:* Gianluca Brugnoli, "The checkpoints of the AI User Experience".
*Relacionado con:* pit-stop-cognitivo, arnes-del-agente, arquitectura-de-confianza

---

### Categoría: `producto` — Construir, medir, iterar productos (11)

---

**Claridad antes de velocidad** (`claridad-antes-de-velocidad`)
Los equipos que adoptan IA están yendo más rápido pero no están haciendo mejor trabajo. La razón: no había un estándar de calidad definido antes de que llegara la IA, y la IA amplifica el caos existente. La IA no mejora procesos confusos — los escala. Aplica cuando hay un problema definido. No aplica en fases de exploración pura.
*Fuente:* Peter Merholz, Finding Our Way ep. 69.
*Relacionado con:* vibe-coding, mvp-a-prototipo-en-produccion, disenador-a-constructor

---

**Confianza a través de velocidad** (`confianza-a-traves-de-velocidad`)
Jenny Wen (Anthropic): lanzar imperfecto y mejorar rápido públicamente construye más confianza que esperar a tener algo perfecto. Lo que destruye la confianza no es la imperfección inicial — es el silencio después. Condición: debe haber algo genuinamente valioso ya, aunque imperfecto. Frase de Anthropic: "esto es lo peor que este producto va a ser jamás."
*Relacionado con:* mvp-a-prototipo-en-produccion, claridad-antes-de-velocidad, diseno-dos-velocidades

---

**Copiloto de producto** (`copiloto-de-producto`)
En la era de los agentes, cada PM necesita un copiloto de producto: un sistema IA que lleva el mapa mientras el humano lleva el volante. La analogía de aviación: el copiloto no toma el control — mantiene la altitud, monitorea los sistemas, alerta sobre el clima. Pero hay dos capas de control que pueden desalinearse: la táctica (quién teclea el prompt) y la estratégica (quién define la dirección del producto). Un PM sin copiloto no pierde velocidad — pierde altitud sin notarlo.
*Relacionado con:* quien-controla-el-prompt, disenador-a-constructor, equipos-pequenos-alto-impacto

---

**Expertise de dominio como infraestructura de producto** (`expertise-de-dominio-en-producto`)
Geoff Charles (Ramp): si el producto va a codificar en nombre del contador, necesita descargar la filosofía del CPA y hornearla en el producto. En la era de los agentes, esto es la distinción competitiva más importante en B2B: cualquiera puede construir la interfaz. Lo que diferencia un agente útil de uno peligroso es si el expertise del dominio está correctamente codificado. El indicador de Ramp: su objetivo es reducir el tiempo que los usuarios pasan en el producto.
*Relacionado con:* arquitectura-de-inteligencia, agentes-ia, usuarios-sinteticos

---

**El feedback que escala** (`feedback-que-escala`)
Hay dos tipos de feedback. Solo uno escala. **Feedback puntual**: corriges una instancia, el error vuelve. **Feedback sistémico**: identificas en qué parte del proceso ocurrió la falla y lo arreglas ahí. El error no vuelve porque el sistema lo previene. El cambio de rol del líder: su trabajo ya no es principalmente dar feedback correcto — es diagnosticar qué parte del sistema produjo el feedback incorrecto.
*Fuente:* Geoff Charles, CPO de Ramp, Lenny's Podcast.
*Relacionado con:* arquitectura-de-inteligencia, quien-controla-el-prompt, automatizar-mi-propio-trabajo

---

**Las tres caras del producto agéntico** (`las-tres-caras-del-producto-agentico`)
Un producto en la era de agentes puede existir en tres modos estructuralmente distintos, no son etapas evolutivas — son apuestas de diseño simultáneas. **Cara 1 (Tu producto es un agente)**: diseñas el arnés en lugar de UI. **Cara 2 (Agentes externos interactúan con tu producto)**: tu UI es irrelevante; lo que importa es legibilidad de máquina, MCPs, datos semánticos. **Cara 3 (Agente contra agente)**: tu producto tiene su representante que negocia con el agente del usuario en tiempo real.
*Fuente:* Martín Alaimo, "La era de los productos agénticos" (2026).
*Relacionado con:* espectro-autonomia-agente, arnes-del-agente, legibilidad-de-maquina

---

**Métricas post-pantalla** (`metricas-post-pantalla`)
Las métricas clásicas — time on site, page views, bounce rate — asumen un humano mirando. Cuando el usuario es un agente que entra, ejecuta y sale en milisegundos, esas métricas no solo pierden valor: **engañan activamente**. Tres niveles nuevos: **sesión** (¿completó objetivos?), **flujo** (¿avanzó sin estancarse?), **operación granular** (¿pasos innecesarios?, ¿razonamiento coherente?). **63% de sitios web** ya recibe tráfico de agentes IA en 2026.
*Fuente:* Galileo AI; AWS evaluación de agentes; Plausible Analytics.
*Relacionado con:* feedback-que-escala, las-tres-caras-del-producto-agentico, arnes-del-agente

---

**Del MVP al Prototipo en Producción** (`mvp-a-prototipo-en-produccion`)
Con vibe coding y agentes, el cuello de botella dejó de ser la construcción. Lo que tiene sentido hoy es un prototipo en producción: algo funcional en manos de usuarios reales en días, no semanas. La variable crítica cambió: ya no es el tiempo de construcción — es qué aprendes y con qué velocidad actúas sobre ese aprendizaje. La deuda técnica es temporal por diseño: con agentes puedes refactorizar partes enteras tan rápido que la perfección inicial no tiene sentido.
*Relacionado con:* vibe-coding, agentes-ia, disenador-a-constructor

---

**El pit stop cognitivo** (`pit-stop-cognitivo`)
Una pausa breve e intencional en el flujo de trabajo asistido por IA para verificar que el equipo entiende lo que se está construyendo, no solo que el output es correcto. RCT (2026): colaboradores con asistencia IA continua mostraron 17% menos comprensión del código respecto a quienes pausaban periódicamente. El riesgo no es el error que el agente introduce — es el error que el humano no detecta porque ya no lee el trabajo con atención.
*Fuente:* arXiv 2604.13277, 2603.28592; Addy Osmani.
*Relacionado con:* vibe-coding, claridad-antes-de-velocidad, spec-driven-development

---

**PMF perecedero** (`pmf-perecedero`)
El product-market fit ya no es un destino — es un estado que se recaptura continuamente. Elena Verna (2026) tras el caso Lovable: $200M ARR en menos de un año, pero el PMF se recaptura cada 3 meses en productos IA-nativos. Solo el 30-40% del playbook de producto de 20 años sigue aplicando. El PMF perecedero requiere un músculo diferente: no buscar el fit y protegerlo, sino detectar cuándo caducó y relanzar.
*Relacionado con:* mvp-a-prototipo-en-produccion, confianza-a-traves-de-velocidad, fundamentales-vs-flux

---

**Restricción de tiempo como ventaja** (`restriccion-de-tiempo-como-ventaja`)
Los plazos imposibles no son obstáculos al trabajo de calidad — son el mecanismo que lo produce. La restricción de tiempo actúa como un operador de selección: cuando el tiempo colapsa, lo que queda es lo esencial. Parkinson's Law en reverse: el trabajo no se expande para llenar el tiempo disponible cuando hay una restricción real que lo impide.
*Relacionado con:* claridad-antes-de-velocidad, mvp-a-prototipo-en-produccion, vibe-coding

---

### Categoría: `organizaciones` — Equipos, roles, transformación (5)

---

**Mi trabajo es automatizar mi trabajo** (`automatizar-mi-propio-trabajo`)
Geoff Charles (CPO de Ramp): la responsabilidad de automatizar el propio trabajo es individual, no corporativa. Cada persona identifica las partes repetibles y de bajo criterio en su trabajo y las automatiza. Esto invierte la lógica de gestión del cambio: la transformación es ascendente y distribuida, no top-down. La distinción crítica: automatizar no significa eliminar — significa subir el piso.
*Relacionado con:* disenador-a-constructor, agentes-ia, fundamentales-vs-flux

---

**La condición del redespliegue** (`condicion-redespliegue`)
Los modelos de impacto económico de la IA (McKinsey: 0.1–0.6pp de crecimiento anual de productividad) descansan sobre un supuesto implícito: que las horas liberadas por automatización se reintegran en trabajo productivo. Ese supuesto no es automático — es una condición que debe cumplirse activamente. Si una organización automatiza el 30% de las tareas pero no rediseña los roles ni asigna nuevo trabajo de mayor valor, el resultado es capacidad ociosa o reducción de headcount.
*Relacionado con:* automatizar-mi-propio-trabajo, feedback-que-escala, equipos-pequenos-alto-impacto

---

**Equipos Pequeños de Alto Impacto** (`equipos-pequenos-alto-impacto`)
Unidad de 2-10 personas que, potenciada por IA, alcanza resultados antes reservados para equipos de 50-100. Tres habilitadores: perfiles híbridos, herramientas IA (vibe coding + agentes + usuarios sintéticos), velocidad de iteración. Nueva ecuación: antes 10 roles → 1 feature → 4 semanas. Ahora 1 rol → 10 features → 4 días. Cursor alcanzó $29B de valuación sin PMs full-time.
*Relacionado con:* disenador-a-constructor, vibe-coding, agentes-ia

---

**IA sin ecosistema** (`ia-sin-ecosistema`) ⬆ nuevo 2026-04-24
La IA generativa no falla porque los modelos son insuficientes. Falla porque las organizaciones tratan la tecnología como si el valor viviera en ella, cuando vive en lo que la rodea. Rahul Kapoor (Wharton): toda tecnología de propósito general requiere **activos complementarios** — infraestructura de datos propia, workflows rediseñados, talento específico, gobernanza real. Sin esos complementos, el modelo más capaz es económicamente estéril. McKinsey (2026): 80% de empresas invierten en IA generativa; la mayoría sin ROI visible para sus directorios. Nokia y Kodak como casos históricos del patrón: liderazgo tecnológico sin liderazgo comercial por no construir el ecosistema.
*Fuente:* Rahul Kapoor, Wharton; McKinsey, 2026.
*Relacionado con:* gobernanza-ia-performativa, condicion-redespliegue, capital-de-contexto

---

**El juicio como trabajo completo** (`juicio-como-trabajo-completo`) ⬆ nuevo 2026-04-24
Cuando los agentes hacen todo el trabajo preparatorio — construyen timelines, analizan casos, redactan resúmenes, generan opciones — el humano se mueve "above the loop": su único trabajo es revisar y decidir. El problema: el juicio no se aprende leyendo sobre él — se construye ejerciéndolo en tareas de menor riesgo, cometiendo errores recuperables, desarrollando intuición a través de la fricción. Esas tareas son exactamente las que los agentes ahora hacen primero. Krivkovich (McKinsey): "cut early-career roles now, and in five years you'll be poaching senior talent at a massive premium." Las organizaciones que más se benefician de los agentes hoy son las que más comprometen su capacidad de juicio mañana.
*Fuente:* McKinsey + American Arbitration Association, 2026.
*Relacionado con:* ia-como-filtro-de-entrada, condicion-redespliegue, automatizar-mi-propio-trabajo

---

### Categoría: `economia` — Mercado laboral, impacto económico (3)

---

**IA como filtro de entrada al mercado laboral** (`ia-como-filtro-de-entrada`)
La IA generativa no destruye empleo uniformemente: lo filtra por nivel de experiencia. Automatiza exactamente las tareas que servían como rampa de aprendizaje. El trabajo de entrada era entrenamiento disfrazado de producción. **Datos:** –16% en empleo relativo para trabajadores 22-25 años en ocupaciones de alta exposición (Stanford, 2025); –35% en postings entry-level en EE.UU. enero 2023 - junio 2025 (Revelio Labs).
*Relacionado con:* disenador-a-constructor, momento-liminal, fundamentales-vs-flux

---

**La inversión del sesgo tecnológico** (`inversion-sesgo-tecnologico`)
Las olas anteriores de automatización afectaban desproporcionadamente a los trabajadores de menor educación. La IA generativa invierte ese patrón. Los trabajadores con doctorado o maestría pasaron de 28% a 57% de automatización potencial (+29pp), mientras que quienes no terminaron la secundaria pasaron de 54% a 63% (+9pp). Lo que se automatiza no son tareas físicas — es la aplicación de expertise: redactar, analizar, sintetizar, argumentar. (McKinsey, 2023)
*Relacionado con:* ia-como-filtro-de-entrada, automatizacion-vs-ampliacion, fundamentales-vs-flux

---

**Señal anticipada en el mercado laboral** (`senal-anticipada-mercado-laboral`)
Ciertos grupos absorben el impacto de una disrupción antes de que sea visible en el mercado general — actúan como indicadores adelantados. Los trabajadores jóvenes en ocupaciones de alta exposición a IA cumplen ese rol hoy. El problema es que sistemáticamente se interpretan mal: se atribuyen a factores locales en lugar de reconocerse como evidencia de cambio estructural.
*Relacionado con:* ia-como-filtro-de-entrada, momento-liminal, gobernanza-ia-performativa

---

### Categoría: `filosofia` — Pensamiento abstracto, epistemología, marcos (4)

---

**Arquitectura de inteligencia** (`arquitectura-de-inteligencia`)
El trabajo del diseñador no es producir artefactos: es ayudar a personas y organizaciones a actuar inteligentemente. Con IA, la tentación es delegar la estructuración del conocimiento al modelo. La arquitectura de inteligencia es el trabajo que el humano debe hacer antes y después del AI, no durante. El Segundo Cerebro es una implementación personal: define qué información entra, cómo se estructura, cómo se relaciona, y cómo se activa.
*Fuente:* Jorge Arango, Finding Our Way ep. 69.
*Relacionado con:* agentes-ia, claridad-antes-de-velocidad, quien-controla-el-prompt

---

**Colonialismo cultural digital** (`colonialismo-cultural-digital`)
Los sistemas digitales operan con filtros de legibilidad que determinan qué formas de expresión y conocimiento son reconocibles para el sistema — y cuáles no existen. Lo que no es legible algorítmicamente no se suprime; simplemente no aparece. Los sistemas de IA entrenados en datos que sobrerepresentan idiomas y normas occidentales reproducen esa asimetría. El mecanismo no necesita intención colonial para producir efectos coloniales.
*Relacionado con:* quien-controla-el-prompt, agentes-ia, disenador-a-constructor

---

**Lo ilegible como señal** (`lo-ilegible-como-senal`)
Evan Tana (South Park Commons): una idea es **legible** cuando es fácil de entender y evaluar; es **ilegible** cuando está en la frontera y su valor todavía no puede expresarse con claridad. Las mejores inversiones tempranas (OpenAI, Stripe, Notion) eran ilegibles en su momento. La distinción sutil: lo ilegible con potencial genera **energía** en quienes lo tocan. Lo ilegible vacío simplemente confunde.
*Relacionado con:* arquitectura-de-inteligencia, momento-liminal, fundamentales-vs-flux

---

**El momento liminal** (`momento-liminal`)
El espacio entre lo que ya no funciona y lo que todavía no ha tomado forma. Del latín *limen* (dintel de puerta): ya saliste de un cuarto pero no entraste al siguiente. Las reglas del cuarto anterior no aplican; las del siguiente no existen. La llegada de la IA generativa al diseño y producto es un momento liminal de primer orden. Navegarlo bien no requiere certeza — requiere incomodidad productiva.
*Relacionado con:* disenador-a-constructor, claridad-antes-de-velocidad, fundamentales-vs-flux

---

## Las 14 correlaciones documentadas

| Correlación | Insight central |
|-------------|-----------------|
| `ia-como-filtro-de-entrada` ↔ `agentes-ia` | Los agentes que reemplazan trabajo de entrada son el mecanismo técnico del filtro |
| `automatizacion-vs-ampliacion` ↔ `fundamentales-vs-flux` | El modo de impacto correlaciona con el tipo de habilidad (flux vs. fundamental) |
| `senal-anticipada-mercado-laboral` ↔ `gobernanza-ia-performativa` | Ambos muestran el mismo patrón: las capas visibles de respuesta existen, las funcionales no |
| `ia-como-filtro-de-entrada` ↔ `disenador-a-constructor` | El filtro hace urgente la transición: quien no evoluciona a constructor cae en la zona de automatización |
| `claridad-antes-de-velocidad` ↔ `momento-liminal` | En la liminalidad, la claridad no precede al movimiento — se construye mientras se avanza |
| `fundamentales-vs-flux` ↔ `disenador-a-constructor` | La transición requiere distinguir qué habilidades son fundamentales transferibles y cuáles son flux |
| `automatizar-mi-propio-trabajo` ↔ `expertise-de-dominio-en-producto` | Automatizar el propio trabajo requiere saber qué partes son de bajo criterio y cuáles requieren expertise irreemplazable |
| `vibe-coding` ↔ `spec-driven-development` | Vibe coding para explorar el espacio del problema; SDD para ejecutar con precisión lo que esa exploración reveló |
| `pit-stop-cognitivo` ↔ `confianza-a-traves-de-velocidad` | La pausa que sostiene la velocidad: la velocidad visible para usuarios la habilita la pausa invisible del equipo |
| `copiloto-de-producto` ↔ `quien-controla-el-prompt` | El mapa y el volante: dos capas de control (táctica y estratégica) que pueden desalinearse |
| `pit-stop-cognitivo` ↔ `feedback-que-escala` | Lo que el sistema no puede enseñarse a sí mismo: feedback-que-escala codifica errores conocidos; pit-stop detecta lo que el sistema no sabe que tiene |
| `espectro-autonomia-agente` ↔ `fabrica-oscura-de-software` | El operador que no está: la fábrica oscura es operar como operador sin estar presente, no como observador |
| `espectro-autonomia-agente` ↔ `capital-de-contexto` | El precio de entrada para cada posición: el capital de contexto determina qué posición de autonomía es seguro ocupar |
| `fabrica-oscura-de-software` ↔ `capital-de-contexto` | El único activo que queda: la fábrica oscura como stress test del capital de contexto |

**Correlaciones implícitas pendientes de documentar:**
- `sycophancy-como-riesgo-de-diseno` ↔ `espiral-delusional` — causa (arquitectura RLHF) y efecto (espiral cognitiva) del mismo mecanismo
- `juicio-como-trabajo-completo` ↔ `ia-como-filtro-de-entrada` — el filtro en entrada y la pérdida del pipeline de formación son la misma dinámica en dos horizontes temporales
- `ia-sin-ecosistema` ↔ `condicion-redespliegue` — ecosistema fallido y redespliegue fallido como dos patrones del mismo error organizacional
- `metacognicion-del-disenador` ↔ `pit-stop-cognitivo` — metacognición individual y pausa de equipo como la misma operación en dos niveles
- `el-moat-del-gusto` ↔ `fundamentales-vs-flux` — el gusto como fundamental no-reemplazable; la agencia como distinción del humano cuando todos los flux son iguales
- `arnes-del-agente` ↔ `espectro-autonomia-agente` — el arnés codifica la posición del agente en el espectro
- `web-bifurcada` ↔ `legibilidad-de-maquina` — la bifurcación de la web es la consecuencia agregada del gap de legibilidad
- `comprehension-debt` ↔ `fabrica-oscura-de-software` — la fábrica oscura como condición que hace inevitable la deuda de comprensión
- `ux-checkpoints` ↔ `pit-stop-cognitivo` — checkpoints externos (UX) y pausas internas (equipo) son la misma operación en dos niveles
- `agencia-humana-como-imperativo-ux` ↔ `comprehension-debt` — sistemas que bypasean al usuario producen dependencia sin comprensión
- `metricas-post-pantalla` ↔ `feedback-que-escala` — instrumentar lo que importa hoy, no lo que importaba ayer
- `las-tres-caras-del-producto-agentico` ↔ `arnes-del-agente` ↔ `legibilidad-de-maquina` — clúster operativo del producto agéntico

---

## Mapa de nodos centrales

Los conceptos más conectados del vault (hubs):

- **`disenador-a-constructor`** — nodo central. Aparece como destino en casi todas las correlaciones. Es el concepto marco del sistema.
- **`agentes-ia`** — segundo hub. Es la infraestructura técnica que habilita la mayoría de los otros conceptos.
- **`espectro-autonomia-agente`** — hub del clúster agéntico. Conecta arnés, capital de contexto, fábrica oscura, agencia humana, las tres caras y arquitectura de confianza.
- **`arnes-del-agente`** — hub operativo emergente. Es el artefacto donde aterrizan las decisiones de diseño en sistemas agénticos.
- **`capital-de-contexto`** — hub estratégico. Conecta espectro de autonomía, fábrica oscura, pit stop cognitivo, comprehension debt y arquitectura de inteligencia.
- **`arquitectura-de-inteligencia`** — marco epistemológico que conecta el trabajo de diseño con el conocimiento estructurado.
- **`momento-liminal`** — concepto de orientación. Muchos conceptos apuntan a él como contexto.
- **`gobernanza-ia-performativa`** — hub de riesgo. Es el destino de `sycophancy`, `espiral-delusional`, `espectro-autonomia-agente`, `ia-sin-ecosistema`, `senal-anticipada`.

---

## Familias de conceptos (clusters)

El ATLAS agrupa los 51 conceptos en 6 familias:

- **`agencia-ia`** (13 conceptos) — el clúster más grande. Une el diseño UX agéntico (agencia humana, arquitectura de confianza, ux-checkpoints, **sycophancy como riesgo de diseño**), la ingeniería del agente (arnés, espectro de autonomía, fábrica oscura, **espiral delusional**), y la nueva forma de los productos (las tres caras, web bifurcada, legibilidad de máquina, métricas post-pantalla).
- **`transicion-ia`** (17 conceptos) — el clúster más numeroso. El cambio estructural en roles, productos, mercado laboral y modelos de trabajo. Incluye los 6 nuevos: **ia-sin-ecosistema**, **juicio-como-trabajo-completo**, **el-moat-del-gusto**, de-usuario-a-cliente-servido, gobernanza-ia-performativa, impuesto-de-verificacion y los de economía.
- **`velocidad-output`** (9 conceptos) — vibe coding, SDD, MVP/prototipo, confianza a través de velocidad, pit stop cognitivo, restricción de tiempo, comprehension debt, quien-controla-el-prompt, feedback-que-escala.
- **`epistemologia-practica`** (6 conceptos) — arquitectura de inteligencia, capital de contexto, claridad antes de velocidad, lo ilegible como señal, colonialismo cultural digital, **metacognición del diseñador**.
- **`equipos-impacto`** (4 conceptos) — usuarios sintéticos, equipos pequeños de alto impacto, copiloto de producto, PMF perecedero.
- **`sistemas-conocimiento`** (2 conceptos) — conocimiento autoorganizado por LLM, expertise de dominio en producto.

---

## Fuentes clave del vault

| Fuente | Conceptos que generó |
|--------|---------------------|
| Finding Our Way, ep. 69 (Peter Merholz + Jorge Arango) | claridad-antes-de-velocidad, arquitectura-de-inteligencia |
| Finding Our Way, ep. 58 (Jesse James Garrett + Peter Merholz) | quien-controla-el-prompt |
| Finding Our Way, LIMINAL-1 y LIMINAL-2 | momento-liminal |
| Finding Our Way, ep. 68 (Dan Saffer) | fundamentales-vs-flux |
| Lenny's Podcast — Geoff Charles (CPO de Ramp) | automatizar-mi-propio-trabajo, expertise-de-dominio-en-producto, feedback-que-escala |
| Lenny's Podcast — Jenny Wen (Anthropic) | confianza-a-traves-de-velocidad, diseno-dos-velocidades, lo-ilegible-como-senal |
| Stanford Digital Economy Lab, 2025 (Brynjolfsson et al.) | ia-como-filtro-de-entrada, senal-anticipada-mercado-laboral, automatizacion-vs-ampliacion |
| McKinsey "Economic potential of generative AI", 2023 | condicion-redespliegue, inversion-sesgo-tecnologico |
| McKinsey 2026 (Krivkovich) + American Arbitration Association | juicio-como-trabajo-completo, ia-sin-ecosistema |
| Rahul Kapoor, Wharton School | ia-sin-ecosistema |
| YC Winter 2025 data + Menlo Ventures | equipos-pequenos-alto-impacto, vibe-coding |
| Salesforce Agentforce + Connectivity Report | agentes-ia, web-bifurcada |
| HBR Feb 2026 | capital-de-contexto |
| BCG/HBR Mar 2026 (n=1,488); Workday Research 2026; Microsoft Research CHI 2025 (n=319) | impuesto-de-verificacion |
| arXiv 2602.19141 (MIT CSAIL, Kartik Chandra et al., 2026); Fanous et al., 2025 | espiral-delusional, sycophancy-como-riesgo-de-diseno |
| arXiv 2506.12469, U. Washington 2026 | espectro-autonomia-agente |
| StrongDM case study, 2026 | fabrica-oscura-de-software |
| Karpathy llm-wiki, abril 2026 | conocimiento-autoorganizado-por-llm |
| arXiv 2604.13277 (Glasgow); Anthropic RCT; Addy Osmani | pit-stop-cognitivo, comprehension-debt |
| Elena Verna / Lovable case 2026 | pmf-perecedero |
| Scout interno 2026-04-18 | restriccion-de-tiempo-como-ventaja, copiloto-de-producto |
| **Martín Alaimo, "La era de los productos agénticos" (2026)** | arnes-del-agente, web-bifurcada, legibilidad-de-maquina, las-tres-caras-del-producto-agentico |
| **Gianluca Brugnoli, "The checkpoints of the AI User Experience"** | agencia-humana-como-imperativo-ux, arquitectura-de-confianza, de-usuario-a-cliente-servido, ux-checkpoints |
| Cloudflare blog "Markdown for Agents" (feb 2026); Ben Word | web-bifurcada |
| Galileo AI, AWS evaluación de agentes, Plausible Analytics | metricas-post-pantalla |
| Felix Lee, AI-First Designer Newsletter; Julie Zhuo, 2026 | el-moat-del-gusto |
| Ulises Arvizu, Iterative Thinking, 2026 | metacognicion-del-disenador |
| Experiencia propia / Wayta IA | disenador-a-constructor, mvp-a-prototipo-en-produccion, usuarios-sinteticos, spec-driven-development |

---

## Cómo usar este contexto

Cuando Luigui comparte este archivo en un chat de Claude.ai:

1. **Para generar presentaciones**: los conceptos son los bloques. Pregunta qué narrativa quiere construir y qué audiencia tiene. La "escalera" validada para charlas: Usuarios Sintéticos → Vibe Coding → Agentes IA. Para charlas sobre **producto agéntico**: las tres caras → arnés → ux-checkpoints → métricas post-pantalla.

2. **Para profundizar un concepto**: identifica sus ejes de tensión, busca los conceptos relacionados, y usa las correlaciones existentes como puntos de partida.

3. **Para nuevas correlaciones**: busca tensiones no resueltas entre conceptos de distintas categorías. Las mejores correlaciones no son co-ocurrencias — son tensiones productivas. Ver "Correlaciones implícitas pendientes" — hay más de 12 sin documentar formalmente.

4. **Para propuestas**: los conceptos más persuasivos para audiencias de liderazgo son: claridad-antes-de-velocidad, feedback-que-escala, quien-controla-el-prompt, expertise-de-dominio-en-producto, capital-de-contexto, comprehension-debt, impuesto-de-verificacion.

5. **Para explorar el impacto de la IA en el trabajo**: el clúster ia-como-filtro-de-entrada + inversion-sesgo-tecnologico + senal-anticipada-mercado-laboral + condicion-redespliegue + juicio-como-trabajo-completo es el más basado en evidencia empírica del vault.

6. **Para explorar agentes y autonomía** (clúster operativo más nuevo): espectro-autonomia-agente + arnes-del-agente + fabrica-oscura-de-software + capital-de-contexto + las-tres-caras-del-producto-agentico.

7. **Para explorar UX agéntico y confianza**: agencia-humana-como-imperativo-ux + arquitectura-de-confianza + ux-checkpoints + de-usuario-a-cliente-servido (todos derivados del artículo de Brugnoli).

8. **Para explorar el cambio en producto**: web-bifurcada + legibilidad-de-maquina + las-tres-caras-del-producto-agentico + metricas-post-pantalla. La pregunta clave: ¿el producto existe y es operable en la capa de agentes?

9. **Para explorar deuda y velocidad sostenible**: comprehension-debt + pit-stop-cognitivo + capital-de-contexto + impuesto-de-verificacion. Datos duros: 17% menos comprensión con IA continua (Anthropic RCT); 40% de ganancias de IA se pierden verificando outputs (Workday).

10. **Para explorar riesgo de IA y seguridad de diseño**: sycophancy-como-riesgo-de-diseno + espiral-delusional + arquitectura-de-confianza + gobernanza-ia-performativa. El clúster más nuevo. Útil para charlas sobre responsabilidad en productos que usan LLMs.

11. **Para explorar el futuro del trabajo y formación de criterio**: juicio-como-trabajo-completo + ia-como-filtro-de-entrada + ia-sin-ecosistema + condicion-redespliegue. La pregunta: ¿qué se pierde cuando los agentes hacen el trabajo de entrada?

---

*Este archivo es un snapshot del vault al 2026-05-11. Para el estado más actualizado, consultar directamente `Conocimiento/ATLAS.md` en el vault.*
