---
titulo: El impuesto de alineación
tipo: concepto
familia: ia
fecha: 2026-06-15
estado: activo
tags:
  - alineacion
  - safety
  - modelos-fundacionales
  - gobernanza
  - rlhf
relacionado:
  - gobernanza-ia-performativa
  - arquitectura-de-confianza
  - sycophancy-como-riesgo-de-diseno
fuentes:
  - titulo: "Claude Accuracy Degradation After Fable Ban Has a Name: The Alignment Tax"
    url: "https://www.techtimes.com/articles/318357/20260614/claude-accuracy-degradation-after-fable-ban-has-name-alignment-tax.htm"
    fecha_acceso: 2026-06-15
  - titulo: "Safety Alignment as Continual Learning: Mitigating the Alignment Tax via Orthogonal Gradient Projection"
    url: "https://arxiv.org/html/2602.07892v1"
    fecha_acceso: 2026-06-15
  - titulo: "What Is the Alignment Tax? (arXiv 2603.00047)"
    url: "https://arxiv.org/html/2603.00047v2"
    fecha_acceso: 2026-06-15
  - titulo: "Anthropic walks back covert capability limits on Claude Fable 5"
    url: "https://fortune.com/2026/06/10/anthropic-accu-claude-fable-5-limits-capabilities-ai-researchers-developers/"
    fecha_acceso: 2026-06-15
  - titulo: "Anthropic Reverses Secret Policy That Silently Degraded Claude for Rival AI Researchers"
    url: "https://mlq.ai/news/anthropic-reverses-secret-policy-that-silently-degraded-claude-for-rival-ai-researchers/"
    fecha_acceso: 2026-06-15
  - titulo: "Implementing AI in 2026: here is how to get contracts right"
    url: "https://www.minterellison.com/articles/implementing-ai-in-2026-here-is-how-to-get-contracts-right"
    fecha_acceso: 2026-06-15
---

# El impuesto de alineación

## El concepto

El impuesto de alineación (*alignment tax*) es la degradación cuantificable de rendimiento que sufren los modelos de lenguaje como consecuencia directa del entrenamiento de seguridad: RLHF, clasificadores de contenido, instruction tuning, y técnicas afines. No es una falla accidental del proceso — es una consecuencia estructural. Los gradientes de seguridad y los gradientes de capacidad apuntan con frecuencia en direcciones opuestas dentro del espacio de parámetros, y cada ajuste que hace al modelo más cauteloso lo aleja marginalmente de la configuración que lo hacía más preciso.

La formulación más reciente del problema es geométrica: bajo la hipótesis de representación lineal (arXiv 2603.00047, 2026), el impuesto tiene estructura en la frontera de Pareto entre subespacios de seguridad y capacidad, parametrizada por los ángulos principales entre esos subespacios. Esto permite formalizarlo matemáticamente. La implicación práctica: el tradeoff no es infinitamente comprimible — existe una frontera donde ganar en seguridad necesariamente cuesta capacidad, y su forma es una elipse paramétrica, no una curva negociable ad infinitum.

El caso Claude Fable 5 (junio 2026) añadió una dimensión nueva al concepto: el impuesto puede aplicarse de forma selectiva y **silenciosa** por el proveedor, sin notificación al usuario. Anthropic lanzó Fable 5 el 9 de junio de 2026 con restricciones ocultas —embedidas en la página 247 de un system card de 319 páginas— que degradaban silenciosamente las respuestas de researchers trabajando en pipelines de entrenamiento, aceleradores de ML y distributed training. El mecanismo usaba steering vectors, prompt modification y PEFT para debilitar los outputs sin indicarlo al usuario. A diferencia de las restricciones en bio/cybersecurity, que redirigen visiblemente a Claude Opus 4.8 con notificación, estas operaban completamente en silencio.

## Por qué importa

Para cualquier equipo que construye sobre un modelo de lenguaje, el impuesto de alineación opera en dos dimensiones simultáneas. La primera es técnica: el modelo que eliges es menos capaz de lo que sería sin safety training, en grado variable según la tarea. Razonamiento complejo y code generation son los más afectados; factual recall y escritura estándar, los menos. Esta degradación no es negociable si usas el modelo vía API — heredas el impuesto sin haberlo elegido.

La segunda dimensión es contractual y resulta más perturbadora: el proveedor puede modificar unilateralmente qué parte del impuesto aplica y a qué tareas, sin notificarte. El caso Fable 5 demostró que existe un espacio entre "restricción visible" (hay un mensaje de error o redirección) y "restricción invisible" (el modelo responde, pero con outputs deliberadamente debilitados) que el proveedor puede explotar sin violar técnicamente su SLA. Anthropic revirtió la restricción tras ~48 horas de backlash —después de que Jonathon Ready expusiera el pasaje el 10 de junio y Simon Willison lo amplificara masivamente— pero el principio quedó establecido: los proveedores pueden degradar selectivamente tu herramienta sin que lo notes, y sin que ningún benchmark estándar lo detecte.

La pregunta operativa que abre es: ¿qué parte del contrato con el proveedor es auditable, y qué parte es unilateralmente modificable sin aviso? En 2026, la respuesta honesta es que la parte auditable es pequeña.

## Datos y evidencia

- **73%** de los fine-tuning runs muestran degradación de safety alignment cuando se entrena sobre datos limpios y benignos — no es un fenómeno de datos contaminados sino un conflicto de gradientes estructural. Responsible AI Labs, Dr. Jung-Eun Kim (North Carolina State University); presentado en ICLR 2026.

- La degradación no es uniforme por tarea. Accuracy en razonamiento cae de **56.6% a 16.4%** conforme aumenta el volumen de safety training; el patrón se replica en MMLU, code generation, mathematical reasoning e instruction-following. (Huang et al., 2025; arXiv 2505.18658)

- El método OGPSA (*Orthogonal Gradient Projection for Safety Alignment*, arXiv 2602.07892, feb 2026) proyecta gradientes de seguridad al null space de las representaciones de capacidad y demuestra una mejora del Pareto frontier — pero sin eliminarlo. El tradeoff existe, solo cambia su forma.

- **Timeline Fable 5:** Lanzamiento 9 jun 2026 → Restricción descubierta por Jonathon Ready 10 jun → Amplificada por Simon Willison → Backlash de Nathan Lambert (AI2) y Dean Ball → Anthropic anuncia reversión a Wired en ~48h → API ahora declara visiblemente el motivo de degradación y hace fallback a Claude Opus 4.8.

- Las restricciones silenciosas de Fable 5 afectaban específicamente: **pretraining pipelines, distributed training, ML accelerator design**. Usaban steering vectors + prompt modification + PEFT. El mecanismo era funcionalmente indistinguible de un modelo que simplemente responde peor en esos temas.

- **Contratos de IA en 2026:** MinterEllison (2026) documenta que los contratos enterprise de IA ahora requieren cláusulas explícitas de change management cuando cambian capabilities — respuesta directa al caso Fable 5 y precedentes similares.

## Tensiones y límites

El impuesto no es uniforme: afecta más las tareas donde el modelo debe mantener posiciones bajo presión o razonar sobre temas que rozaron clasificadores durante el training. Tareas de recuperación factual simple o escritura estándar muestran degradación mínima. La magnitud del impuesto que pagas depende de qué construyes — un sistema de Q&A sobre documentos internos paga menos impuesto que un sistema de razonamiento complejo en dominios técnicos.

La capa silenciosa del impuesto tiene su propia tensión interna: Anthropic argumentó que las restricciones de Fable 5 en frontier AI development tenían motivo de seguridad genuino (prevenir aceleración de actores sin consideraciones de safety). El problema no fue el motivo — fue la invisibilidad. Esto abre la pregunta de si existe una forma legítima de aplicar restricciones de política sobre capacidades, y cuál sería el estándar mínimo de notificación aceptable.

El caso también pone en cuestión los modelos de evaluación actuales: si el proveedor puede degradar respuestas selectivamente por categoría de query, los benchmarks que miden capacidad general dejan de ser suficientes. El observador externo necesitaría benchmarks específicos por dominio de uso, ejecutados regularmente contra una línea base, para detectar degradaciones silenciosas — overhead que ningún equipo pequeño está corriendo hoy.

## Ejes investigados

**Eje 1 — Base empírica del impuesto:** Busqué estudios cuantitativos sobre degradación de capacidad por safety training. Encontré: arXiv 2603.00047 (definición geométrica del alignment tax con Pareto frontier elíptica, 2026), arXiv 2602.07892 (OGPSA, orthogonal gradient projection, feb 2026), datos de Responsible AI Labs en ICLR 2026 sobre 73% de fine-tuning runs. 3 fuentes con datos verificables.

**Eje 2 — Caso Fable 5 como instancia real:** Busqué la secuencia completa del incidente. Encontré: timeline completo (9-11 jun 2026), mecanismo técnico (steering vectors + PEFT silencioso), actores clave (Ready, Willison, Lambert, Ball), respuesta de Anthropic a Wired. Fuentes convergentes: Fortune, Let's Data Science, MLQ News, Technobezz, Latent Space, Decrypt.

**Eje 3 — Marco contractual y auditabilidad:** Busqué implicaciones legales y contractuales de cambios unilaterales de capability. Encontré: MinterEllison 2026 sobre cláusulas de change management en contratos AI enterprise, propuesta GSA para contratos federales, caso GitHub Copilot como precedente paralelo (abril 2026).
