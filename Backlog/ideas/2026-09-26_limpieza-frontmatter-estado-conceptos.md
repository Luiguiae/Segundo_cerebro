---
id: limpieza-frontmatter-estado-conceptos
titulo: Deuda de schema en el frontmatter de conceptos — 2 conceptos que fallan Gate 0 (`estado` y `categorias_secundarias` cerrados 2026-09-26)
fecha_captura: 2026-09-26
estado: borrador
raiz_proyecto: N/A — vive dentro de ~/Documents/Segundo_cerebro/
tags: [segundo-cerebro, schema, frontmatter, limpieza, gate-0]
---

## 1. Problema
**Estado al 2026-09-26 (actualizado):** (a) y (b) están **CERRADAS** — Luigui decidió que `Plantillas/taxonomia.md` es la fuente de verdad del schema, y con esa fuente ambas se resuelven (detalle abajo). **Sigue abierta solo (c):** 2 conceptos que fallan Gate 0 + la decisión sobre sus tags.

Una sola categoría de problema — deuda de schema del frontmatter de conceptos — con tres manifestaciones. Redacción original (2026-09-26, antes de la decisión):

**a) `estado` / `rutina-trabajo-enfocada` — ✅ CERRADA 2026-09-26.** El reporte de poda (`Conocimiento/Mantenimiento/poda-candidatos.md`, 2026-09-26) muestra `rutina-trabajo-enfocada` como "(borrador)". Luigui indicó que `estado` no forma parte del schema no-negociable de conceptos atómicos (titulo, tipo, fecha, familia, categorias_secundarias, tags, relacionado, fuentes) y pidió registrarlo como limpieza aparte, del mismo tipo que `categoria` en la auditoría de mayo.

**Evidencia en el repo que contradice esa lista (verificada 2026-09-26):**
- `Plantillas/taxonomia.md` (plantilla canónica, línea 36, y regla de la línea 72) define `estado: borrador | activo | archivado` como campo del schema.
- Gate 0 (`CLAUDE.md`, regla 9) lista `estado` entre los campos **requeridos**: un concepto sin `estado` falla Gate 0.
- `rutina-trabajo-enfocada` tiene `estado: borrador` real en su frontmatter; 101 de 103 conceptos llevan el campo.
- Herramientas que dependen de `estado`: la rúbrica y la auditoría (fijan activo/borrador), el graduador de borradores, `poda-por-uso.py`, la columna Estado de `ATLAS.md`.

**Resolución (fuente: `Plantillas/taxonomia.md`, líneas 36 y 72, + Gate 0 en `CLAUDE.md` regla 9):** `estado` es campo real y requerido del schema; `rutina-trabajo-enfocada` con `estado: borrador` es correcto — el concepto no pasó Gate 2 en la auditoría del 2026-08-24 (2/4) y hay una propuesta de graduación sin revisar en `Inbox/2026-08-31_1122_borradores-graduados.tmp.md`. **No hay limpieza que hacer y el archivo no se toca.** La lista de campos "no-negociables" que Luigui citó (fuera del repo) no prevalece sobre `taxonomia.md`.

**b) `categorias_secundarias` — ✅ CERRADA 2026-09-26.** No está en `taxonomia.md`; se eliminó de 9 conceptos en la auditoría del 2026-08-24 por ser equivalente al `categoria` prohibido. Hoy hay 0 conceptos con ese campo, pero la lista de Luigui lo incluía como parte del schema. **Resolución (misma fuente):** `taxonomia.md` no lo define (0 menciones), así que no es campo vigente; sigue eliminado y no vuelve al schema.

**c) Dos conceptos sin auditar que fallan hoy — 🔴 ABIERTA** (ambos del 2026-08-28, sin trackear; cuentan en el ATLAS = 103, en el baseline de `vault-brief.md` y en el reporte de poda). Verificado campo por campo contra `taxonomia.md` y Gate 0:

| concepto | Gate 0 (CLAUDE.md regla 9) | taxonomía |
|---|---|---|
| `diseno-multiinteligencia` | falta `estado` (requerido) · lleva `slug` (prohibido) · 7 tags (máx. 5) · 4 `relacionado` (máx. 3) | tags fuera del vocabulario controlado: `sistemas-complejos`, `inteligencia-distribuida`, `epistemologia`, `organizaciones` (existe `organizacion`) |
| `criterio-transferible-vs-respuesta-memorizada` | falta `estado` (requerido) · lleva `slug` (prohibido) · 7 tags (máx. 5) · 4 `relacionado` (máx. 3) | tags fuera del vocabulario controlado: `generalizacion`, `feedback` |

Cumplen: `familia` válida, `relacionado` apunta a conceptos que existen y las tres secciones obligatorias del cuerpo. Es exactamente el mismo tipo de falla que la auditoría del 2026-08-24 normalizó en 6 conceptos (`slug` + `estado` ausente + tags/relacionado sobre el límite); estos dos son posteriores a esa auditoría.

La lista de schema que cita Luigui no está en el repo: no se encontró ningún documento "no-negociable" ni el registro de la Mejora 004 (`categoria`) en `docs/`, `Backlog/` ni `Plantillas/`. Su fuente vive fuera del vault.

## 2. Usuario objetivo
Luigui (dueño del schema) y Jarvis, que aplica Gate 0 sobre lo que dice `taxonomia.md`.

## 3. Casos de uso principales
- ~~Decidir la fuente de verdad del schema (a) y (b).~~ **Hecho 2026-09-26:** `taxonomia.md`.
- Normalizar los 2 conceptos de (c) una vez decidido — `slug`, tags y `relacionado` se arreglan igual con cualquier respuesta; lo de `estado` depende de (a).

## 4. Criterios de aceptación
Pendiente de maduración.

## 5. Fuera de alcance
- Modificar `rutina-trabajo-enfocada.md` (no hay nada que limpiar — ver (a)) ni los 2 conceptos de (c) hasta decidir sus tags (instrucción de Luigui, 2026-09-26: "no tocar ahora").
- ~~Retirar `estado` de `taxonomia.md`/Gate 0~~ **Descartado 2026-09-26:** `estado` es campo del schema.

## 6. Stack / arquitectura
Pendiente de maduración.

## 7. Métricas de éxito
Pendiente de maduración.

## 8. Preguntas abiertas
- ~~¿Cuál es la fuente de verdad del schema: `taxonomia.md` + Gate 0 o la lista de campos no-negociables de Luigui?~~ **Resuelta 2026-09-26 por Luigui: `taxonomia.md`** (define `estado` en las líneas 36/72 y no define `categorias_secundarias`).
- ~~Si `estado` sale del frontmatter, ¿dónde vive el ciclo borrador/activo/archivado?~~ **Moot:** `estado` no sale.
- ~~¿`categorias_secundarias` vuelve al schema?~~ **Resuelta:** no — no está en `taxonomia.md`.
- 🔴 **Abierta.** Para (c): ¿se agregan al vocabulario controlado los tags fuera de lista (`sistemas-complejos`, `inteligencia-distribuida`, `epistemologia`, `generalizacion`, `feedback`) o se reemplazan por tags existentes? Regla 7 de `CLAUDE.md`: los tags nuevos se proponen, no se crean solos. Después: normalizar los 2 conceptos (quitar `slug`, agregar `estado`, dejar ≤5 tags y ≤3 `relacionado`).
