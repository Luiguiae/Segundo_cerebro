---
titulo: "Las tres caras del producto agéntico"
tipo: concepto
fecha: 2026-04-20
categoria: producto
familia: agencia-ia
estado: activo
tags: [producto, agentes, ia, diseño, estrategia]
relacionado: [espectro-autonomia-agente, arnes-del-agente, legibilidad-de-maquina]
fuentes:
  - titulo: "La era de los productos agénticos: rediseñando para agentes de inteligencia artificial"
    autor: "Martín Alaimo"
    fecha_acceso: 2026-04-20
---

# Las tres caras del producto agéntico

## El concepto
Un producto en la era de agentes puede existir en tres modos estructuralmente distintos,
cada uno con implicaciones de diseño completamente diferentes. No son etapas evolutivas
ni niveles de madurez — son tres apuestas de diseño simultáneas que pueden coexistir:

**Cara 1 — Tu producto es un agente.** En lugar de UI, diseñas el arnés: qué puede hacer
el agente, con qué herramientas, cuáles son sus guardrails, cuándo confirma antes de actuar.
El usuario delega la navegación; tu trabajo es definir el espacio de acción del delegado.

**Cara 2 — Agentes externos interactúan con tu producto.** Tu UI es irrelevante para estos
visitantes. Lo que importa es qué tan legible es tu sistema para una máquina: tus MCPs,
la estructura semántica de tus datos, tus reglas de negocio explícitas. Un competidor con
peor producto pero sistema más predecible gana en esta capa.

**Cara 3 — Agente contra agente.** Tu producto tiene su propio representante que negocia
en tiempo real con el agente del usuario: propone alternativas, aplica estrategia comercial,
prioriza stock. La interacción ya no es humano-sistema sino máquina-máquina con la lógica
de negocio del producto incorporada.

## Por qué importa
La mayoría de los equipos de producto piensan en la transición a agentes como un único
cambio ("hacemos un agente"). El framework de tres caras revela que son decisiones
independientes con lógicas distintas. Un producto puede estar en la Cara 2 sin haber
construido nada nuevo — simplemente exponiendo mejor lo que ya tiene. O puede estar en
la Cara 3 sin que sus usuarios humanos noten nada. Cada cara requiere capacidades distintas,
métricas distintas y definiciones distintas de qué significa un producto exitoso.

## Tensiones y límites
Las tres caras no son mutuamente excluyentes pero sí compiten por recursos de diseño y
desarrollo. Priorizar la Cara 1 (construir el agente propio) puede dejar desatendida la
Cara 2 (legibilidad para agentes externos), que tiene mayor impacto a corto plazo si el
tráfico agéntico ya es significativo. La Cara 3 introduce complejidad nueva: cuando dos
agentes negocian, ¿quién define los límites de esa negociación? ¿Qué pasa cuando los
intereses del agente del producto y del agente del usuario entran en conflicto directo?
