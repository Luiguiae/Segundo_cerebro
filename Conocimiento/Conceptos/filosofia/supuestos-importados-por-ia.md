---
titulo: "Supuestos importados por IA"
tipo: concepto
familia: agencia-ia
categorias_secundarias: [filosofia, organizaciones]
tags: [criterio, gobernanza-ia, fundamentos]
relacionado: [quien-controla-el-prompt, gobernanza-ia-performativa, arnes-del-agente]
edges:
  - target: quien-controla-el-prompt
    tipo: refines
    why: "Los supuestos importados operan en la capa invisible debajo del prompt. Quien controla el prompt controla la capa táctica; los supuestos filosóficos del modelo controlan la capa que precede esa decisión."
  - target: gobernanza-ia-performativa
    tipo: enables
    why: "La gobernanza performativa es el síntoma observable; los supuestos importados no examinados son la causa filosófica subyacente. Las organizaciones no pueden gobernar lo que nunca decidieron aceptar."
  - target: arnes-del-agente
    tipo: extends
    why: "El arnés define qué puede hacer el agente — límites operacionales explícitos. Los supuestos filosóficos del modelo definen qué quiere hacer — restricciones implícitas de diseño. Son dos capas de la misma arquitectura de control."
fecha: 2026-06-25
estado: activo
fuentes:
  - titulo: "Great Leaders Question Philosophical Assumptions"
    autor: "Faisal Hoque, Paul Scade, Pranay Sanklecha, Sverre Spoelstra"
    url: "https://hbr.org/2026/06/great-leaders-question-philosophical-assumptions"
    fecha_acceso: 2026-06-25
---

# Supuestos importados por IA

> "Integrar un modelo de IA en tu empresa no es adoptar una herramienta. Es adoptar una filosofía — y aceptarla sin leerla es la forma más cara de tercerizar tu criterio."

## El concepto

Cuando una organización adopta un modelo de IA, no importa solo una capacidad técnica: importa el conjunto de premisas filosóficas que el desarrollador embedió en él. Esas premisas — sobre qué cuenta como conocimiento verdadero, qué propósito tiene el sistema, y qué compromisos éticos están codificados — determinan el comportamiento del modelo antes de que el usuario formule cualquier pregunta.

Claude's Constitution de Anthropic, desarrollada por filósofos académicos junto al equipo técnico, gobierna cada interacción de Claude. Más de 300,000 empresas usan Claude — incluyendo ocho de las diez más grandes de Estados Unidos. La mayoría no ha leído ese documento, no ha discutido si está de acuerdo con sus premisas, y no tiene un proceso para detectar cuándo esas premisas entran en conflicto con las propias.

Esta dinámica no es exclusiva de Claude. Cada modelo de IA tiene premisas filosóficas embebidas. La diferencia está en si el desarrollador las documenta (como Anthropic) o las deja implícitas (como la mayoría). En ambos casos, la organización las importa.

## Por qué importa

La tercerización filosófica es la forma más invisible de tercerización. Cuando una empresa subcontrata logística, lo sabe y lo gestiona. Cuando importa los supuestos filosóficos de un modelo de IA, raramente lo nota — y casi nunca lo gestiona.

El riesgo opera en tres capas simultáneas:

**Ontológica.** El modelo tiene una definición implícita de qué es el usuario, qué es el producto, qué es el valor. Apple construyó parte de su identidad corporativa sobre la premisa "no eres nuestro producto, eres nuestro cliente". Un modelo entrenado con premisas distintas sobre los datos del usuario puede subvertir esa identidad sin que ningún ejecutivo haya tomado esa decisión.

**Epistemológica.** El modelo tiene criterios implícitos sobre qué cuenta como evidencia confiable, qué fuentes son autoritativas, y cómo manejar la incertidumbre. Esos criterios se importan a cada proceso donde el modelo participa. El Pentágono descubrió esto cuando intentó exigir respuestas "objetivamente verdaderas y libres de contaminación ideológica" — una posición epistemológica que el modelo no necesariamente comparte, y que el Pentágono no había examinado antes de la adopción.

**Ética.** El modelo tiene límites y compromisos. El caso del contrato con el Pentágono ilustra el choque: Anthropic mantuvo dos restricciones específicas — no vigilancia masiva doméstica, no armas completamente autónomas — y eligió perder el contrato antes de cederlas. Las organizaciones que usan Claude operan dentro de esos límites sin haber elegido activamente aceptarlos.

## Datos y evidencia

- Más de 300,000 empresas usan Claude, incluyendo 8 de las 10 más grandes de EE.UU. (Anthropic, 2026).
- Claude's Constitution fue desarrollada por filósofos académicos con el equipo técnico de Anthropic — es un marco filosófico operativo, no un documento de marketing ni cumplimiento.
- En enero 2026, el Pentágono solicitó a Anthropic aceptar cláusulas para uso militar en "cualquier uso legal". Anthropic insistió en dos restricciones específicas y rechazó cederlas. El Pentágono terminó el contrato y negoció con un competidor. Los productos de Anthropic aún estaban activos en operaciones militares al momento de publicación, y el conflicto estaba en litigación activa. (Hoque et al., HBR, junio 2026)
- Los autores señalan: "a pesar de que un número creciente de organizaciones integra el modelo, ha habido poca discusión sobre si los líderes entienden y están de acuerdo con los supuestos codificados en el producto de Anthropic — o qué deberían hacer si no lo están." (HBR, 2026)

## Tensiones y límites

**No todos los supuestos son legibles.** Claude's Constitution es pública. Pero parte del comportamiento de cualquier modelo está determinado por el entrenamiento — RLHF, datos de ajuste, refuerzos implícitos — y esos supuestos no están documentados en ningún lugar accesible. La transparencia de Anthropic es la excepción, no la norma del mercado.

**Alineación no es lo mismo que elección.** Una organización puede estar totalmente de acuerdo con las premisas filosóficas de un modelo — lo cual puede ser completamente legítimo. La cuestión no es si los supuestos son correctos; es si la organización los *eligió* o los *asumió por defecto*.

**Los supuestos no son estáticos.** Cambian con cada versión del modelo. Una organización que evaluó Claude en 2025 puede estar operando bajo premisas distintas en 2026 sin saberlo — lo que los autores llaman *deriva filosófica*.

**El examen tiene costo real.** Leer Claude's Constitution, entender sus implicaciones filosóficas y evaluar su alineación con los valores organizacionales requiere tiempo y capacidad crítica que la mayoría de los equipos de liderazgo no tiene instalada ni prioriza.

## Ejes investigados

- Claude's Constitution como modelo de transparencia filosófica documentada — caso Anthropic
- Caso Pentágono / Anthropic: colisión entre supuestos importados y supuestos organizacionales bajo presión económica real
- Apple / datos de usuario: ejemplo de alineación ontológica explícita usada como diferenciador de producto
- La relación entre supuestos importados no examinados y gobernanza performativa
- RLHF como supuesto filosófico específico importado: optimización por satisfacción del usuario como decisión de diseño con consecuencias éticas (ver `sycophancy-como-riesgo-de-diseno`)
