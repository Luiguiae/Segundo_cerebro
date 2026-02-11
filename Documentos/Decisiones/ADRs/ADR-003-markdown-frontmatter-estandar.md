---
titulo: "ADR-003: Markdown + Frontmatter como formato estándar LLM-friendly"
tipo: adr
estado: aceptado
autor: Luigui Avila
fecha: 2026-01-11
updated: 2026-02-10
tags: [formato, markdown, frontmatter, estandar]
fuentes:
  - Documentos/00-start-here/README.md
  - Plantillas/prd-plantilla.md
  - Plantillas/adr-plantilla.md
  - Plantillas/bench-plantilla.md
---

## Contexto

El repositorio Segundo Cerebro está diseñado para trabajar con LLMs (Cursor) y documentar pensamiento, decisiones y diseño, según `Documentos/00-start-here/README.md`. Para maximizar recuperación de contexto, trazabilidad y versionado, se requiere un formato primario consistente.

La información generada suele venir en múltiples formatos:
- Notas sueltas en diversos formatos
- Conversaciones de chat
- Documentos en formatos binarios (Word, PDF)
- Screenshots e imágenes
- PDFs con contenido no indexable

Esta diversidad de formatos reduce la capacidad de:
- **Búsqueda:** Los LLMs no pueden buscar eficientemente en formatos binarios
- **Chunking:** Difícil dividir contenido en fragmentos útiles para contexto
- **Reutilización:** Los agentes no pueden extraer y reutilizar información fácilmente
- **Versionado:** Los diffs en formatos binarios no son útiles para tracking de cambios

Además, sin metadatos consistentes es difícil:
- Filtrar por autor, fecha, estado o tags
- Identificar tipo de documento
- Establecer trazabilidad entre documentos relacionados
- Mantener consistencia en plantillas (como `Plantillas/prd-plantilla.md`, `Plantillas/adr-plantilla.md`, `Plantillas/bench-plantilla.md`)

## Decisión

Se adopta **Markdown (.md)** como formato primario para todo contenido del repositorio, acompañado de un bloque de metadatos estándar al inicio (frontmatter YAML o un bloque de metadatos consistente en Markdown).

### Reglas

1. **Formato primario:** Todo documento nuevo debe ser `.md`

2. **Metadatos mínimos obligatorios:** Todo documento debe iniciar con metadatos que incluyan:
   - `titulo` o `title`
   - `tipo` o `type`
   - `estado` o `status`
   - `autor` o `owner`
   - `fecha` o `date`
   - `updated` (fecha de última actualización)
   - `tags` (array de tags)
   - `fuente(s)` o `fuentes` (referencias a documentos origen)

3. **Prioridad de texto plano:** Se prioriza texto plano estructurado con headings y listas sobre formatos binarios

4. **Anexos:** PDFs, imágenes y otros formatos se permiten solo como anexos, pero deben tener un `.md` asociado que:
   - Resuma el contenido del anexo
   - Contextualice el contenido
   - Incluya metadatos estándar
   - Referencie la ubicación del anexo

5. **Estandarización transversal:** Esta regla aplica a todos los tipos de documentos:
   - PRDs (`Documentos/PRDS/`)
   - ADRs (`Documentos/Decisiones/ADRs/`)
   - Estudios (`Documentos/Estudios/`)
   - Benchmarks (`Documentos/Benchmarks/`)
   - Research (`Documentos/Research/`)
   - Procesos (`Documentos/Procesos/`)
   - Presentaciones (`Documentos/Presentaciones/`)

## Alternativas consideradas

**1. Mantener múltiples formatos sin estándar**
- **Descartada porque:** Reduce capacidad de búsqueda, chunking y reutilización por agentes. Dificulta versionado y trazabilidad. No maximiza recuperación de contexto para LLMs.

**2. Usar solo texto plano sin metadatos estructurados**
- **Descartada porque:** Sin metadatos consistentes es difícil filtrar por autor, fecha, estado, tags o tipo de documento. Reduce capacidad de establecer trazabilidad entre documentos relacionados.

**3. Adoptar otro formato estructurado (JSON, YAML, XML)**
- **Descartada porque:** Aunque estructurados, no son tan legibles para humanos como Markdown. Requieren herramientas especializadas para edición. Markdown es más accesible y ampliamente soportado por LLMs.

**4. Usar Markdown sin frontmatter, solo estructura de headings**
- **Descartada porque:** Aunque mejora búsqueda y chunking, no permite filtrado por metadatos. No facilita trazabilidad ni identificación de tipo de documento. Las plantillas existentes (`Plantillas/prd-plantilla.md`, `Plantillas/adr-plantilla.md`) ya usan frontmatter.

**5. Adoptar Markdown + Frontmatter como formato estándar**
- **Seleccionada porque:** Maximiza recuperación de contexto, trazabilidad y versionado. Permite búsqueda eficiente, chunking útil y reutilización por agentes. Facilita filtrado por metadatos y mantiene legibilidad para humanos. Es consistente con plantillas existentes.

## Consecuencias

### Positivas

- **Mejor búsqueda, lectura y recuperación de contexto por LLMs:** Markdown es fácilmente parseable y indexable por LLMs, mejorando capacidad de encontrar y usar información relevante
- **Versionado limpio:** Los diffs en Markdown son útiles y legibles, permitiendo tracking efectivo de cambios en el tiempo
- **Estandarización transversal:** Aplica consistentemente a PRDs, ADRs, estudios, benchmarks, procesos y workshops, creando ecosistema coherente
- **Filtrado por metadatos:** Permite filtrar documentos por autor, fecha, estado, tags o tipo, facilitando navegación y organización
- **Trazabilidad mejorada:** Los metadatos de `fuente(s)` permiten establecer relaciones entre documentos
- **Legibilidad humana:** Markdown es fácil de leer y editar sin herramientas especializadas
- **Compatibilidad:** Ampliamente soportado por herramientas de versionado, editores y LLMs

### Negativas / Riesgos

- **Requiere disciplina para transformar insumos:** Necesita esfuerzo consciente para convertir PDFs, notas sueltas, chats y otros formatos a Markdown estructurado
- **Trabajo extra al inicio:** Puede implicar trabajo adicional al resumir y normalizar contenido existente en otros formatos
- **Curva de aprendizaje:** Requiere familiaridad con sintaxis Markdown y estructura de frontmatter
- **Riesgo de inconsistencia:** Sin disciplina, documentos pueden no seguir el estándar de metadatos, reduciendo beneficios
- **Mantenimiento de anexos:** Requiere mantener sincronización entre documentos `.md` y sus anexos (PDFs, imágenes)
- **Limitaciones de Markdown:** Algunos formatos complejos (tablas muy complejas, fórmulas matemáticas) pueden requerir extensiones o alternativas

## Notas

- Esta decisión establece el formato estándar para todo contenido nuevo en el Segundo Cerebro
- Los documentos existentes en otros formatos deben migrarse gradualmente a Markdown con metadatos estándar
- Las plantillas existentes (`Plantillas/prd-plantilla.md`, `Plantillas/adr-plantilla.md`, `Plantillas/bench-plantilla.md`) ya siguen este patrón y deben usarse como referencia
- Los LLMs que trabajen con el repositorio deben ser instruidos a crear documentos en Markdown con frontmatter estándar
- El frontmatter puede usar YAML (entre `---`) o formato Markdown consistente, pero debe ser parseable y estructurado
- Los metadatos mínimos son obligatorios; campos adicionales pueden agregarse según necesidad del tipo de documento

---

**Referencias:**
- `Documentos/00-start-here/README.md` - Estructura oficial del repositorio
- `Plantillas/prd-plantilla.md` - Plantilla para PRDs con frontmatter
- `Plantillas/adr-plantilla.md` - Plantilla para ADRs con frontmatter
- `Plantillas/bench-plantilla.md` - Plantilla para benchmarks
- `Documentos/Decisiones/ADRs/ADR-002-separacion-research-estudios-decisiones.md` - Separación de carpetas
