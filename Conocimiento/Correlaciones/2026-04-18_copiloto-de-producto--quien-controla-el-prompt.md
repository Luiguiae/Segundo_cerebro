---
titulo: "El mapa y el volante"
tipo: correlacion
conceptos: [copiloto-de-producto, quien-controla-el-prompt]
fecha: 2026-04-18
tags: [roles, producto, ia, poder, estrategia]
estado: activo
---

# El mapa y el volante

## La tensión

`quien-controla-el-prompt` dice que el poder en equipos con IA está en quien
teclea el prompt — que el prompt es la destilación del modelo del problema, el
criterio de calidad, y la comprensión del usuario. Quien lo escribe toma
decisiones de diseño aunque no lo llame así.

`copiloto-de-producto` dice que el poder está en quien mantiene el modelo mental
del destino mientras el agente ejecuta — que la habilidad crítica es la
orientación bajo presión, no la operación técnica.

Leídos por separado, los dos conceptos reivindican formas distintas de influencia
en el mismo proceso. Juntos, parecen competir por el mismo rol.

## El insight no obvio

No compiten: describen dos capas de control que son simultáneamente necesarias
y peligrosamente fáciles de desalinear.

El **control táctico** vive en el prompt: qué se construye en esta iteración,
cómo se instruye al agente, qué criterios aplica. Es el volante — la interfaz
directa con la ejecución.

El **control estratégico** vive en el modelo mental del copiloto: hacia dónde
va el producto, cuándo cambiar de ruta, qué no debe construirse aunque sea
técnicamente posible. Es el mapa — la visión que da sentido a cada giro.

El error más costoso en equipos AI-native no es que el prompt sea malo — es que
quien controla el prompt y quien tiene el mapa son personas distintas que no
están en conversación constante. El agente ejecuta el prompt con precisión
técnica en la dirección equivocada, y nadie lo detecta hasta que el producto
se ha alejado demasiado del destino.

## La consecuencia operativa

La correlación resuelve la pregunta práctica que `quien-controla-el-prompt`
deja abierta: ¿control del prompt para qué fin? La respuesta es que el
prompt-controller y el copiloto pueden ser la misma persona o personas distintas,
pero el criterio de quién debería controlar el prompt es siempre el mismo: quien
tiene o puede acceder al mapa.

Un diseñador que controla el prompt sin el modelo mental del sistema completo
toma buenas decisiones locales y malas decisiones globales. Un copiloto que tiene
el mapa pero no influye sobre el prompt pierde el producto en los detalles de
implementación que nunca especificó.

La alineación entre mapa y volante no es automática — es el trabajo central del
rol de copiloto de producto.

## El límite de la tensión

En proyectos pequeños, piloto y copiloto son la misma persona en momentos
distintos — y la tensión entre las dos capas se gestiona internamente. La
correlación se vuelve crítica en sistemas complejos donde múltiples personas
interactúan con agentes distintos: ahí la desalineación entre mapa y volante
es la causa más frecuente de deriva del producto.
