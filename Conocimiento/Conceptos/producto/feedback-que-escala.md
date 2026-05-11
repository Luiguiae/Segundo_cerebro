---
titulo: "El feedback que escala"
tipo: concepto
familia: velocidad-output
tags: [ia, sistemas, liderazgo, criterio, organizacion]
relacionado: [arquitectura-de-inteligencia, quien-controla-el-prompt, automatizar-mi-propio-trabajo]
edges:
  - target: pit-stop-cognitivo
    tipo: requires
    why: "El feedback que escala captura señales sobre outputs del sistema pero no sobre el estado cognitivo del equipo que los produce. pit-stop-cognitivo provee la capa de feedback que feedback-que-escala no alcanza: detecta cuándo el equipo acumula deuda de criterio o fatiga de decisión que no aparece en ningún loop de feedback sobre resultados."
fecha: 2026-04-10
estado: activo
fuentes:
  - titulo: "Lenny's Podcast — Geoff Charles, CPO de Ramp"
    url: "https://www.youtube.com/watch?v=RBqT2PHWdBg"
    fecha_acceso: 2026-04-10
---

## El concepto

Hay dos tipos de feedback. Solo uno escala.

**Feedback puntual:** le dices a alguien que el botón debe estar arriba del fold. Lo arreglan. La próxima vez, el botón vuelve a estar abajo del fold. Tienes que decirlo de nuevo. Geoff Charles, CPO de Ramp, cuenta que dijo lo mismo cien veces antes de entender que el problema no era la persona — era el sistema.

**Feedback sistémico:** identificas en qué parte del proceso ocurrió la falla. ¿Qué prompt no lo capturó? ¿Qué skill no lo tenía codificado? ¿Qué componente del design system no lo aplicaba? Arreglas ahí. El error no vuelve a ocurrir — no porque la persona aprendió, sino porque el sistema lo previene.

La distinción es crítica en un mundo donde el código lo genera IA: el criterio de calidad ya no vive principalmente en la mente del diseñador o del engineer. Vive en los prompts, los skills, los design systems, los procesos de revisión. Si el criterio no está codificado en el sistema, desaparece cada vez que cambia la persona.

## Por qué importa

Si estás dando el mismo feedback más de dos veces, el problema no es la persona — es que ese criterio todavía no está en el sistema. El trabajo del líder ya no es principalmente dar feedback correcto; es diagnosticar qué parte del sistema produjo el feedback incorrecto y arreglarlo ahí.

La IA no solo acelera la construcción — hace que el criterio de calidad sea codificable de formas que antes no eran posibles. El valor real de un design system vivo no es la consistencia visual — es que es el lugar donde el criterio puede codificarse para que la IA lo aplique sin intervención humana en cada instancia.

## Tensiones y límites

Esto solo funciona cuando el proceso de construcción es lo suficientemente explícito como para ser inspeccionado. Si el código lo escribe un humano desde cero cada vez, es difícil saber dónde codificar el criterio. El peligro opuesto: sistematizar demasiado pronto puede congelar criterios que todavía están evolucionando. No todo feedback merece ser codificado inmediatamente.
