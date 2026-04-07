---
titulo: "Vibe Coding"
alias: ["vibecoding", "coding por intención", "ai-assisted coding"]
tags: [construccion, herramientas, desarrollo, producto, velocidad]
tipo: concepto
familia: velocidad-output
fecha: 2026-03-04
fuente:
  tipo: articulo
  referencia: "Múltiples fuentes: Figma, Humai 2026 Guide, Felix Lee, Ryo Lu"
  autor: "Investigación acumulada"
relacionado: [disenador-a-constructor, agentes-ia, mvp-a-prototipo-en-produccion]
proyectos: []
estado: activo
---

## ¿Qué es?
Vibe coding es un modo de construir software donde el punto de partida no es la estructura técnica sino la intención, el mood y la dirección. El desarrollador o diseñador describe lo que quiere en lenguaje natural y la IA genera el código. La barrera entre imaginar y construir desaparece.

## ¿Por qué importa?
El cuello de botella de la construcción de software siempre fue técnico. Vibe coding lo elimina. Un diseñador sin experiencia en código puede tener un producto funcional en horas. El 25% de las startups de Y Combinator Winter 2025 tienen el 95% de su código generado por IA — no es futuro, es presente.

Además, corrige una limitación de muchas herramientas “no-code con IA”: en productos como Lovable o v0 es fácil empezar, pero es difícil **graduarse** hacia arquitecturas más complejas. Con Cursor, el mismo entorno sirve tanto para:

- Primeros experimentos simples.
- Como para un codebase serio mantenido por un equipo experto.

## ¿Cómo funciona?
Existen tres capas de madurez:

1. **Layer 1 - Exploración**: Experimentos rápidos, variaciones, demos. Velocidad > Pulido. Herramientas: Bolt, Lovable.
2. **Layer 2 - MVP**: Flujos reales, interacciones, conexiones básicas de datos. Funcionalidad trabajando. Herramientas: Lovable, v0.
3. **Layer 3 - Engineering**: Calidad, consistencia, componentes apropiados, Git. Production-ready. Herramientas: Cursor, Claude Code.

El error más común es quedarse en Layer 1 y llamarlo "producto".

### Dos estilos de trabajo con agentes

Ryo Lu describe dos rutas sanas para trabajar con modelos/agentes al construir:

1. **Slop → oro**  
   - Dejar que el agente genere una primera versión “sloppy”.  
   - Usar esa estructura general como andamiaje y luego refinar a mano.
2. **Planear primero**  
   - Pensar el flujo, hacer mocks claros y detallar la intención.  
   - Dejar que el agente ejecute ese plan con mucha más precisión.

Ambos caminos son válidos — lo importante es que el **criterio y refinamiento siguen siendo humanos**, especialmente en detalles visuales (espaciados, alineaciones) donde los modelos todavía fallan.

## Ejemplos concretos
- Ryo Lu (Head of Design en Cursor) construyó ryOS — un sistema operativo retro completo — enteramente con vibe coding en Cursor.
- Felix Lee (CEO ADPList) construyó una herramienta de UX audit instantáneo, portfolio con IA conversacional, y herramientas internas con database y auth.
- Diseñadores de Google, Apple y Meta inscritos en el curso "Vibe Coding for Designers" (8,000+) pasaron de $50/hr a $150-400/hr al poder construir.

## Tensiones o limitaciones
- Funciona bien para prototipos, falla en producción a escala sin revisión técnica.
- Genera vulnerabilidades de seguridad si no se entiende el código generado.
- "Deuda técnica se compone exponencialmente cuando no entiendes tu código" — crítica válida para uso sin fundamentos.
- La paradoja: necesitas MÁS conocimiento técnico para usar IA bien, no menos. IA amplifica lo que le traes.
- La IA es mala inventando sistemas completos desde cero, pero muy buena **componiendo cosas que ya existen** (design systems, librerías, patrones). De ahí la importancia de “construir ladrillos”, no piezas sueltas.

## Se conecta con...
- [[disenador-a-constructor]] → vibe coding es el habilitador técnico principal de esta evolución
- [[agentes-ia]] → los agentes extienden el vibe coding a tareas más complejas y multi-paso
- [[mvp-a-prototipo-en-produccion]] → vibe coding elimina el cuello de botella que hacía lento al MVP clásico
- [[equipos-pequenos-alto-impacto]] → permite a equipos pequeños competir con grandes organizaciones

## Citas o fragmentos clave
> "Cursor changed everything for designers. I went from sketching UI to shipping a full agent OS." — Ryo Lu

> "AI is raw material, not finished goods. Most people stop at the first output, rather than using it to begin." — Ryo Lu

## Mis notas
- La distinción entre Layer 1, 2 y 3 es crítica para no confundir prototipo con producto.
- El stack más sólido para diseñadores: Figma → Figma Make → Lovable → Cursor.
- MCP (Model Context Protocol) es el game-changer: permite que la IA "sepa" tu design system en lugar de "adivinarlo".
- Ryo Lu es la figura de referencia en este concepto — Head of Design en Cursor, construyó ryOS.
- Felix Lee es el evangelista del movimiento — CEO ADPList, meta de 1M diseñadores como builders.
