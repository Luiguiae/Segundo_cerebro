# JARVIS_LOG

---

### 2026-04-11 — correlación: automatizar-mi-propio-trabajo ↔ expertise-de-dominio-en-producto

**Instrucción:** "par c"

**Rúbrica:**
- Gate 2.1 Tensión real: ✓ — contradicción de secuencia: automatiza para descubrir expertise vs. codifica expertise antes de automatizar
- Gate 2.2 Síntesis no obvia: ✓ — insight central (automatizar es arqueología de expertise tácito; los fallos del agente son el mapa del conocimiento no codificado) no está en ninguno de los dos conceptos por separado
- Gate 2.3 Ambos existen: ✓

**Acciones:**
- `Conocimiento/Correlaciones/2026-04-11_automatizar-mi-propio-trabajo--expertise-de-dominio-en-producto.md`: escrito
- ATLAS regenerado

**Resultados:** **OK**

**ATLAS regenerado:** sí — 20 conceptos · 44 tags únicos · 4 correlaciones en vault

---

### 2026-04-11 — corrección frontmatter 6 conceptos nuevos

**Instrucción:** "corrige antes de pasar a las correlaciones"

**Problemas detectados y corregidos:**

| Concepto | Correcciones |
|----------|-------------|
| `automatizar-mi-propio-trabajo` | + `familia: transicion-ia` · + `estado: activo` · `relacionado` 4→3 (removido `quien-controla-el-prompt`) · tags: reemplazados 4 no controlados (`productividad`, `responsabilidad`, `organizaciones`, `trabajo`) por `organizacion`, `builder`, `principio` |
| `expertise-de-dominio-en-producto` | + `familia: sistemas-conocimiento` · + `estado: activo` · `relacionado` 4→3 (removido `automatizar-mi-propio-trabajo`) · tags: reemplazados `dominio`, `expertise`, `b2b`, `diseño` por `criterio`; reducidos a 5 |
| `feedback-que-escala` | + `familia: velocidad-output` · + `estado: activo` · `relacionado` 4→3 (removido `claridad-antes-de-velocidad`) · tags: reemplazados `feedback`, `calidad`, `proceso`, `diseño`, `organizaciones` por `liderazgo`, `criterio`, `organizacion`; reducidos a 5 |
| `confianza-a-traves-de-velocidad` | + `familia: velocidad-output` · + `estado: activo` · tags: reemplazados `confianza`, `lanzamiento`, `marca` por `principio`; reducidos a 5 |
| `diseno-dos-velocidades` | + `familia: transicion-ia` · + `estado: activo` · `relacionado` 4→3 (removido `fundamentales-vs-flux`) · tags: reemplazados `proceso`, `vision`, `ejecucion` por `criterio`; reducidos a 5 |
| `lo-ilegible-como-senal` | + `familia: epistemologia-practica` · + `estado: activo` · `relacionado` 4→3 (removido `disenador-a-constructor`) · tags: reemplazados `innovacion`, `intuicion`, `deteccion`, `ideas`, `vanguardia` por `criterio`, `captura`, `hipotesis`; reducidos a 5 |

**Resultados:** 6 conceptos — todos **OK**

**ATLAS regenerado:** sí — 20 conceptos · 44 tags únicos · 20 con links

---

### 2026-04-10 11:00 — 2 correlaciones generadas

**Instrucción:** "Par 4 y par 5" (de propuesta de correlaciones de alta tensión)

**Rúbrica aplicada:**

`claridad-antes-de-velocidad--momento-liminal`:
- Gate 1: ✓ atómico · ✓ propio · ✓ frontmatter · ✓ nombre de archivo
- Gate 2.1 Tensión real: ✓ — contradicción directa sobre cuándo llega la claridad
- Gate 2.2 Síntesis no obvia: ✓ — distinción entre claridad de proceso vs. claridad de orientación no se obtiene leyendo ambos conceptos por separado
- Gate 2.3 Ambos existen: ✓

`fundamentales-vs-flux--disenador-a-constructor`:
- Gate 1: ✓ atómico · ✓ propio · ✓ frontmatter · ✓ nombre de archivo
- Gate 2.1 Tensión real: ✓ — ¿construir es fundamental o flux? Los dos conceptos tiran en direcciones opuestas
- Gate 2.2 Síntesis no obvia: ✓ — el insight (lo fundamental no es construir sino el criterio que la construcción entrena) no está en ninguno de los dos conceptos por separado
- Gate 2.3 Ambos existen: ✓

**Acciones:**
- `Conocimiento/Correlaciones/2026-04-10_claridad-antes-de-velocidad--momento-liminal.md`: escrito
- `Conocimiento/Correlaciones/2026-04-10_fundamentales-vs-flux--disenador-a-constructor.md`: escrito
- ATLAS regenerado

**Resultados:**
- `claridad-antes-de-velocidad--momento-liminal`: **OK**
- `fundamentales-vs-flux--disenador-a-constructor`: **OK**

**ATLAS regenerado:** sí — 14 conceptos · 41 tags únicos · 3 correlaciones en vault

---

### 2026-04-10 10:30 — renombrado INDEX.md → ATLAS.md (vault-wide)

**Instrucción:** "Renombra INDEX.md a ATLAS.md, actualiza todas las referencias en el vault, regenera el archivo."

**Acciones:**
- `Conocimiento/INDEX.md` renombrado a `Conocimiento/ATLAS.md`
- `Prompts/Meta/generar_index.py`: OUTPUT_FILE, título, encabezado Context Layer, argparse description, print final — todos actualizados a ATLAS.md
- `CLAUDE.md`: 9 menciones de INDEX/INDEX.md reemplazadas por ATLAS/ATLAS.md
- `Prompts/JARVIS/prompts-jarvis.md`: 14 menciones de INDEX.md/INDEX actualizadas a ATLAS.md/ATLAS
- `Conocimiento/Conceptos/arquitectura-de-inteligencia.md`: 1 mención en cuerpo → ATLAS.md
- `Prompts/Meta/generar_presentacion.py`: INDEX_FILE + mensaje de error → ATLAS.md
- `Prompts/Presentaciones/prompt-generar-presentacion.md`: 1 mención → ATLAS.md
- `Proyectos/correlacion-conceptos/`: 4 archivos actualizados (tasks.md, plan.md, SPEC.md, SKILL.md)
- `Proyectos/rastreador-conocimiento/`: 6 archivos actualizados (SPEC.md, AGENTES.md, plan.md, tareas.md, prompt-rastreador-conocimiento.md, redactor.py, cruzador.py)
- Script ejecutado: ATLAS.md regenerado correctamente

**Resultados:**
- `Conocimiento/ATLAS.md`: **OK** — generado, 14 conceptos, 14/14 con resumen
- `Conocimiento/INDEX.md`: **eliminado** — ya no existe
- Referencias residuales: **0** — vault-wide scan limpio

**ATLAS regenerado:** sí — 14 conceptos procesados · 41 tags únicos · 14 con links

---

### 2026-04-10 09:56 — actualización generar_index.py a v2

**Instrucción:** "Reemplaza generar_index.py con versión que incluye resúmenes, sección por familia y encabezado Context Layer."

**Acciones:**
- `Prompts/Meta/generar_index.py` reescrito a v2
- Nueva función `extract_resumen()`: extrae primer párrafo del cuerpo, ignora frontmatter/encabezados/líneas vacías, trunca a 120 chars
- Tabla principal: nueva columna "Resumen"
- Nueva sección "## Conceptos por familia" con `→ [resumen]` bajo cada concepto
- Encabezado del INDEX: nota "Context Layer — Jarvis lee este archivo al inicio de cada sesión"
- Instrucciones finales: actualizada referencia a `Prompts/JARVIS/prompts-jarvis.md`
- Script ejecutado y INDEX regenerado

**Resultados:**
- `generar_index.py`: **OK** — v2 operacional
- `Conocimiento/INDEX.md`: **OK** — tabla con resúmenes + 5 familias agrupadas

**INDEX regenerado:** sí — 14 conceptos procesados · 14/14 con resumen extraído · 0 sin resumen · 41 tags únicos

---

### 2026-04-10 15:00 — configuración sistema de sesiones

**Instrucción:** "Jarvis, agrega rituales de sesión, crea carpeta Sesiones/, actualiza CLAUDE.md y prompts-jarvis.md, crea sesión inicial, regenera INDEX."

**Acciones:**
- Creada carpeta `Conocimiento/Fuentes/Sesiones/`
- `CLAUDE.md`: agregada sección "Ritual de inicio de sesión" antes de "Reglas que siempre sigues"
- `CLAUDE.md`: agregada sección "Ritual de cierre de sesión" antes de "Reglas que siempre sigues"
- `CLAUDE.md`: actualizada estructura de carpetas — agregada línea `Sesiones/` bajo `Fuentes/`
- `CLAUDE.md`: agregado comando "Cerrar sesión" en sección "Comandos que entiendes"
- `Prompts/JARVIS/prompts-jarvis.md`: agregada sección "5 · Gestión de sesiones" (prompts 5.1 y 5.2)
- `Prompts/JARVIS/prompts-jarvis.md`: actualizada tabla de referencia rápida
- `Conocimiento/Fuentes/Sesiones/2026-04-10.md`: creada sesión inicial con estado del vault

**Resultados:**
- `Conocimiento/Fuentes/Sesiones/`: **OK** — carpeta creada
- `CLAUDE.md`: **OK** — dos secciones de ritual agregadas + estructura + comando
- `Prompts/JARVIS/prompts-jarvis.md`: **OK** — sección 5 agregada
- `Conocimiento/Fuentes/Sesiones/2026-04-10.md`: **OK** — sesión inicial creada

**INDEX regenerado:** sí — 14 conceptos procesados, 41 tags únicos, 14 conceptos con links

---

### 2026-04-07 — renombrado equipos-pequeños → equipos-pequenos

**Instrucción:** "ok, realiza el cambio"

**Acciones:**
- `equipos-pequeños-alto-impacto.md` renombrado a `equipos-pequenos-alto-impacto.md` (eliminado `ñ`)
- Referencias `[[equipos-pequeños-alto-impacto]]` actualizadas en 4 conceptos: `disenador-a-constructor.md`, `vibe-coding.md`, `agentes-ia.md`, `mvp-a-prototipo-en-produccion.md`
- `equipos-pequenos-alto-impacto.md`: `borrador` → `activo`
- INDEX regenerado
- `Plantillas/taxonomia.md`: referencia al nombre antiguo persiste — no modificable por Jarvis; actualizar manualmente

**Resultados:**
- `equipos-pequenos-alto-impacto.md`: **OK** → activo

**INDEX regenerado:** sí — 14 conceptos, 41 tags únicos, 14 conceptos con links

---

### 2026-04-07 — corrección de frontmatter + auditoría final

**Instrucción:** "Corrige el frontmatter de los 11 conceptos en borrador: tags ≤5 (más específicos sobre genéricos), relacionado ≤3 (vínculos más directos). Luego auditoría completa, promueve los que pasen, regenera INDEX."

**Acciones:**
- Corregidos tags en 11 conceptos: reducidos a ≤5, eliminando los más genéricos (`ia` en 7 conceptos, `producto` y `construccion` donde eran secundarios)
- Corregido `relacionado` en 6 conceptos: reducidos a ≤3, eliminando vínculos más débiles (en todos los casos se eliminó `equipos-pequeños-alto-impacto` como referencia)
- Corregidos tags inválidos: `organizaciones` → `organizacion`; `tecnología`/`descolonización` → sin acentos; tags multi-palabra reemplazados por tags controlados de una sola palabra
- `diseno-uxui-y-ia.md`: `relacionado` corregido de títulos legibles a slugs kebab-case
- Promovidos 10 conceptos de `borrador` → `activo`
- INDEX regenerado

**Auditoría final — resultados:**

| archivo | gate 1 | gate 2 | resultado | estado |
|---------|--------|--------|-----------|--------|
| `claridad-antes-de-velocidad.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `arquitectura-de-inteligencia.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `spec-driven-development.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `disenador-a-constructor.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `vibe-coding.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `mvp-a-prototipo-en-produccion.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `usuarios-sinteticos.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `quien-controla-el-prompt.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `momento-liminal.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `fundamentales-vs-flux.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `agentes-ia.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `colonialismo-cultural-digital.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `diseno-uxui-y-ia.md` | ✓✓✓✓ | ✓✓✓✓ | **OK** | activo |
| `equipos-pequeños-alto-impacto.md` | ✓✓✓✗ | ✓✓✓✓ | ADVERTENCIA | borrador |
| `2026-04-03_vibe-coding--spec-driven-development.md` | ✓✓✓✓ | ✓✓✓ | **OK** | activo |

**Decisiones de tag por concepto:**
- `disenador-a-constructor`: eliminado `ia` (genérico)
- `vibe-coding`: eliminado `ia` (genérico)
- `mvp-a-prototipo-en-produccion`: eliminados `ia` y `producto` (genéricos); conservados los 5 más específicos del concepto
- `usuarios-sinteticos`: eliminado `ia` (genérico)
- `equipos-pequeños-alto-impacto`: eliminado `ia` (genérico)
- `quien-controla-el-prompt`: eliminados `ia`, `producto`, `organizaciones`; reemplazado por `organizacion` (tag válido)
- `momento-liminal`: eliminado `ia` (genérico)
- `fundamentales-vs-flux`: eliminados `ia` y `cambio` (genéricos)
- `agentes-ia`: eliminados `producto` y `construccion` (secundarios); `ia` conservado porque es central al concepto
- `colonialismo-cultural-digital`: tags con acentos normalizados; `tecnología` reemplazado por `sistemas`; añadido `colonialismo`
- `diseno-uxui-y-ia`: tags multi-palabra reemplazados por [diseño, ia, producto, criterio, herramientas]

**Bloqueador pendiente:**
- `equipos-pequeños-alto-impacto.md` — Gate 1.4: nombre de archivo contiene `ñ` (acento), viola convención kebab sin acentos. Permanece en `borrador`. Para promover: renombrar a `equipos-pequenos-alto-impacto.md` y actualizar todas las referencias en otros conceptos y correlaciones.

**INDEX regenerado:** sí — 14 conceptos procesados, 41 tags únicos (↓ de 45), 14 conceptos con links

---

### 2026-04-07 — tercera auditoría completa del vault

**Instrucción:** "Lee CLAUDE.md y audita el vault. Reporta el resultado al final."

**Acciones:**
- Leídos `taxonomia.md` y `rubrica.md`
- Leídos 14 conceptos en `Conocimiento/Conceptos/`
- Leída 1 correlación en `Conocimiento/Correlaciones/`
- Evaluados Gate 1 y Gate 2 contra rúbrica vigente
- INDEX regenerado con `generar_index.py`

**Resultados:**

| archivo | resultado | estado |
|---------|-----------|--------|
| `claridad-antes-de-velocidad.md` | **OK** | activo |
| `arquitectura-de-inteligencia.md` | **OK** | activo |
| `spec-driven-development.md` | **OK** | activo |
| `2026-04-03_vibe-coding--spec-driven-development.md` | **OK** | activo |
| `disenador-a-constructor.md` | ADVERTENCIA | borrador |
| `vibe-coding.md` | ADVERTENCIA | borrador |
| `agentes-ia.md` | ADVERTENCIA | borrador |
| `mvp-a-prototipo-en-produccion.md` | ADVERTENCIA | borrador |
| `usuarios-sinteticos.md` | ADVERTENCIA | borrador |
| `equipos-pequeños-alto-impacto.md` | ADVERTENCIA | borrador |
| `quien-controla-el-prompt.md` | ADVERTENCIA | borrador |
| `momento-liminal.md` | ADVERTENCIA | borrador |
| `fundamentales-vs-flux.md` | ADVERTENCIA | borrador |
| `colonialismo-cultural-digital.md` | ADVERTENCIA | borrador |
| `diseno-uxui-y-ia.md` | ADVERTENCIA | borrador |

**Sin cambios de estado:** Las advertencias persisten sin modificar desde la segunda auditoría. Requieren decisión de Luigui (ver propuestas en entrada anterior). Los 3 conceptos activos mantienen su estado correctamente.

**INDEX regenerado:** sí — 14 conceptos procesados, 45 tags únicos, 14 conceptos con links

---

### 2026-04-07 — segunda auditoría + reparaciones

**Instrucción:** "Aplica familias, agrega tags, reescribe rechazados, crea concepto faltante, limpia relacionado, regenera INDEX, segunda auditoría"

**Acciones:**
- `familia` añadido a los 11 conceptos existentes
- 23 tags nuevos añadidos a `Plantillas/taxonomia.md` en sus categorías correspondientes
- `diseno-uxui-y-ia.md`: cuerpo reescrito completo (Gate 1.2 subsanado)
- `spec-driven-development.md`: creado desde cero en `Conceptos/`
- `relacionado` limpiado en 5 archivos (referencias a inexistentes eliminadas, excesos reducidos a máx 3)
- `INDEX.md` regenerado: 14 conceptos, 45 tags únicos

**Segunda auditoría — resultados:**

| archivo | resultado | razón |
|---------|-----------|-------|
| `spec-driven-development.md` | **OK → activo** | Pasa Gate 1 y Gate 2 completos; frontmatter canónico sin extras |
| `2026-04-03_vibe-coding--spec-driven-development.md` | **OK → activo** | Gate 2 correlación: tensión real ✓, síntesis no obvia ✓, ambos conceptos ahora existen ✓ |
| `diseno-uxui-y-ia.md` | ADVERTENCIA | Gate 1.3: tags multi-palabra y con acentos (`diseño de experiencia de usuario`, `ux/ui`) no conformes; promovido de RECHAZADO a ADVERTENCIA |
| `disenador-a-constructor.md` | ADVERTENCIA | Gate 1.3: 6 tags (máx 5); `relacionado` tiene 4 entradas (máx 3) |
| `vibe-coding.md` | ADVERTENCIA | Gate 1.3: 6 tags (máx 5); `relacionado` tiene 4 entradas (máx 3) |
| `agentes-ia.md` | ADVERTENCIA | Gate 1.3: 7 tags (máx 5) — relacionado ya corregido a 3 |
| `mvp-a-prototipo-en-produccion.md` | ADVERTENCIA | Gate 1.3: 7 tags (máx 5); `relacionado` tiene 4 entradas (máx 3) |
| `usuarios-sinteticos.md` | ADVERTENCIA | Gate 1.3: 6 tags (máx 5); `relacionado` tiene 4 entradas (máx 3) |
| `equipos-pequeños-alto-impacto.md` | ADVERTENCIA | Gate 1.3: 6 tags (máx 5); `relacionado` tiene 4 entradas (máx 3) |
| `colonialismo-cultural-digital.md` | ADVERTENCIA | Gate 1.3: tags con acentos (`tecnología`, `descolonización`) y `tecnologia` no en lista controlada |
| `quien-controla-el-prompt.md` | ADVERTENCIA | Gate 1.3: 7 tags (máx 5); `organizaciones` no es tag controlado (debería ser `organizacion`) |
| `momento-liminal.md` | ADVERTENCIA | Gate 1.3: 6 tags (máx 5) |
| `fundamentales-vs-flux.md` | ADVERTENCIA | Gate 1.3: 7 tags (máx 5) |

**Cambios de estado aplicados en segunda auditoría:**
- `spec-driven-development.md`: `borrador` → `activo`
- `2026-04-03_vibe-coding--spec-driven-development.md`: `borrador` → `activo`

**Bloqueador sistémico persistente:** Los conceptos originales (creados antes de que existiera `taxonomia.md`) tienen entre 6 y 7 tags, excediendo el máximo de 5. Son 10 archivos afectados. Ninguno puede llegar a `activo` sin reducir sus tags. Requiere decisión de Luigui sobre cuáles conservar por archivo.

**[PROPUESTA] Reducción de tags pendiente por archivo:**

| archivo | tags actuales | acción necesaria |
|---------|--------------|-----------------|
| `disenador-a-constructor.md` | [diseño, construccion, ia, roles, producto, transformacion] | eliminar 1 tag |
| `vibe-coding.md` | [construccion, ia, herramientas, desarrollo, producto, velocidad] | eliminar 1 tag |
| `agentes-ia.md` | [agentes, ia, equipos, automatizacion, producto, escala, construccion] | eliminar 2 tags |
| `mvp-a-prototipo-en-produccion.md` | [producto, mvp, velocidad, iteracion, aprendizaje, construccion, ia] | eliminar 2 tags |
| `usuarios-sinteticos.md` | [research, validacion, ia, producto, usuarios, diseño] | eliminar 1 tag |
| `equipos-pequeños-alto-impacto.md` | [equipos, producto, ia, velocidad, organizacion, startups] | eliminar 1 tag |
| `quien-controla-el-prompt.md` | [ia, diseño, producto, estrategia, organizaciones, poder, prompts] | eliminar 2 tags; cambiar `organizaciones` → `organizacion` |
| `momento-liminal.md` | [liderazgo, cambio, incertidumbre, transicion, ia, diseño] | eliminar 1 tag |
| `fundamentales-vs-flux.md` | [diseño, educacion, ia, habilidades, fundamentos, cambio, criterio] | eliminar 2 tags |
| `colonialismo-cultural-digital.md` | [tecnología, cultura, descolonización, poder] — 4 tags pero con acentos | normalizar a kebab sin acentos; `tecnologia` no en lista controlada |
| `diseno-uxui-y-ia.md` | [diseño de experiencia de usuario, inteligencia artificial, ux/ui] | reemplazar por tags controlados de una sola palabra |

**[PROPUESTA] Reducción de relacionado pendiente:**

| archivo | relacionado actual | acción |
|---------|-------------------|--------|
| `disenador-a-constructor.md` | 4 entradas | eliminar 1 |
| `vibe-coding.md` | 4 entradas | eliminar 1 |
| `mvp-a-prototipo-en-produccion.md` | 4 entradas | eliminar 1 |
| `usuarios-sinteticos.md` | 4 entradas | eliminar 1 |
| `equipos-pequeños-alto-impacto.md` | 4 entradas | eliminar 1 |

**INDEX regenerado:** sí — 14 conceptos procesados, 45 tags únicos, 14 conceptos con links

---

### 2026-04-07 — audita el vault

**Instrucción:** "Jarvis, audita el vault"

**Acciones:**
- Leídos 11 conceptos en `Conocimiento/Conceptos/`
- Leída 1 correlación en `Conocimiento/Correlaciones/`
- Evaluados contra Gate 1 y Gate 2 de `Plantillas/rubrica.md`
- Actualizados campos `estado` en frontmatter de cada archivo
- Ejecutado `Prompts/Meta/generar_index.py`

**Resultados:**

| archivo | resultado | razón principal |
|---------|-----------|-----------------|
| `colonialismo-cultural-digital.md` | ADVERTENCIA | Falta `familia`; `relacionado` tiene 4 entradas (máx 3); campos no-canónicos en frontmatter |
| `diseno-uxui-y-ia.md` | RECHAZADO | Gate 1.2 falla: cuerpo lee como resumen de artículo sin interpretación propia; falta `familia` |
| `equipos-pequeños-alto-impacto.md` | ADVERTENCIA | Falta `familia`; `estado: consolidado` no es valor válido en taxonomía; tag `startups` no controlado |
| `quien-controla-el-prompt.md` | ADVERTENCIA | Falta `familia`; `estado` ausente (añadido); `relacionado` apunta a `arquitectura-de-inteligencia` y `claridad-antes-de-velocidad` que no existen en `Conceptos/`; tags `poder` y `prompts` no controlados |
| `momento-liminal.md` | ADVERTENCIA | Falta `familia`; `estado` ausente (añadido); `relacionado` apunta a `claridad-antes-de-velocidad` y `arquitectura-de-inteligencia` que no existen; tags `liderazgo`, `cambio`, `incertidumbre` no controlados |
| `fundamentales-vs-flux.md` | ADVERTENCIA | Falta `familia`; `estado` ausente (añadido); `relacionado` apunta a `claridad-antes-de-velocidad` que no existe; tags `educacion`, `habilidades`, `fundamentos`, `cambio`, `criterio` no controlados |
| `usuarios-sinteticos.md` | ADVERTENCIA | Falta `familia`; tags `research`, `validacion`, `usuarios` no controlados |
| `mvp-a-prototipo-en-produccion.md` | ADVERTENCIA | Falta `familia`; `estado: consolidado` no válido (corregido a `borrador`); tags `mvp`, `aprendizaje` no controlados |
| `vibe-coding.md` | ADVERTENCIA | Falta `familia`; `estado: consolidado` no válido (corregido a `borrador`); tags `herramientas`, `desarrollo` no controlados |
| `agentes-ia.md` | ADVERTENCIA | Falta `familia`; `estado: consolidado` no válido (corregido a `borrador`); `relacionado` tiene 5 entradas (máx 3); tags `escala` no controlado |
| `disenador-a-constructor.md` | ADVERTENCIA | Falta `familia`; `estado: consolidado` no válido (corregido a `borrador`); tags `roles`, `transformacion` no controlados |
| `2026-04-03_vibe-coding--spec-driven-development.md` | RECHAZADO | Gate 2 correlación falla: `spec-driven-development` no existe como archivo en `Conceptos/`; `estado` ausente (añadido) |

**Cambios de estado aplicados:**
- `equipos-pequeños-alto-impacto.md`: `consolidado` → `borrador`
- `vibe-coding.md`: `consolidado` → `borrador`
- `agentes-ia.md`: `consolidado` → `borrador`
- `mvp-a-prototipo-en-produccion.md`: `consolidado` → `borrador`
- `disenador-a-constructor.md`: `consolidado` → `borrador`
- `quien-controla-el-prompt.md`: campo `estado` añadido como `borrador`
- `momento-liminal.md`: campo `estado` añadido como `borrador`
- `fundamentales-vs-flux.md`: campo `estado` añadido como `borrador`
- `2026-04-03_vibe-coding--spec-driven-development.md`: campo `estado` añadido como `borrador`

**Ningún concepto promovido a `activo`** — todos fallan Gate 1.3 por falta del campo `familia`.

---

**[PROPUESTA] Tags a añadir a `taxonomia.md`**

Los siguientes tags están en uso en el vault pero no están en la lista controlada. Requieren confirmación de Luigui antes de validarse:

| tag usado | aparece en | categoría sugerida |
|-----------|-----------|-------------------|
| `poder` | quien-controla-el-prompt | Postura epistémica |
| `prompts` | quien-controla-el-prompt | Dominio |
| `liderazgo` | momento-liminal | Perfil / audiencia |
| `cambio` | momento-liminal, fundamentales-vs-flux | Temporalidad |
| `incertidumbre` | momento-liminal | Postura epistémica |
| `educacion` | fundamentales-vs-flux | Dominio |
| `habilidades` | fundamentales-vs-flux | Dominio |
| `fundamentos` | fundamentales-vs-flux | Postura epistémica |
| `criterio` | fundamentales-vs-flux | Postura epistémica |
| `research` | usuarios-sinteticos | Proceso |
| `validacion` | usuarios-sinteticos | Proceso (alternativa a `evaluacion`) |
| `usuarios` | usuarios-sinteticos | Perfil / audiencia |
| `startups` | equipos-pequeños-alto-impacto | Dominio |
| `mvp` | mvp-a-prototipo-en-produccion | Dominio |
| `aprendizaje` | mvp-a-prototipo-en-produccion | Proceso |
| `herramientas` | vibe-coding | Dominio |
| `desarrollo` | vibe-coding | Dominio |
| `escala` | agentes-ia | Dominio |
| `roles` | disenador-a-constructor | Perfil / audiencia |
| `transformacion` | disenador-a-constructor | Temporalidad |
| `cultura` | colonialismo-cultural-digital | Dominio |
| `colonialismo` | colonialismo-cultural-digital | Dominio |
| `descolonizacion` | colonialismo-cultural-digital | Dominio |

**[PROPUESTA] Conceptos faltantes referenciados en `relacionado`**

Los siguientes conceptos son referenciados por archivos existentes pero no tienen archivo en `Conceptos/`. Requieren creación o eliminación de la referencia:

| concepto faltante | referenciado por |
|-------------------|-----------------|
| `arquitectura-de-inteligencia` | quien-controla-el-prompt, momento-liminal |
| `claridad-antes-de-velocidad` | quien-controla-el-prompt, momento-liminal, fundamentales-vs-flux |
| `spec-driven-development` | 2026-04-03_vibe-coding--spec-driven-development.md |

**[PROPUESTA] Campo `familia` — asignación sugerida**

Todos los conceptos del vault carecen del campo `familia`. Asignaciones propuestas según taxonomía (requieren confirmación):

| concepto | familia sugerida |
|----------|----------------|
| `disenador-a-constructor` | `transicion-ia` |
| `momento-liminal` | `transicion-ia` |
| `fundamentales-vs-flux` | `transicion-ia` |
| `vibe-coding` | `velocidad-output` |
| `quien-controla-el-prompt` | `velocidad-output` |
| `mvp-a-prototipo-en-produccion` | `velocidad-output` |
| `equipos-pequeños-alto-impacto` | `equipos-impacto` |
| `usuarios-sinteticos` | `equipos-impacto` |
| `agentes-ia` | `agencia-ia` |
| `colonialismo-cultural-digital` | `epistemologia-practica` |
| `diseno-uxui-y-ia` | `transicion-ia` (pendiente reescritura) |

**INDEX regenerado:** sí — 11 conceptos procesados, 39 tags únicos, 11 conceptos con links

---
