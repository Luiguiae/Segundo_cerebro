# Tareas atómicas — Skill correlacion-conceptos

Cada tarea produce una sección o bloque del archivo final `SKILL.md`. Son independientes entre sí salvo donde se indica. El orden de ejecución sigue las dependencias del plan.

---

## T1 — Estructura base y metadatos del SKILL.md

**Descripción:** Crear el archivo `SKILL.md` con la cabecera de la skill: nombre, versión, descripción corta, cómo se activa (frases trigger), y declaración del modelo de herramientas (Claude Code para leer/escribir archivos en disco).

**Archivos afectados:**
- Crea: `SKILL.md` (en la raíz del proyecto o donde se decida cargarla)

**Criterio de done:**
- El archivo existe con frontmatter o cabecera válida para una skill de Claude.ai
- Incluye al menos dos frases de activación (una para modo demanda, una para modo discovery)
- Declara explícitamente que usa Claude Code para I/O de archivos

---

## T2 — Instrucciones Modo A: correlación bajo demanda

**Descripción:** Añadir al SKILL.md el bloque de instrucciones para cuando el usuario especifica dos conceptos. Debe cubrir: (1) localizar los archivos en `Conocimiento/Conceptos/`, (2) extraer información relevante (frontmatter + cuerpo), (3) identificar la tensión o fricción, (4) construir la narrativa tensión → síntesis, (5) proponer el título automáticamente sin pedir confirmación, (6) guardar en `Conocimiento/Correlaciones/YYYY-MM-DD_concepto-a--concepto-b.md`.

**Archivos afectados:**
- Modifica: `SKILL.md`

**Criterio de done:**
- Las instrucciones cubren los 6 pasos descritos
- Se especifica que el título debe expresar la tensión, no solo los nombres de los conceptos
- Se especifica el manejo del caso en que uno de los conceptos no existe como archivo (informar al usuario, no generar)

**Depende de:** T1

---

## T3 — Instrucciones Modo B: descubrimiento autónomo

**Descripción:** Añadir al SKILL.md el bloque de instrucciones para cuando el usuario pide "encuentra correlaciones". Debe cubrir: (1) leer solo `titulo` y `tags` del frontmatter de cada archivo en `Conocimiento/Conceptos/` (no el cuerpo completo), (2) identificar 3–5 pares con mayor tensión productiva priorizando contradicción sobre similitud, (3) presentar la lista al usuario con una frase que explique el potencial de cada par, (4) esperar confirmación antes de generar archivos.

**Archivos afectados:**
- Modifica: `SKILL.md`

**Criterio de done:**
- Las instrucciones distinguen explícitamente tensión productiva de similitud temática
- El flujo incluye el paso de confirmación antes de generar
- Se limita la propuesta a máx. 5 pares

**Depende de:** T1

---

## T4 — Plantilla de output (template del archivo de correlación)

**Descripción:** Insertar en el SKILL.md el template exacto que Claude debe usar para cada archivo generado. Incluye: frontmatter YAML con campos `tipo`, `conceptos`, `fecha`, `tags` (máx. 5), y las secciones `# Título`, `## La tensión`, `## La síntesis`, `## Aplicaciones`, `## Conceptos relacionados`.

**Archivos afectados:**
- Modifica: `SKILL.md`

**Criterio de done:**
- El template está completo con todos los campos del SPEC
- Incluye instrucciones inline sobre qué escribir en cada sección
- Especifica que `tags` tiene máximo 5 entradas

**Depende de:** T2, T3

---

## T5 — Reglas de comportamiento y límites explícitos

**Descripción:** Añadir una sección al SKILL.md con las restricciones hard de la v1: no correlacionar más de 3 conceptos simultáneos, no modificar ni referenciar ATLAS.md, no generar slides, no inventar conceptos que no existan como archivos, proponer título automáticamente (no preguntar).

**Archivos afectados:**
- Modifica: `SKILL.md`

**Criterio de done:**
- Cada restricción del SPEC está listada explícitamente
- Las restricciones están en lenguaje imperativo claro ("no hagas X", "si Y entonces Z")

**Depende de:** T4

---

## T6 — Ejemplo interno (few-shot) con correlación completa

**Descripción:** Escribir dentro del SKILL.md un ejemplo de correlación bien formada entre dos conceptos ficticios o reales del Segundo Cerebro. El ejemplo debe mostrar: el frontmatter correcto, un título que capture tensión (no nombres), una sección "La tensión" con fricción real, una "La síntesis" con insight genuino, y dos aplicaciones concretas.

**Archivos afectados:**
- Modifica: `SKILL.md`

**Criterio de done:**
- El ejemplo sigue exactamente el template de T4
- La narrativa del ejemplo pasa el test del SPEC: genera reacción de "no había pensado en eso"
- El ejemplo NO usa conceptos genéricos como "innovación" o "tecnología"

**Depende de:** T4, T5
