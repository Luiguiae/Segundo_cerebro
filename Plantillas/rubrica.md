# Rúbrica de calidad del Segundo Cerebro

> Jarvis aplica esta rúbrica antes de escribir cualquier archivo al vault.
> Si un archivo no pasa el gate mínimo, Jarvis NO lo escribe.
> En su lugar, lo reporta en `JARVIS_LOG.md` con la razón específica del rechazo
> y propone qué necesita el concepto para ser aprobado.

---

## Gate 1 — Criterios universales (aplica a todo tipo de archivo)

Todo archivo debe cumplir **los 4** para continuar:

| # | criterio | señal de falla |
|---|----------|----------------|
| 1 | **Atómico**: contiene una sola idea central | El archivo necesita dos títulos para describirse |
| 2 | **Propio**: escrito en las palabras del sistema, no copiado de una fuente | Lee como resumen de artículo, no como concepto destilado |
| 3 | **Frontmatter completo**: todos los campos obligatorios presentes y válidos | Falta `familia`, `estado`, o `tags` está vacío |
| 4 | **Nombre de archivo correcto**: sigue la convención de `taxonomia.md` | Tiene mayúsculas, acentos, o no usa kebab-case |

---

## Gate 2 — Criterios por tipo

### Para `concepto`

Debe cumplir **al menos 3 de 4**:

| # | criterio | cómo evaluarlo |
|---|----------|---------------|
| 1 | **No es un resumen**: el cuerpo del archivo agrega interpretación, no solo describe | ¿Se podría reemplazar con un link a la fuente? Si sí, falla. |
| 2 | **Tiene tensión interna**: el concepto reconoce su límite, su paradoja, o cuándo no aplica | ¿El texto dice solo cosas positivas del concepto? Si sí, falla. |
| 3 | **Relacionable**: tiene al menos un concepto en el campo `relacionado` que ya existe | `relacionado: []` o vínculos a conceptos inexistentes → falla |
| 4 | **Transferible**: alguien que no estuvo en la sesión puede entender el concepto sin contexto adicional | ¿El texto asume que conoces el contexto de creación? Si sí, falla. |

### Para `correlacion`

Debe cumplir **los 3**:

| # | criterio | cómo evaluarlo |
|---|----------|---------------|
| 1 | **Tensión real, no co-ocurrencia**: los conceptos no solo aparecen juntos, se contradicen o compiten | ¿El título podría ser "[A] y [B]"? Si sí, la tensión no existe. |
| 2 | **Síntesis no obvia**: el insight de la correlación no se obtiene leyendo cada concepto por separado | ¿Alguien que leyó ambos conceptos por separado ya sabe la conclusión? Si sí, falla. |
| 3 | **Ambos conceptos existen**: los dos archivos fuente están en `Conocimiento/Conceptos/` | Si uno no existe, no generar la correlación. |

### Para `fuente`

Debe cumplir **al menos 2 de 3**:

| # | criterio | cómo evaluarlo |
|---|----------|---------------|
| 1 | **Identificable**: tiene URL o referencia de origen en el frontmatter | Sin `url` o `referencia` → falla |
| 2 | **Procesada**: hay al menos una nota de Luigui o interpretación, no solo texto crudo | ¿Es solo una transcripción sin ninguna observación? Si sí, falla. |
| 3 | **Accionable**: tiene al menos una sección `## Conceptos a extraer` con 1+ ideas candidatas | Sin esa sección → no bloquea, pero Jarvis lo anota en el log como recomendación |

---

## Niveles de decisión

| resultado | qué hace Jarvis |
|-----------|----------------|
| **Aprueba** (pasa Gate 1 y Gate 2) | Escribe el archivo, actualiza ATLAS, registra en log como `[OK]` |
| **Rechaza** (falla Gate 1 o Gate 2 mínimo) | NO escribe el archivo. Registra en log como `[RECHAZADO]` con criterio específico. Propone qué editar. |
| **Aprueba con advertencia** (pasa pero con criterios débiles) | Escribe el archivo con `estado: borrador`. Registra en log como `[ADVERTENCIA]`. |

---

## Registro en JARVIS_LOG.md

Cada evaluación queda registrada con el formato real definido en `CLAUDE.md`
("Formato del JARVIS_LOG.md"):

```markdown
### YYYY-MM-DD HH:MM — [comando ejecutado]

**Instrucción:** "Jarvis, [lo que pidió Luigui]"

**Acciones:**
- [acción 1]
- [acción 2]

**Resultados:**
- [archivo]: [OK | RECHAZADO | ADVERTENCIA] — [razón si no es OK]

**ATLAS regenerado:** sí / no — [N conceptos procesados]
```

---

## Lo que la rúbrica NO evalúa

- **Extensión del cuerpo**: un concepto puede ser de 3 párrafos o de 10 líneas. La longitud no es criterio.
- **Estilo de escritura**: no hay un tono obligatorio. Lo que importa es que sea claro.
- **Originalidad de la idea**: el concepto puede venir de una fuente externa. Lo que se evalúa es si fue destilado correctamente.
- **Relevancia para la charla "De Diseñador a Constructor"**: la rúbrica evalúa calidad estructural, no pertinencia temática.
