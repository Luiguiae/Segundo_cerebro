# Contexto del Segundo Cerebro — Luigui Avila

> Archivo generado el 2026-04-16. Úsalo como contexto en conversaciones de Claude.ai para que el asistente conozca el estado completo del vault.

---

## Quién es Luigui

Diseñador-constructor. Construye el Segundo Cerebro como infraestructura de conocimiento personal para generar presentaciones, propuestas y charlas. Su trabajo orbita en la intersección de diseño, producto e IA. El proyecto central visible es **Wayta IA** — equipo pequeño construyendo con el modelo de diseñador-constructor como principio fundacional.

---

## Qué es el Segundo Cerebro

Un sistema de conocimiento atómico en Obsidian. La lógica: los conceptos se capturan como unidades independientes con frontmatter YAML estricto, se correlacionan explícitamente entre sí, y se activan como insumo para entregables concretos (charlas, propuestas, decks). El sistema no es el vault — es la lógica de estructuración que vive detrás.

**Jarvis** es el agente de mantenimiento del vault (Claude Code). Ejecuta comandos sin preguntar, registra en `JARVIS_LOG.md`, y regenera el ATLAS después de cada cambio.

---

## Estado actual del vault

- **24 conceptos activos** (todos en estado `activo`)
- **8 correlaciones documentadas**
- **1 sesión registrada** (2026-04-10)
- Última acción registrada: auditoría completa del vault + 3 conceptos nuevos + 4 correlaciones (2026-04-15)

---

## Los 24 conceptos activos

### Familia: `transicion-ia` — El cambio de rol en la era IA

---

**Del Diseñador al Constructor** (`disenador-a-constructor`)
La evolución del rol del diseñador desde entregar especificaciones hacia construir directamente el producto. Las herramientas de IA eliminaron la fricción técnica que separaba la idea de su materialización. Antes: handoff = pérdida de intención. Ahora: diseñar y construir son el mismo gesto. Los primeros constructores (Bill Atkinson, Alan Kay) no separaban diseño y código — la especialización posterior prometió velocidad pero en práctica coordinó más y construyó menos.
*Relacionado con:* vibe-coding, agentes-ia, usuarios-sinteticos, equipos-pequenos-alto-impacto

---

**El momento liminal** (`momento-liminal`)
El espacio entre lo que ya no funciona y lo que todavía no ha tomado forma. Del latín *limen* (dintel de puerta): ya saliste de un cuarto pero no entraste al siguiente. Las reglas del cuarto anterior no aplican; las del siguiente no existen. La llegada de la IA generativa al diseño y producto es un momento liminal de primer orden. Navegarlo bien no requiere certeza — requiere incomodidad productiva: sentir que el terreno se mueve y seguir avanzando.
*Relacionado con:* disenador-a-constructor, claridad-antes-de-velocidad

---

**Fundamentales vs. flux** (`fundamentales-vs-flux`)
Marco de Dan Saffer (Carnegie Mellon) para navegar la educación en diseño en la era IA. Los **fundamentales** son principios que permanecen porque los humanos no cambian: tipografía, percepción visual, cómo se encuadra un problema, criterio de calidad. El **flux** son procesos, métodos y herramientas: wireframes, handoffs, Figma, los roles mismos. El error común: confundir herramientas dominadas con fundamentales. Prompting, evaluación de outputs de IA y criterio son potencialmente fundamentales nuevos; aprender una herramienta específica de IA es flux.
*Relacionado con:* momento-liminal, disenador-a-constructor, vibe-coding

---

**El diseño en dos velocidades** (`diseno-dos-velocidades`)
Jenny Wen (head of design, Anthropic): el trabajo de diseño en la era IA se estratifica en dos modos que coexisten. **Modo ejecución**: acompañar mientras se construye, dar feedback en tiempo real, implementar polish directamente en código — no ser el cuello de botella. **Modo visión**: apuntar al equipo hacia algo, horizonte de 3-6 meses, a veces es un prototipo no un deck. El modo ejecución gana por defecto. Proteger el modo visión requiere resistencia activa a esa urgencia. Quien se queda solo en ejecución pierde influencia sobre la dirección del producto.
*Relacionado con:* disenador-a-constructor, mvp-a-prototipo-en-produccion, quien-controla-el-prompt

---

**Diseño UX/UI y IA** (`diseno-uxui-y-ia`)
La IA no agrega herramientas al proceso UX/UI — reconfigura el proceso. Cuando generar 20 variaciones toma segundos, el trabajo colapsa de producción a juicio. La IA produce outputs abundantes pero sin criterio propio; sin diseñador que evalúe, solo genera velocidad sin dirección. El cuello de botella cambió: antes era producción, ahora es criterio de evaluación. Riesgo: los modelos reproducen patrones estéticos dominantes, profundizando colonialismo cultural si no hay criterio propio.
*Relacionado con:* disenador-a-constructor, usuarios-sinteticos

---

**Mi trabajo es automatizar mi trabajo** (`automatizar-mi-propio-trabajo`)
Geoff Charles (CPO de Ramp): la responsabilidad de automatizar el propio trabajo es individual, no corporativa. Cada persona identifica las partes repetibles y de bajo criterio en su trabajo — y las automatiza. Esto invierte la lógica de gestión del cambio: la transformación es ascendente y distribuida, no top-down. La distinción crítica: automatizar no significa eliminar — significa subir el piso. Las tareas que consumían atención pasan al sistema; la persona se mueve hacia trabajo de juicio. Si no subes ese piso activamente, alguien más lo hace por ti.
*Relacionado con:* disenador-a-constructor, agentes-ia, fundamentales-vs-flux

---

**Gobernanza de IA performativa** (`gobernanza-ia-performativa`)
Cuando una organización construye las capas visibles de gobernanza de IA (política de uso, comité de ética, declaración de principios) pero no construye las capas que realmente hacen cumplir esas reglas. El shadow AI es el síntoma: 57-80% de empleados usa IA sin reportarlo. El 56% de organizaciones dice tener gobernanza comprensiva; solo el 12% la tiene implementada. El 97% de brechas de seguridad relacionadas con IA ocurren en organizaciones sin controles de acceso reales — no sin políticas, sin controles. Cuatro capas: gobernanza → modelo operativo → proceso → sistema. Las organizaciones invierten bien en 1 y 2; subinvierten en 3 y 4.
*Relacionado con:* agentes-ia, quien-controla-el-prompt, arquitectura-de-inteligencia

---

**IA como filtro de entrada al mercado laboral** (`ia-como-filtro-de-entrada`)
La IA generativa no destruye empleo uniformemente: lo filtra por nivel de experiencia. Automatiza exactamente las tareas que servían como rampa de aprendizaje — las que entrenaban a los junior antes de convertirlos en seniors. El trabajo de entrada era entrenamiento disfrazado de producción. Si el nivel de entrada desaparece, la próxima generación de seniors nunca se forma. **Datos:** –16% en empleo relativo para trabajadores 22-25 años en ocupaciones de alta exposición a IA (Stanford, 2025); –35% en postings entry-level en EE.UU. enero 2023 - junio 2025 (Revelio Labs); –25% en contratación entry-level en las 15 empresas tech más grandes 2023-2024.
*Relacionado con:* disenador-a-constructor, momento-liminal, fundamentales-vs-flux

---

**Automatización vs. amplificación** (`automatizacion-vs-ampliacion`)
La IA tiene dos modos de impacto estructuralmente distintos: **automatización** (la tarea pasa de humano a máquina, el humano sale del proceso) y **amplificación** (la IA multiplica la capacidad del humano que ya hace esa tarea). El modo no es fijo: la misma herramienta puede automatizar el trabajo de un junior y amplificar el de un senior en la misma ocupación. El seniority actúa como variable que cambia el modo de impacto. La automatización supera actualmente a la amplificación en impacto neto en empleo.
*Relacionado con:* ia-como-filtro-de-entrada, fundamentales-vs-flux, agentes-ia

---

**Señal anticipada en el mercado laboral** (`senal-anticipada-mercado-laboral`)
Ciertos grupos absorben el impacto de una disrupción antes de que sea visible en el mercado general — actúan como indicadores adelantados. Los trabajadores jóvenes en ocupaciones de alta exposición a IA cumplen ese rol hoy. La metáfora: el canario en la mina de carbón. El problema es que sistemáticamente se interpretan mal: se atribuyen a factores locales (contracción tech, jóvenes sin habilidades) en lugar de reconocerlas como evidencia de cambio estructural. Identificar una señal anticipada requiere: grupo sistemáticamente distinto del promedio, efecto específico a la variable estudiada, dirección consistente en múltiples fuentes.
*Relacionado con:* ia-como-filtro-de-entrada, momento-liminal, gobernanza-ia-performativa

---

### Familia: `velocidad-output` — Cómo construir más rápido y mejor

---

**Vibe Coding** (`vibe-coding`)
Modo de construir software donde el punto de partida es la intención, no la estructura técnica. El desarrollador describe en lenguaje natural; la IA genera el código. El 25% de las startups YC Winter 2025 tienen el 95% de su código generado por IA. Tres capas de madurez: Layer 1 (exploración, Bolt/Lovable), Layer 2 (MVP, Lovable/v0), Layer 3 (engineering, Cursor/Claude Code). El error más común: quedarse en Layer 1 y llamarlo producto. Dos estilos de trabajo: *slop → oro* (primera versión sloppy + refinamiento manual) o *planear primero* (mocks + intención → agente ejecuta). El criterio y refinamiento siguen siendo humanos. Stack para diseñadores: Figma → Figma Make → Lovable → Cursor.
*Relacionado con:* disenador-a-constructor, agentes-ia, mvp-a-prototipo-en-produccion, equipos-pequenos-alto-impacto

---

**Spec-Driven Development** (`spec-driven-development`)
Todo lo que un agente de IA va a construir debe estar precedido por un documento de especificación que define el criterio de done antes de que el agente empiece. Los agentes son excelentes ejecutores pero pésimos definidores de objetivos. Sin spec, el agente infiere el criterio de "terminado" — y puede inferirlo diferente en cada prompt. Un spec mínimo define cuatro cosas: el problema (qué situación del usuario se resuelve), el criterio de done (comportamiento observable), las restricciones (qué no puede hacer la solución), y el contexto de uso (quién lo usa, cuándo). Tensión con vibe coding: vibe coding para explorar, SDD para ejecutar lo que ya se sabe que hay que construir.
*Relacionado con:* vibe-coding, agentes-ia, mvp-a-prototipo-en-produccion

---

**Del MVP al Prototipo en Producción** (`mvp-a-prototipo-en-produccion`)
El MVP clásico no muere, pero cambia. Con vibe coding y agentes, el cuello de botella dejó de ser la construcción. Lo que tiene sentido hoy es un prototipo en producción: algo funcional en manos de usuarios reales en días, no semanas. El riesgo se desplazó: antes era construir algo que nadie quería (construir era caro). Hoy es quedarte analizando mientras alguien más ya itera en producción. La variable crítica cambió: ya no es el tiempo de construcción — es qué aprendes y con qué velocidad actúas sobre ese aprendizaje. La deuda técnica es temporal por diseño: con agentes puedes refactorizar partes enteras tan rápido que la perfección inicial no tiene sentido.
*Relacionado con:* vibe-coding, agentes-ia, disenador-a-constructor, equipos-pequenos-alto-impacto

---

**Claridad antes de velocidad** (`claridad-antes-de-velocidad`)
Los equipos que adoptan IA están yendo más rápido pero no están haciendo mejor trabajo. La razón: no había un estándar de calidad definido antes de que llegara la IA, y la IA amplifica el caos existente. Velocidad sin claridad no produce ventaja competitiva — produce más ruido más rápido. El error más común: tomar los flujos de trabajo actuales y automatizarlos sin preguntar qué resultado se desea. La IA no mejora procesos confusos — los escala. Aplica cuando hay un problema definido y se está eligiendo cómo abordarlo. No aplica en fases de exploración pura donde el objetivo es descubrir.
*Fuente:* Peter Merholz, Finding Our Way ep. 69 con Jorge Arango.
*Relacionado con:* vibe-coding, mvp-a-prototipo-en-produccion, disenador-a-constructor

---

**Confianza a través de velocidad** (`confianza-a-traves-de-velocidad`)
Jenny Wen (Anthropic): lanzar imperfecto y mejorar rápido públicamente construye más confianza que esperar a tener algo perfecto. El mecanismo es relacional: lanzar temprano es una promesa implícita de "estamos aquí, escuchamos, vamos a mejorar". Lo que destruye la confianza no es la imperfección inicial — es el silencio después. Condición: debe haber algo genuinamente valioso ya, aunque imperfecto. Frase de Anthropic: "esto es lo peor que este producto va a ser jamás." Tensión productiva con *claridad-antes-de-velocidad*: lanzas rápido porque tienes claridad suficiente sobre el valor central, y usas el feedback real para refinar lo que no está claro.
*Relacionado con:* mvp-a-prototipo-en-produccion, claridad-antes-de-velocidad, diseno-dos-velocidades

---

**El feedback que escala** (`feedback-que-escala`)
Hay dos tipos de feedback. Solo uno escala. **Feedback puntual**: corriges una instancia, el error vuelve a ocurrir. **Feedback sistémico**: identificas en qué parte del proceso ocurrió la falla — qué prompt no lo capturó, qué skill no lo tenía codificado, qué componente del design system no lo aplicaba — y arreglas ahí. El error no vuelve a ocurrir porque el sistema lo previene. El cambio de rol del líder: su trabajo ya no es principalmente dar feedback correcto — es diagnosticar qué parte del sistema produjo el feedback incorrecto, y arreglarlo ahí. Regla: si estás dando el mismo feedback más de dos veces, el problema no es la persona — es que ese criterio todavía no está en el sistema.
*Fuente:* Geoff Charles, CPO de Ramp, Lenny's Podcast.
*Relacionado con:* arquitectura-de-inteligencia, quien-controla-el-prompt, automatizar-mi-propio-trabajo

---

**Quien controla el prompt controla el producto** (`quien-controla-el-prompt`)
En el flujo tradicional, quien controlaba las especificaciones controlaba el producto. Ahora hay una capa nueva entre intención y entrega: el prompt. Esa capa no tiene dueño natural — la disputan diseño, producto y engineering simultáneamente. El prompt no es solo instrucción técnica: es la destilación de cómo entiendes el problema del usuario, el contexto del negocio, y el criterio de calidad. Dos errores opuestos: **abandono** (diseño delega los prompts como "trabajo técnico" y pierde influencia) y **territorialismo** (diseño declara ownership del prompt como entregable). La posición correcta: diseño aporta el criterio de calidad y comprensión del usuario al proceso de prompting, independientemente de quién teclee.
*Fuente:* Finding Our Way, ep. 58, Jesse James Garrett y Peter Merholz.
*Relacionado con:* agentes-ia, disenador-a-constructor, arquitectura-de-inteligencia

---

### Familia: `agencia-ia` — Los agentes como infraestructura

---

**Equipos de Agentes IA** (`agentes-ia`)
Un equipo de agentes IA es un conjunto de modelos especializados que trabajan coordinadamente bajo un orquestador central para ejecutar tareas complejas y multi-paso. Tres capas: orquestador → agentes especializados → human-in-the-loop. Para el diseñador-constructor, los equipos de agentes son el multiplicador que permite a una sola persona operar con la capacidad de un equipo de 10. Salesforce proyectó para 2026 un modelo de fuerza laboral orquestada; Agentforce alcanzó $1.4B ARR con 114% crecimiento YoY. Dos estrategias cuando el agente "se pierde": aceptar primera pasada sloppy y refinar encima, o planear más antes (dividir tarea, explicitar pasos y criterio de éxito).
*Relacionado con:* disenador-a-constructor, vibe-coding, usuarios-sinteticos, equipos-pequenos-alto-impacto

---

### Familia: `equipos-impacto` — Cómo operan los equipos modernos

---

**Equipos Pequeños de Alto Impacto** (`equipos-pequenos-alto-impacto`)
Unidad de 2-10 personas que, potenciada por IA, alcanza resultados antes reservados para equipos de 50-100. No es un equipo al que le faltan recursos — es uno que no los necesita. Tres habilitadores: perfiles híbridos (diseñadores que construyen, roles difusos), herramientas IA (vibe coding + agentes + usuarios sintéticos), velocidad de iteración (build → medir → aprender → rebuild en días). Nueva ecuación: antes 10 roles → 1 feature → 4 semanas. Ahora 1 rol → 10 features → 4 días. Cursor alcanzó $29B de valuación sin PMs full-time. El 38% de los top 100 launches en Product Hunt 2025 involucraron al menos un diseñador-fundador.
*Relacionado con:* disenador-a-constructor, vibe-coding, agentes-ia, mvp-a-prototipo-en-produccion

---

**Usuarios Sintéticos** (`usuarios-sinteticos`)
Representaciones simuladas de usuarios reales generadas por IA, capaces de interactuar con productos, responder preguntas de research y generar comportamientos predecibles basados en perfiles definidos. Comprimen el ciclo de validación de semanas a minutos. Se define un perfil (demografía, comportamientos, necesidades, frustraciones) y se simula su interacción con un producto o flujo. No reemplazan la validación con usuarios reales — la complementan en fases tempranas. La calidad del output depende directamente de la calidad del perfil: basura entra, basura sale. No capturan comportamientos emergentes ni contextos imprevistos.
*Relacionado con:* disenador-a-constructor, vibe-coding, mvp-a-prototipo-en-produccion, agentes-ia

---

### Familia: `epistemologia-practica` — Cómo estructurar el conocimiento

---

**Arquitectura de inteligencia** (`arquitectura-de-inteligencia`)
El trabajo del diseñador — y de cualquier profesional del conocimiento — no es producir artefactos: es ayudar a personas y organizaciones a actuar inteligentemente. Eso requiere dejar entrar la información correcta y estructurarla cuidadosamente. Con IA, la tentación es delegar la estructuración del conocimiento al modelo. El riesgo: si no hay una arquitectura intencional detrás, el AI devuelve estructura superficial. La arquitectura de inteligencia es el trabajo que el humano debe hacer antes y después del AI, no durante. El Segundo Cerebro es una implementación personal de este concepto: define qué información entra (taxonomía), cómo se estructura (conceptos atómicos), cómo se relaciona (ATLAS), y cómo se activa (presentaciones).
*Fuente:* Jorge Arango, Finding Our Way ep. 69.
*Relacionado con:* agentes-ia, claridad-antes-de-velocidad, quien-controla-el-prompt

---

**Lo ilegible como señal** (`lo-ilegible-como-senal`)
Hay ideas que generan energía antes de tener forma. Evan Tana (South Park Commons) propone un marco para VCs basado en legibilidad: una idea es **legible** cuando es fácil de entender y evaluar; es **ilegible** cuando está en la frontera y su valor todavía no puede expresarse con claridad. Las mejores inversiones tempranas (OpenAI, Stripe, Notion) eran ilegibles en su momento. Jenny Wen aplica esto al diseño en Anthropic: el rol del diseñador incluye detectar lo ilegible con anticipación para estar ahí cuando la forma emerge. La distinción sutil: lo ilegible con potencial genera **energía** en quienes lo tocan. Lo ilegible vacío simplemente confunde.
*Relacionado con:* momento-liminal, arquitectura-de-inteligencia, fundamentales-vs-flux

---

**Colonialismo cultural digital** (`colonialismo-cultural-digital`)
Los sistemas digitales operan con filtros de legibilidad que determinan qué formas de expresión, conocimiento y valor cultural son reconocibles para el sistema — y cuáles no existen. Lo que no es legible algorítmicamente no se suprime; simplemente no aparece. El mecanismo no necesita intención colonial para producir efectos coloniales. Distinción con marcos adyacentes: colonialismo digital (Kwet: quién posee la infraestructura), colonialismo de datos (Couldry & Mejias: la vida como recurso extractivo), capitalismo de vigilancia (Zuboff: modificación conductual). El colonialismo cultural digital es el más invisible y el más estructurante: define qué puede pensarse dentro de la infraestructura. Los sistemas de IA entrenados en datos que sobrerepresentan idiomas y normas occidentales reproducen esa asimetría.
*Relacionado con:* quien-controla-el-prompt, agentes-ia, disenador-a-constructor

---

### Familia: `sistemas-conocimiento` — Conocimiento como infraestructura

---

**Expertise de dominio como infraestructura de producto** (`expertise-de-dominio-en-producto`)
Hay una diferencia fundamental entre un producto que ayuda al usuario a hacer su trabajo y uno que hace el trabajo del usuario. El segundo requiere expertise real en el dominio del usuario. Geoff Charles (Ramp): si el producto va a codificar en nombre del contador — no a ayudarlo — necesita descargar la filosofía del CPA y hornearla en el producto. En la era de los agentes, esto es la distinción competitiva más importante en B2B: cualquiera puede construir la interfaz y conectar el modelo. Lo que diferencia un agente útil de uno peligroso es si el expertise del dominio está correctamente codificado. El indicador de Ramp: su objetivo es reducir el tiempo que los usuarios pasan en el producto, no aumentarlo. El éxito es la invisibilidad.
*Relacionado con:* arquitectura-de-inteligencia, agentes-ia, usuarios-sinteticos

---

## Las 8 correlaciones documentadas

| Correlación | Tipo de relación |
|-------------|-----------------|
| `ia-como-filtro-de-entrada` ↔ `agentes-ia` | Los agentes que reemplazan trabajo de entrada son el mecanismo técnico del filtro |
| `automatizacion-vs-ampliacion` ↔ `fundamentales-vs-flux` | El modo de impacto (automatizar vs. amplificar) correlaciona con el tipo de habilidad (flux vs. fundamental) |
| `senal-anticipada-mercado-laboral` ↔ `gobernanza-ia-performativa` | Ambos muestran el mismo patrón: las capas visibles de respuesta existen, las funcionales no |
| `ia-como-filtro-de-entrada` ↔ `disenador-a-constructor` | El filtro de entrada hace urgente la transición: quien no evoluciona a constructor, cae en la zona de automatización |
| `claridad-antes-de-velocidad` ↔ `momento-liminal` | En la liminalidad, la claridad no precede al movimiento — se construye mientras se avanza |
| `fundamentales-vs-flux` ↔ `disenador-a-constructor` | La transición requiere distinguir qué habilidades de diseño son fundamentales transferibles y cuáles son flux que no viajan |
| `automatizar-mi-propio-trabajo` ↔ `expertise-de-dominio-en-producto` | Automatizar el propio trabajo requiere primero saber qué partes son de bajo criterio (flux) y cuáles requieren expertise irreemplazable |
| `vibe-coding` ↔ `spec-driven-development` | Son herramientas para fases distintas del mismo proceso: vibe coding para explorar el espacio del problema, SDD para ejecutar con precisión lo que esa exploración reveló |

---

## Mapa de nodos centrales

Los conceptos más conectados del vault (hubs):

- **`disenador-a-constructor`** — nodo central. Aparece como destino en casi todas las correlaciones. Es el concepto marco del sistema.
- **`agentes-ia`** — segundo hub. Es la infraestructura técnica que habilita la mayoría de los otros conceptos.
- **`vibe-coding`** — habilitador técnico del diseñador-constructor.
- **`arquitectura-de-inteligencia`** — marco epistemológico que conecta el trabajo de diseño con el conocimiento estructurado.
- **`momento-liminal`** — concepto de orientación. Muchos conceptos apuntan a él como contexto.

---

## Las 7 familias conceptuales

| Familia | Descripción | Conceptos |
|---------|-------------|-----------|
| `transicion-ia` | El cambio de rol y de mercado en la era IA | disenador-a-constructor, momento-liminal, fundamentales-vs-flux, diseno-dos-velocidades, diseno-uxui-y-ia, automatizar-mi-propio-trabajo, gobernanza-ia-performativa, ia-como-filtro-de-entrada, automatizacion-vs-ampliacion, senal-anticipada-mercado-laboral |
| `velocidad-output` | Cómo construir más rápido y mejor | vibe-coding, spec-driven-development, mvp-a-prototipo-en-produccion, claridad-antes-de-velocidad, confianza-a-traves-de-velocidad, feedback-que-escala, quien-controla-el-prompt |
| `agencia-ia` | Los agentes como infraestructura | agentes-ia |
| `equipos-impacto` | Cómo operan los equipos modernos | equipos-pequenos-alto-impacto, usuarios-sinteticos |
| `epistemologia-practica` | Cómo estructurar y capturar conocimiento | arquitectura-de-inteligencia, claridad-antes-de-velocidad, lo-ilegible-como-senal, colonialismo-cultural-digital |
| `sistemas-conocimiento` | Conocimiento como infraestructura de producto | expertise-de-dominio-en-producto |

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
| YC Winter 2025 data + Menlo Ventures | equipos-pequenos-alto-impacto, vibe-coding |
| Salesforce Agentforce data | agentes-ia |
| Ryo Lu (Cursor), Felix Lee (ADPList) | vibe-coding |
| Experiencia propia / Wayta IA | disenador-a-constructor, mvp-a-prototipo-en-produccion, usuarios-sinteticos, spec-driven-development |

---

## Cómo usar este contexto

Cuando Luigui comparte este archivo en un chat de Claude.ai:

1. **Para generar presentaciones**: los conceptos son los bloques. Pregunta qué narrativa quiere construir y qué audiencia tiene. La "escalera" validada para charlas: Usuarios Sintéticos → Vibe Coding → Agentes IA.

2. **Para profundizar un concepto**: identifica sus ejes de tensión, busca los conceptos relacionados, y usa las correlaciones existentes como puntos de partida.

3. **Para nuevas correlaciones**: busca tensiones no resueltas entre conceptos de distintas familias. Las mejores correlaciones no son co-ocurrencias — son tensiones productivas.

4. **Para propuestas**: los conceptos más persuasivos para audiencias de liderazgo son: claridad-antes-de-velocidad, feedback-que-escala, quien-controla-el-prompt, expertise-de-dominio-en-producto.

5. **Para explorar el impacto de la IA**: el clúster ia-como-filtro-de-entrada + automatizacion-vs-ampliacion + senal-anticipada-mercado-laboral es el más basado en evidencia empírica del vault.

---

*Este archivo es un snapshot del vault al 2026-04-16. Para el estado más actualizado, consultar directamente `Conocimiento/ATLAS.md` en el vault.*
