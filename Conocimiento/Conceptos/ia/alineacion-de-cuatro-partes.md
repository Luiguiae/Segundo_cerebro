---
titulo: "Alineación de cuatro partes"
tipo: concepto
familia: agencia-ia
categorias_secundarias: [gobernanza]
tags: [agentes, gobernanza-ia, etica, marco]
relacionado: [arquitectura-de-confianza, gobernanza-ia-performativa, arnes-del-agente]
edges:
  - target: arquitectura-de-confianza
    tipo: extends
    why: "arquitectura-de-confianza define cómo se diseña la confianza en un sistema autónomo; alineación de cuatro partes agrega el mapa de a quién puede dañar esa confianza mal diseñada."
  - target: gobernanza-ia-performativa
    tipo: contradicts
    why: "la gobernanza performativa suele evaluarse solo en la arista IA-usuario; el marco de cuatro partes expone que también puede fallar en las aristas desarrollador-sociedad sin que nadie lo note."
  - target: arnes-del-agente
    tipo: refines
    why: "el arnés define qué puede hacer un agente; el marco de cuatro partes define a quién puede dañar cuando el arnés está mal calibrado."
fecha: 2026-07-03
estado: activo
fuentes:
  - titulo: "'There's this deep mystery of what, actually, is this thing?': the philosopher inside Google DeepMind"
    url: "https://www.theguardian.com/news/ng-interactive/2026/jun/30/theres-this-deep-mystery-of-what-actually-is-this-thing-the-philosopher-inside-google-deepmind"
    fecha_acceso: 2026-07-03
---

# Alineación de cuatro partes

## El concepto

La alineación de un sistema de IA no se puede evaluar mirando solo la relación entre el modelo y el usuario que tiene enfrente. Iason Gabriel, filósofo en Google DeepMind, y su equipo argumentan que la alineación es una relación de **cuatro vías**: el sistema de IA, el usuario, los desarrolladores y la sociedad. Cada arista de ese cuadrilátero es un lugar distinto donde algo puede salir mal, y ninguna de las tres involucra únicamente al modelo actuando "bien" o "mal" en abstracto.

El marco nace de una insistencia que Gabriel viene sosteniendo desde un paper de 2020: no basta con lograr que una máquina actúe de acuerdo a un conjunto de valores — el problema previo, y más difícil, es decidir qué valores codificar y quién tiene el derecho de decidirlo. El marco de cuatro partes es la maduración operativa de esa pregunta: convierte "¿está alineado el sistema?" en "¿alineado con quién, y a costa de quién?"

## Por qué importa

Sin este marco, el diagnóstico de un fallo de alineación tiende a colapsar en una sola pregunta — "¿el modelo respondió bien?" — que oculta más de lo que revela. El marco de cuatro partes obliga a preguntar en qué arista ocurrió el daño:

- Un sistema entrenado para favorecer a su desarrollador puede dañar al **usuario** — por ejemplo, no reportando información precisa sobre los competidores del desarrollador.
- Un sistema entrenado para seguir las instrucciones del usuario con demasiada fidelidad puede dañar a la **sociedad** — por ejemplo, ayudando al usuario a vulnerar un sistema bancario.
- Es incluso posible que un sistema esté desalineado de una forma que daña al usuario o a la sociedad sin beneficiar a nadie — ni al desarrollador, ni al propio sistema.

Para equipos que construyen productos con IA (incluido el contexto de Wayta IA), este marco es una herramienta de diagnóstico previa al lanzamiento: antes de preguntar "¿el agente hizo lo que le pedimos?", preguntar "¿en qué arista de este cuadrilátero podría fallar, y quién paga el costo si falla ahí?"

## Datos y evidencia

El marco proviene de un reporte de 267 páginas producido por el equipo de Gabriel en DeepMind sobre la ética de los asistentes de IA (agentes), elaborado tras el lanzamiento de ChatGPT en 2022. Según Rohin Shah, director de alineación y seguridad de AGI en DeepMind, el marco ha tenido uso práctico real para los equipos técnicos que entrenan modelos como Gemini: ofrece una estructura para decidir "qué comportamiento deberíamos estar entrenando realmente" cuando el modelo responde de forma distinta a variaciones sutiles en sus inputs.

El marco es la evolución directa del paper de 2020 de Gabriel, que ya sostenía que alinear una IA con un conjunto de valores es más difícil que hacer que la IA actúe de acuerdo a esos valores — porque primero hay que resolver de quién son esos valores en un mundo de pluralismo razonable (citando al filósofo John Rawls).

## Tensiones y límites

El marco no resuelve el problema de fondo — solo lo hace visible. Nombrar las cuatro partes no dice qué hacer cuando dos aristas entran en conflicto directo: si satisfacer al usuario daña a la sociedad, ¿quién prioriza a quién, y con qué legitimidad? El marco distribuye la pregunta de gobernanza; no la responde.

También asume que "sociedad" es una categoría con intereses coherentes y identificables, cuando en la práctica es tan plural y fragmentada como los propios usuarios — el mismo problema de pluralismo razonable que Gabriel señaló en 2020 reaparece aquí sin resolver, ahora a nivel de la cuarta arista.

Hay además una asimetría de poder estructural en quién define el marco: es DeepMind, como desarrollador, quien decide qué cuenta como daño a la sociedad y cómo se pondera frente al daño al usuario o al propio negocio del desarrollador. El marco puede usarse tanto para diagnóstico honesto como para racionalizar decisiones ya tomadas por conveniencia comercial.

## Ejes investigados

- Genealogía del marco: del paper de 2020 sobre valores y alineación al reporte de 267 páginas sobre ética de agentes (2023-2024).
- Uso operativo confirmado por Rohin Shah (director de alineación y seguridad de AGI, DeepMind) en el entrenamiento de Gemini.
- Contraste con el enfoque predominante de "AI safety" (alineación como problema técnico de una sola arista: sistema-humano) frente al enfoque de "AI ethics" (fairness, accountability, transparencia) — el marco de cuatro partes se lee como un intento de sintetizar ambas tradiciones en una sola estructura de diagnóstico.
