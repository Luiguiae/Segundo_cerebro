---
titulo: El feedback que escala
slug: feedback-que-escala
tipo: concepto
familia: velocidad-output
categoria: producto
fecha: 2026-04-10
fuente: "Lenny's Podcast — Geoff Charles, CPO de Ramp"
fuente_url: "https://www.youtube.com/watch?v=RBqT2PHWdBg"
relacionado: [arquitectura-de-inteligencia, quien-controla-el-prompt, automatizar-mi-propio-trabajo]
tags: [ia, sistemas, liderazgo, criterio, organizacion]
estado: activo
---

# El feedback que escala

Hay dos tipos de feedback. Solo uno escala.

**Feedback puntual:** le dices a alguien que el botón debe estar arriba del fold. Lo arreglan. La próxima vez que alguien construye algo, el botón vuelve a estar abajo del fold. Tienes que decirlo de nuevo. Y de nuevo. Y de nuevo. Geoff Charles, CPO de Ramp, cuenta que dijo lo mismo cien veces antes de entender que el problema no era la persona — era el sistema.

**Feedback sistémico:** identificas en qué parte del proceso ocurrió la falla. ¿Qué prompt no lo capturó? ¿Qué skill no lo tenía codificado? ¿Qué componente del design system no lo aplicaba? Arreglas ahí. El error no vuelve a ocurrir — no porque la persona aprendió, sino porque el sistema lo previene.

La distinción es crítica en un mundo donde el código lo genera IA: el criterio de calidad ya no vive principalmente en la mente del diseñador o del engineer. Vive en los prompts, los skills, los design systems, los procesos de revisión. Si el criterio no está codificado en el sistema, desaparece cada vez que cambia la persona.

## El cambio de rol del líder

En este modelo, el trabajo del líder ya no es principalmente dar feedback correcto — es diagnosticar qué parte del sistema produjo el feedback incorrecto, y arreglarlo ahí.

Geoff lo formula así: si atrapas una mala experiencia de usuario, la pregunta no es "¿quién lo hizo mal?" La pregunta es "¿qué prompt falló, qué skill falló, qué design system falló?" Dar feedback a la persona es un band-aid de una sola instancia. Arreglar el proceso es una corrección que escala a todos los futuros outputs.

## La provocación

> Si estás dando el mismo feedback más de dos veces, el problema no es la persona. Es que ese criterio todavía no está en el sistema.

## La condición que lo hace posible

Esto solo funciona cuando el proceso de construcción es lo suficientemente explícito como para ser inspeccionado. Si el código lo escribe un humano desde cero cada vez, es difícil saber dónde codificar el criterio. Cuando el código lo genera IA siguiendo prompts y skills, cada decisión de diseño tiene un lugar preciso donde vivir: en el prompt, en el skill, en el componente del design system, en el proceso de revisión.

La IA no solo acelera la construcción — hace que el criterio de calidad sea codificable de formas que antes no eran posibles.

## Aplicaciones

- **Para líderes de diseño:** antes de dar feedback en una revisión, preguntar: "¿dónde debería haber estado codificado este criterio para que no llegara hasta aquí?" Esa pregunta convierte cada revisión en una oportunidad de mejora sistémica.
- **Para equipos que adoptan IA:** el valor real de tener un design system vivo no es la consistencia visual — es que es el lugar donde el criterio de calidad puede codificarse para que la IA lo aplique sin intervención humana en cada instancia.
- **Para propuestas internas:** el argumento para invertir en prompts, skills y sistemas de revisión no es eficiencia — es que es la única forma de que el criterio de calidad escale más rápido que la velocidad de construcción.

## Conceptos relacionados

- [[arquitectura-de-inteligencia]] — el feedback sistémico es una forma de arquitecturar la inteligencia: codificar criterio en el sistema para que el output mejore sin intervención constante
- [[quien-controla-el-prompt]] — el prompt es uno de los lugares donde vive el criterio codificado; mejorarlo en respuesta a feedback es la forma más directa de hacer que el feedback escale
- [[automatizar-mi-propio-trabajo]] — codificar criterio en el sistema es una forma de automatizar el trabajo de dar feedback — el sistema lo aplica, la persona se ocupa de los casos que el sistema todavía no puede manejar
