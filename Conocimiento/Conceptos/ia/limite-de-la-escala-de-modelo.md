---
titulo: El límite de la escala de modelo
tipo: concepto
fecha: 2026-08-24
familia: agencia-ia
estado: activo
tags: [ia, agentes, escalamiento, benchmarks, limites]
relacionado: [agente-como-carpeta, llm-como-motor-de-plausibilidad, arnes-del-agente]
fuentes:
  - titulo: "From Question Answering to Task Completion: A Survey on Agent System and Harness Design"
    url: "https://arxiv.org/abs/2606.20683"
    fecha_acceso: 2026-08-24
    nota: "Guo, Hao, Wang et al. (City University of Hong Kong, U. Sydney, Peking U., TokenRhythm Technologies), arXiv:2606.20683, junio 2026"
---

# El límite de la escala de modelo

## El concepto

Durante años, la estrategia dominante para mejorar un sistema de IA fue simple: modelo más grande, más datos, más cómputo. Esa estrategia sigue funcionando — pero solo para un tipo específico de tarea, y ese tipo de tarea ya no es el que más importa.

El survey de Guo et al. documenta dos límites distintos que juntos explican por qué escalar el modelo dejó de ser la palanca correcta para mejorar agentes.

**El límite de recursos-desempeño:** aumentar la capacidad del modelo sigue mejorando el desempeño frontier, pero las ganancias son cada vez más costosas, desiguales entre capacidades, y limitadas por la latencia de inferencia. LLaMA 3.1 lo ilustra con precisión: pasar del modelo de 70B al de 405B multiplicó el cómputo de entrenamiento de 7.0 a 30.84 millones de horas de GPU H100 —un aumento de 4.4 veces— para obtener apenas 2.6 puntos de mejora en MMLU, 2.6 en MBPP EvalPlus, y 1.7 en GSM8K. Los modelos frontier de GPT, Claude y Gemini se están agrupando en un rango de puntaje cada vez más estrecho en benchmarks como MMLU-Pro y GPQA Diamond, haciendo que las mejoras posteriores sean menos discriminativas que los saltos de generación anteriores.

**El límite de medición:** este es el hallazgo más profundo. Los benchmarks tradicionales son estáticos, de horizonte corto y autocontenidos —el input es fijo, el output se evalúa una sola vez, y el entorno no cambia en respuesta a las acciones del modelo. Las tareas de agentes tienen una forma estructuralmente distinta: requieren comprensión de contexto largo, razonamiento multi-paso, interacción sostenida con el entorno, adaptación a metas subespecificadas, y robustez ante errores intermedios que se acumulan a lo largo de la trayectoria completa. Un modelo puede dominar benchmarks de pregunta-respuesta —donde la escala sigue produciendo ganancias predecibles— y fallar consistentemente en completar tareas reales de horizonte largo, porque el desempeño en esas tareas no es una propiedad del modelo aislado: es una propiedad de la trayectoria completa de ejecución.

## Por qué importa

Este es el fundamento empírico riguroso detrás de una intuición que ya circulaba en el diseño de producto con IA: que un modelo "más inteligente" no garantiza un agente más confiable. El survey lo formula con precisión: el desempeño de agentes de horizonte largo es una **propiedad a nivel de trayectoria** —el agente debe observar repetidamente, construir contexto, elegir acciones, preservar estado, interpretar feedback, y recuperarse de errores. Cada paso es una oportunidad de fallo, y los errores pequeños se componen sobre muchos pasos.

La consecuencia práctica es una reasignación del presupuesto de ingeniería. Si el cuello de botella no está principalmente en la capacidad bruta de razonamiento del modelo sino en la infraestructura que rodea su ejecución —qué observa, cómo se construye su contexto, qué acciones tiene disponibles, dónde persiste el estado, cómo se detectan y reparan los errores— entonces invertir en mejorar esa infraestructura de ejecución (el harness) produce mejoras más confiables y más baratas que esperar la siguiente generación de modelo.

## Datos y evidencia

- **LLaMA 3.1, 70B → 405B:** cómputo de entrenamiento de 7.0M a 30.84M horas de GPU H100 (4.4x) para +2.6 puntos MMLU, +2.6 MBPP EvalPlus, +1.7 GSM8K. El modelo de 405B permaneció lejos de un desempeño casi perfecto en benchmarks de razonamiento más difíciles como MATH y MMLU-Pro.
- **Patrón similar en Qwen3:** las ganancias de un modelo base mucho más grande varían sustancialmente entre benchmarks, sin una relación lineal clara entre tamaño y mejora.
- **Compresión de puntajes frontier:** los lanzamientos recientes de GPT, Claude y Gemini ocupan cada vez más un rango de puntaje alto y estrecho tanto en MMLU-Pro como en GPQA Diamond, lo que hace que las diferencias de puntaje sean difíciles de interpretar como diferencias significativas en capacidad real de agente.
- **Evidencia de que el harness sí mueve la aguja con el mismo modelo:** SWE-agent demostró que rediseñar la interfaz agente-computadora, sin cambiar el modelo base, mejora sustancialmente el desempeño en benchmarks de codificación. Meta-Harness mostró que harnesses optimizados automáticamente superan baselines diseñados a mano en Terminal-Bench.
- **Estudio de horizonte temporal:** una investigación reciente citada por el survey evalúa agentes por la duración de tareas humanas que pueden completar a una probabilidad de éxito fija, en lugar de por precisión de una sola respuesta —un cambio de métrica que hace central la confiabilidad de horizonte largo.

## Tensiones y límites

**Relación con `llm-como-motor-de-plausibilidad`:** ese concepto argumenta que las LLMs no razonan sino que calculan plausibilidad, y que por eso ningún upgrade elimina el fallo estructuralmente. Este concepto añade una capa complementaria y más técnica: incluso si el modelo mejora su capacidad de "plausibilidad" en preguntas aisladas, esa mejora no se traduce proporcionalmente en mejor desempeño de tareas largas, porque el desempeño de tarea depende de la trayectoria completa —observación, contexto, control, acción, estado y verificación— no solo de la calidad de cada respuesta individual.

**Relación con `agente-como-carpeta`:** ese concepto describe la arquitectura donde el agente es una definición estática (la carpeta) que un runtime (el harness) ejecuta. Este concepto explica *por qué* esa arquitectura importa tanto: si el harness es el lugar donde se resuelven los fallos de horizonte largo, entonces invertir en el diseño del harness —no solo en cambiar de modelo— es la palanca de mejora más confiable disponible hoy.

**Límite del concepto:** esto no es un argumento de que escalar el modelo ya no sirve. La escala sigue siendo indispensable como motor cognitivo de cualquier agente —sin ella, no hay comprensión de lenguaje, razonamiento ni propuesta de acción posible. El argumento es más preciso: una vez que el modelo entra en un régimen de alta precisión en evaluaciones comunes, la escala adicional produce mejoras cada vez más pequeñas y específicas de capacidad, mientras impone mayor costo, latencia y carga operativa —y esa relación de rendimientos decrecientes es particularmente severa para tareas de horizonte largo, no para preguntas aisladas.

## Ejes investigados

- Boundary de recursos-desempeño: evidencia cuantitativa de rendimientos decrecientes al escalar modelo (LLaMA 3.1, Qwen3, compresión de puntajes frontier)
- Boundary de medición: por qué los benchmarks estáticos de horizonte corto no capturan la confiabilidad de tareas de horizonte largo
- El desempeño de agente como propiedad de trayectoria completa, no de capacidad de modelo aislada
- Evidencia empírica de que el rediseño del harness mejora el desempeño con el modelo fijo (SWE-agent, Meta-Harness)
- Implicación de asignación de presupuesto de ingeniería: invertir en harness vs. esperar el siguiente modelo
