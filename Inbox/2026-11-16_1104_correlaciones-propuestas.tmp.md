# Correlaciones propuestas — 2026-11-16

Corrida semanal de "busca correlaciones" (rutina cloud `vault-correlaciones-y-graduacion-semanal`). Confirmados 100 conceptos `estado: activo` en `Conceptos/` (4 excluidos: `gestion-del-tiempo` y `rutina-trabajo-enfocada` en `estado: borrador`; `diseno-multiinteligencia` y `criterio-transferible-vs-respuesta-memorizada` sin campo `estado`), 29 correlaciones existentes en `Correlaciones/`.

Conjunto de exclusión reconstruido con un script: 29 pares con archivo en `Correlaciones/` + 132 pares únicos ya propuestos en los 9 `Inbox/*_correlaciones-propuestas.tmp.md` pendientes (2026-08-25 a 2026-11-09, leídos íntegros vía regex) + 134 pares únicos extraídos de todo `JARVIS_LOG.md` = 183 pares únicos excluidos en total.

Mención cruzada literal: 1 candidato nuevo encontrado (`corrupcion-silenciosa-por-delegacion` → `disenador-a-constructor`, mencionado explícitamente en el cuerpo del primero). Señal de ≥3 tags compartidos sobre los 100 conceptos activos: 179 pares no excluidos, todos con exactamente 3 tags compartidos (ninguno con 4 o 5). Como el empate en número de tags no distingue dentro del tier, se diversificó la selección (máximo 2 apariciones por concepto) para evitar que un solo concepto con tags genéricos (`arnes-del-agente`) dominara los 19 cupos restantes solo por orden alfabético. Completados los 20 candidatos: 1 por mención cruzada + 19 por tags compartidos.

Sobrevivientes autocrítica adversarial: **5 de 20**
Descartados: **15**

Pares descartados y razón:
- `corrupcion-silenciosa-por-delegacion`×`disenador-a-constructor`: la propia prosa de `corrupcion-silenciosa-por-delegacion` ya desarrolla la tensión con el modelo diseñador-constructor ("el criterio humano está siendo aplicado sobre una base que ya no es fiel al original") — síntesis ya resuelta en el cuerpo del primer concepto (criterio 2).
- `arnes-del-agente`×`disenador-a-constructor`: la tensión plausible (construir rápido vs. calibrar el arnés continuamente) se superpone con el límite ya declarado por `disenador-a-constructor` sobre profundidad técnica ("construir un MVP no es lo mismo que construir a escala") y con la propia sección de tensión de `arnes-del-agente` sobre calibración continua — insuficiente especificidad nueva (criterio 2).
- `arnes-del-agente`×`diseno-dos-velocidades`: la distinción modo-ejecución/modo-visión de `diseno-dos-velocidades` ya cubre en abstracto cualquier trabajo que requiera dos velocidades distintas; aplicarla al arnés es una instancia más del mismo marco, no una tensión nueva (criterio 2).
- `arquitectura-de-confianza`×`de-usuario-a-cliente-servido`: ambos citan la misma fuente (Brugnoli) y llegan al mismo reencuadre — el estándar de calidad pasa de usabilidad a confianza/calidad-de-colaboración — sin tensión entre sí, solo la misma tesis vista dos veces (criterio 1).
- `arquitectura-de-inteligencia`×`ia-sin-ecosistema`: ambos diagnostican "qué falta para que la IA genere valor" desde altitudes distintas (estructuración individual del conocimiento vs. activos complementarios organizacionales) sin contradicción real entre sí — co-ocurrencia complementaria, no tensión (criterio 1).
- `autoautomatizacion-del-disenador`×`deuda-cognitiva-organizacional`: el segundo es explícitamente el primero multiplicado a escala organizacional ("distributed de-skilling" de BCG es la misma mecánica agregada); la síntesis es obvia para quien leyó ambos por separado (criterio 2).
- `cambio-como-estado-permanente`×`feedback-que-escala`: tensión real (codificar criterio en el sistema asume una ventana de estabilidad que el cambio permanente niega) pero de menor especificidad que la seleccionada entre `cambio-como-estado-permanente` y `gobernanza-ia-performativa` — esta última nombra un mecanismo causal concreto en vez de una advertencia general ya cubierta por la propia sección de tensión de `feedback-que-escala` sobre sistematizar demasiado pronto.
- `capas-de-profundidad-sistemica`×`granularidad-como-decision-de-mapeo`: convergen en la misma conclusión meta (el detalle/profundidad mal elegido produce mapas inútiles) sin síntesis nueva — mismo patrón de descarte que pares equivalentes en la corrida del 2026-11-02 (criterio 2).
- `capital-de-contexto`×`cuello-de-botella-del-flujo`: la advertencia posible (invertir en un hoard de contexto para un paso que no es el cuello de botella es esfuerzo desperdiciado) es una aplicación genérica del criterio de `cuello-de-botella-del-flujo` a cualquier inversión, no una tensión específica entre ambos conceptos — insuficiente especificidad frente a la seleccionada entre `autoautomatizacion-del-disenador` y `cuello-de-botella-del-flujo`.
- `claridad-antes-de-velocidad`×`gobernanza-ia-performativa`: la gobernanza performativa es un ejemplo del principio general de `claridad-antes-de-velocidad` (velocidad sin estándar de calidad definido), no una tensión entre dos fuerzas distintas — relación de "ejemplifica", no de tensión (criterio 1).
- `claridad-antes-de-velocidad`×`ia-sin-ecosistema`: complementariedad esperada (ambos son condiciones necesarias pero distintas para que la IA genere valor); alguien que leyó los dos por separado ya concluye que se necesitan ambas sin que la correlación agregue un mecanismo nuevo (criterio 2).
- `comprehension-debt`×`diseno-dos-velocidades`: el costo adicional posible (deuda de comprensión, no solo pérdida de influencia estratégica, en modo-ejecución) se superpone con la propia advertencia de `diseno-dos-velocidades` sobre el costo de quedarse solo en ese modo — variación de un punto ya señalado, insuficiente novedad.
- `condicion-redespliegue`×`feedback-que-escala`: aplica el marco punctual/sistémico de `feedback-que-escala` a la pregunta de quién posee el redespliegue — observación razonable pero de menor especificidad e impacto que la seleccionada entre `condicion-redespliegue` e `ia-como-filtro-de-entrada`, que aporta evidencia empírica concreta de por qué el redespliegue falla estructuralmente para una cohorte específica.
- `conocimiento-autoorganizado-por-llm`×`design-system-como-api-para-agentes`: el segundo es una instancia concreta de la postura "arquitectura con intención humana" que el primero ya contrasta explícitamente contra el enfoque de Karpathy — refuerza un lado de un debate ya planteado, no genera tensión nueva (criterio 2).
- `conocimiento-autoorganizado-por-llm`×`expertise-de-dominio-en-producto`: `conocimiento-autoorganizado-por-llm` ya advierte en su propia sección de tensión que el LLM Wiki "puede volverse un compendio de información bien estructurada pero no necesariamente correcta o valiosa" — la misma advertencia que `expertise-de-dominio-en-producto` hace desde el otro lado (agente confiado sin juicio real), síntesis ya resuelta (criterio 2).

---

## 1. La gobernanza de IA se queda performativa porque se diseña como proyecto, no como estado

**Par:** `cambio-como-estado-permanente` × `gobernanza-ia-performativa`

**Señales:** 3 tags compartidos (`ia`, `organizacion`, `cambio`) — sin conexión previa en `relacionado` ni mención cruzada en los cuerpos.

**Justificación de la tensión real (1 línea):** `gobernanza-ia-performativa` mide la brecha entre política declarada y enforcement real como un problema de subinversión, sin nombrar nunca que escribir una política es tratar el riesgo de IA como un proyecto con fecha de término — exactamente el error que `cambio-como-estado-permanente` dice que vuelve obsoleto cualquier rollout antes de que termine.

---

```yaml
---
titulo: "La gobernanza de IA se queda performativa porque se diseña como proyecto, no como estado"
tipo: correlacion
conceptos: [cambio-como-estado-permanente, gobernanza-ia-performativa]
fecha: 2026-11-16
tags: [ia, organizacion, cambio, tension, no-leido]
estado: borrador
---
```

# La gobernanza de IA se queda performativa porque se diseña como proyecto, no como estado

## La tensión

`gobernanza-ia-performativa` documenta la brecha entre las capas visibles de control (política, comité de ética, declaración de principios) y las capas que realmente hacen cumplir esas reglas (proceso, sistema): 56% de organizaciones dice tener gobernanza comprensiva, solo 12% la tiene implementada en práctica. El concepto trata esa brecha como un problema de dónde invierte la organización — las capas visibles son rápidas de construir, las invisibles son lentas y costosas. `cambio-como-estado-permanente` describe un mecanismo distinto: el toolkit clásico de gestión del cambio asume un estado A, una intervención, y un estado B estable — y ese supuesto se rompe cuando el cambio deja de ser un evento y se vuelve el modo normal de operación. Los modelos mejoran en ciclos de semanas; los competidores reconfiguran expectativas antes de que termine el rollout anterior.

## El insight no obvio

Una política de gobernanza de IA es, por diseño, un artefacto de proyecto: se redacta, se ratifica, se declara "lista". Es exactamente la forma que `cambio-como-estado-permanente` dice que ya no funciona — un estado B al que se llega y en el que se puede operar con normalidad. El problema no es solo que las capas de proceso y sistema sean más lentas y caras de construir, como dice `gobernanza-ia-performativa` — es que incluso si se construyeran, quedarían obsoletas al ritmo en que el propio `cambio-como-estado-permanente` documenta que las capacidades de los agentes se expanden: en ciclos de semanas, más rápido que cualquier ciclo de revisión de política. La gobernanza se queda atrapada en las capas 1 y 2 (política, modelo operativo) no solo por falta de inversión, sino porque esas son las únicas capas que un marco de gestión de cambio episódico sabe producir: un documento, un comité, una fecha de "listo". Las capas 3 y 4 (proceso, sistema) exigen exactamente la competencia que `cambio-como-estado-permanente` dice que las organizaciones todavía no han desarrollado — operar dentro del movimiento, no gestionar una transición hacia la estabilidad. La gobernanza performativa no es un fallo de ejecución sobre un plan correcto: es el output esperado de aplicar herramientas de proyecto a un problema que ya no tiene forma de proyecto.

## El límite

No todo caso de gobernanza performativa se explica por inmadurez en gestión del cambio: `gobernanza-ia-performativa` nombra explícitamente organizaciones que construyen compliance cosmético de forma deliberada como decisión consciente de riesgo, lo cual no tiene relación con el marco de cambio permanente. Tampoco migrar la gobernanza a un modelo "continuo" garantiza que deje de ser performativa — la propia sección de tensión de `cambio-como-estado-permanente` advierte que el cambio permanente erosiona las condiciones de estandarización que la calidad operacional requiere; una gobernanza diseñada para moverse constantemente podría volverse tan inestable como la tecnología que intenta gobernar, sin ganar enforcement real en el proceso.

---

## 2. La condición del redespliegue asume una escalera que el filtro de entrada ya desmontó

**Par:** `condicion-redespliegue` × `ia-como-filtro-de-entrada`

**Señales:** 3 tags compartidos (`ia`, `automatizacion`, `transicion`) — sin conexión previa en `relacionado` ni mención cruzada en los cuerpos.

**Justificación de la tensión real (1 línea):** `condicion-redespliegue` asume que existe trabajo de mayor valor disponible al que redirigir la capacidad liberada por automatización, pero `ia-como-filtro-de-entrada` muestra que para la cohorte junior ese trabajo de mayor valor es precisamente la categoría que la misma ola de automatización está eliminando.

---

```yaml
---
titulo: "La condición del redespliegue asume una escalera que el filtro de entrada ya desmontó"
tipo: correlacion
conceptos: [condicion-redespliegue, ia-como-filtro-de-entrada]
fecha: 2026-11-16
tags: [ia, automatizacion, transicion, tension, no-leido]
estado: borrador
---
```

# La condición del redespliegue asume una escalera que el filtro de entrada ya desmontó

## La tensión

`condicion-redespliegue` argumenta que el valor económico de la automatización no es automático: requiere que la organización rediseñe roles y redirija activamente las horas liberadas a trabajo de mayor valor. Sin ese redespliegue intencional, el resultado es capacidad ociosa o reducción de headcount — y el concepto señala que ninguna función organizacional estándar tiene esa pregunta como responsabilidad propia. `ia-como-filtro-de-entrada` documenta un mecanismo distinto y medido: la IA no destruye empleo de forma uniforme, cierra específicamente la puerta de entrada — automatiza las tareas rutinarias que antes servían de rampa de aprendizaje para quien recién empieza (-16% en empleo relativo para 22-25 años, -35% en postings entry-level, -25% en contratación junior en grandes tech).

## El insight no obvio

`condicion-redespliegue` trata la ausencia de destino para la capacidad liberada como un problema de diseño organizacional resoluble — "si una organización... no asigna nuevo trabajo de mayor valor... el resultado es capacidad ociosa." Para la cohorte junior específicamente, `ia-como-filtro-de-entrada` muestra que el problema no es solo que nadie asigne ese trabajo de mayor valor: es que el trabajo de mayor valor al que un junior se redespliega tradicionalmente — las tareas formativas de aprender haciendo — es la misma categoría que la IA está eliminando como "filtro de entrada". No hay una escalera intacta esperando del otro lado del redespliegue; la escalera y la tarea automatizada son, en este caso, la misma estructura. El propio límite que `condicion-redespliegue` declara como hipótesis general ("el redespliegue puede no ser posible para todos los roles... no siempre hay un trabajo de mayor valor disponible") es exactamente el patrón que `ia-como-filtro-de-entrada` documenta con datos como el resultado dominante y medido para una cohorte entera, no como una excepción marginal.

## El límite

`ia-como-filtro-de-entrada` reconoce en su propia sección de tensión que el efecto podría ser transitorio: si emergen categorías nuevas de trabajo entry-level (orquestación de agentes, evaluación de outputs de IA), el filtro se desplazaría en vez de eliminarse, y el destino de redespliegue que `condicion-redespliegue` necesita volvería a existir, aunque con otro contenido. Esta tensión tampoco aplica igual a la redistribución de trabajadores de nivel medio o senior, donde `condicion-redespliegue` describe casos donde el trabajo de mayor valor sí existe pero nadie lo asigna — ahí el problema sigue siendo organizacional, no estructural, como en la cohorte junior.

---

## 3. Automatizar el propio criterio apuesta a que ese paso es el cuello de botella — casi nunca lo es

**Par:** `autoautomatizacion-del-disenador` × `cuello-de-botella-del-flujo`

**Señales:** 3 tags compartidos (`ia`, `automatizacion`, `criterio`) — sin conexión previa en `relacionado` ni mención cruzada en los cuerpos.

**Justificación de la tensión real (1 línea):** el paso que un profesional más tienta delegar por completo —su propio juicio, por ser el más lento y costoso— no es necesariamente el cuello de botella real del sistema, y cuando no lo es, `autoautomatizacion-del-disenador` y `cuello-de-botella-del-flujo` dejan de ser un trade-off (más rápido pero más tonto) y se vuelven una pérdida compuesta: el mismo throughput de sistema, pagado con atrofia de criterio permanente.

---

```yaml
---
titulo: "Automatizar el propio criterio apuesta a que ese paso es el cuello de botella — casi nunca lo es"
tipo: correlacion
conceptos: [autoautomatizacion-del-disenador, cuello-de-botella-del-flujo]
fecha: 2026-11-16
tags: [ia, automatizacion, criterio, tension, no-leido]
estado: borrador
---
```

# Automatizar el propio criterio apuesta a que ese paso es el cuello de botella — casi nunca lo es

## La tensión

`autoautomatizacion-del-disenador` documenta, con el paper de HBS/BCG sobre 244 consultores, que delegar thinking + doing detiene el crecimiento de habilidades en toda dimensión — a diferencia de los "Centauros", que alternan y refuerzan su expertise. El mecanismo: cuando la IA entrega un output rápido y limpio, el cerebro registra la tarea como completada y el circuito de fricción-error-corrección que construye criterio nunca se activa. `cuello-de-botella-del-flujo` establece un criterio de despliegue distinto: automatizar cualquier paso que no sea el cuello de botella del sistema no mejora el throughput total, aunque el modelo lo haga excelente — el caso GitHub Copilot lo muestra con datos: código 55% más rápido, pero el ciclo commit-to-producción no acelera porque el paso limitante era la revisión, no la escritura.

## El insight no obvio

El paso que un profesional más tienta delegar por completo es, casi por definición, el que más fricción personal le genera — y la fricción personal se siente como el cuello de botella, aunque no lo sea a nivel de sistema. `autoautomatizacion-del-disenador` describe el costo de automatizar juicio: atrofia permanente, confirmada como cero crecimiento en los datos de BCG. `cuello-de-botella-del-flujo` describe, independientemente, que automatizar un paso que no es el limitante no mueve el throughput — produce "teatro de capacidad", como el +98% de PRs con +91% de tiempo de revisión que el propio concepto documenta. Unidos: cuando el paso de juicio que alguien automatiza no es, de hecho, el cuello de botella del sistema (la aprobación, la revisión, la decisión de otro nivel sigue siendo el límite real), la operación no es un trade-off de "más rápido pero con peor criterio a futuro" — es una pérdida compuesta donde ninguno de los dos beneficios aparece: el sistema no es más rápido (el cuello de botella sigue en otro lado) y el profesional sí es permanentemente menos capaz. Ninguno de los dos conceptos nombra esta combinación: `autoautomatizacion-del-disenador` mide el costo individual sin preguntar si la tarea delegada era sistémicamente relevante; `cuello-de-botella-del-flujo` mide el throughput del sistema sin considerar el costo de capacidad que paga la persona que automatizó el paso equivocado.

## El límite

La pérdida compuesta depende de que el paso de juicio delegado no sea, en efecto, el cuello de botella real. Si lo es — por ejemplo, un practicante independiente donde su propio juicio es literalmente el límite de producción del sistema completo — automatizarlo sí puede entregar la ganancia de throughput que `cuello-de-botella-del-flujo` predice, aunque siga pagando el costo de atrofia que documenta `autoautomatizacion-del-disenador`; en ese caso los dos conceptos se mantienen en trade-off, no en pérdida compuesta. Diagnosticar cuál de los dos casos aplica exige exactamente el análisis de sistema que `cuello-de-botella-del-flujo` pide — un análisis que, por sí solo, no protege contra el costo individual que mide el otro concepto.

---

## 4. El capital de contexto puede ser comprehension debt con mejor empaque

**Par:** `capital-de-contexto` × `comprehension-debt`

**Señales:** 3 tags compartidos (`ia`, `conocimiento`, `criterio`) — sin conexión previa en `relacionado` ni mención cruzada en los cuerpos.

**Justificación de la tensión real (1 línea):** `capital-de-contexto` promete que el hoard de prompts y precedentes compone y no decae, pero esa promesa depende de que cada entrada llevara comprensión humana genuina al momento de agregarse — exactamente la condición que `comprehension-debt` muestra que se puede saltar sin que nadie lo note, porque el output pasa el gate de revisión aunque nadie lo haya entendido de verdad.

---

```yaml
---
titulo: "El capital de contexto puede ser comprehension debt con mejor empaque"
tipo: correlacion
conceptos: [capital-de-contexto, comprehension-debt]
fecha: 2026-11-16
tags: [ia, conocimiento, criterio, tension, no-leido]
estado: borrador
---
```

# El capital de contexto puede ser comprehension debt con mejor empaque

## La tensión

`capital-de-contexto` describe el "hoard" — prompts, cadenas de razonamiento probadas, contexto acumulado — como un activo que compone y no decae: cada ejemplo "incluye trazabilidad de por qué funcionó", y el *context graph* es "un registro vivo de decisiones reales... no solo documenta qué ocurrió, sino por qué fue permitido ocurrir". `comprehension-debt` documenta que el volumen de artefactos generados por IA puede crecer mientras la comprensión genuina de un equipo sobre ellos se queda atrás — en el RCT de Anthropic, ingenieros asistidos por IA completaron la tarea en tiempo similar pero obtuvieron 17% menos en el quiz de comprensión posterior. El código se ve limpio, los tests pasan, y el ajuste de cuentas llega en silencio.

## El insight no obvio

La trazabilidad que `capital-de-contexto` exige para un hoard maduro — "cada ejemplo incluye trazabilidad de por qué funcionó" — se puede llenar con una explicación plausible sin que nadie del equipo haya verificado genuinamente que esa explicación es correcta. Es la misma brecha que mide `comprehension-debt`: el output pasa el gate de aprobación (el prompt funcionó, el documento se ve bien, el campo "por qué funcionó" tiene texto) sin que eso implique comprensión real. Bajo esta lectura, un hoard puede crecer en volumen y sofisticación aparente — más entradas en el context graph, más precedentes documentados — mientras su confiabilidad real declina, que es la inversión exacta de la promesa central de `capital-de-contexto`: que el capital compone y no decae. La comprehension debt es invisible en el hoard por el mismo mecanismo que es invisible en el código: cada entrada pasó su propio gate en el momento en que se agregó. Lo que `capital-de-contexto` vende como un moat difícil de replicar "porque tardó meses en construirse" puede ser difícil de replicar por la razón equivocada — no porque codifique juicio real, sino porque separar qué entradas están genuinamente validadas de las que se aceptaron por fe toma tanto tiempo como construir el hoard en primer lugar.

## El límite

Esto no es un defecto inherente a la estrategia de acumular contexto — `capital-de-contexto` ya declara límites propios (portabilidad entre modelos, mal ajuste para tareas creativas divergentes) que son independientes de este riesgo. Un equipo que aplique antes de agregar al hoard la misma disciplina que `comprehension-debt` identifica como la única mitigación validada ("rewrite before commit": reescribir y comprender antes de aceptar) construiría un hoard en gran medida inmune a esta tensión. La correlación describe un riesgo condicional a la curación descuidada, no una falla necesaria del concepto de capital de contexto en sí.

---

## 5. La arquitectura de inteligencia es el activo que la comoditización no puede tocar

**Par:** `arquitectura-de-inteligencia` × `inteligencia-como-utilidad`

**Señales:** 3 tags compartidos (`ia`, `estrategia`, `sistemas`) — sin conexión previa en `relacionado` ni mención cruzada en los cuerpos.

**Justificación de la tensión real (1 línea):** `inteligencia-como-utilidad` nombra "el arnés y el contexto" como los lugares donde migra el valor cuando el modelo se comoditiza, pero no explica cómo se construye ese contexto con calidad en vez de ruido — `arquitectura-de-inteligencia` aporta exactamente ese mecanismo, y al unirlos, hacer bien la estructuración deliberada del conocimiento deja de ser solo buena práctica de diseño y se vuelve la forma de producir el único activo económico que sobrevive a la comoditización.

---

```yaml
---
titulo: "La arquitectura de inteligencia es el activo que la comoditización no puede tocar"
tipo: correlacion
conceptos: [arquitectura-de-inteligencia, inteligencia-como-utilidad]
fecha: 2026-11-16
tags: [ia, estrategia, conocimiento, tension, no-leido]
estado: borrador
---
```

# La arquitectura de inteligencia es el activo que la comoditización no puede tocar

## La tensión

`arquitectura-de-inteligencia` argumenta que el trabajo real del diseñador es estructurar deliberadamente cómo el conocimiento fluye y se activa en un sistema humano u organizacional — y que sin esa arquitectura intencional, "el AI devuelve estructura superficial... que no reflejan los modelos mentales de quien los necesita". `inteligencia-como-utilidad` describe cómo la inferencia de LLM colapsa en precio (99.7% en tres años) y se convierte en utilidad, exactamente como pasó con la electricidad o el cómputo en la nube — y que cuando el modelo es la utilidad, "el valor migra hacia las capas que el builder no diseñó para competir: el arnés y el contexto".

## El insight no obvio

`inteligencia-como-utilidad` nombra el capital de contexto como el diferenciador que sobrevive a la comoditización del modelo, pero no explica el mecanismo por el cual ese contexto se construye con calidad real en vez de acumularse como ruido estructurado. `arquitectura-de-inteligencia` provee exactamente ese mecanismo: la estructuración deliberada y humana de cómo el conocimiento se organiza y se activa — el trabajo que, según Arango, el AI no puede hacer por sí solo sin producir estructura superficial. Unidos, el argumento se reencuadra: hacer arquitectura de inteligencia bien no es una práctica epistémica recomendable que además ayuda con la IA — es, bajo la lente económica de `inteligencia-como-utilidad`, el proceso de producción del único activo del stack que no se comoditiza. Saltarse ese trabajo no solo produce la "estructura superficial" que `arquitectura-de-inteligencia` critica en términos de calidad de conocimiento — significa no construir la única capa del stack donde, según `inteligencia-como-utilidad`, todavía queda margen.

## El límite

`inteligencia-como-utilidad` advierte en su propia sección de tensión que el arnés puede convertirse en mecanismo de lock-in invertido si se construye sobre la infraestructura propietaria de un proveedor en vez de un estándar abierto (MCP). Esto limita la síntesis: el trabajo de arquitectura de inteligencia solo se convierte en el moat duradero que describe `inteligencia-como-utilidad` si se construye sobre infraestructura que el builder realmente controla. Estructurar el conocimiento deliberadamente dentro de un arnés controlado por un proveedor externo puede seguir evaporándose como ventaja competitiva si ese proveedor cambia los términos — sin importar cuán bien diseñada esté la arquitectura de información en sí misma.
