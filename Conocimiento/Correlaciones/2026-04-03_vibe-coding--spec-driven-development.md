---
titulo: "La trampa de construir sin saber qué estás construyendo"
tipo: correlacion
conceptos: [vibe-coding, spec-driven-development]
fecha: 2026-04-03
tags: [construccion, agentes-ia, proceso, velocidad, intencion]
estado: activo
---

# La trampa de construir sin saber qué estás construyendo

## La tensión
Vibe coding asume que la dirección emerge del movimiento: pruebas, el agente responde, algo aparece, y desde ahí navegas. Spec-driven development asume lo contrario: que construir sin un destino definido es la forma más cara de iterar. La fricción no es sobre velocidad — ambos pueden ser rápidos. Es sobre quién tiene el control del criterio de done. En vibe coding, ese criterio lo negocias con el agente en tiempo real, y puede cambiar con cada prompt. En SDD, ese criterio existe antes de que el agente entre. El problema real es que vibe coding entrena una dependencia: cada vez que llegas a un callejón sin salida, el instinto es promtpear más en lugar de pensar más. El spec no existe porque nadie lo pidió — y cuando el proyecto crece, no hay forma de saber si lo que se construyó resuelve el problema original.

## La síntesis
El error es tratar vibe coding y spec-driven development como filosofías opuestas. Son herramientas para fases distintas de un mismo proceso. Vibe coding es excelente para explorar el espacio del problema — cuando no sabes qué construir, iterar rápido con un agente te da información real sobre qué es posible y qué se siente bien. SDD es necesario cuando ya sabes qué construir y necesitas que el agente ejecute con precisión, sin que cada sesión reinterprete el objetivo. La secuencia no es elegir uno: es usar vibe coding para validar intuiciones y generar material para el spec, y luego usar SDD para construir con ese spec como ancla. El diseñador que entiende esto no abandona la exploración — la hace deliberada.

## Aplicaciones
- Al arrancar un feature nuevo en Designer Buddy: una sesión de vibe coding de 30 minutos para explorar qué siente bien en el flujo de UI, seguida de un SPEC.md que cristaliza lo aprendido antes de pasarle el trabajo serio a Claude Code
- En un sprint de prototipado con stakeholders: vibe coding produce el artefacto de conversación rápido; el spec captura las decisiones que ese artefacto reveló, para que la siguiente iteración no repita los mismos errores
- Al onboardear a otro diseñador en un plugin activo: el spec es el documento que explica por qué las cosas están como están — algo que ningún historial de prompts puede reemplazar

## Conceptos relacionados
- [[claridad-antes-de-velocidad]] — el spec operacionaliza la claridad de proceso; vibe coding es la herramienta para fases donde aún no hay esa claridad
- [[agentes-ia]] — los agentes necesitan un spec para no reinterpretar el objetivo en cada sesión; sin él, la velocidad de ejecución agéntica no tiene ancla
