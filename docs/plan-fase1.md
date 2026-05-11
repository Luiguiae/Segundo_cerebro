---
plan: fase1-grafo-conocimiento
fecha: 2026-05-11
mejora: mejora-006-evolucion-grafo-conocimiento
estado: borrador — pendiente revisión
---

# Plan Fase 1 — Grafo tipado de conocimiento

## Instrucciones de lectura

Este documento lista los 51 conceptos del vault organizados en dos secciones:

**Sección A — Con correlación documentada (21 conceptos, 14 archivos en `Correlaciones/`):**
Cada concepto tiene un draft del campo `edges:` listo para añadir al frontmatter.
El draft incluye el `tipo` de relación y un `why` de mínimo 30 palabras explicando el mecanismo.
La dirección del edge es **desde el concepto listado hacia el target**.

**Sección B — Sin correlación documentada (30 conceptos):**
Candidatos de edges derivados del campo `relacionado:` actual.
Solo se propone el `tipo` más plausible y una nota breve.
Requieren correlación documentada o revisión antes de escribirse como edges definitivos.

**Tipos de relación disponibles:**
`analogous_to` · `same_mechanism_as` · `contradicts` · `refines` · `requires` · `enables` · `exemplifies` · `extends` · `precedes`

**Formato final de edges en frontmatter:**
```yaml
edges:
  - target: slug
    tipo: relationship_type
    why: "Mínimo 30 palabras explicando el mecanismo específico de la relación"
```

---

## Sección A — Conceptos con correlación documentada

### 1. `ia/vibe-coding`
**Correlación documentada:** `2026-04-03_vibe-coding--spec-driven-development.md`

```yaml
edges:
  - target: spec-driven-development
    tipo: contradicts
    why: "Ambos abordan cómo se produce software con IA, pero desde criterios opuestos: vibe-coding acepta la ambigüedad del done como parte constitutiva del flujo; spec-driven lo fija antes de ejecutar. La tensión no es estilística sino estructural: quién define el estándar de calidad y en qué momento del proceso lo hace."
```

---

### 2. `ia/spec-driven-development`
**Correlación documentada:** `2026-04-03_vibe-coding--spec-driven-development.md`

```yaml
edges:
  - target: vibe-coding
    tipo: contradicts
    why: "spec-driven-development fija el criterio de done antes de ejecutar; vibe-coding lo negocia en tiempo real con el output emergente. La tensión es estructural: el spec presupone que el problema es definible antes de resolverlo, lo que vibe-coding refuta al tratar la ejecución como proceso de descubrimiento."
```

---

### 3. `producto/claridad-antes-de-velocidad`
**Correlación documentada:** `2026-04-10_claridad-antes-de-velocidad--momento-liminal.md`

```yaml
edges:
  - target: momento-liminal
    tipo: contradicts
    why: "claridad-antes-de-velocidad exige orientación explícita como prerequisito de acción efectiva; momento-liminal propone que la desorientación productiva es la condición propia del umbral, no un problema a resolver antes de actuar. La tensión es epistemológica: ¿la claridad precede al conocimiento o emerge de habitar la incertidumbre?"
```

---

### 4. `filosofia/momento-liminal`
**Correlación documentada:** `2026-04-10_claridad-antes-de-velocidad--momento-liminal.md`

```yaml
edges:
  - target: claridad-antes-de-velocidad
    tipo: contradicts
    why: "momento-liminal propone que el umbral es productivo precisamente porque no tiene orientación fija; claridad-antes-de-velocidad trata la falta de orientación como obstáculo que debe resolverse antes de actuar. La tensión determina si la ambigüedad se gestiona como condición o como falla."
```

---

### 5. `diseno/fundamentales-vs-flux`
**Correlaciones documentadas:** `2026-04-10_fundamentales-vs-flux--disenador-a-constructor.md` · `2026-04-15_automatizacion-vs-ampliacion--fundamentales-vs-flux.md`

```yaml
edges:
  - target: disenador-a-constructor
    tipo: refines
    why: "La práctica constructiva es el método para entrenar el criterio que permite identificar qué es fundamental y qué es flux. Sin este criterio encarnado en la ejecución real, la distinción se vuelve teórica e inaplicable en decisiones concretas de diseño bajo presión o ambigüedad."
  - target: automatizacion-vs-ampliacion
    tipo: same_mechanism_as
    why: "Ambos conceptos proponen la misma línea divisoria con distinto vocabulario: lo que automatizacion-vs-ampliacion llama 'amplificable' coincide con lo que fundamentales-vs-flux llama 'fundamental'; lo 'automatizable' coincide con lo 'flux'. El mecanismo subyacente es idéntico: distinguir lo que requiere criterio de lo que es procedimiento repetible."
```

---

### 6. `diseno/disenador-a-constructor`
**Correlaciones documentadas:** `2026-04-10_fundamentales-vs-flux--disenador-a-constructor.md` · `2026-04-15_ia-como-filtro-de-entrada--disenador-a-constructor.md`

```yaml
edges:
  - target: fundamentales-vs-flux
    tipo: refines
    why: "disenador-a-constructor amplifica la distinción de fundamentales-vs-flux: la construcción no es una habilidad técnica adicional sino el método por el que el diseñador encarna el criterio necesario para distinguir qué es fundamental de qué es intercambiable en un sistema dado."
  - target: ia-como-filtro-de-entrada
    tipo: requires
    why: "El modo constructor presupone un diseñador con criterio formado en el proceso de aprendizaje junior. ia-como-filtro-de-entrada documenta que ese proceso formativo está cerrándose. El diseñador-constructor requiere exactamente el tipo de experiencia temprana que el filtro de entrada elimina del mercado laboral."
```

---

### 7. `organizaciones/automatizar-mi-propio-trabajo`
**Correlación documentada:** `2026-04-11_automatizar-mi-propio-trabajo--expertise-de-dominio-en-producto.md`

```yaml
edges:
  - target: expertise-de-dominio-en-producto
    tipo: requires
    why: "Automatizar el propio trabajo requiere primero saber qué vale la pena automatizar, lo que exige expertise de dominio. Sin ese expertise, se automatizan los pasos superficiales del proceso, no los que capturan criterio real. El intento de automatizar también funciona como arqueología: revela el expertise que el trabajador no sabía que tenía."
```

---

### 8. `producto/expertise-de-dominio-en-producto`
**Correlación documentada:** `2026-04-11_automatizar-mi-propio-trabajo--expertise-de-dominio-en-producto.md`

```yaml
edges:
  - target: automatizar-mi-propio-trabajo
    tipo: requires
    why: "El expertise de dominio no se vuelve legible hasta que se intenta automatizar. La automatización del propio trabajo es el mecanismo de externalización del expertise tácito: fuerza al experto a articular qué hace exactamente y por qué, convirtiendo conocimiento implícito en estructura transferible."
```

---

### 9. `ia/automatizacion-vs-ampliacion`
**Correlación documentada:** `2026-04-15_automatizacion-vs-ampliacion--fundamentales-vs-flux.md`

```yaml
edges:
  - target: fundamentales-vs-flux
    tipo: same_mechanism_as
    why: "La distinción automatizable/amplificable de automatizacion-vs-ampliacion opera sobre la misma línea que la distinción flux/fundamental. Lo flux es automatizable porque no requiere criterio situacional; lo fundamental es amplificable porque el criterio que lo define es precisamente lo que la IA no puede reemplazar sin perder valor."
```

---

### 10. `economia/ia-como-filtro-de-entrada`
**Correlaciones documentadas:** `2026-04-15_ia-como-filtro-de-entrada--agentes-ia.md` · `2026-04-15_ia-como-filtro-de-entrada--disenador-a-constructor.md`

```yaml
edges:
  - target: agentes-ia
    tipo: contradicts
    why: "El mismo sistema de IA tiene efectos estructuralmente opuestos según la posición del actor: ia-como-filtro-de-entrada documenta que cierra el acceso a posiciones junior; agentes-ia documenta que amplifica el alcance de operadores con criterio. Multiplica a quienes ya tienen criterio y sustituye a quienes venían a adquirirlo."
  - target: disenador-a-constructor
    tipo: requires
    why: "El diseñador-constructor presupone un actor con criterio para evaluar lo que construye. ia-como-filtro-de-entrada muestra que el filtro está cerrando el camino formativo por el que ese criterio se adquiría históricamente. La transición al modo constructor requiere exactamente la experiencia junior que el filtro elimina."
```

---

### 11. `ia/agentes-ia`
**Correlación documentada:** `2026-04-15_ia-como-filtro-de-entrada--agentes-ia.md`

```yaml
edges:
  - target: ia-como-filtro-de-entrada
    tipo: contradicts
    why: "agentes-ia documenta que la IA amplifica el alcance de operadores con criterio establecido; ia-como-filtro-de-entrada documenta que la misma IA cierra el acceso formativo para quienes vendrían a desarrollar ese criterio. La contradicción es estructural: el mismo sistema beneficia y daña a actores en diferentes posiciones del escalafón."
```

---

### 12. `economia/senal-anticipada-mercado-laboral`
**Correlación documentada:** `2026-04-15_senal-anticipada-mercado-laboral--gobernanza-ia-performativa.md`

```yaml
edges:
  - target: gobernanza-ia-performativa
    tipo: same_mechanism_as
    why: "Ambos documentan la misma estructura de falla institucional: señal observable de impacto sistémico seguida de respuesta que gestiona la percepción del riesgo sin modificar el sistema que lo genera. senal-anticipada-mercado-laboral muestra la señal; gobernanza-ia-performativa muestra el mecanismo de respuesta que la absorbe sin procesarla."
```

---

### 13. `ia/gobernanza-ia-performativa`
**Correlación documentada:** `2026-04-15_senal-anticipada-mercado-laboral--gobernanza-ia-performativa.md`

```yaml
edges:
  - target: senal-anticipada-mercado-laboral
    tipo: same_mechanism_as
    why: "gobernanza-ia-performativa describe el mecanismo por el que las instituciones responden a señales de riesgo con acciones que satisfacen la demanda de respuesta sin alterar el sistema. senal-anticipada-mercado-laboral provee un caso específico y documentado de esa señal siendo absorbida performativamente por organizaciones y gobiernos."
```

---

### 14. `producto/copiloto-de-producto`
**Correlación documentada:** `2026-04-18_copiloto-de-producto--quien-controla-el-prompt.md`

```yaml
edges:
  - target: quien-controla-el-prompt
    tipo: refines
    why: "quien-controla-el-prompt opera en la capa táctica: quién formula la instrucción inmediata al modelo en un momento dado. copiloto-de-producto opera en la capa estratégica: quién mantiene la orientación del producto en el tiempo. El copiloto refina el concepto de control añadiendo la dimensión temporal y organizacional que la pregunta táctica no resuelve."
```

---

### 15. `diseno/quien-controla-el-prompt`
**Correlación documentada:** `2026-04-18_copiloto-de-producto--quien-controla-el-prompt.md`

```yaml
edges:
  - target: copiloto-de-producto
    tipo: refines
    why: "quien-controla-el-prompt es la capa táctica del control de la IA; copiloto-de-producto es la capa estratégica. Quien controla el prompt decide la instrucción inmediata; el copiloto de producto mantiene la orientación que hace que cada prompt sirva al objetivo correcto. Ambas capas son necesarias y operan en tiempos distintos."
```

---

### 16. `ia/espectro-autonomia-agente`
**Correlaciones documentadas:** `2026-04-18_espectro-autonomia-agente--capital-de-contexto.md` · `2026-04-18_espectro-autonomia-agente--fabrica-oscura-de-software.md`

```yaml
edges:
  - target: capital-de-contexto
    tipo: requires
    why: "El espectro de autonomía del agente describe posiciones disponibles desde executor hasta observer; capital-de-contexto determina cuál de esas posiciones es sostenible para un actor dado. Sin capital suficiente, delegar la posición de observer es insostenible: sin contexto acumulado no se puede evaluar si el agente se está desviando."
  - target: fabrica-oscura-de-software
    tipo: refines
    why: "La fábrica oscura de software es una realización concreta de una posición extrema en el espectro: operador que ha delegado ejecución completa sin presencia activa. Refina el espectro dotándolo de una forma organizacional específica — no es solo una categoría abstracta sino una configuración que ya existe con consecuencias documentadas."
```

---

### 17. `ia/capital-de-contexto`
**Correlaciones documentadas:** `2026-04-18_espectro-autonomia-agente--capital-de-contexto.md` · `2026-04-18_fabrica-oscura-de-software--capital-de-contexto.md`

```yaml
edges:
  - target: espectro-autonomia-agente
    tipo: requires
    why: "El capital de contexto determina qué posición en el espectro de autonomía del agente es sostenible. La misma posición de observer que es segura con alto capital se vuelve riesgosa con capital bajo: sin modelos mentales acumulados sobre el dominio, no hay capacidad real de evaluar si el agente opera correctamente."
  - target: fabrica-oscura-de-software
    tipo: requires
    why: "La fábrica oscura de software es sostenible solo si el capital de contexto ha sido suficientemente acumulado y codificado para que el sistema funcione sin supervisión continua. El capital no es un prerequisito opcional: es la condición que distingue la fábrica oscura funcional del abandono de control con consecuencias catastróficas."
```

---

### 18. `ia/fabrica-oscura-de-software`
**Correlaciones documentadas:** `2026-04-18_espectro-autonomia-agente--fabrica-oscura-de-software.md` · `2026-04-18_fabrica-oscura-de-software--capital-de-contexto.md`

```yaml
edges:
  - target: espectro-autonomia-agente
    tipo: exemplifies
    why: "La fábrica oscura de software es la forma más concreta y visible de una posición extrema en el espectro de autonomía: el operador no está presente pero el sistema opera. Ejemplifica el espectro al mostrar qué aspecto tiene la posición más autónoma en la práctica organizacional real, incluyendo los riesgos específicos que genera."
  - target: capital-de-contexto
    tipo: exemplifies
    why: "La fábrica oscura de software es la prueba más exigente del capital de contexto: el sistema funciona sin supervisión humana continua porque el capital ha sido acumulado y codificado con suficiente densidad. Ejemplifica el concepto al mostrar el umbral mínimo de capital que se necesita — y lo que ocurre cuando no se alcanza."
```

---

### 19. `producto/pit-stop-cognitivo`
**Correlaciones documentadas:** `2026-04-18_pit-stop-cognitivo--confianza-a-traves-de-velocidad.md` · `2026-04-18_pit-stop-cognitivo--feedback-que-escala.md`

```yaml
edges:
  - target: confianza-a-traves-de-velocidad
    tipo: enables
    why: "pit-stop-cognitivo describe pausas de revisión intencionales que aparentemente ralentizan el proceso; confianza-a-traves-de-velocidad propone que la velocidad sostenida de entrega es el mecanismo de construcción de confianza. El pit-stop habilita la velocidad sostenida: sin revisión periódica, la velocidad acumula deuda que destruye la confianza que intenta construir."
  - target: feedback-que-escala
    tipo: extends
    why: "feedback-que-escala captura señales sobre lo que el sistema produce; pit-stop-cognitivo captura señales sobre cómo el equipo está procesando lo que produce — problemas de criterio, fatiga, deriva sistémica. El pit-stop extiende el alcance del feedback hacia la dimensión cognitiva y organizacional que los loops sobre output no pueden detectar."
```

---

### 20. `producto/confianza-a-traves-de-velocidad`
**Correlación documentada:** `2026-04-18_pit-stop-cognitivo--confianza-a-traves-de-velocidad.md`

```yaml
edges:
  - target: pit-stop-cognitivo
    tipo: requires
    why: "La confianza construida a través de la velocidad es frágil si la velocidad no es sostenible. pit-stop-cognitivo provee el mecanismo que hace sostenible la velocidad: las pausas de revisión evitan la acumulación de deuda que eventualmente interrumpe el flujo de entrega y destruye la confianza que la velocidad había construido."
```

---

### 21. `producto/feedback-que-escala`
**Correlación documentada:** `2026-04-18_pit-stop-cognitivo--feedback-que-escala.md`

```yaml
edges:
  - target: pit-stop-cognitivo
    tipo: requires
    why: "El feedback que escala captura señales sobre outputs del sistema pero no sobre el estado cognitivo del equipo que los produce. pit-stop-cognitivo provee la capa de feedback que feedback-que-escala no alcanza: detecta cuándo el equipo está acumulando deuda de criterio o fatiga de decisión que no aparece en ningún loop de feedback sobre resultados."
```

---

---

## Sección B — Conceptos sin correlación documentada (candidatos)

> Para cada concepto: slug · relacionado actual · candidatos de edges con tipo propuesto y nota breve.
> Estos candidatos requieren correlación documentada o revisión explícita antes de convertirse en edges definitivos.

---

### `diseno/agencia-humana-como-imperativo-ux`
**Relacionado actual:** `[espectro-autonomia-agente, ux-checkpoints, comprehension-debt]`

| target | tipo propuesto | nota |
|---|---|---|
| espectro-autonomia-agente | `requires` | La agencia humana define qué posición del espectro es éticamente aceptable, no solo técnicamente posible |
| ux-checkpoints | `enables` | Los checkpoints son los momentos operacionales donde la agencia humana se ejerce en el flujo real |
| comprehension-debt | `contradicts` | La agencia humana exige comprensión activa del sistema; la deuda de comprensión la erosiona sin hacerlo visible |

---

### `diseno/arquitectura-de-confianza`
**Relacionado actual:** `[gobernanza-ia-performativa, arnes-del-agente, ux-checkpoints]`

| target | tipo propuesto | nota |
|---|---|---|
| gobernanza-ia-performativa | `contradicts` | Arquitectura real de confianza (estructural, técnica) vs gobernanza performativa (gestión de percepción) |
| arnes-del-agente | `requires` | El arnes es el mecanismo técnico que implementa la arquitectura de confianza en el sistema real |
| ux-checkpoints | `exemplifies` | Los checkpoints son instancias específicas donde la arquitectura de confianza se materializa en el flujo UX |

---

### `diseno/de-usuario-a-cliente-servido`
**Relacionado actual:** `[disenador-a-constructor, las-tres-caras-del-producto-agentico, agencia-humana-como-imperativo-ux]`

| target | tipo propuesto | nota |
|---|---|---|
| disenador-a-constructor | `extends` | La transición a cliente servido amplía la trayectoria del diseñador-constructor al rol de definición de qué servicio se presta |
| las-tres-caras-del-producto-agentico | `requires` | La transición requiere entender qué cara del producto se está construyendo y para quién |
| agencia-humana-como-imperativo-ux | `requires` | El cambio de modo usuario a cliente servido exige mantener agencia humana sobre la definición del servicio |

---

### `diseno/diseno-dos-velocidades`
**Relacionado actual:** `[disenador-a-constructor, mvp-a-prototipo-en-produccion, quien-controla-el-prompt]`

| target | tipo propuesto | nota |
|---|---|---|
| disenador-a-constructor | `extends` | El diseño de dos velocidades opera dentro del modo constructor y lo hace más granular: velocidad de exploración vs velocidad de entrega |
| mvp-a-prototipo-en-produccion | `extends` | El mvp-a-prototipo-en-produccion es una implementación del diseño de dos velocidades en el ciclo de producto |
| quien-controla-el-prompt | `requires` | La velocidad rápida requiere control claro del prompt para evitar que la exploración consuma el tiempo de entrega |

---

### `diseno/diseno-uxui-y-ia`
**Relacionado actual:** `[disenador-a-constructor, usuarios-sinteticos, quien-controla-el-prompt]`

| target | tipo propuesto | nota |
|---|---|---|
| disenador-a-constructor | `requires` | El diseño UX/UI con IA requiere el modo constructor — el diseñador opera las herramientas, no solo las especifica |
| usuarios-sinteticos | `requires` | El diseño UX/UI con IA implica validar con usuarios sintéticos antes de exponer a usuarios reales |
| quien-controla-el-prompt | `extends` | Extiende la pregunta del control del prompt al contexto específico del diseño de interfaces |

---

### `diseno/el-moat-del-gusto`
**Relacionado actual:** `[fundamentales-vs-flux, disenador-a-constructor, quien-controla-el-prompt]`

| target | tipo propuesto | nota |
|---|---|---|
| fundamentales-vs-flux | `requires` | El moat del gusto es la capacidad encarnada de distinguir fundamentales de flux — la distinción depende del criterio |
| disenador-a-constructor | `extends` | El moat del gusto es la ventaja diferencial que acumula el diseñador-constructor como resultado de construir en vez de solo especificar |
| quien-controla-el-prompt | `enables` | El gusto es lo que permite controlar el prompt con criterio: sin gusto formado, el control es mecánico, no editorial |

---

### `diseno/metacognicion-del-disenador`
**Relacionado actual:** `[claridad-antes-de-velocidad, arquitectura-de-inteligencia, pit-stop-cognitivo]`

| target | tipo propuesto | nota |
|---|---|---|
| claridad-antes-de-velocidad | `requires` | La metacognición es el mecanismo que genera la claridad que claridad-antes-de-velocidad exige como prerequisito |
| arquitectura-de-inteligencia | `refines` | La metacognición es el mecanismo personal de lo que arquitectura-de-inteligencia plantea a nivel sistémico |
| pit-stop-cognitivo | `extends` | El pit-stop es el momento estructurado donde se ejecuta la metacognición del diseñador |

---

### `diseno/sycophancy-como-riesgo-de-diseno`
**Relacionado actual:** `[espiral-delusional, gobernanza-ia-performativa, arquitectura-de-confianza]`

| target | tipo propuesto | nota |
|---|---|---|
| espiral-delusional | `same_mechanism_as` | Ambos documentan el mismo mecanismo: feedback positivo que amplifica errores en vez de corregirlos |
| gobernanza-ia-performativa | `exemplifies` | La sycophancy del modelo es un caso específico de respuesta que satisface la demanda de respuesta sin resolver el problema subyacente |
| arquitectura-de-confianza | `contradicts` | La sycophancy destruye la confianza que la arquitectura de confianza intenta construir |

---

### `diseno/ux-checkpoints`
**Relacionado actual:** `[pit-stop-cognitivo, arnes-del-agente, arquitectura-de-confianza]`

| target | tipo propuesto | nota |
|---|---|---|
| pit-stop-cognitivo | `analogous_to` | Ambos son pausas intencionales — el pit-stop en el proceso del equipo, el checkpoint en el flujo UX del usuario |
| arnes-del-agente | `requires` | Los checkpoints requieren el arnes para ser ejecutables técnicamente sin fricción excesiva |
| arquitectura-de-confianza | `exemplifies` | Los checkpoints son la implementación UX de la arquitectura de confianza en el punto de contacto con el usuario |

---

### `economia/inversion-sesgo-tecnologico`
**Relacionado actual:** `[ia-como-filtro-de-entrada, automatizacion-vs-ampliacion, fundamentales-vs-flux]`

| target | tipo propuesto | nota |
|---|---|---|
| ia-como-filtro-de-entrada | `extends` | Extiende el análisis del filtro de entrada al nivel macroeconómico: no solo qué empleos filtra sino qué tipo de inversión financia ese filtro |
| automatizacion-vs-ampliacion | `refines` | La inversión del sesgo tecnológico explica el incentivo económico que determina cuándo se automatiza y cuándo se amplifica |
| fundamentales-vs-flux | `extends` | Recontextualiza la distinción al nivel de política: el sesgo invierte en automatizar lo flux dejando sin apoyo lo fundamental |

---

### `filosofia/arquitectura-de-inteligencia`
**Relacionado actual:** `[agentes-ia, claridad-antes-de-velocidad, quien-controla-el-prompt]`

| target | tipo propuesto | nota |
|---|---|---|
| agentes-ia | `refines` | Agrega la dimensión filosófica y estructural a lo que agentes-ia describe funcionalmente: no solo qué hacen sino cómo se diseña el sistema que los contiene |
| claridad-antes-de-velocidad | `requires` | La arquitectura de inteligencia requiere claridad de propósito antes de elegir qué componentes incluir |
| quien-controla-el-prompt | `extends` | Extiende la pregunta del control del prompt al nivel de la arquitectura del sistema completo |

---

### `filosofia/colonialismo-cultural-digital`
**Relacionado actual:** `[quien-controla-el-prompt, agentes-ia, disenador-a-constructor]`

| target | tipo propuesto | nota |
|---|---|---|
| quien-controla-el-prompt | `extends` | Extiende la pregunta del control del prompt a la dimensión geopolítica y cultural: quién controla los modelos que controlan los prompts |
| agentes-ia | `extends` | Extiende el análisis de los agentes IA a su impacto en la diversidad cultural y lingüística global |
| disenador-a-constructor | `contradicts` | El modo constructor asume acceso equitativo a las herramientas; el colonialismo digital cuestiona estructuralmente ese acceso |

---

### `filosofia/lo-ilegible-como-senal`
**Relacionado actual:** `[arquitectura-de-inteligencia, momento-liminal, fundamentales-vs-flux]`

| target | tipo propuesto | nota |
|---|---|---|
| arquitectura-de-inteligencia | `refines` | Lo ilegible como señal agrega el criterio de la ilegibilidad como dato válido en el diseño de sistemas de inteligencia |
| momento-liminal | `same_mechanism_as` | Ambos proponen que lo ambiguo/ilegible/desorientado tiene valor epistémico propio, no es solo ruido a eliminar |
| fundamentales-vs-flux | `extends` | Lo ilegible puede ser señal de un fundamental emergente que todavía no tiene nombre ni categoría en el sistema actual |

---

### `ia/arnes-del-agente`
**Relacionado actual:** `[espectro-autonomia-agente, gobernanza-ia-performativa, las-tres-caras-del-producto-agentico]`

| target | tipo propuesto | nota |
|---|---|---|
| espectro-autonomia-agente | `enables` | El arnes es el mecanismo que hace posible operar en diferentes posiciones del espectro de forma segura y reversible |
| gobernanza-ia-performativa | `contradicts` | El arnes es gobernanza real (técnica, verificable) en contraste con la gobernanza performativa que gestiona percepción |
| las-tres-caras-del-producto-agentico | `requires` | Gestionar las tres caras del producto agentico requiere el arnes como infraestructura de control técnico |

---

### `ia/comprehension-debt`
**Relacionado actual:** `[pit-stop-cognitivo, vibe-coding, spec-driven-development]`

| target | tipo propuesto | nota |
|---|---|---|
| pit-stop-cognitivo | `requires` | El pit-stop cognitivo es el mecanismo para detectar y frenar la acumulación de deuda de comprensión antes de que sea irreversible |
| vibe-coding | `extends` | Extiende el análisis de vibe-coding al costo cognitivo oculto que el modo de producción por flujo genera sin que el equipo lo note |
| spec-driven-development | `contradicts` | spec-driven-development es la respuesta estructural a la deuda de comprensión que vibe-coding acumula: el spec fuerza comprensión antes de ejecutar |

---

### `ia/conocimiento-autoorganizado-por-llm`
**Relacionado actual:** `[arquitectura-de-inteligencia, automatizar-mi-propio-trabajo, agentes-ia]`

| target | tipo propuesto | nota |
|---|---|---|
| arquitectura-de-inteligencia | `extends` | El conocimiento autoorganizado por LLM es una implementación concreta de lo que arquitectura-de-inteligencia plantea como principio |
| automatizar-mi-propio-trabajo | `enables` | El conocimiento autoorganizado enables automatizar la gestión del conocimiento propio sin perder la estructura |
| agentes-ia | `requires` | El conocimiento autoorganizado a escala requiere agentes IA para mantenerse coherente con el crecimiento del vault |

---

### `ia/espiral-delusional`
**Relacionado actual:** `[arquitectura-de-confianza, gobernanza-ia-performativa, ux-checkpoints]`

| target | tipo propuesto | nota |
|---|---|---|
| arquitectura-de-confianza | `contradicts` | La espiral delusional destruye la confianza que la arquitectura intenta construir: el sistema se refuerza a sí mismo sin corrección |
| gobernanza-ia-performativa | `same_mechanism_as` | Ambos describen sistemas que se refuerzan sin corrección externa: la espiral es el mecanismo, la gobernanza performativa es la respuesta institucional que lo permite |
| ux-checkpoints | `requires` | Los checkpoints son la interrupción necesaria para que la espiral delusional no se cierre sobre sí misma |

---

### `ia/impuesto-de-verificacion`
**Relacionado actual:** *(vacío — sin campo relacionado documentado)*

> No hay candidatos de edges desde `relacionado:`. Propuesta manual basada en contenido del concepto:

| target | tipo propuesto | nota |
|---|---|---|
| pit-stop-cognitivo | `contradicts` | El pit-stop es drenaje cognitivo intencional y recuperable; el impuesto de verificación es drenaje no intencional y acumulativo — mismo dominio, orígenes opuestos |
| automatizacion-vs-ampliacion | `refines` | El impuesto precisa el tercer modo que automatizacion-vs-ampliacion no contempla: ni automatización ni amplificación, sino drenaje por supervisión |

> **Nota:** Se recomienda también actualizar el campo `relacionado:` de este concepto antes de la Fase 2.

---

### `ia/legibilidad-de-maquina`
**Relacionado actual:** `[web-bifurcada, colonialismo-cultural-digital, lo-ilegible-como-senal]`

| target | tipo propuesto | nota |
|---|---|---|
| web-bifurcada | `requires` | La web bifurcada requiere legibilidad de máquina para funcionar: la capa para agentes presupone que el contenido es parseble |
| colonialismo-cultural-digital | `extends` | Extiende el análisis del colonialismo al nivel de los estándares técnicos: quién define qué es legible para las máquinas |
| lo-ilegible-como-senal | `contradicts` | La legibilidad de máquina exige que todo sea codificable y estructurado; lo ilegible como señal propone que la ilegibilidad tiene valor epistémico propio que la codificación destruye |

---

### `ia/usuarios-sinteticos`
**Relacionado actual:** `[disenador-a-constructor, mvp-a-prototipo-en-produccion, agentes-ia]`

| target | tipo propuesto | nota |
|---|---|---|
| disenador-a-constructor | `enables` | Los usuarios sintéticos enables al diseñador-constructor testear sin necesidad de reclutamiento real en etapas tempranas |
| mvp-a-prototipo-en-produccion | `enables` | Los usuarios sintéticos enables acelerar el ciclo de mvp al comprimir el ciclo de validación inicial |
| agentes-ia | `exemplifies` | Los usuarios sintéticos son un tipo específico de agente IA orientado a validación de producto — el caso más concreto del concepto general |

---

### `ia/web-bifurcada`
**Relacionado actual:** `[agentes-ia, arnes-del-agente, quien-controla-el-prompt]`

| target | tipo propuesto | nota |
|---|---|---|
| agentes-ia | `requires` | La web bifurcada es el contexto donde los agentes IA operan: requiere que los agentes existan para que la bifurcación tenga sentido estructural |
| arnes-del-agente | `extends` | El arnes del agente debe diseñarse para la web bifurcada: el contexto de información cambia cuando los agentes son los principales consumidores |
| quien-controla-el-prompt | `extends` | La web bifurcada extiende la pregunta del control del prompt a la infraestructura de acceso a información: quién controla qué ve el agente |

---

### `organizaciones/condicion-redespliegue`
**Relacionado actual:** `[automatizar-mi-propio-trabajo, feedback-que-escala, equipos-pequenos-alto-impacto]`

| target | tipo propuesto | nota |
|---|---|---|
| automatizar-mi-propio-trabajo | `requires` | La condición de redespliegue requiere primero automatizar el trabajo propio para liberar la capacidad a redirigir |
| feedback-que-escala | `requires` | El redespliegue requiere feedback que escale para evaluar si el nuevo valor generado justifica el cambio de modo |
| equipos-pequenos-alto-impacto | `enables` | La condición de redespliegue es lo que enables que equipos pequeños mantengan alto impacto con el tiempo: sin redespliegue, el equipo queda atrapado en su propio backlog |

---

### `organizaciones/equipos-pequenos-alto-impacto`
**Relacionado actual:** `[disenador-a-constructor, vibe-coding, agentes-ia]`

| target | tipo propuesto | nota |
|---|---|---|
| disenador-a-constructor | `requires` | El equipo pequeño de alto impacto requiere miembros en modo constructor: sin criterio para ejecutar, el equipo pequeño solo es poco numeroso |
| vibe-coding | `requires` | vibe-coding es el modo de producción que permite al equipo pequeño iterar a velocidad de impacto sin esperar aprobaciones de ciclos largos |
| agentes-ia | `enables` | Los agentes IA enables la escala de impacto que hace del equipo pequeño algo competitivo frente a equipos más grandes |

---

### `organizaciones/ia-sin-ecosistema`
**Relacionado actual:** `[gobernanza-ia-performativa, condicion-redespliegue, capital-de-contexto]`

| target | tipo propuesto | nota |
|---|---|---|
| gobernanza-ia-performativa | `exemplifies` | La IA sin ecosistema es el caso más concreto de gobernanza performativa: se adopta la herramienta como señal sin construir el sistema que la haría funcionar |
| condicion-redespliegue | `contradicts` | La IA sin ecosistema hace imposible la condición de redespliegue: sin procesos rediseñados, no hay dónde redirigir el tiempo liberado |
| capital-de-contexto | `requires` | Construir el ecosistema para que la IA funcione requiere capital de contexto: sin modelos mentales compartidos, los prompts son aleatorios |

---

### `organizaciones/juicio-como-trabajo-completo`
**Relacionado actual:** `[ia-como-filtro-de-entrada, condicion-redespliegue, automatizar-mi-propio-trabajo]`

| target | tipo propuesto | nota |
|---|---|---|
| ia-como-filtro-de-entrada | `extends` | Extiende el análisis del filtro a la capa del trabajo que sí persiste: si la IA filtra la entrada, lo que queda es el juicio — este concepto define qué es ese trabajo |
| condicion-redespliegue | `enables` | El juicio como trabajo completo enables la condición de redespliegue al definir hacia dónde se redirige la capacidad liberada por la automatización |
| automatizar-mi-propio-trabajo | `requires` | Automatizar el propio trabajo requiere el juicio previo sobre qué vale la pena automatizar y qué pertenece al dominio del criterio no delegable |

---

### `producto/las-tres-caras-del-producto-agentico`
**Relacionado actual:** `[espectro-autonomia-agente, arnes-del-agente, legibilidad-de-maquina]`

| target | tipo propuesto | nota |
|---|---|---|
| espectro-autonomia-agente | `extends` | Extiende el espectro de autonomía a la dimensión del producto: no solo posiciones del operador sino caras del producto que el operador construye |
| arnes-del-agente | `requires` | Las tres caras del producto agentico requieren el arnes para que cada capa funcione de forma segura y monitoreada |
| legibilidad-de-maquina | `requires` | La cara técnica del producto agentico requiere legibilidad de máquina para que los agentes puedan operar sobre el contenido |

---

### `producto/metricas-post-pantalla`
**Relacionado actual:** `[feedback-que-escala, las-tres-caras-del-producto-agentico, arnes-del-agente]`

| target | tipo propuesto | nota |
|---|---|---|
| feedback-que-escala | `extends` | Extiende el análisis de feedback al contexto donde no hay pantalla visible: las métricas post-pantalla son la capa de feedback que feedback-que-escala no llega a describir |
| las-tres-caras-del-producto-agentico | `requires` | Medir el producto agentico en sus tres caras requiere métricas post-pantalla: la cara de backend no genera eventos de interfaz |
| arnes-del-agente | `enables` | El arnes es lo que hace posible capturar métricas post-pantalla sin instrumentación manual en cada punto del sistema |

---

### `producto/mvp-a-prototipo-en-produccion`
**Relacionado actual:** `[vibe-coding, agentes-ia, disenador-a-constructor]`

| target | tipo propuesto | nota |
|---|---|---|
| vibe-coding | `enables` | vibe-coding enables el ciclo de mvp a prototipo en producción al reducir el costo de iteración por debajo del umbral de justificación formal |
| agentes-ia | `enables` | Los agentes IA enables acelerar el ciclo al ejecutar tareas repetitivas del ciclo de desarrollo sin intervención manual |
| disenador-a-constructor | `requires` | El ciclo mvp-a-prototipo requiere el modo constructor: el diseñador que no puede construir no puede iterar a la velocidad que el ciclo exige |

---

### `producto/pmf-perecedero`
**Relacionado actual:** `[mvp-a-prototipo-en-produccion, confianza-a-traves-de-velocidad, fundamentales-vs-flux]`

| target | tipo propuesto | nota |
|---|---|---|
| mvp-a-prototipo-en-produccion | `extends` | Extiende el análisis del ciclo mvp al ciclo de vida completo del ajuste mercado-producto: el mvp no termina en producción, termina cuando el PMF expira |
| confianza-a-traves-de-velocidad | `requires` | El PMF perecedero requiere velocidad continua de entrega para renovar la confianza antes de que el ajuste expire y el usuario busque alternativas |
| fundamentales-vs-flux | `refines` | El PMF perecedero refina la distinción: el ajuste de mercado-producto es flux, no fundamental — identificar cuál es cuál define la estrategia de producto |

---

### `producto/restriccion-de-tiempo-como-ventaja`
**Relacionado actual:** `[claridad-antes-de-velocidad, mvp-a-prototipo-en-produccion, vibe-coding]`

| target | tipo propuesto | nota |
|---|---|---|
| claridad-antes-de-velocidad | `contradicts` | La restricción de tiempo fuerza claridad por presión; claridad-antes-de-velocidad propone que la claridad debe preceder la acción por diseño — orígenes opuestos de la misma condición |
| mvp-a-prototipo-en-produccion | `enables` | La restricción de tiempo enables el ciclo de mvp al forzar cortes de scope que hacen posible una primera entrega real |
| vibe-coding | `requires` | vibe-coding requires restricciones de tiempo como mecanismo de convergencia: sin ellas, la exploración por flujo no tiene condición de cierre |

---

## Resumen ejecutivo

| Estado | Cantidad |
|---|---|
| Conceptos con edges drafted (Sección A) | 21 |
| Conceptos con edges candidatos (Sección B) | 30 |
| Correlaciones fuente en `Correlaciones/` | 14 |
| Edges drafted total | 28 |
| Edges candidatos total | 80 |
| **Total conceptos** | **51** |

**Próximo paso tras aprobación:** añadir `edges:` al frontmatter de los 21 conceptos de Sección A, actualizar `generar_index.py` para leer `edges:` y generar sección de grafo tipado en ATLAS.md, regenerar ATLAS, git commit y push.
