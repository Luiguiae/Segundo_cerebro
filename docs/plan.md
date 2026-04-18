# Plan — Mejora 004: Categorización de Conceptos en Carpetas

**Spec:** `mejora-004-categorizacion-conceptos.md`
**Estado:** pendiente de aprobación
**Riesgo general:** bajo — todos los cambios son reversibles con `git revert`

---

## Resumen

Migrar 34 conceptos planos de `Conocimiento/Conceptos/` a 6 subcarpetas temáticas,
agregar el campo `categoria` al frontmatter de cada archivo, y actualizar
`generar_index.py` para que atraviese subcarpetas y agrupe por categoría en el ATLAS.

---

## Fases

### Fase 1 — Crear las 6 subcarpetas
**Archivos afectados:** solo el filesystem  
**Riesgo:** ninguno — operación aditiva, no mueve ni modifica nada

Crear dentro de `Conocimiento/Conceptos/`:
```
ia/
diseno/
producto/
organizaciones/
economia/
filosofia/
```

---

### Fase 2 — Mover los 34 archivos a sus carpetas
**Archivos afectados:** 34 `.md` en `Conocimiento/Conceptos/`  
**Riesgo:** bajo — git rastrea los moves; Obsidian resuelve `[[wikilinks]]` por nombre de archivo, no por ruta

Mapping completo según el spec:

| Carpeta | Conceptos |
|---------|-----------|
| `ia/` (10) | agentes-ia, automatizacion-vs-ampliacion, capital-de-contexto, conocimiento-autoorganizado-por-llm, espectro-autonomia-agente, fabrica-oscura-de-software, gobernanza-ia-performativa, spec-driven-development, usuarios-sinteticos, vibe-coding |
| `diseno/` (5) | disenador-a-constructor, diseno-dos-velocidades, diseno-uxui-y-ia, fundamentales-vs-flux, quien-controla-el-prompt |
| `producto/` (9) | claridad-antes-de-velocidad, confianza-a-traves-de-velocidad, copiloto-de-producto, expertise-de-dominio-en-producto, feedback-que-escala, mvp-a-prototipo-en-produccion, pit-stop-cognitivo, pmf-perecedero, restriccion-de-tiempo-como-ventaja |
| `organizaciones/` (3) | automatizar-mi-propio-trabajo, condicion-redespliegue, equipos-pequenos-alto-impacto |
| `economia/` (3) | ia-como-filtro-de-entrada, inversion-sesgo-tecnologico, senal-anticipada-mercado-laboral |
| `filosofia/` (4) | arquitectura-de-inteligencia, colonialismo-cultural-digital, lo-ilegible-como-senal, momento-liminal |

**Total: 34 conceptos. 0 archivos quedan en la raíz de `Conceptos/`.**

---

### Fase 3 — Agregar campo `categoria` al frontmatter
**Archivos afectados:** 34 `.md`  
**Riesgo:** bajo — edición aditiva del frontmatter; el campo `familia` no se toca

Por cada archivo se inserta `categoria: [nombre-carpeta]` después del campo `familia`.
Conceptos con peso real en dos categorías reciben además `categorias_secundarias: [otra]`.

Conceptos con categoría secundaria identificados en el spec:
- Ninguno especificado explícitamente en v1 — se agrega solo `categoria`

---

### Fase 4 — Actualizar `generar_index.py`
**Archivos afectados:** `Prompts/Meta/generar_index.py`  
**Riesgo:** medio — cambio en script de infraestructura; verificable corriendo el script antes del commit

Dos cambios quirúrgicos:

**Cambio 1 — `cargar_conceptos()` línea 80:**
```python
# Antes:
for archivo in sorted(directorio.glob("*.md")):
# Después:
for archivo in sorted(directorio.rglob("*.md")):
```
Esto hace que el script traverse subcarpetas automáticamente. Sin este cambio, el ATLAS quedaría vacío tras la migración.

**Cambio 2 — agregar función `agrupar_por_categoria()` y nueva sección en el ATLAS:**
```python
def agrupar_por_categoria(conceptos):
    grupos = defaultdict(list)
    for c in conceptos:
        cat = c.get("categoria", "sin-categoria") or "sin-categoria"
        grupos[cat].append(c)
    return dict(sorted(grupos.items()))
```
Y en `generar_markdown()`, agregar sección "Conceptos por categoría" con el conteo
por carpeta, paralela a la sección "Conceptos por familia" existente.

---

### Fase 5 — Verificar referencias en `Correlaciones/`
**Archivos afectados:** 14 archivos en `Conocimiento/Correlaciones/`  
**Riesgo:** ninguno esperado

Las correlaciones usan slugs en el frontmatter (`conceptos: [slug-a, slug-b]`) y
en el cuerpo como `` `slug` `` o `[[slug]]` — nunca rutas de archivo. Obsidian
resuelve `[[slug]]` por nombre independientemente de la carpeta donde viva el archivo.

Verificar que ninguna correlación use rutas relativas explícitas.

---

### Fase 6 — Regenerar ATLAS y verificar output
**Archivos afectados:** `Conocimiento/ATLAS.md`  
**Riesgo:** ninguno — archivo generado, siempre regenerable

Correr `python3 Prompts/Meta/generar_index.py` y confirmar:
- Conceptos procesados: 34
- 0 conceptos en "sin-categoría"
- Sección nueva "Conceptos por categoría" presente en ATLAS.md

---

### Fase 7 — Commit
```
feat: mejora-004 categorización de conceptos en carpetas
```

Incluye: 34 archivos movidos, frontmatters actualizados, script actualizado, ATLAS regenerado.

---

## Dependencias entre fases

```
Fase 1 → Fase 2 → Fase 3 → Fase 4 → Fase 5 (paralela) → Fase 6 → Fase 7
```

Fases 2 y 3 se ejecutan juntas: al mover cada archivo se agrega el campo `categoria`
en el mismo paso, evitando dos pasadas sobre los 34 archivos.

---

## Criterio de done

- [ ] 0 archivos `.md` en la raíz de `Conocimiento/Conceptos/`
- [ ] Los 34 archivos tienen el campo `categoria` en el frontmatter
- [ ] `generar_index.py` corre sin errores
- [ ] ATLAS.md muestra 34 conceptos con sección por categoría
- [ ] Ninguna correlación tiene referencias rotas
- [ ] Commit limpio en `main`
