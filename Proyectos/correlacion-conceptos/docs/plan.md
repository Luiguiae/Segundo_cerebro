# Plan de implementación — Skill correlacion-conceptos

## Objetivo

Producir un único archivo `SKILL.md` que Claude.ai pueda cargar como skill. Al activarse, la skill lee archivos `.md` de `Conocimiento/Conceptos/`, detecta correlaciones con sesgo de tensión productiva, y escribe el resultado en `Conocimiento/Correlaciones/` con el formato especificado en SPEC.

El output NO es código ejecutable. Es un prompt estructurado que instruye a Claude cómo comportarse.

---

## Fases de implementación

### Fase 1 — Estructura base del SKILL.md
Definir el esqueleto del archivo: metadatos, descripción de la skill, cómo se activa, y qué herramientas usa. Esta fase no tiene lógica aún — solo establece el contrato del archivo.

### Fase 2 — Modo A: Correlación bajo demanda
Escribir las instrucciones para el flujo donde el usuario especifica dos conceptos. Incluye: cómo Claude localiza los archivos, cómo extrae contenido relevante del frontmatter y cuerpo, cómo construye la narrativa tensión → síntesis, y cómo determina el título sin pedir confirmación.

### Fase 3 — Modo B: Descubrimiento autónomo
Escribir las instrucciones para el flujo donde Claude lee todos los conceptos disponibles, propone 3–5 pares con mayor tensión productiva, espera confirmación del usuario, y genera los archivos aprobados.

### Fase 4 — Plantilla de output
Definir dentro del SKILL.md el template exacto que Claude debe seguir al escribir cada archivo de correlación: frontmatter YAML, secciones, convención de nombre, y reglas de tags (máx. 5).

### Fase 5 — Reglas de comportamiento y límites
Añadir las restricciones explícitas: qué hacer si un concepto no existe como archivo, límite de 3 conceptos en v1, no tocar INDEX.md, proponer título automáticamente, no generar slides.

### Fase 6 — Ejemplos internos (few-shot)
Incluir dentro del SKILL.md un ejemplo completo de correlación bien formada para anclar el tono narrativo que se espera. Esto es crítico para que la skill no produzca output genérico.

---

## Dependencias

| Fase | Depende de |
|------|-----------|
| 2    | 1 (necesita la estructura base) |
| 3    | 1 |
| 4    | 2 y 3 (la plantilla debe estar alineada con ambos modos) |
| 5    | 4 |
| 6    | 4 y 5 (el ejemplo debe seguir la plantilla final y respetar los límites) |

Las fases 2 y 3 pueden desarrollarse en paralelo una vez que Fase 1 esté aprobada.

---

## Riesgos identificados

**R1 — Tono genérico en la narrativa**
Si la skill no tiene un ejemplo concreto o instrucciones de tono precisas, Claude producirá texto académico o neutro en lugar de narrativa lista para slide.
Mitigación: Fase 6 (few-shot) + instrucción explícita de tono en Fase 2.

**R2 — Ambigüedad en localización de archivos**
Claude.ai no tiene filesystem propio. La skill debe instruir a Claude para pedir o usar Claude Code cuando se necesite leer/escribir archivos reales.
Mitigación: Fase 1 define explícitamente el modelo de herramientas (Claude Code para I/O de archivos).

**R3 — Desbordamiento del contexto en Modo B**
Si hay muchos conceptos, leer todos puede consumir contexto innecesario.
Mitigación: Fase 3 limita el discovery a leer solo nombre de archivo + frontmatter `tags` y `titulo`, no el cuerpo completo.

**R4 — Título propuesto demasiado literal**
Si el título solo concatena los nombres de los conceptos, pierde el valor de capturar la tensión.
Mitigación: Instrucción explícita en Fase 2: el título debe expresar la tensión, no los nombres.
