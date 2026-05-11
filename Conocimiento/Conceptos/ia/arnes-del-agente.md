---
titulo: "Arnés del agente"
tipo: concepto
fecha: 2026-04-20
familia: agencia-ia
estado: activo
tags: [agentes, ia, diseño, producto, criterio]
relacionado: [espectro-autonomia-agente, gobernanza-ia-performativa, las-tres-caras-del-producto-agentico]
fuentes:
  - titulo: "La era de los productos agénticos: rediseñando para agentes de inteligencia artificial"
    autor: "Martín Alaimo"
    fecha_acceso: 2026-04-20
---

# Arnés del agente

## El concepto
Cuando el producto es un agente, el artefacto central del diseño ya no es la pantalla
sino el arnés: el sistema de reglas, herramientas, permisos y guardrails que definen el
espacio de acción del agente. El arnés responde a cuatro preguntas: ¿qué puede hacer el
agente?, ¿qué información puede ver?, ¿cuándo debe confirmar antes de actuar?, ¿qué nunca
puede hacer sin importar la instrucción recibida? Las validaciones que antes eran botones
deshabilitados, campos obligatorios y mensajes de error son ahora restricciones explícitas
dentro del arnés. El loop de control — cómo el agente busca, evalúa, decide y actúa —
es el nuevo flujo de usuario. Solo que el usuario que lo "navega" es una máquina.

## Por qué importa
El arnés es el punto donde la lógica de negocio deja de ser implícita (codificada en la
UI) y se vuelve explícita (codificada como reglas interpretables por un agente). Esta
externalización fuerza una claridad que muchos productos nunca tuvieron: cuando no puedes
comunicar una restricción con un botón deshabilitado, tienes que articularla como regla.
El arnés mal diseñado produce el mismo tipo de error que una UI confusa, pero amplificado:
un agente que no entiende sus límites no se detiene en una pantalla de error — ejecuta
acciones incorrectas a velocidad de máquina. La calidad del arnés determina directamente
si el agente amplifica la intención del usuario o la distorsiona.

## Tensiones y límites
Tensión directa con `espectro-autonomia-agente`: el arnés define la posición del agente
en ese espectro, pero la posición correcta no es fija — cambia según el contexto de la
tarea, el historial del usuario y el nivel de reversibilidad de las acciones. Un arnés
rígido que siempre confirma antes de actuar produce un agente seguro pero inútil. Un arnés
permisivo que nunca confirma produce velocidad pero acumula riesgo. El diseño del arnés
es inherentemente un problema de calibración continua, no de configuración única.
