---
titulo: "ADR-004: Convención de nombres, slugs y numeración"
tipo: adr
estado: aceptado
autor: Luigui Avila
fecha: 2026-01-11
updated: 2026-02-10
tags: [convencion, nombres, slugs, organizacion]
fuentes:
  - Documentos/Decisiones/ADRs/
  - Documentos/00-start-here/README.md
  - Documentos/Estudios/
  - Documentos/Research/
  - Documentos/PRDS/
  - Documentos/Benchmarks/
  - Documentos/Procesos/
  - Documentos/Presentaciones/
---

# ADR-004: Convención de nombres, slugs y numeración para el Segundo Cerebro

## Contexto

El repositorio Segundo Cerebro crecerá de forma continua y será utilizado como fuente de contexto para LLMs (Cursor), según `Documentos/00-start-here/README.md`. El repositorio contiene múltiples tipos de documentos organizados en carpetas:

- `Documentos/Decisiones/ADRs/` - Decisiones arquitectónicas
- `Documentos/Estudios/` - Análisis profundos o exploratorios
- `Documentos/Research/` - Investigación, hallazgos, insights
- `Documentos/PRDS/` - PRDs de productos
- `Documentos/Benchmarks/` - Comparativas y evaluaciones
- `Documentos/Procesos/` - Flujos, procesos, BPMN, Mermaid
- `Documentos/Presentaciones/` - Presentaciones, workshops, charlas

Sin una convención estricta de nombres de archivos y carpetas, se generan problemas:

- **Ambigüedades:** Nombres similares o duplicados dificultan identificación única
- **Duplicaciones:** Archivos con nombres como `documento-final.md`, `documento-v2.md`, `documento-nuevo.md` crean confusión
- **Dificultades de búsqueda:** LLMs y humanos no pueden buscar eficientemente sin patrones consistentes
- **Referencia cruzada:** Difícil referenciar documentos entre sí sin nombres estables
- **Automatización futura:** Scripts, agentes y pipelines requieren patrones predecibles para funcionar correctamente

La falta de convención también dificulta el cumplimiento de las reglas obligatorias para uso con LLM documentadas en `Documentos/00-start-here/README.md`, especialmente "NO inventar carpetas ni rutas" y "Usar SIEMPRE los nombres exactos definidos arriba".

## Decisión

Se establece una convención obligatoria de nombres para archivos y carpetas en el Segundo Cerebro.

### Reglas generales

1. **kebab-case:** Usar palabras en minúscula separadas por guiones (`-`)
2. **Sin espacios:** Evitar espacios en nombres de archivos y carpetas
3. **Sin mayúsculas:** Usar solo minúsculas (excepto prefijos específicos como ADR-)
4. **Sin acentos:** Eliminar acentos y caracteres especiales
5. **Sin caracteres especiales:** Evitar caracteres como `@`, `#`, `$`, `%`, `&`, `*`, `()`, `[]`, `{}`
6. **Descriptivos:** Los nombres deben describir claramente el contenido
7. **Estables:** Los nombres no deben cambiar con el tiempo (excepto correcciones de errores)

### Convenciones específicas por tipo

**ADRs:**
- Formato: `ADR-00X-descripcion-corta.md`
- Ejemplo: `ADR-001-usuarios-sinteticos.md`
- Numeración: Secuencial (ADR-001, ADR-002, ADR-003, etc.)
- El número nunca cambia, aunque el archivo se edite

**Estudios:**
- Formato: `tema-principal.md`
- Ejemplo: `usuarios-sinteticos.md`
- Sin numeración, solo tema descriptivo

**Research:**
- Formato: `exploracion-tema.md`
- Ejemplo: `exploracion-usuarios-sinteticos.md`
- Enfocado en exploración temprana

**PRDs:**
- Formato: `prd-nombre-del-producto.md`
- Ejemplo: `prd-segundo-cerebro.md`
- Prefijo `prd-` para identificación rápida

**Benchmarks:**
- Formato: `benchmark-tema.md`
- Ejemplo: `benchmark-herramientas-ia.md`
- Prefijo `benchmark-` para identificación rápida

**Procesos:**
- Formato: `proceso-nombre.md`
- Ejemplo: `proceso-investigacion-usuarios.md`
- Prefijo `proceso-` para identificación rápida

**Presentaciones:**
- Formato: `presentacion-tema.md`
- Ejemplo: `presentacion-segundo-cerebro.md`
- Prefijo `presentacion-` para identificación rápida

**Workshops:**
- Formato: `workshop-tema.md`
- Ejemplo: `workshop-usuarios-sinteticos.md`
- Prefijo `workshop-` para identificación rápida

### Prohibiciones explícitas

Se prohíbe el uso de:
- Sufijos de versión: `final`, `v2`, `v3`, `nuevo`, `actualizado`
- Indicadores temporales: `ok`, `listo`, `terminado`, `borrador`
- Caracteres especiales: espacios, mayúsculas innecesarias, acentos, símbolos
- Nombres genéricos: `documento.md`, `archivo.md`, `test.md`

## Alternativas consideradas

**1. Mantener nombres libres sin convención**
- **Descartada porque:** Genera ambigüedades, duplicaciones y dificultades para búsqueda, referencia cruzada y automatización. No cumple con reglas obligatorias de "NO inventar carpetas ni rutas" y "Usar SIEMPRE los nombres exactos definidos arriba".

**2. Usar camelCase en lugar de kebab-case**
- **Descartada porque:** Aunque válido técnicamente, kebab-case es más legible en URLs, más compatible con sistemas de archivos y más común en documentación. Los ADRs existentes ya usan kebab-case.

**3. Permitir espacios y caracteres especiales**
- **Descartada porque:** Genera problemas de compatibilidad entre sistemas operativos, dificulta uso en scripts y automatización, y complica referencia cruzada en Markdown.

**4. Usar numeración secuencial para todos los tipos de documentos**
- **Descartada porque:** Añade complejidad innecesaria. Solo ADRs requieren numeración secuencial para mantener orden cronológico de decisiones. Otros tipos de documentos se identifican mejor por tema.

**5. Permitir sufijos de versión (v2, final, nuevo)**
- **Descartada porque:** Crea duplicaciones y confusión. Los cambios deben documentarse en el contenido del archivo o mediante versionado de Git, no en el nombre del archivo.

**6. Establecer convención estricta de kebab-case con prefijos específicos**
- **Seleccionada porque:** Proporciona consistencia cognitiva y técnica, facilita búsqueda y referencia cruzada, permite automatización futura, y es compatible con sistemas existentes. Los prefijos permiten identificación rápida del tipo de documento.

## Consecuencias

### Positivas

- **Consistencia cognitiva y técnica:** Nombres predecibles facilitan navegación y comprensión del repositorio para humanos y LLMs
- **Mejor referencia cruzada:** Nombres estables permiten referenciar documentos entre sí sin riesgo de rotura de enlaces
- **Facilita automatización:** Scripts, agentes y pipelines pueden trabajar con patrones predecibles
- **Búsqueda mejorada:** LLMs y herramientas de búsqueda pueden encontrar documentos más eficientemente
- **Compatibilidad:** kebab-case es compatible con todos los sistemas operativos y herramientas
- **Claridad de propósito:** Los prefijos (prd-, benchmark-, proceso-, etc.) identifican inmediatamente el tipo de documento
- **Estabilidad:** Los nombres no cambian, facilitando trazabilidad y versionado

### Negativas / Riesgos

- **Requiere disciplina inicial:** Necesita esfuerzo consciente para seguir la convención al crear nuevos documentos
- **Puede implicar renombrar archivos existentes:** Documentos que no cumplan la convención deben renombrarse, lo que puede romper referencias existentes
- **Curva de aprendizaje:** Requiere tiempo para internalizar las convenciones y aplicarlas consistentemente
- **Riesgo de inconsistencia:** Sin disciplina, documentos pueden no seguir la convención, reduciendo beneficios
- **Mantenimiento continuo:** Requiere revisión periódica para asegurar que todos los documentos siguen la convención
- **Migración de referencias:** Renombrar archivos puede requerir actualizar referencias en otros documentos

## Notas

- Esta convención aplica a todos los archivos nuevos creados en el Segundo Cerebro
- Los archivos existentes que no cumplan la convención deben renombrarse gradualmente
- Los LLMs que trabajen con el repositorio deben ser instruidos a seguir esta convención al crear nuevos documentos
- La numeración de ADRs es secuencial y nunca cambia; si un ADR se depreca, se marca como "Deprecated" pero mantiene su número
- Los prefijos específicos (prd-, benchmark-, proceso-, etc.) son obligatorios para facilitar identificación rápida
- Esta convención complementa el ADR-003 sobre Markdown + Frontmatter, estableciendo estándares tanto de formato como de nomenclatura

---

**Referencias:**
- `Documentos/00-start-here/README.md` - Estructura oficial del repositorio y reglas obligatorias
- `Documentos/Decisiones/ADRs/ADR-001-usuarios-sinteticos.md` - Ejemplo de nomenclatura ADR
- `Documentos/Decisiones/ADRs/ADR-002-separacion-research-estudios-decisiones.md` - Separación de carpetas
- `Documentos/Decisiones/ADRs/ADR-003-markdown-frontmatter-estandar.md` - Formato estándar
- `Documentos/Estudios/usuarios-sinteticos.md` - Ejemplo de nomenclatura de estudio
