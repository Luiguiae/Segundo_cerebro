---
titulo: Criterio transferible vs. respuesta memorizada
slug: criterio-transferible-vs-respuesta-memorizada
tipo: concepto
fecha: 2026-08-28
familia: agencia-ia
tags: [ia, agentes, aprendizaje, conocimiento, generalizacion, feedback, diseño]
relacionado: [agente-como-carpeta, feedback-que-escala, limite-de-la-escala-de-modelo, arnes-del-agente]
fuentes:
  - titulo: "HarnessCompass: Guiding Automatic Harness Evolution toward Generalizable and Effective Agent Harnesses"
    url: "https://arxiv.org/abs/2608.01918"
    fecha_acceso: 2026-08-28
    nota: "Zhang, Zhou, Song et al. (Beijing Institute of Technology, City University of Hong Kong), arXiv:2608.01918, agosto 2026"
---

# Criterio transferible vs. respuesta memorizada

## El concepto

Cuando un sistema aprende de su propia experiencia y acumula ese aprendizaje en una memoria persistente, hay dos formas radicalmente distintas de escribir esa memoria — y solo una de ellas produce conocimiento que sirve para algo nuevo.

El paper HarnessCompass documenta esta distinción con una claridad poco común, comparando dos versiones de un mismo sistema que evoluciona su propio comportamiento a partir de sus fallos. En la versión sin restricciones, la memoria acumulada queda dominada por recetas específicas de casos ya vistos:

> *"la tarea django-13158 falló porque la guía derivó hacia reescrituras que preservan la forma en `QuerySet.none()`. Para queries combinadas, la vacuidad debe propagarse hacia `combined_queries`..."*

En la versión con restricciones, la memoria registra principios generales junto con una condición explícita de cuándo aplican:

> *"Regla de propiedad de la ruta de ejecución. Aplicabilidad: cuando varias capas cercanas podrían plausiblemente parchearse, rastrea el valor que falla hasta la función que realmente lo emite, y parchea a ese propietario en lugar de un ayudante anterior o un formateador posterior."*

Ninguna de las dos entradas es más "correcta" en el momento en que se escribe — ambas surgieron de resolver un problema real. La diferencia está en qué pueden hacer después. La primera responde una pregunta muy específica: "cómo modificar django-13158". La segunda responde una pregunta de forma completamente distinta: "cómo decidir qué capa modificar cuando se viola un contrato compartido". La primera es una respuesta memorizada. La segunda es un criterio transferible.

## Por qué importa

La prueba de fuego que usan los autores para distinguir uno del otro es trasladable fuera del contexto técnico del paper: **¿esto seguiría ayudando en un caso que nunca he visto?** Si la respuesta nombra una tarea, un símbolo, un archivo o un caso específico, no es conocimiento — es una respuesta memorizada disfrazada de principio. Si no puede reformularse sin esa referencia específica, no debería guardarse como aprendizaje: hay que descartarla.

La consecuencia práctica es medible, no solo teórica: la versión con restricciones de generalización pasó de 54% a 66% de éxito en solo 5 iteraciones, superando a la versión sin restricciones que necesitó 20 iteraciones para llegar a 63% — y la ventaja se amplía específicamente en las tareas nunca vistas durante el aprendizaje (60.4% vs. 54.7%). El sistema que memoriza respuestas mejora rápido en lo que ya conoce y se estanca frente a lo nuevo. El sistema que extrae criterios mejora más lento al principio, pero ese aprendizaje sigue funcionando cuando aparece un caso distinto — incluso cuando se transfiere a un modelo base completamente diferente del que se usó para aprender.

Esto no es exclusivo de sistemas de IA. Es el mismo mecanismo que distingue una base de conocimiento útil de un archivo de tickets resueltos: una biblioteca de "cómo resolví el problema del cliente X" no ayuda al siguiente problema que no se parece exactamente al anterior. Una biblioteca de "cuándo aplica esta estrategia y cuándo no" sí.

## Datos y evidencia

- **HarnessCompass (2026):** con la restricción de generalización, Pass@1 sube de 54% a 62% en solo 2 iteraciones; sin ella, alcanzar una mejora similar toma muchas más iteraciones y no transfiere a tareas nuevas.
- **Brecha de transferencia:** la ventaja del sistema con restricciones sobre el sistema sin restricciones es mayor en tareas nunca vistas (5.7 puntos porcentuales) que en las tareas usadas para aprender (3.0 puntos) — evidencia directa de que el mecanismo protege específicamente la capacidad de generalizar, no solo el desempeño en lo ya conocido.
- **Transferencia entre sistemas distintos:** el aprendizaje extraído con restricciones, obtenido enteramente con un modelo, mejoró el desempeño de un modelo base completamente distinto sin ningún ajuste adicional — evidencia de que codificó principios de ingeniería reutilizables, no atajos específicos de un sistema.
- **Costo del atajo:** sin la restricción, el sistema encuentra una vía directa para subir el puntaje en el corto plazo — memorizar respuestas específicas es más rápido que extraer principios — pero esa vía deja al sistema fuertemente acoplado a los casos ya vistos, sin beneficio real ante lo desconocido.

## Tensiones y límites

**Relación con `feedback-que-escala`:** ese concepto ya establece la distinción entre feedback puntual (corrige una instancia, el error vuelve) y feedback sistémico (corrige el proceso, el error no vuelve). Este concepto añade precisión sobre *cómo* se codifica correctamente ese feedback sistémico: no basta con "meterlo en el sistema" — tiene que escribirse como una regla condicional con un criterio explícito de cuándo aplica, nunca como la solución a un caso puntual. Un feedback sistémico mal codificado puede seguir siendo, en el fondo, una respuesta memorizada con más pasos.

**Tensión con la velocidad de captura:** escribir una respuesta memorizada es más rápido y se siente más productivo en el momento — resuelve el caso que tienes enfrente con precisión total. Escribir un criterio transferible exige el trabajo adicional de preguntarse "¿por qué funcionó esto, y cuándo dejaría de funcionar?" antes de dar el aprendizaje por cerrado. Esa fricción adicional es exactamente lo que separa el conocimiento útil del que solo parece útil.

**Límite del concepto:** no toda respuesta específica es descartable. Hay información que genuinamente es de un solo caso y no debe forzarse a convertirse en principio general —intentarlo produce reglas vacías o mal calibradas. La disciplina no es "generaliza siempre", es "generaliza solo lo que realmente generaliza, y descarta el resto en lugar de guardarlo disfrazado de lección".

## Ejes investigados

- Distinción empírica entre memoria dominada por recetas específicas y memoria estructurada como reglas condicionales con criterio de aplicabilidad explícito (HarnessCompass, 2026)
- La prueba de fuego trasladable: "¿esto ayudaría a un caso que nunca he visto?" como criterio de descarte de aprendizaje mal capturado
- Evidencia cuantitativa de que restringir el aprendizaje a lo transferible mejora tanto la velocidad de mejora como la capacidad de generalización, no solo una de las dos
- Transferencia de aprendizaje entre sistemas distintos como prueba de que el criterio capturado es genuinamente de principio, no de atajo específico
- Relación con la codificación de feedback organizacional: la misma disciplina aplica a bases de conocimiento humanas, no solo a memoria de sistemas de IA
