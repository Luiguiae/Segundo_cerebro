---
titulo: "Corrupción silenciosa por delegación"
tipo: concepto
familia: velocidad-output
fecha: 2026-05-15
estado: activo
tags: [agentes, confianza, control, criterio, productividad]
relacionado:
  - comprehension-debt
  - espectro-autonomia-agente
  - pit-stop-cognitivo
fuentes:
  - titulo: "LLMs Corrupt Your Documents When You Delegate"
    url: "https://arxiv.org/abs/2604.15597"
    fecha_acceso: 2026-05-15
  - titulo: "DELEGATE-52 Dataset — Microsoft / Hugging Face"
    url: "https://huggingface.co/datasets/microsoft/delegate52"
    fecha_acceso: 2026-05-15
---

# Corrupción silenciosa por delegación

## El concepto

Cuando un LLM edita documentos de forma continua en nombre del usuario, introduce errores dispersos pero severos que se acumulan silenciosamente a lo largo de la interacción. El fenómeno no es que el modelo se niegue a ejecutar la tarea — en casi todos los casos, intenta cumplir. El problema es que cumple imperfectamente, y cada imperfección se convierte en el estado base del siguiente turno. La degradación es invisible en el corto plazo y devastadora en el largo.

## Por qué importa

En el modelo disenador-a-constructor, la delegación de trabajo a agentes es el multiplicador central: un humano con criterio + agentes ejecutores = capacidad de equipo grande. Pero ese multiplicador tiene un precio oculto. Si el trabajo que el agente produce se corrompe turno a turno sin que nadie lo detecte, el criterio humano está siendo aplicado sobre una base que ya no es fiel al original. No se amplifica el trabajo — se valida silenciosamente su degradación. El concepto obliga a replantear qué significa supervisar: no es aprobar el output de cada turno, es detectar la acumulación que ningún turno individual hace visible.

## Datos y evidencia

- Microsoft Research (arXiv 2604.15597, Philippe Laban et al., abril 2026): benchmark DELEGATE-52 con 19 LLMs, 52 dominios profesionales, 310 entornos de trabajo, documentos reales de 2–5k tokens.
- Modelos frontier (Gemini 3.1 Pro, Claude 4.6 Opus, GPT 5.4): **25% de corrupción de contenido** tras 20 interacciones delegadas.
- Promedio de todos los modelos evaluados: **50% de degradación** en el mismo horizonte.
- Python es el único dominio de 52 donde la mayoría de modelos alcanza el umbral de "listo" (≥98% de fidelidad). Los dominios de lenguaje natural y dominios nicho (notación musical, estados financieros) muestran degradación mayor.
- El uso de herramientas agénticas (agentic tool use) **no mejora** el desempeño frente al modo sin herramientas.
- El desempeño tras 2 interacciones **no predice** el desempeño a 20 interacciones — las simulaciones cortas subestiman la severidad real.
- Los factores que agravan la degradación se **componen**: tamaño del documento × longitud de interacción × presencia de archivos distractor producen peor resultado que la suma de sus efectos individuales.

## Tensiones y límites

**Tensión principal:** el paper estudia flujos de edición en modo relay simulado (sin humano en el loop), no interacción real con supervisión activa. En la práctica, un usuario atento puede detectar errores antes de que se acumulen. El verdadero riesgo es el modo "vibe coding + delego + confío" — exactamente el patrón que se vuelve dominante cuando la velocidad de generación supera la velocidad de revisión.

**Límite del benchmark:** mide únicamente reversibilidad de ediciones. Ediciones subjetivas o con múltiples soluciones válidas quedan fuera del alcance. El benchmark tampoco simula interacción multi-turno real con un humano que corrige — solo single-turn por paso.

**Tensión con la narrativa de productividad IA:** el paper no niega que los agentes aceleren el trabajo. Dice que acelerar sin supervisión estructurada produce documentos que se ven correctos y no lo son — lo cual es más peligroso que un error visible.

## Ejes investigados

- Mecanismo de corrupción en flujos delegados a LLMs: cómo los errores dispersos se componen en degradación severa
- DELEGATE-52: benchmark de Microsoft Research para medir fidelidad de edición en 52 dominios profesionales
- Efecto del uso de herramientas agénticas sobre la degradación (resultado: sin mejora)
- Relación entre longitud de interacción y severidad de degradación
- Único dominio "listo" para delegación: Python; todos los demás por debajo del umbral de confianza
