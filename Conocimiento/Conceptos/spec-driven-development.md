---
titulo: "Spec-Driven Development"
tipo: concepto
familia: velocidad-output
tags: [codigo, construccion, ia, iteracion, estrategia]
relacionado: [vibe-coding, agentes-ia, mvp-a-prototipo-en-produccion]
fecha: 2026-04-07
estado: activo
---

## ¿Qué es?
Spec-Driven Development (SDD) es el principio de que todo lo que un agente de IA va a construir debe estar precedido por un documento de especificación que define el criterio de done antes de que el agente empiece. No es documentación — es una decisión sobre qué se está construyendo y por qué, cristalizada antes de delegar la ejecución.

## ¿Por qué importa?
Los agentes de IA son excelentes ejecutores pero pésimos definidores de objetivos. Si el criterio de "terminado" no existe antes de la sesión, el agente lo infiere — y puede inferirlo diferente en cada prompt. El resultado es un producto funcionalmente existente, pero que nadie puede defender ni mantener, porque no hay contrato con el problema original.

La adopción masiva de vibe coding hizo este problema visible: equipos que iteraban rápido llegaban a versiones que parecían funcionales pero no tenían ningún ancla con lo que querían resolver. El spec es ese ancla.

## ¿Cómo funciona?
Un spec mínimo define cuatro cosas antes de abrir el editor:
1. **El problema**: ¿qué situación del usuario estamos resolviendo? (no qué feature estamos construyendo)
2. **El criterio de done**: ¿cómo sabemos que el agente terminó bien? (comportamiento observable, no "que se vea bien")
3. **Las restricciones**: ¿qué no puede hacer esta solución? (stack, tiempo, complejidad aceptable)
4. **El contexto de uso**: ¿quién lo usa, cuándo, con qué expectativas?

Con ese spec, el agente tiene un ancla. Sin él, cada sesión puede reinterpretar el objetivo.

## Ejemplos concretos
- Un diseñador-constructor escribe un `SPEC.md` de 10 líneas antes de pedirle a Claude Code que construya un feature. La sesión produce algo que puede defender ante stakeholders porque el criterio existe fuera del historial de prompts.
- Un equipo usa Cursor sin spec y termina con un codebase donde cada parte fue construida con una definición distinta de "qué resuelve esto" — el producto funciona pero no escala porque nadie entiende el sistema completo.
- En Wayta IA: el principio "el motor decide, la IA solo narra" es SDD en acción — el spec son las reglas deterministas, el agente las ejecuta dentro de ese contrato.

## Tensiones o limitaciones
- El spec crea fricción al inicio: en proyectos exploratorios donde el problema no está claro, forzar un spec prematuro puede limitar el descubrimiento legítimo.
- Un spec mal escrito es peor que no tener spec: define el problema incorrecto con precisión.
- Existe tensión directa con vibe coding: la velocidad de exploración de vibe coding se pierde si cada sesión requiere un spec completo. La solución no es elegir uno — es saber cuándo usar cada uno. Vibe coding para explorar; SDD para ejecutar lo que ya se sabe que hay que construir.

## Se conecta con...
- [[vibe-coding]] → son herramientas para fases distintas del mismo proceso: vibe coding para explorar el espacio del problema, SDD para ejecutar con precisión lo que esa exploración reveló
- [[agentes-ia]] → los agentes sin spec reinterpretan el objetivo en cada sesión; el spec es el contrato que los ancla y hace predecible su output
- [[mvp-a-prototipo-en-produccion]] → el spec es lo que convierte un prototipo funcional en algo con intención defendible que puede escalar

## Citas o fragmentos clave
> "El criterio de done no lo puede definir el agente. Si no existe antes de la sesión, el agente lo inventa — y lo inventa diferente cada vez."

## Mis notas
- SDD no significa documentación pesada — significa que el criterio de done existe antes de que el agente empiece. El spec mínimo cabe en 10 líneas.
- La secuencia sana: vibe coding para explorar → insight sobre qué construir → spec para cristalizarlo → agente para ejecutar con ese spec como ancla.
- Pendiente: definir qué campos mínimos tiene un SPEC.md para proyectos del tamaño de Wayta IA.
