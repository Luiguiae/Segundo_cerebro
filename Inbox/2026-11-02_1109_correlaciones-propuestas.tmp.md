# Correlaciones propuestas — 2026-11-02

Corrida semanal de "busca correlaciones" (rutina cloud `vault-correlaciones-y-graduacion-semanal`). Continuación directa de la corrida anterior (2026-10-26): mención cruzada literal sigue agotada (72/72 excluidos desde esa corrida), así que se continuó con la señal de tags compartidos (≥2), priorizando primero los pares con 4 tags compartidos y completando hasta 20 con pares de 3 tags.

Conjunto de exclusión reconstruido: 29 pares con archivo en `Correlaciones/` + 15 pares ya propuestos en los 7 `Inbox/*_correlaciones-propuestas.tmp.md` pendientes (2026-08-25, 08-31, 09-07, 09-21, 09-28, 09-30, 10-26 — leídos íntegros, ninguno se repite aquí) + 82 pares únicos descartados explícitamente en corridas anteriores (extraídos de todo `JARVIS_LOG.md` desde 2026-08-25) = 123 pares únicos excluidos. Sobre 100 conceptos `estado: activo` (104 totales − 2 `borrador` − 2 sin campo `estado`), quedan **1.267 pares** con ≥2 tags compartidos sin excluir.

Sobrevivientes autocrítica adversarial: **5 de 20**
Descartados: **15**

Pares descartados y razón:
- `agencia-humana-como-imperativo-ux`×`ux-checkpoints`, `arquitectura-de-confianza`×`ux-checkpoints`: ya conectados en `relacionado`; ambos vienen de la misma fuente (Brugnoli) y describen el mismo mecanismo de checkpoints desde ángulos adyacentes, no una tensión real (criterio 1).
- `ia-como-filtro-de-entrada`×`automatizacion-vs-ampliacion`: ya conectados en `relacionado`; `automatizacion-vs-ampliacion` reutiliza el mismo dato de Stanford (−16% empleo junior) que `ia-como-filtro-de-entrada` — es la misma evidencia vista desde el mismo ángulo, no síntesis nueva (criterio 2).
- `arnes-del-agente`×`las-tres-caras-del-producto-agentico`: ya conectados en `relacionado`; "Cara 1" del segundo concepto ya define explícitamente "diseñar el arnés" — síntesis resuelta en la propia prosa (criterio 2).
- `arnes-del-agente`×`metricas-post-pantalla`: la tensión (más guardrails bajan el Action Advancement score) es real pero de baja novedad — cualquiera que conozca ambos conceptos la infiere sin esfuerzo (criterio 2, versión débil).
- `legibilidad-de-maquina`×`web-bifurcada`: ya conectados en `relacionado`; `web-bifurcada` es una instanciación concreta de `legibilidad-de-maquina`, no un concepto independiente que tensione con él (criterio 1).
- `legibilidad-de-maquina`×`las-tres-caras-del-producto-agentico`: ya conectados en `relacionado`; "Cara 2" del segundo concepto define legibilidad de máquina casi textualmente — síntesis resuelta en la propia prosa (criterio 2).
- `disenador-a-constructor`×`diseno-dos-velocidades`: ya conectados en `relacionado`; el segundo concepto usa al primero como premisa explícita y ya integra la relación en su propio texto (criterio 2).
- `disenador-a-constructor`×`diseno-uxui-y-ia`: ya conectados en `relacionado`; el segundo es una instanciación del primero en el dominio UX, sin tensión propia (criterio 1).
- `diseno-dos-velocidades`×`diseno-uxui-y-ia`: describen el mismo desplazamiento (producción→juicio) en framings distintos, sin contradicción real entre ambos — co-ocurrencia, no tensión (criterio 1).
- `diseno-dos-velocidades`×`el-moat-del-gusto`: la síntesis posible (tiempo protegido vs. agencia/coraje son necesarios-pero-no-suficientes por separado) es genérica y aplicable a casi cualquier par concepto-organizacional/concepto-individual — insuficientemente específica a estos dos textos.
- `diseno-sistemico-como-cambio-de-alcance`×`granularidad-como-decision-de-mapeo`: ambos textos ya convergen en la misma conclusión meta ("la elección de alcance/resolución no es neutral, revela sesgos de quien mapea") — leído uno, el punto del otro ya está dado (criterio 2). Se prefirió la pareja con `capas-de-profundidad-sistemica` (sobreviviente #3), que aporta un eje genuinamente distinto (profundidad, no solo resolución).
- `diseno-uxui-y-ia`×`el-moat-del-gusto`: la sección de tensión de `diseno-uxui-y-ia` ya menciona "pierde agencia cultural" al aceptar outputs sin criterio — adelanta la tesis central de `el-moat-del-gusto` (agencia como moat, no el gusto) sin necesitar el segundo texto (criterio 2).
- `metacognicion-del-disenador`×`granularidad-como-decision-de-mapeo`: ambos reformulan el mismo principio ("saber qué ignorar/no saber es la habilidad, no saberlo todo") en dos dominios distintos — misma conclusión, sin síntesis nueva (criterio 2). Se prefirió la pareja con `lo-ilegible-como-senal` (sobreviviente #5), que sí produce una prescripción contradictoria entre ambos conceptos.

Quedan **1.247 pares** candidatos por tags sin evaluar (1.267 − 20), disponibles para la próxima corrida semanal.

---

## 1. Escapar el riesgo geopolítico del modelo te lleva al terreno sin rieles de seguridad

**Par:** `riesgo-geopolitico-del-modelo` × `seguridad-asimetrica-de-modelos-abiertos`

**Señales:** ≥2 tags compartidos (4: `estrategia`, `etica`, `gobernanza-ia`, `ia`) — conexión unidireccional ya existente (`seguridad-asimetrica-de-modelos-abiertos.relacionado` incluye a `riesgo-geopolitico-del-modelo`, pero no hay archivo de correlación ni síntesis explícita entre ambos en ningún cuerpo).

**Justificación de la tensión real (1 línea):** la salida que `riesgo-geopolitico-del-modelo` sugiere para evitar la revocación estatal de un modelo cerrado (migrar a open-weight) es exactamente el terreno sin alineación que `seguridad-asimetrica-de-modelos-abiertos` muestra que usan los atacantes sin restricción — control político y control de seguridad se mueven en direcciones opuestas sobre el mismo continuo cerrado-abierto, y ningún texto lo nombra.

---

```yaml
---
titulo: "Escapar el riesgo geopolítico del modelo te lleva al terreno sin rieles de seguridad"
tipo: correlacion
conceptos: [riesgo-geopolitico-del-modelo, seguridad-asimetrica-de-modelos-abiertos]
fecha: 2026-11-02
tags: [ia, gobernanza-ia, estrategia, tension, no-leido]
estado: borrador
---
```

# Escapar el riesgo geopolítico del modelo te lleva al terreno sin rieles de seguridad

## La tensión

`riesgo-geopolitico-del-modelo` documenta que depender de un modelo frontier cerrado es una apuesta política: el gobierno puede revocar el acceso en horas sin falla técnica del modelo, como ocurrió con Fable 5 y Mythos 5 en junio de 2026 (suspendidos a las 72 horas de su lanzamiento). El propio concepto señala la respuesta institucional emergente — "geopatriation", migrar hacia modelos open-weight no sujetos a controles de exportación (ECCN 4E091) — como una vía razonable para reducir esa exposición. `seguridad-asimetrica-de-modelos-abiertos` muestra el costo oculto de exactamente esa salida: los modelos open-weight sin restricciones (DeepSeek, GLM-5.2, Kimi K3, Qwen) son el mismo terreno donde operan, sin fricción alguna, los atacantes que los controles de alineación de los modelos cerrados sí bloquean. El caso Unit 42 (julio 2026) lo prueba de forma literal: un actor fue bloqueado al intentar usar Claude Code y Codex, y migró sin pérdida de capacidad a DeepSeek vía un framework abierto, comprometiendo más de 460 sistemas sin intervención humana. Huir del riesgo político del modelo cerrado significa entrar al único espacio donde no hay rieles de seguridad.

## El insight no obvio

Leídos juntos, los dos conceptos revelan que no existe una combinación "segura" entre control político y control de seguridad: son dos ejes que se mueven en direcciones opuestas sobre el mismo continuo modelo-cerrado-a-abierto. El modelo cerrado da seguridad de alineación (rechaza payloads de ataque, aunque también rechace a defensores legítimos — el "impuesto de alineación" que el propio concepto de seguridad asimétrica cuantifica en 2.72×) pero cuesta soberanía política: puede ser revocado por decreto sin aviso. El modelo abierto da soberanía política — nadie puede revocarlo — pero cuesta seguridad de alineación: no rechaza nada, ni a ti ni a tu atacante. Migrar de uno a otro no resuelve el riesgo, lo transforma en otro de naturaleza distinta. Ninguno de los dos conceptos, por separado, nombra esta relación inversa: `riesgo-geopolitico-del-modelo` presenta el open-weight como "alternativa" sin mencionar el costo de seguridad que acarrea; `seguridad-asimetrica-de-modelos-abiertos` presenta el acceso irrestricto del atacante como un problema de diseño de alineación, sin conectarlo con la razón estructural por la que cada vez más actores —legítimos y no— migran hacia ese terreno: la huida del riesgo geopolítico del modelo cerrado.

## El límite

La tensión se resuelve parcialmente con los programas de acceso verificado que `seguridad-asimetrica-de-modelos-abiertos` documenta — el Cyber Verification Program de Anthropic, "Trusted Access for Cyber" de OpenAI —, que dan seguridad de alineación a defensores sin el rechazo ciego que castiga por igual a quien ataca y a quien responde a un incidente. Pero esos programas no resuelven el riesgo geopolítico: siguen dependiendo del mismo proveedor cerrado, sujeto a las mismas directivas gubernamentales que suspendieron Fable 5 en 72 horas. Un actor que busca evadir ambos riesgos simultáneamente no tiene opción disponible hoy — solo puede elegir cuál de los dos costos prefiere absorber.

---

## 2. La transparencia que genera confianza puede ser la misma rendición cognitiva que evita

**Par:** `arquitectura-de-confianza` × `soberania-epistemica`

**Señales:** 3 tags compartidos (`agentes`, `diseño`, `ux`) — sin conexión previa en `relacionado` ni mención cruzada en los cuerpos.

**Justificación de la tensión real (1 línea):** la transparencia de proceso que `arquitectura-de-confianza` prescribe para construir confianza (mostrar el "black box" de forma legible) puede ser consumida por el Sistema 1 exactamente igual que una respuesta opaca, produciendo el mismo cierre cognitivo prematuro que `soberania-epistemica` documenta como rendición de agencia — ver cómo opera un sistema no es lo mismo que evaluarlo críticamente, y ninguno de los dos textos distingue entre ambos.

---

```yaml
---
titulo: "La transparencia que genera confianza puede ser la misma rendición cognitiva que evita"
tipo: correlacion
conceptos: [arquitectura-de-confianza, soberania-epistemica]
fecha: 2026-11-02
tags: [diseño, ux, confianza, tension, no-leido]
estado: borrador
---
```

# La transparencia que genera confianza puede ser la misma rendición cognitiva que evita

## La tensión

`arquitectura-de-confianza` prescribe la transparencia de proceso como mecanismo central para construir confianza en sistemas autónomos: Waymo convierte su "black box" en experiencia legible en tiempo real, y eso genera seguridad en el pasajero. `soberania-epistemica` documenta el mecanismo inverso para interfaces fluidas: aunque sean transparentes, si entregan la explicación directamente al Sistema 1 (heurístico, automático) sin activar el Sistema 2 (analítico, deliberado), producen cierre cognitivo prematuro — el usuario acepta porque evaluar cuesta más de lo que vale, no porque haya evaluado. Las dos prescripciones pueden colisionar en el mismo diseño: una visualización legible y fluida de "por qué el agente hizo esto" genera exactamente la confianza que `arquitectura-de-confianza` busca, precisamente porque es fácil de consumir — y esa facilidad de consumo es el mecanismo exacto que `soberania-epistemica` identifica como rendición de agencia cognitiva.

## El insight no obvio

La transparencia de proceso, diseñada para construir confianza, puede ser consumida por el Sistema 1 exactamente igual que una respuesta opaca: el usuario "ve" la explicación sin evaluarla, y la sensación de estar informado sustituye al acto de pensar. `arquitectura-de-confianza` no distingue entre transparencia que invita a evaluación crítica y transparencia que solo invita a sentirse cómodo — trata ambas como la misma victoria de diseño. `soberania-epistemica` sí nombra esa distinción en abstracto (fricción deseable vs. fricción accidental) pero no la aplica al caso específico de la transparencia-como-mecanismo-de-confianza: su ejemplo de referencia (checkpoints) ya asume fricción explícita, no transparencia fluida como la de Waymo. Juntos revelan que el estándar de calidad de diseño en sistemas agénticos no es uno sino dos — confianza vs. comprensión — y pueden apuntar en direcciones opuestas: un sistema puede ser perfectamente confiable y transparente y seguir produciendo rendición cognitiva en quien lo opera.

## El límite

No toda transparencia fluida es rendición: en contextos de bajo riesgo o alta repetición (confirmar un pedido simple), exigir fricción epistémica constante sería el mismo error que `ux-checkpoints` ya describe como "fricción sin valor, que erosiona la confianza en lugar de construirla". La distinción depende de la reversibilidad y del costo de evaluación, igual que en `agencia-humana-como-imperativo-ux`. El límite real de esta correlación es que ninguno de los dos conceptos ofrece todavía un criterio operativo para diseñar transparencia que informe sin producir cierre cognitivo prematuro — ambos señalan el problema desde direcciones opuestas sin resolverlo.

---

## 3. Ampliar el alcance y profundizar las capas compiten por el mismo presupuesto de atención

**Par:** `diseno-sistemico-como-cambio-de-alcance` × `capas-de-profundidad-sistemica`

**Señales:** 3 tags compartidos (`diseño`, `marco`, `sistemas`) — misma fecha de creación (2026-08-21), sin conexión previa en `relacionado`.

**Justificación de la tensión real (1 línea):** los dos conceptos definen la ambición del trabajo sistémico en ejes distintos e independientes —alcance (cuánto ciclo de vida cubrir) y profundidad (hasta qué capa excavar)— que compiten por el mismo tiempo y capital político finito de un proyecto, y la mayoría de los proyectos extienden uno sin notar que están dejando el otro superficial.

---

```yaml
---
titulo: "Ampliar el alcance y profundizar las capas compiten por el mismo presupuesto de atención"
tipo: correlacion
conceptos: [diseno-sistemico-como-cambio-de-alcance, capas-de-profundidad-sistemica]
fecha: 2026-11-02
tags: [diseño, sistemas, marco, tension, no-leido]
estado: borrador
---
```

# Ampliar el alcance y profundizar las capas compiten por el mismo presupuesto de atención

## La tensión

`diseno-sistemico-como-cambio-de-alcance` define el trabajo sistémico como extender el alcance: cubrir todo el ciclo de vida, los efectos secundarios, los actores fuera del encargo original — la pregunta es "¿hasta dónde llega esto?". `capas-de-profundidad-sistemica` define el mismo trabajo como profundizar: moverse de la capa material visible hacia las capas sociotécnicas y socioculturales donde viven las causas que se resisten a la solución técnica. Son dos ejes de ambición sistémica —qué tan ancho, qué tan profundo— que compiten por el mismo recurso escaso: el tiempo y el capital político que un equipo de diseño tiene disponible para un proyecto. Ninguno de los dos conceptos, leído por separado, nombra que son ejes independientes que no pueden maximizarse simultáneamente con recursos finitos.

## El insight no obvio

La mayoría de los proyectos de diseño sistémico eligen, sin decidirlo explícitamente, extender uno de los dos ejes y dejar el otro superficial. Un proyecto puede mapear el ciclo de vida completo de un servicio (alcance amplio) sin tocar nunca las capas socioculturales que explican por qué el sistema actual existe así (profundidad baja) — y eso se siente como rigor sistémico sin serlo. Simétricamente, un proyecto puede excavar hasta las narrativas de poder detrás de un solo punto de contacto (profundidad alta) sin considerar cómo ese punto se conecta con el resto del ciclo de vida (alcance bajo). El punto ciego que ninguno de los dos documentos nombra: la decisión de qué eje extender rara vez es deliberada — depende de qué eje es más visible o más defendible ante el cliente, no de dónde está realmente el problema. "Diseño sistémico" se usa como etiqueta de calidad para ambos casos, aunque cada uno deje sin tocar la mitad del espacio de intervención posible.

## El límite

Los dos conceptos coinciden en que la elección —de alcance o de profundidad— nunca es neutral y refleja los sesgos de quien diseña (ver también `visibilidad-relativa-al-observador`). Esto limita la utilidad práctica de nombrar la tensión: saber que hay dos ejes en competencia no dice cuál priorizar en un proyecto concreto, y ningún criterio del vault resuelve hoy esa priorización — solo exige hacerla explícita en vez de dejarla implícita.

---

## 4. Ver más que los demás en la sala no es ver el sistema completo

**Par:** `ilusion-de-omnipotencia-del-disenador` × `visibilidad-relativa-al-observador`

**Señales:** 3 tags compartidos (`sistemas`, `tension`, `poder`) — misma fecha de creación (2026-08-21), sin conexión previa en `relacionado`.

**Justificación de la tensión real (1 línea):** `visibilidad-relativa-al-observador` da el mecanismo causal exacto que `ilusion-de-omnipotencia-del-disenador` describe solo por sus síntomas — la ilusión nace porque el diseñador que mapea un sistema casi siempre tiene más visibilidad relativa que cualquier actor individual dentro de él, y esa ventaja comparativa se confunde con visibilidad absoluta.

---

```yaml
---
titulo: "Ver más que los demás en la sala no es ver el sistema completo"
tipo: correlacion
conceptos: [ilusion-de-omnipotencia-del-disenador, visibilidad-relativa-al-observador]
fecha: 2026-11-02
tags: [diseño, sistemas, poder, tension, no-leido]
estado: borrador
---
```

# Ver más que los demás en la sala no es ver el sistema completo

## La tensión

`ilusion-de-omnipotencia-del-disenador` describe cómo mapear muchas capas y actores de un sistema genera una sensación de poder de acción que no corresponde al poder real de transformarlo. `visibilidad-relativa-al-observador` describe que la visibilidad de un sistema nunca es objetiva ni total — depende de la posición de quien observa, y cada posición ve una porción distinta y queda ciega a otras: el ciudadano no ve el cronograma de mantenimiento que la municipalidad documenta; el técnico no ve la experiencia de ruptura del ciudadano. Juntos exponen el mecanismo preciso de la ilusión: el diseñador que mapea un sistema casi siempre ve más conexiones que cualquier actor individual dentro de ese sistema —más que el ciudadano, más que el técnico—, y esa ventaja comparativa de visibilidad se confunde con visibilidad absoluta. La ilusión de omnipotencia no nace de ver poco; nace de ver más que los demás en la sala.

## El insight no obvio

`ilusion-de-omnipotencia-del-disenador` no explica por qué ocurre la ilusión — solo describe sus costos (sobrediseño, desplazamiento de responsabilidad hacia el diseñador cuando el sistema no cambia). `visibilidad-relativa-al-observador` da el mecanismo exacto que falta: la posición del diseñador-que-mapea es estructuralmente la de mayor visibilidad relativa dentro de ese ejercicio específico —reúne lo que el ciudadano, el técnico y la institución ven por separado—, y esa posición privilegiada-en-ese-contexto-puntual se lee, sin quererlo, como posición de conocimiento total. El error no es de carácter (arrogancia) sino estructural: cualquiera que ocupe el rol de integrador de perspectivas va a sentir que sabe más de lo que realmente puede transformar, porque la tarea misma de mapear produce esa sensación comparativa. Ninguno de los dos textos, por separado, conecta la causa (ventaja de visibilidad relativa durante el mapeo) con el efecto (ilusión de omnipotencia sobre la capacidad de intervención).

## El límite

`visibilidad-relativa-al-observador` ya advierte que llevar el relativismo al extremo paraliza ("si todo es parcial, ningún mapa vale") — y lo mismo aplica aquí: nombrar el mecanismo de la ilusión no debería convertirse en excusa para no intervenir. `ilusion-de-omnipotencia-del-disenador` ya señala que cierta ilusión, en dosis calibradas, es motor de acción necesario. Integrar ambos conceptos no elimina la ilusión — ofrece un chequeo específico: antes de actuar con la confianza que da ver más que otros, preguntar explícitamente si ver más conexiones que el actor X da poder sobre esas conexiones, o solo visibilidad sobre ellas.

---

## 5. La exigencia de poder explicar por qué crees algo puede matar la señal que todavía no puedes explicar

**Par:** `metacognicion-del-disenador` × `lo-ilegible-como-senal`

**Señales:** 3 tags compartidos (`diseño`, `ia`, `criterio`) — vecinos comunes (`arquitectura-de-inteligencia`, `claridad-antes-de-velocidad`), sin conexión directa previa en `relacionado`.

**Justificación de la tensión real (1 línea):** metacognición exige poder articular con precisión cómo se llegó a una conclusión y trata la falta de esa articulación como señal de sospecha; lo ilegible como señal exige proteger precisamente las intuiciones que generan energía sin poder articularse todavía — aplicado al mismo momento (una intuición sin justificación formada), ambos prescriben comportamientos opuestos.

---

```yaml
---
titulo: "La exigencia de poder explicar por qué crees algo puede matar la señal que todavía no puedes explicar"
tipo: correlacion
conceptos: [metacognicion-del-disenador, lo-ilegible-como-senal]
fecha: 2026-11-02
tags: [diseño, criterio, aprendizaje, tension, no-leido]
estado: borrador
---
```

# La exigencia de poder explicar por qué crees algo puede matar la señal que todavía no puedes explicar

## La tensión

`metacognicion-del-disenador` sostiene que la calidad del trabajo de diseño depende de poder articular con precisión cómo se llegó a una conclusión — "la claridad no te protege de estar equivocado, te ayuda a equivocarte mejor". `lo-ilegible-como-senal` sostiene lo opuesto para un tipo específico de contenido: las ideas con más potencial son precisamente las que todavía no pueden articularse, y exigirles explicación prematura es el error que hace perder la oportunidad — "si todos la entendían desde el inicio, ya era tarde". Un diseñador que aplica rigurosamente la disciplina metacognitiva — exigirse siempre saber y poder explicar por qué cree algo — tiene un criterio sistemático para descartar exactamente las señales ilegibles que `lo-ilegible-como-senal` dice que vale la pena proteger.

## El insight no obvio

Los dos conceptos no hablan de dominios distintos que no se tocan — prescriben comportamientos opuestos frente al mismo tipo de situación: una intuición sin justificación articulada todavía. Metacognición dice: si no puedes explicar por qué, es señal de que no sabes lo que no sabes, trátalo con sospecha. Lo ilegible dice: si no puedes explicar por qué pero genera energía, es la señal más valiosa que vas a tener, protégelo precisamente porque no puedes explicarlo. La resolución que ninguno de los dos textos ofrece explícitamente es que hablan de momentos distintos del mismo proceso: la disciplina metacognitiva es el criterio correcto para *evaluar* una conclusión ya formada (¿cómo llegué aquí?, ¿qué asumí sin validar?); la receptividad a lo ilegible es el criterio correcto para *decidir qué capturar* antes de que haya una conclusión que evaluar. Aplicar el criterio de evaluación en la fase de captura mata la señal antes de que pueda madurar — el mismo error que comete un equipo que exige un business case articulado para toda idea temprana.

## El límite

La distinción de fase (capturar vs. evaluar) no es tan limpia en la práctica: un diseñador necesita metacognición incluso para notar que algo es ilegible-con-energía y no solo confuso — esa discriminación ya es un acto metacognitivo, aunque no sea el tipo de articulación completa que `metacognicion-del-disenador` describe. El límite real es de secuencia, no de exclusión: ambos criterios conviven, pero aplicarlos en el orden equivocado — evaluar antes de capturar — es donde está el costo que esta correlación señala.
