---
titulo: "Vibe coding"
tipo: concepto
familia: velocidad-output
tags: [construccion, herramientas, desarrollo, producto, velocidad]
relacionado: [disenador-a-constructor, agentes-ia, mvp-a-prototipo-en-produccion]
edges:
  - target: spec-driven-development
    tipo: contradicts
    why: "Ambos abordan cómo se produce software con IA, pero desde criterios opuestos: vibe-coding acepta la ambigüedad del done como parte constitutiva del flujo; spec-driven lo fija antes de ejecutar. La tensión no es estilística sino estructural: quién define el estándar de calidad y en qué momento del proceso lo hace."
fecha: 2026-03-04
estado: activo
---

## El concepto

Vibe coding es un modo de construir software donde el punto de partida no es la estructura técnica sino la intención, el mood y la dirección. El desarrollador o diseñador describe lo que quiere en lenguaje natural y la IA genera el código. La barrera entre imaginar y construir desaparece.

Existen tres capas de madurez: Layer 1 (exploración) con herramientas como Bolt y Lovable para experimentos rápidos donde velocidad > pulido; Layer 2 (MVP) con flujos reales y conexiones básicas de datos; Layer 3 (engineering) con calidad, consistencia y producción real mediante Cursor o Claude Code. El error más común es quedarse en Layer 1 y llamarlo "producto".

Ryo Lu describe dos estilos sanos de trabajo con agentes: *slop → oro* (dejar que el agente genere una primera versión y refinar a mano sobre esa estructura), o *planear primero* (hacer mocks claros, detallar la intención, dejar que el agente ejecute ese plan con mucha más precisión). En ambos casos, el criterio y el refinamiento final siguen siendo humanos.

## Por qué importa

El cuello de botella de la construcción de software siempre fue técnico. Vibe coding lo elimina. El 25% de las startups de Y Combinator Winter 2025 tienen el 95% de su código generado por IA — no es futuro, es presente. Un diseñador sin experiencia en código puede tener un producto funcional en horas.

A diferencia de muchas herramientas no-code, el mismo entorno de vibe coding (Cursor) sirve tanto para primeros experimentos como para codebases serios mantenidos por equipos expertos — no hay techo de complejidad artificial.

## Tensiones y límites

Funciona bien para prototipos, falla en producción a escala sin revisión técnica. Genera vulnerabilidades de seguridad si no se entiende el código generado. La paradoja: necesitas MÁS conocimiento técnico para usar IA bien, no menos — la IA amplifica lo que le traes. Es mala inventando sistemas completos desde cero, pero muy buena componiendo cosas que ya existen (design systems, librerías, patrones). De ahí la importancia de construir ladrillos consistentes, no piezas sueltas.
