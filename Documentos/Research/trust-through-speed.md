---
titulo: "Trust through speed: confianza como resultado de la velocidad de iteración"
tipo: research
estado: borrador
autor: Luigui Avila
fecha: 2026-03-04
updated: 2026-03-04
tags: [confianza, velocidad, iteracion, producto, lanzamiento, research-preview, marca]
fuentes:
  - autor: "Jenny Wen"
    titulo: "Lenny's Podcast — The future of design"
    url: "https://www.youtube.com/watch?v=eh8bcBIAAFo"
---

# Trust through speed

Hipótesis sobre cómo la velocidad de iteración visible construye más confianza de marca que la calidad de lanzamiento.

---

## Hipótesis central

En el contexto de productos de IA — donde los modelos son no-deterministas, los estados no se pueden mockear y los casos de uso emergen en producción — **lanzar rápido e iterar visiblemente construye más confianza que esperar a lanzar perfecto**.

Lo que destruye la confianza no es lanzar imperfecto. Es lanzar imperfecto y no hacer nada después.

---

## Preguntas abiertas

- ¿Existe un umbral mínimo de calidad por debajo del cual "research preview" no es una etiqueta legítima sino una excusa?
- ¿Este patrón aplica igual a productos de consumo masivo que a productos para developers? ¿O los developers tienen mayor tolerancia a lo roto?
- ¿Cómo se mantiene la promesa de iteración cuando el equipo está en ejecución máxima y no queda capacidad para responder feedback?
- ¿Cuándo termina el "research preview" y empieza la responsabilidad plena de calidad?

---

## El patrón observado (Claude Cowork como caso)

Jenny Wen describe el lanzamiento de Claude Cowork:

1. **Research Preview como contrato explícito** — No es ocultar los defectos. Es declarar públicamente: "esto es lo peor que va a estar. Mejorará."
2. **La promesa implícita** — "Vamos a tomar tu feedback y vamos a iterar. Vamos a mostrarte que lo usamos."
3. **La ejecución de la promesa** — Tweeting activo, fixes rápidos, updates visibles. La velocidad del fix es evidencia de que el feedback fue escuchado.
4. **Claude Code como habilitador** — Los fixes llegan rápido porque Claude Code puede implementarlos rápido. La velocidad del ciclo no es solo decisional — es técnica.

> "The way that you really lose trust around quality and releasing something early is if you release it early and then nothing ever happens. That is something that degrades a brand."

---

## Condiciones para que funcione

Para que "trust through speed" sea una estrategia legítima y no una racionalización:

1. **Hay algo genuinamente valioso** — El producto ya ofrece algo que algunos usuarios no obtendrían de otra forma.
2. **El equipo puede iterar de verdad** — Capacidad técnica + velocidad real de implementación.
3. **La comunicación es honesta** — La etiqueta "research preview" es un contrato, no un escudo.
4. **El feedback circula** — Hay un mecanismo real para que el feedback llegue a quien decide qué construir.

---

## Tensión con la tradición de diseño

El proceso de diseño canónico prescribe validar antes de lanzar. El patrón "trust through speed" invierte el orden: **valida lanzando**. Esto solo es viable cuando:

- Los modelos de IA son no-deterministas (no puedes mockear todos los estados)
- Los casos de uso emergen de cómo la gente lo usa realmente
- El costo de lanzar imperfecto es menor que el costo de llegar tarde al mercado

Jenny Wen: "You have to see people try it out with their use cases, because with these models you can design them for different use cases, but you actually discover use cases as you see people using them."

---

## Conexión con el Espectro de Delegación

Existe una intersección con el framework de Soto Miño: antes de lanzar en research preview, el equipo necesita tener explícito **qué tipo de error es aceptable** y **quién responde por él**. Sin eso, "trust through speed" es abdicación de responsabilidad, no estrategia.

---

## Se conecta con...

- `Documentos/Research/decisiones-invisibles-y-gobernanza-ia.md` → las decisiones de qué lanzar y cuándo necesitan tener dueño explícito
- `Proyectos/Wayta_IA/` → ¿cuándo lanzar Wayta IA? ¿En qué condiciones el motor determinista está suficientemente sólido para validar en producción?
- Charla "Diseñador Constructor" → el diseñador que shipea también es el que decide cuándo algo es suficientemente bueno para salir
