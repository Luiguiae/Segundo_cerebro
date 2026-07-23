---
titulo: Automatizar lo verificable, no lo especificable
tipo: concepto
familia: ia
tags: [ia, agentes, verificacion, automatizacion, paradigma]
relacionado: [impuesto-de-verificacion, ai-evals-como-disciplina, ingenieria-agentica]
fecha: 2026-07-23
estado: borrador
fuentes:
  - titulo: "Sequoia Ascent 2026 summary"
    url: "https://karpathy.bearblog.dev/sequoia-ascent-2026/"
    fecha_acceso: 2026-07-23
  - titulo: "Andrej Karpathy's Verifiability Thesis: Why AI Is Superhuman at Code and Fails at Car Washes"
    url: "https://www.mindstudio.ai/blog/andrej-karpathy-verifiability-thesis-ai-superhuman-code-fails-car-wash"
    fecha_acceso: 2026-07-23
  - titulo: "Eval engineering: The missing piece of agentic AI governance"
    url: "https://siliconangle.com/2026/05/17/eval-engineering-missing-piece-agentic-ai-governance/"
    fecha_acceso: 2026-07-23
  - titulo: "Verification Is the New Bottleneck - Not Generation"
    url: "https://danielkeller.com/tech/verification-not-generation/"
    fecha_acceso: 2026-07-23
  - titulo: "Spec-Driven Development Is Eating Software Engineering (2026)"
    url: "https://medium.com/@visrow/spec-driven-development-is-eating-software-engineering-a-map-of-30-agentic-coding-frameworks-6ac0b5e2b484"
    fecha_acceso: 2026-07-23
---

# Automatizar lo verificable, no lo especificable

## El concepto

El software clásico automatiza lo que puedes **especificar**: si puedes reducir una tarea a instrucciones deterministas, la máquina la ejecuta. La frontera de la automatización la fijaba la capacidad de formalización —si no podías escribir el algoritmo, no había automatización.

Los LLMs invierten el predicado. Automatizan lo que puedes **verificar**: si puedes juzgar si un resultado es correcto o no —aunque no puedas describir el proceso para llegar a él— un modelo entrenado con refuerzo puede aprender a hacerlo. El criterio migra del proceso (¿sé cómo llegar al resultado?) al resultado (¿puedo saber si el resultado es correcto?).

Andrej Karpathy articuló esta distinción en el Sequoia Ascent 2026: "Traditional computers automate what you can specify in code, while this latest round of LLMs can automate what you can verify." El mecanismo técnico detrás es el aprendizaje por refuerzo: cuando existe un entorno reestablecible con una señal de verificación clara, los modelos pueden practicar la tarea indefinidamente. Código, matemáticas, tests y benchmarks aceleran más rápido porque su verificación es objetiva, rápida y automática.

## Por qué importa

Este cambio redefine no solo qué se puede automatizar, sino quién es responsable de que funcione. En el paradigma anterior, el ingeniero era el cuello de botella de especificación: si no podías describir la tarea, no había automatización posible. En el paradigma nuevo, el ingeniero es el cuello de botella de verificación: si no puedes evaluar la salida del agente, la automatización opera sin ancla.

El trabajo del ingeniero no desaparece —muta hacia la "ingeniería agéntica": diseño de specs (articular el objetivo con la precisión suficiente para que un agente lo entienda), revisión de diffs (juicio sobre los cambios que el agente genera), y construcción de eval loops (el sistema que verifica continuamente que el agente no se degrada). Estas habilidades no son productividad adicional sobre el trabajo anterior —son el trabajo nuevo.

La implicación más profunda: el impuesto de verificación no es solo un costo operativo que eventualmente se optimizará. Es el límite estructural de qué tan rápido puede avanzar la automatización en cualquier dominio. La frontera de lo automatable la dibuja ahora la capacidad de evaluación, no la de codificación.

## Datos y evidencia

- **57% de los equipos tienen agentes en producción, pero solo 52% corre evals** (Sequoia Ascent 2026, citado por Karpathy). El gap es donde viven las regresiones no detectadas. [Karpathy, julio 2026]

- **96% de los equipos que construyen con LLMs reportan dificultades con los evals** — la capacidad de generar ya no es la restricción principal, la de evaluar sí. [Docker AI Engineer World's Fair 2026, vía SiliconAngle, mayo 2026]

- **APEX-SWE benchmark (2026):** los modelos frontier se agrupan en 30–40% pass@1 en tareas de integración y observabilidad —exactamente las tareas que requieren verificación de comportamiento real. La "disciplina epistémica" (distinguir lo asumido de lo verificado) emerge como la brecha de habilidad dominante. [MarkTechPost, mayo 2026]

- **Punto de inflexión — diciembre 2025:** Karpathy identifica el momento en que "los modelos más recientes empezaron a producir bloques de código que simplemente funcionaban" como el punto en que la generación dejó de ser el cuello de botella. [Sequoia Ascent 2026]

- **Distribución de capacidades como evidencia:** los modelos alcanzan su pico en dominios verificables (código, matemáticas) y se estancan donde la verificación es difusa o subjetiva —la tesis ya se manifiesta en cómo se distribuyen las capacidades actuales de los modelos, no es solo una predicción. [MindStudio verifiability framework, 2026]

## Tensiones y límites

**La verificación también se puede automatizar —hasta cierto punto.** Si los evals son el nuevo cuello de botella, la respuesta natural es automatizar los evals. Pero un eval automatizado solo verifica lo que fue programado para verificar —la frontera se mueve, no desaparece. Los sistemas de IA que generan sus propios criterios de verificación (self-eval) introducen el riesgo de Goodhart: optimizan para la métrica, no para el objetivo.

**No todo lo verificable es verificable de forma barata.** Hay dominios donde la verificación existe pero es cara, lenta o requiere expertise raro (auditoría médica, revisión legal, inferencia científica). El paradigma favorece la automatización donde la verificación es rápida y automática, no donde es posible pero costosa —lo que puede sesgar qué se automatiza hacia lo fácil de medir, no hacia lo más importante.

**La línea vibe coding / ingeniería agéntica no es tan nítida.** Karpathy traza la distinción como un piso (vibe coding democratiza) vs. un techo (agentic engineering eleva). Pero en la práctica el mismo equipo puede hacer ambos según el contexto —y la "ingeniería agéntica" puede ser vibe coding con más burocracia si los evals son formales pero no significativos.

**¿Quién verifica los verificadores?** Si la frontera de automatización la define la calidad de los evals, y los evals los diseñan humanos con sesgos y puntos ciegos, el paradigma hereda los límites epistemológicos de quienes evalúan. El problema no desaparece —se mueve un nivel más arriba.

## Ejes investigados

**Eje 1 — El cambio de paradigma especificable→verificable.** Confirmado y bien documentado desde el Sequoia Ascent 2026. Karpathy lo articula como la diferencia entre Software 1.0 (especificación determinista) y LLMs (verificación como señal de entrenamiento). El mecanismo técnico —RL con entornos de verificación reestablecibles— es el puente entre la tesis conceptual y la práctica. Convergencia de al menos 4 fuentes independientes (MindStudio verifiability thesis, evoailabs, karpathy-wiki, Sequoia Ascent 2026 original).

**Eje 2 — El nuevo rol del ingeniero (spec + diff + evals).** Bien documentado como framework de "ingeniería agéntica". La tríada spec design → diff review → eval loops aparece consistentemente como la estructura del trabajo nuevo. El dato de brecha (57% con agentes en producción, 52% con evals) cuantifica dónde falla la adopción actual. Complementado con el movimiento Spec-Driven Development —30+ frameworks activos en 2026 según análisis de Vishal Mysore en Medium— que confirma que la transformación del rol ya tiene infraestructura.

**Eje 3 — Evals como cuello de botella estructural.** El más respaldado empíricamente. El 96% de dificultad con evals (Docker/AI Engineer World's Fair 2026), el APEX-SWE benchmark (30–40% pass@1 en integration/observability), y el framing de SiliconAngle ("eval engineering as missing piece of governance") convergen en que el problema es sistémico. La conexión con el concepto `impuesto-de-verificacion` del vault es directa: ese concepto lo plantea como costo operativo; este eje propone que es un límite estructural —la diferencia no es menor.
