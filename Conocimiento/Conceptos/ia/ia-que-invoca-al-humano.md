---
titulo: La IA que Invoca al Humano
tipo: concepto
familia: agencia-ia
fecha: 2026-05-21
tags: [agentes-ia, diseno-agentico, mcp, colaboracion-humano-ia, autonomia]
relacionado: [ux-checkpoints, espectro-autonomia-agente, arnes-del-agente]
estado: activo
fuentes:
  - titulo: "Human Tool: An MCP-Style Framework for Human-Agent Collaboration"
    url: "https://arxiv.org/abs/2602.12953"
    fecha_acceso: 2026-05-21
  - titulo: "Why having 'humans in the loop' in an AI war is an illusion"
    url: "https://www.technologyreview.com/2026/04/16/1136029/humans-in-the-loop-ai-war-illusion/"
    fecha_acceso: 2026-05-21
  - titulo: "Human-in-the-Loop vs Human-on-the-Loop for AI Agents"
    url: "https://www.waxell.ai/blog/human-in-the-loop-vs-human-on-the-loop-ai-agents"
    fecha_acceso: 2026-05-21
---

# La IA que Invoca al Humano

## El concepto

Durante décadas, el diseño de sistemas con supervisión humana asumió una dirección fija: el
humano decide cuándo intervenir. El paradigma Human-in-the-Loop (HITL) y su variante
Human-on-the-Loop (HOTL) sitúan al humano como supervisor que activa su participación. El
agente ejecuta; el humano monitorea y, en algún momento, para.

El paper *Human Tool* (arXiv 2602.12953, Tsinghua University / HKUST et al., febrero 2026)
invierte la pregunta: ¿y si el agente invoca al humano igual que invoca una API? El framework
propone una abstracción de interfaz tipo MCP donde el humano es modelado como una herramienta
callable con un schema estructurado de tres dimensiones: **capacidades** (qué puede hacer el
humano que el agente no puede), **información** (qué contexto necesita el humano para
responder), y **autoridad** (qué decisiones requieren firma humana por política o riesgo). El
agente consulta ese schema dinámicamente para decidir cuándo y cómo invocar la contribución
humana.

La distinción semántica importa: "herramienta" aquí no implica subordinación del humano al
sistema. Es una abstracción de coordinación — la misma lógica que usas para invocar una base
de datos o un servicio externo, aplicada a la expertise humana. El agente no toma el control;
lo comparte de forma explícita y trazable.

## Por qué importa

El diseño actual del arnés del agente parte siempre desde el humano: el humano diseña los
checkpoints, decide dónde pausar, configura cuándo confiar. Esto produce un sistema donde el
humano necesita anticipar todos los escenarios de intervención antes de que el agente corra.
El problema: los agentes producen escenarios que el diseñador no anticipó.

La inversión de perspectiva de Human Tool cambia el artefacto de diseño. En lugar de "¿dónde
pone el humano sus checkpoints?", la pregunta es "¿qué triggers activan la llamada al humano
desde el sistema?". El arnés deja de ser una jaula de restricciones y se convierte en un
protocolo de colaboración: el agente tiene herramientas para reconocer su propio límite de
competencia y escalar activamente.

La consecuencia práctica más relevante es la reducción del workload cognitivo: en lugar de
supervisión continua (que genera el impuesto de verificación), el humano recibe llamadas
estructuradas en momentos precisos. Los estudios controlados del paper reportan mejora en
rendimiento de tareas, reducción de carga de trabajo humano y dinámicas de colaboración más
equilibradas frente a sistemas de baseline.

## Datos y evidencia

- **arXiv 2602.12953** (Tsinghua, Zhejiang, BJTU, HKUST, Anhui — febrero 2026): Framework
  validado en estudios controlados en tareas de toma de decisiones y tareas creativas.
  Resultados: mejor rendimiento, menor workload humano, dinámicas de colaboración más
  equilibradas vs. baseline. Autores: Yuanrong Tang et al.

- **MIT Technology Review, 16 abril 2026** ("Why having 'humans in the loop' in an AI war is
  an illusion"): "The immediate danger is not that machines will act without human oversight;
  it is that human overseers have no idea what the machines are actually 'thinking.'" Los
  sistemas de IA de última generación son cajas negras cuyo razonamiento interno no puede ser
  verificado ni por sus propios creadores. La inversión en comprensión del razonamiento IA es
  "minúscula" comparada con la inversión en capacidad de los modelos.

- **Error cascade en sistemas multi-agente** (AlignX AI, marzo 2026): "A misinterpreted brief
  compounding across five autonomous agents, running thousands of times per second, may not be
  recoverable and cause permanent harm." La invocación activa permite interrumpir el cascade
  antes de que se propague.

- **Factores de contingencia para escalación** (arXiv 2507.14034, 2026): Los tres factores
  que determinan cuándo invocar supervisión humana: complejidad de la tarea, riesgo
  operacional y fiabilidad del sistema en ese dominio específico.

## Tensiones y límites

**La paradoja del schema humano**: el framework funciona solo si el agente tiene un modelo
correcto de las capacidades del humano. Si el schema está mal calibrado, el agente invoca al
humano en los momentos equivocados — o no lo invoca cuando debería porque su schema no
reconoce el límite. Quién mantiene actualizado ese schema es un problema de diseño no resuelto
en el paper.

**La caja negra persiste**: MIT Technology Review (abril 2026) señala la tensión central: que
sea el agente quien decida cuándo llamar al humano no resuelve la opacidad del razonamiento.
El humano no puede verificar si la invocación se activó por la razón correcta. La
"invocación" puede ser tan nominal como el oversight que reemplaza.

**La atrofia por invocación escasa**: cuanto más capaz es el agente, menos frecuentemente
invocará al humano. El humano pierde contexto entre invocaciones y, cuando sí es llamado,
puede no tener el criterio para intervenir correctamente. Es la dinámica de
`juicio-como-trabajo-completo` en sentido inverso: el juicio se degrada no porque el agente
lo reemplace, sino porque solo se ejerce en llamadas dispersas.

**No aplica en tiempo real**: la arquitectura presupone que el humano puede responder dentro
del ciclo del agente. En sistemas que operan en milisegundos, el overhead de la invocación
humana es estructuralmente incompatible con la velocidad del sistema.

## Ejes investigados

**Eje 1 — El paper Human Tool y sus mecanismos** (arxiv.org/abs/2602.12953): El paper propone
una abstracción de tres dimensiones (capabilities / information / authority) y tres preguntas
operativas: cómo definir el schema humano, cuándo invocar, cómo comunicarse minimizando
overhead. Validado en estudios controlados en tareas de decisión y creativas. Tsinghua /
HKUST et al., febrero 2026. 2 fuentes sólidas encontradas.

**Eje 2 — Taxonomía de triggers de invocación** (arXiv 2507.14034; waxell.ai; tekleaders.com):
Los tres factores de contingencia (complejidad, riesgo operacional, fiabilidad del sistema)
como criterios para activar la invocación. Distinción HITL / HOTL y evolución hacia modelos
mixtos donde el nivel de oversight se determina dinámicamente por riesgo y política. 3 fuentes
encontradas.

**Eje 3 — La crítica: la ilusión del oversight humano** (technologyreview.com abril 2026;
bioethics.com abril 2026): MIT Technology Review argumenta que el problema de fondo no es
quién inicia la coordinación sino la opacidad del razonamiento del agente. La inversión de
perspectiva de Human Tool no resuelve ese problema — lo desplaza. 2 fuentes sólidas.
