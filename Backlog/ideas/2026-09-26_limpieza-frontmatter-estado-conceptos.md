---
id: limpieza-frontmatter-estado-conceptos
titulo: Limpieza aparte — campo `estado` (y `categorias_secundarias`) en el frontmatter de conceptos
fecha_captura: 2026-09-26
estado: borrador
raiz_proyecto: N/A — vive dentro de ~/Documents/Segundo_cerebro/
tags: [segundo-cerebro, schema, frontmatter, limpieza, gate-0]
---

## 1. Problema
El reporte de poda (`Conocimiento/Mantenimiento/poda-candidatos.md`, 2026-09-26) muestra `rutina-trabajo-enfocada` como "(borrador)". Luigui indicó que `estado` no forma parte del schema no-negociable de conceptos atómicos (titulo, tipo, fecha, familia, categorias_secundarias, tags, relacionado, fuentes) y pidió registrarlo como limpieza aparte, del mismo tipo que `categoria` en la auditoría de mayo. **No se toca ningún concepto hasta resolver esto.**

**Evidencia en el repo que contradice esa lista (verificada 2026-09-26):**
- `Plantillas/taxonomia.md` (plantilla canónica, línea 36, y regla de la línea 72) define `estado: borrador | activo | archivado` como campo del schema.
- Gate 0 (`CLAUDE.md`, regla 9) lista `estado` entre los campos **requeridos**: un concepto sin `estado` falla Gate 0.
- `rutina-trabajo-enfocada` tiene `estado: borrador` real en su frontmatter; 101 de 103 conceptos llevan el campo.
- Herramientas que dependen de `estado`: la rúbrica y la auditoría (fijan activo/borrador), el graduador de borradores, `poda-por-uso.py`, la columna Estado de `ATLAS.md`.
- `categorias_secundarias` **no** está en `taxonomia.md`; se eliminó de 9 conceptos en la auditoría del 2026-08-24 por ser equivalente al `categoria` prohibido. Hoy hay 0 conceptos con ese campo.
- La lista de schema que cita Luigui no está en el repo: no se encontró ningún documento "no-negociable" ni el registro de la Mejora 004 (`categoria`) en `docs/`, `Backlog/` ni `Plantillas/`. Su fuente vive fuera del vault.

## 2. Usuario objetivo
Luigui (dueño del schema) y Jarvis, que aplica Gate 0 sobre lo que dice `taxonomia.md`.

## 3. Casos de uso principales
Pendiente de maduración.

## 4. Criterios de aceptación
Pendiente de maduración.

## 5. Fuera de alcance
- Modificar `rutina-trabajo-enfocada.md` o cualquier otro concepto antes de decidir la fuente de verdad.
- Retirar `estado` de `taxonomia.md`/Gate 0 sin una decisión explícita: hoy el ciclo de vida del concepto vive ahí.

## 6. Stack / arquitectura
Pendiente de maduración.

## 7. Métricas de éxito
Pendiente de maduración.

## 8. Preguntas abiertas
- ¿Cuál es la fuente de verdad del schema: `taxonomia.md` + Gate 0 (lo que Jarvis aplica hoy) o la lista de campos no-negociables de Luigui? Hoy divergen en dos campos: `estado` (en taxonomia, fuera de la lista) y `categorias_secundarias` (en la lista, fuera de taxonomia).
- Si `estado` sale del frontmatter, ¿dónde vive el ciclo borrador/activo/archivado que usan la rúbrica, el graduador, la poda y el ATLAS?
- ¿`categorias_secundarias` vuelve al schema? Se eliminó el 2026-08-24 sin objeción, pero la lista de Luigui lo incluye.
- Dato relacionado, aparte: 2 conceptos nuevos sin auditar (`diseno-multiinteligencia`, `criterio-transferible-vs-respuesta-memorizada`, ambos del 2026-08-28, sin trackear) no tienen `estado` y además llevan `slug` (prohibido), más de 5 tags y más de 3 `relacionado`. Fallan Gate 0 hoy, sea cual sea la respuesta anterior.
