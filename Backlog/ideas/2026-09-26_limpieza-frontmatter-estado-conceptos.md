---
id: limpieza-frontmatter-estado-conceptos
titulo: Deuda de schema en el frontmatter de conceptos — `estado`, `categorias_secundarias` y 2 conceptos que fallan Gate 0
fecha_captura: 2026-09-26
estado: borrador
raiz_proyecto: N/A — vive dentro de ~/Documents/Segundo_cerebro/
tags: [segundo-cerebro, schema, frontmatter, limpieza, gate-0]
---

## 1. Problema
Una sola categoría de problema — deuda de schema del frontmatter de conceptos — con tres manifestaciones. **No se toca ningún concepto hasta resolver la primera.**

**a) `estado` / `rutina-trabajo-enfocada`.** El reporte de poda (`Conocimiento/Mantenimiento/poda-candidatos.md`, 2026-09-26) muestra `rutina-trabajo-enfocada` como "(borrador)". Luigui indicó que `estado` no forma parte del schema no-negociable de conceptos atómicos (titulo, tipo, fecha, familia, categorias_secundarias, tags, relacionado, fuentes) y pidió registrarlo como limpieza aparte, del mismo tipo que `categoria` en la auditoría de mayo.

**Evidencia en el repo que contradice esa lista (verificada 2026-09-26):**
- `Plantillas/taxonomia.md` (plantilla canónica, línea 36, y regla de la línea 72) define `estado: borrador | activo | archivado` como campo del schema.
- Gate 0 (`CLAUDE.md`, regla 9) lista `estado` entre los campos **requeridos**: un concepto sin `estado` falla Gate 0.
- `rutina-trabajo-enfocada` tiene `estado: borrador` real en su frontmatter; 101 de 103 conceptos llevan el campo.
- Herramientas que dependen de `estado`: la rúbrica y la auditoría (fijan activo/borrador), el graduador de borradores, `poda-por-uso.py`, la columna Estado de `ATLAS.md`.

**b) `categorias_secundarias`.** No está en `taxonomia.md`; se eliminó de 9 conceptos en la auditoría del 2026-08-24 por ser equivalente al `categoria` prohibido. Hoy hay 0 conceptos con ese campo, pero la lista de Luigui lo incluye como parte del schema.

**c) Dos conceptos sin auditar que fallan hoy** (ambos del 2026-08-28, sin trackear; cuentan en el ATLAS = 103, en el baseline de `vault-brief.md` y en el reporte de poda). Verificado campo por campo contra `taxonomia.md` y Gate 0:

| concepto | Gate 0 (CLAUDE.md regla 9) | taxonomía |
|---|---|---|
| `diseno-multiinteligencia` | falta `estado` (requerido) · lleva `slug` (prohibido) · 7 tags (máx. 5) · 4 `relacionado` (máx. 3) | tags fuera del vocabulario controlado: `sistemas-complejos`, `inteligencia-distribuida`, `epistemologia`, `organizaciones` (existe `organizacion`) |
| `criterio-transferible-vs-respuesta-memorizada` | falta `estado` (requerido) · lleva `slug` (prohibido) · 7 tags (máx. 5) · 4 `relacionado` (máx. 3) | tags fuera del vocabulario controlado: `generalizacion`, `feedback` |

Cumplen: `familia` válida, `relacionado` apunta a conceptos que existen y las tres secciones obligatorias del cuerpo. Es exactamente el mismo tipo de falla que la auditoría del 2026-08-24 normalizó en 6 conceptos (`slug` + `estado` ausente + tags/relacionado sobre el límite); estos dos son posteriores a esa auditoría.

La lista de schema que cita Luigui no está en el repo: no se encontró ningún documento "no-negociable" ni el registro de la Mejora 004 (`categoria`) en `docs/`, `Backlog/` ni `Plantillas/`. Su fuente vive fuera del vault.

## 2. Usuario objetivo
Luigui (dueño del schema) y Jarvis, que aplica Gate 0 sobre lo que dice `taxonomia.md`.

## 3. Casos de uso principales
- Decidir la fuente de verdad del schema (a) y (b).
- Normalizar los 2 conceptos de (c) una vez decidido — `slug`, tags y `relacionado` se arreglan igual con cualquier respuesta; lo de `estado` depende de (a).

## 4. Criterios de aceptación
Pendiente de maduración.

## 5. Fuera de alcance
- Modificar `rutina-trabajo-enfocada.md`, los 2 conceptos de (c) o cualquier otro concepto antes de decidir la fuente de verdad (instrucción de Luigui, 2026-09-26).
- Retirar `estado` de `taxonomia.md`/Gate 0 sin una decisión explícita: hoy el ciclo de vida del concepto vive ahí.

## 6. Stack / arquitectura
Pendiente de maduración.

## 7. Métricas de éxito
Pendiente de maduración.

## 8. Preguntas abiertas
- ¿Cuál es la fuente de verdad del schema: `taxonomia.md` + Gate 0 (lo que Jarvis aplica hoy) o la lista de campos no-negociables de Luigui? Hoy divergen en dos campos: `estado` (en taxonomia, fuera de la lista) y `categorias_secundarias` (en la lista, fuera de taxonomia).
- Si `estado` sale del frontmatter, ¿dónde vive el ciclo borrador/activo/archivado que usan la rúbrica, el graduador, la poda y el ATLAS?
- ¿`categorias_secundarias` vuelve al schema? Se eliminó el 2026-08-24 sin objeción, pero la lista de Luigui lo incluye.
- Para (c): ¿se agregan al vocabulario controlado los tags fuera de lista (`sistemas-complejos`, `inteligencia-distribuida`, `epistemologia`, `generalizacion`, `feedback`) o se reemplazan por tags existentes? Regla 7 de CLAUDE.md: los tags nuevos se proponen, no se crean solos.
