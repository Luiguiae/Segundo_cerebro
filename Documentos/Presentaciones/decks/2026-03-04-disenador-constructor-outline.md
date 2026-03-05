---
titulo: "Del Diseñador al Constructor — Outline de Charla"
tipo: presentacion
estado: borrador
autor: "Luigui Avila"
fecha: 2026-03-04
updated: 2026-03-04
tags: [diseño, construccion, ia, vibe-coding, agentes, producto, roles]
fuentes:
  - Conocimiento/Conceptos/disenador-a-constructor.md
  - Conocimiento/Conceptos/vibe-coding.md
  - Conocimiento/Conceptos/agentes-ia.md
  - autor: "Jenny Wen (Head of Design, Anthropic / ex Director of Design, Figma)"
    titulo: "Lenny's Podcast — The future of design"
    url: "https://www.youtube.com/watch?v=eh8bcBIAAFo"
---

# Del Diseñador al Constructor
## *Cómo la IA borra la frontera entre imaginar y producir*

---

## 1. TÍTULO Y SUBTÍTULO

**Título principal:** Del Diseñador al Constructor

**Subtítulo:** En 10 minutos vas a entender por qué la IA no es una herramienta más — es un cambio de rol.

**Progresión narrativa:** El diseñador como espectador → el diseñador como constructor → el diseñador como equipo completo.

---

## 2. HOOK *(~2 min)*

**Pregunta de apertura:**
> ¿Cuánto tiempo pasó la última vez entre que tuviste una idea y la pudiste mostrar funcionando?

**Por qué importa ahora:**
El 25% de las startups de Y Combinator Winter 2025 tienen el 95% de su código generado por IA. Equipos de menos de 10 personas están alcanzando $10M en revenue. Esto no es el futuro — es lo que está pasando mientras esta presentación ocurre.

El cuello de botella de la construcción de productos siempre fue técnico. Ese cuello de botella desapareció.

**Dato concreto para la audiencia de diseñadores:**
Jenny Wen — Head of Design de Claude, ex Director of Design en Figma — describe cómo cambió su propio trabajo: hace 2-3 años el 60-70% de su tiempo era mocking y prototyping. Hoy es 30-40%. El 30-40% que ganó está en pairing directo con engineers. Más un slice nuevo: implementación real de código.

*Esto no es proyección. Es lo que ya está pasando en los equipos más avanzados del mundo.*

**La tensión que abre la charla:**
Los roles de diseñador y desarrollador fueron separados por una barrera técnica. Esa barrera ya no existe. La pregunta ahora no es si puedes construir — es qué tan rápido puedes iterar lo que construyes.

---

## 3. ACTO 1 — Del Diseñador al Constructor

**Idea central:**
Históricamente, el diseñador dependía del desarrollador para que su visión cobrara vida. El handoff era la principal fuente de pérdida de intención en producto: ciclos largos, distancia entre quien imagina y quien construye. Hoy ese modelo está roto.

**El cambio ocurre en tres dimensiones:**
1. **Herramientas**: IDEs con IA (Cursor, Copilot), generadores de UI y vibe coding permiten construir interfaces funcionales sin dominar ingeniería de software.
2. **Mentalidad**: El artefacto final deja de ser un Figma — es un componente funcional.
3. **Rol en el equipo**: En equipos que usan IA, el perfil híbrido no es una ventaja diferencial — es el estándar esperado.

**El proceso canónico está muerto — y tiene nombre el que viene:**
Jenny Wen lo formuló en una charla en Berlín (sept. 2025): el proceso que los diseñadores trataban como evangelio — investigar, divergir, converger — "is basically dead." No murió con la IA. Estaba muriendo antes. La IA lo terminó.

El proceso fue diseñado para un mundo donde construir era lento y caro. En ese mundo, pensar mucho antes de construir tenía sentido. Hoy, construir es más barato que pensar durante semanas.

El modelo que está tomando su lugar se llama **Stingray** (Board of Innovation). La diferencia clave: en el Doble Diamante primero defines el problema y *luego* buscas soluciones. En el Stingray, problemas y soluciones se exploran **en paralelo** desde el primer día. La IA sintetiza datos, genera hipótesis y prototipos simultáneamente. El horizonte de validación pasa de semanas a días.

```
Doble Diamante:  Discover → Define → Develop → Deliver  (secuencial)
Stingray:        Train → Develop → Iterate               (paralelo, problemas+soluciones a la vez)
```

Lo que el Stingray no elimina: en la fase Iterate sigue requiriendo entrevistas reales con usuarios subrepresentados. La IA acelera lo que rodea a la empatía — no la reemplaza.

**Dos tipos de trabajo de diseño que emergen:**
| Tipo | Descripción | Horizonte |
|---|---|---|
| **Soporte a la ejecución** | Acompañar a engineers, dar feedback en tiempo real, implementar polish | Semanal/diario |
| **Visión y dirección** | Apuntar al equipo hacia algo coherente | 3-6 meses (antes: 2-10 años) |

*El horizonte de visión colapsó. Nadie puede hacer un deck de producto a 5 años cuando la tecnología cambia cada 3 meses.*

**Ejemplo concreto:**
Un product designer valida su propia hipótesis con un prototipo funcional en un día, antes de involucrar al equipo de ingeniería. En un equipo de 3 personas construyendo un producto de IA, el diseñador también hace deploys.

Jenny Wen en Anthropic: "I'm doing a lot of last mile stuff where I'm implementing all the polish, and working with engineers really closely to get the feature across the line, and also prototype stuff in actual code."

**Tensión que genera:**
Si el diseñador puede construir... ¿qué pasa con el handoff? ¿Qué pasa con los roles? ¿Y cómo se construye exactamente?

---

## 4. ACTO 2 — Vibe Coding: el habilitador técnico

**Cómo responde la tensión del Acto 1:**
La herramienta que hace posible al diseñador-constructor se llama vibe coding: describís lo que querés en lenguaje natural y la IA genera el código. La barrera entre imaginar y construir desaparece.

**El modelo de madurez (crítico):**
| Layer | Para qué | Herramientas |
|-------|----------|--------------|
| 1 — Exploración | Experimentos, variaciones, demos | Bolt, Lovable |
| 2 — MVP | Flujos reales, interacciones, datos básicos | Lovable, v0 |
| 3 — Engineering | Calidad, consistencia, production-ready | Cursor, Claude Code |

> El error más común: quedarse en Layer 1 y llamarlo "producto".

**Caso real:**
Ryo Lu, Head of Design en Cursor, construyó ryOS — un sistema operativo retro completo — enteramente con vibe coding en Cursor. Felix Lee, CEO de ADPList, construyó herramientas con database y auth. Diseñadores de Google, Apple y Meta pasaron de $50/hr a $150-400/hr al poder construir.

**Nueva capacidad que abre:**
El diseñador ya no necesita un desarrollador para pasar de idea a producto funcional. Pero construir rápido no es lo mismo que construir bien. ¿Qué pasa cuando el volumen de trabajo supera lo que una persona puede manejar?

> "AI is raw material, not finished goods. Most people stop at the first output, rather than using it to begin." — Ryo Lu

---

## 5. ACTO 3 — Equipos de Agentes: el multiplicador

**Cómo multiplica lo anterior:**
El diseñador-constructor con vibe coding es poderoso. El diseñador-constructor orquestando equipos de agentes IA es otro nivel. Un equipo de agentes es un conjunto de modelos especializados que trabajan de forma coordinada: uno investiga, otro escribe código, otro testea, otro despliega — en paralelo, sin intervención humana constante.

**El modelo:**
- **Orquestador**: recibe la tarea, la descompone y asigna subtareas.
- **Agentes especializados**: ejecutan (coding agent, research agent, testing agent).
- **Human-in-the-loop**: el diseñador supervisa, valida y redirige.

**Hacia dónde va:**
Salesforce proyectó que para 2026 las empresas adoptarán un modelo de fuerza laboral orquestada — múltiples agentes especializados bajo un orquestador central. Agentforce ya alcanzó $1.4B en ARR con 114% de crecimiento. El 90% de los equipos de ingeniería ya usan herramientas IA (Jellyfish 2025), subió de 61% en un año.

> "La próxima ola de IA se parecerá a un equipo coordinado en lugar de un modelo único respondiendo preguntas."

> "Build bricks, not readymades. AI es realmente buena componiendo partes, así que construye grandes ladrillos." — Ryo Lu

**Implicaciones para la audiencia:**
Una persona con la mentalidad correcta y acceso a estas herramientas puede operar con la capacidad de un equipo de 10. Los roles de diseñador, PM e ingeniero no desaparecen — se fusionan. La pregunta ya no es si adoptás estas herramientas, sino qué tan rápido empezás.

**El problema que nadie mencionó todavía:**
Los engineers ya no pueden seguir el ritmo de sus propios agentes. Jenny Wen: *"It's not just designers who are feeling like we have to keep up with engineers. I think even engineers are like, 'How do we keep up with ourselves?'"*

La pregunta para el diseñador-constructor no es solo cómo construir más rápido — es cómo mantener criterio y dirección cuando el sistema está produciendo a una velocidad que ningún humano puede supervisar completamente.

---

## 6. SÍNTESIS *(~3 min)*

**Mensaje central en una oración:**
> La IA no reemplaza al diseñador — convierte al diseñador en el equipo completo. Pero alguien tiene que ser accountable de lo que se decide construir.

**Modelo mental que se llevan:**

```
ANTES:  Diseñar → Handoff → Desarrollar → Iterar (semanas)
AHORA:  Imaginar → Construir → Escalar     (horas)
```

La escalera es:
1. **Diseñador → Constructor** (mentalidad + herramientas)
2. **Constructor + Vibe Coding** (velocidad de materialización)
3. **Constructor + Agentes** (capacidad multiplicada)

**El argumento de cierre — lo que la IA no va a reemplazar:**
La IA va a mejorar en gusto, en juicio estético, en generación de código. Ya lo está haciendo. Lo que no desaparece: **alguien tiene que poder responder por lo que se decidió construir**.

Jenny Wen: *"Someone still needs to be accountable for the decision. The same way that even though Claude can write all this code for you today, it is still an engineer who's accountable for: does that code actually work?"*

Esto no es un argumento de miedo. Es una oportunidad: el diseñador-constructor que entiende el criterio detrás de cada decisión, que puede explicar por qué se construyó lo que se construyó, tiene un rol que la velocidad no puede reemplazar.

**Call to action concreto:**
Tres pasos para empezar esta semana:
1. Elegí un proyecto pequeño (una pantalla, un flujo, una herramienta interna) y construílo vos con Bolt o Lovable.
2. Identificá qué parte de tu trabajo actual es repetitiva y explorá qué agente podría hacerlo.
3. Pasá de pensar "¿puedo construir esto?" a "¿qué quiero construir ahora? ¿y por qué?".

---

## 7. SLIDES CLAVE *(8 slides)*

**Slide 1 — HOOK**
*Título:* "¿Cuánto tardaste la última vez?"
*Visual:* Timeline antes/después del ciclo idea → producto. Izquierda: "semanas con handoff". Derecha: "horas con IA". Contraste visual fuerte, tipografía grande.

**Slide 2 — EL DATO QUE NADIE QUIERE VER**
*Título:* "El trabajo de diseño ya cambió"
*Visual:* Dos tortas (antes / ahora). Antes: 65% mocking, 20% pairing, 10% coordinación. Ahora: 35% mocking, 35% pairing, 15% código, 15% coordinación. Fuente: Jenny Wen, Head of Design Anthropic / ex Director Figma.
*Mensaje:* "Esto no es proyección. Es lo que ya está pasando en los equipos más avanzados."

**Slide 3 — EL PROCESO QUE MURIÓ Y EL QUE LO REEMPLAZA**
*Título:* "El proceso que te enseñaron tiene nombre. El que viene también."
*Visual:* Dos diagramas apilados. Arriba: Doble Diamante (4 bloques secuenciales, etiqueta "20 años, mundo donde construir era caro"). Abajo: Stingray (3 fases con flecha de doble sentido entre Develop y los datos, etiqueta "problemas y soluciones en paralelo"). Diferencia resaltada: SECUENCIAL vs. PARALELO.
*Nota al pie:* Stingray conserva entrevistas reales — en la fase Iterate, con usuarios subrepresentados.

**Slide 4 — EL CAMBIO DE ROL**
*Título:* "El handoff murió"
*Visual:* Diagrama simple de dos mundos. Mundo viejo: Diseñador → Specs → Dev → Producto. Mundo nuevo: Diseñador-Constructor → Producto. Flecha directa, sin intermediarios.

**Slide 5 — VIBE CODING: LAS 3 CAPAS**
*Título:* "No todo vibe coding es igual"
*Visual:* Tabla de tres filas (Layer 1, 2, 3) con columnas: Para qué / Herramientas / Señal de alerta. La fila de Layer 1 en color diferente con el texto: "El error más común: llamar a esto 'producto'."

**Slide 6 — CASO REAL**
*Título:* "Ryo Lu construyó un OS completo solo"
*Visual:* Screenshot de ryOS + foto/logo de Cursor. Cita: "Cursor changed everything for designers. I went from sketching UI to shipping a full agent OS." Dato secundario: Felix Lee y los 8,000+ diseñadores en el curso.

**Slide 7 — AGENTES: EL MULTIPLICADOR**
*Título:* "Una persona. Capacidad de equipo de 10."
*Visual:* Diagrama del modelo orquestador → agentes especializados → human-in-the-loop. En paralelo, dato: "YC W25: equipos <10 personas, $10M revenue". Cita de cierre: "It's not just designers who feel like they have to keep up with engineers. Engineers are like: How do we keep up with ourselves?" — Jenny Wen

**Slide 8 — CALL TO ACTION**
*Título:* "Empezá esta semana"
*Visual:* Tres acciones concretas numeradas, tipografía grande, fondo limpio. En el centro, el modelo mental resumido: "Imaginar → Construir → Escalar". Sin bullets extra, solo los tres pasos. Cierre: "Alguien tiene que poder responder por lo que se decide construir. Ese alguien sos vos."

---

## 8. DATOS DE SOPORTE

| Dato | Fuente |
|------|--------|
| 25% de startups YC W25 tienen 95% de código generado por IA | vibe-coding.md |
| Diseñadores pasaron de $50/hr a $150-400/hr al poder construir | vibe-coding.md |
| 8,000+ diseñadores de Google, Apple y Meta en "Vibe Coding for Designers" | vibe-coding.md |
| Agentforce: $1.4B ARR con 114% crecimiento YoY | agentes-ia.md |
| 90% de equipos de ingeniería usan herramientas IA (Jellyfish 2025, subió de 61%) | agentes-ia.md |
| Equipos YC W25 con <10 personas alcanzando $10M revenue con agentes | agentes-ia.md |
| Salesforce: proyección de fuerza laboral orquestada para 2026 | agentes-ia.md |
| **60-70% → 30-40%** del tiempo en mocking/prototyping (diseñadores avanzados) | Jenny Wen, Lenny Podcast 2026 |
| **30-40% nuevo** en pairing directo con engineers | Jenny Wen, Lenny Podcast 2026 |
| Horizonte de visión de producto: de 2-10 años → **3-6 meses** | Jenny Wen, Lenny Podcast 2026 |
| Doble Diamante: proceso secuencial de 4 fases, ~20 años de uso en design thinking | Design Council |
| Stingray: proceso paralelo de 3 fases (Train → Develop → Iterate), problemas+soluciones simultáneos | Board of Innovation, 2024-2025 |
| Koen Burghouts (VP Innovación, PepsiCo): el Doble Diamante podría ser irrelevante en 5 años en innovación corporativa | Müller vía Board of Innovation |

**Citas para usar:**
- "Cursor changed everything for designers. I went from sketching UI to shipping a full agent OS." — Ryo Lu
- "AI is raw material, not finished goods. Most people stop at the first output, rather than using it to begin." — Ryo Lu
- "Build bricks, not readymades." — Ryo Lu
- "El handoff siempre fue la principal fuente de pérdida de intención en producto." — Luigui Avila
- "La próxima ola de IA se parecerá a un equipo coordinado en lugar de un modelo único respondiendo preguntas."
- "El mejor diseñador es el que puede construir lo que imagina."
- "You as a designer actually do not have the time to make these beautiful mocks anymore." — Jenny Wen
- "It's not just designers who are feeling like we have to keep up with engineers. I think even engineers are like, 'How do we keep up with ourselves?'" — Jenny Wen
- "Someone still needs to be accountable for the decision." — Jenny Wen
- "This design process that designers have been taught — we sort of treat it as gospel. That's basically dead." — Jenny Wen
- "El Doble Diamante nos recuerda que toda innovación empieza y termina en las personas. El Stingray nos muestra que la IA puede ayudarnos a llegar más lejos y más rápido." — Michael Müller
- "La IA puede ser tu copiloto en innovación, pero nunca será el pasajero que vive el viaje." — Michael Müller
