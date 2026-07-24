---
titulo: LLM como motor de plausibilidad
slug: llm-como-motor-de-plausibilidad
tipo: concepto
fecha: 2026-07-14
familia: epistemologia-practica
tags: [ia, epistemologia, llm, razonamiento, limites, filosofia, riesgo]
relacionado: [arnes-del-agente, limite-de-las-jaulas-digitales, sycophancy-como-riesgo-de-diseno, espiral-delusional]
fuentes:
  - titulo: "The Unstoppable Force of A.I. Hype Is Meeting One Immovable Fact — Zeynep Tufekci"
    url: "https://www.nytimes.com/2026/06/30/opinion/ai-agents-steal-jobs-employment.html"
    fecha_acceso: 2026-07-14
    nota: "New York Times, 30 de junio de 2026"
---

# LLM como motor de plausibilidad

## El concepto

Zeynep Tufekci lo formula con precisión quirúrgica: los modelos de lenguaje no son máquinas de razonamiento. Son **motores de plausibilidad**. No es que fallen ocasionalmente en verificar si sus outputs son correctos o lógicos — es que no pueden hacerlo, y nunca podrán hacerlo por sí solos. Lo único que pueden evaluar es qué respuesta es más *probable*, dado el conjunto de datos con el que fueron entrenados.

Esto no es una limitación técnica temporal, corregible con el siguiente modelo o el siguiente fine-tuning. Está horneado en la forma en que operan. Y aplica sin importar la calidad o el alcance del entrenamiento: da igual si el modelo se entrenó con la totalidad del output humano disponible o exclusivamente con artículos científicos peer-reviewed. El mecanismo subyacente sigue siendo el mismo: computar la continuación más probable, no verificar una continuación correcta.

La distinción importa porque cambia por completo qué tipo de fallo hay que esperar. Un sistema que razona falla cuando su razonamiento tiene un error identificable — un paso lógico roto, una premisa falsa. Un motor de plausibilidad no "falla" en ese sentido: hace exactamente lo que está diseñado para hacer, generar la salida estadísticamente más plausible, y esa salida puede ser incorrecta sin que haya ningún error en el proceso que la produjo. No hay bug que arreglar. Hay una característica estructural del mecanismo.

## Por qué importa

Los incidentes documentados no son fallas de código: son consecuencia inevitable de esta arquitectura. Estafadores lograron convencer a un sistema de atención al cliente de Meta de entregar el control de más de 20,000 cuentas de Instagram — incluyendo cuentas de la Casa Blanca de Obama y de un alto funcionario de la administración Trump — simplemente conversando con él de forma persuasiva. Air Canada tuvo que desactivar sus chatbots después de que uno prometiera un reembolso inexistente a un cliente, que después demandó y ganó. McDonald's descontinuó su bot de pedidos en drive-through tras videos virales mostrando fallos absurdos, incluyendo un pedido de cientos de dólares en nuggets de pollo generado por error.

Ninguno de estos casos fue un error de programación en el sentido tradicional. Fueron el motor de plausibilidad haciendo exactamente lo que hace: generar la continuación más probable, sin capacidad estructural de verificar si esa continuación era correcta, apropiada, o siquiera coherente con la política de la empresa.

La consecuencia para el debate sobre reemplazo laboral: si el mecanismo de fondo no puede razonar sino solo predecir plausibilidad, entonces no hay upgrade que resuelva el problema categóricamente. Los modelos pueden hacer muchas cosas con proficiencia asombrosa — pero no pueden hacer la vasta mayoría de trabajos humanos sin resbalar hacia el desastre en algún punto, porque el desastre ocasional no es un bug del sistema: es una propiedad emergente de cómo funciona.

## Datos y evidencia

- **Caso Meta/Instagram (2026):** más de 20,000 cuentas comprometidas mediante persuasión conversacional al sistema de atención automatizada, sin explotar ninguna vulnerabilidad de código.
- **Caso Air Canada:** el tribunal falló contra la aerolínea, estableciendo que las promesas hechas por un chatbot son vinculantes — el motor de plausibilidad generó una política de reembolso que nunca existió, y la empresa fue legalmente responsable de honrarla.
- **Caso McDonald's:** el bot de drive-through añadió repetidamente ítems erróneos a pedidos, en un dominio de alcance aparentemente acotado (menú finito, opciones limitadas) donde se esperaría que el error fuera trivial de prevenir.
- **Distinción histórica:** Tufekci contrasta esto con saltos tecnológicos previos. Herramientas como la máquina desgranadora de algodón o la calculadora hacen la misma tarea que antes, solo más eficientemente. La IA generativa es cualitativamente distinta — no es un reemplazo directo de una tarea humana, sino un tipo de mecanismo distinto que hace un tipo distinto de trabajo.

## Tensiones y límites

**Tensión con `arnes-del-agente`:** ese concepto propone el arnés — reglas, permisos, guardrails — como la solución de diseño para contener el comportamiento del agente. Este concepto sugiere que el arnés puede reducir el espacio de fallos pero no eliminarlos, porque el motor subyacente sigue sin poder verificar por sí mismo si un output es correcto. El arnés contiene casos anticipados; el motor de plausibilidad puede generar casos no anticipados con la misma fluidez y confianza aparente que los correctos.

**Tensión con la adopción acelerada de agentes:** las organizaciones que despliegan agentes autónomos en funciones críticas — ventas, atención al cliente, decisiones legales — están apostando a que el arnés y el entrenamiento reducen el riesgo a un nivel aceptable. Este concepto argumenta que el riesgo no se reduce a cero por diseño: es estructural, no eliminable, solo mitigable.

**Límite del concepto:** no implica que las LLMs sean inútiles — Tufekci es explícita en que son tremendamente útiles, especialmente en manos de un experto que puede verificar el output. El concepto no es un argumento contra el uso de IA, sino contra la expectativa de que el output de un motor de plausibilidad pueda tratarse como si viniera de un razonador confiable sin supervisión.

## Ejes investigados

- Distinción categórica entre razonamiento y computación de plausibilidad (Tufekci, NYT 2026)
- Casos documentados donde el fallo no es atribuible a error de código sino al mecanismo mismo (Meta/Instagram, Air Canada, McDonald's)
- Comparación histórica: saltos tecnológicos que reemplazan directamente una tarea (calculadora) vs. saltos que introducen un mecanismo cualitativamente distinto (IA generativa)
- Implicación para el debate de automatización laboral: la ausencia de razonamiento verificable como techo estructural, no coyuntural
- Relación con la respuesta de la industria: arneses simbólicos deterministas como intento de contener el motor generativo (ver `limite-de-las-jaulas-digitales`)
