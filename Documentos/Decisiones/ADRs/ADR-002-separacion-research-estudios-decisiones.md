---
titulo: "ADR-002: Separación entre Research, Estudios y Decisiones"
tipo: adr
estado: aceptado
autor: Luigui Avila
fecha: 2026-01-11
updated: 2026-02-10
tags: [estructura, organizacion, conocimiento]
fuentes:
  - Documentos/Research/
  - Documentos/Estudios/
  - Documentos/Decisiones/ADRs/
  - Documentos/00-start-here/README.md
  - Plantillas/adr-plantilla.md
---

# ADR-002: Separación entre Research, Estudios y Decisiones en el Segundo Cerebro

## Contexto

El repositorio Segundo Cerebro organiza conocimiento para trabajar con LLMs (Cursor) y documentar pensamiento, decisiones y diseño. Según `Documentos/00-start-here/README.md`, la estructura oficial del repositorio incluye:

- `Research/` → investigación, hallazgos, insights
- `Estudios/` → análisis profundos o exploratorios
- `Decisiones/ADRs/` → decisiones arquitectónicas documentadas

Durante la creación de documentos se ha observado confusión potencial entre estas carpetas, especialmente al generar contenido asistido por IA. Sin una distinción clara, el repositorio corre riesgo de mezclar:

- Hipótesis y exploración temprana
- Análisis estructurados y síntesis
- Evidencia trabajada y conclusiones
- Decisiones arquitectónicas y estratégicas

Esta mezcla reduce la utilidad del repositorio como sistema de pensamiento versionado, ya que LLMs y humanos no pueden distinguir claramente entre pensamiento en desarrollo, análisis trabajado y decisiones tomadas.

## Decisión

Se decide establecer una separación explícita y normativa entre las tres carpetas:

**1. Research/** - Exploración temprana y pensamiento en bruto
- Hipótesis iniciales
- Preguntas abiertas
- Exploración temprana de conceptos
- Pensamiento en desarrollo
- Hallazgos preliminares sin estructura completa

**2. Estudios/** - Análisis estructurados y síntesis
- Análisis profundos o exploratorios estructurados
- Síntesis de información
- Evidencia trabajada
- Conclusiones basadas en análisis
- Documentos con estructura completa y metodología clara

**3. Decisiones/ADRs/** - Decisiones explícitas tomadas
- Decisiones arquitectónicas y estratégicas del sistema
- Contexto de la decisión
- Alternativas consideradas
- Consecuencias documentadas
- Única fuente de verdad para decisiones del Segundo Cerebro

La carpeta `Decisiones/ADRs/` será la única fuente de verdad para decisiones arquitectónicas y estratégicas del sistema.

## Alternativas consideradas

**1. Mantener estructura actual sin distinción explícita**
- **Descartada porque:** Genera confusión al crear y consultar información, especialmente con asistencia de IA. Mezcla hipótesis, análisis y decisiones, reduciendo utilidad del repositorio.

**2. Unificar Research y Estudios en una sola carpeta**
- **Descartada porque:** No distingue entre pensamiento en desarrollo y análisis estructurado. Reduce claridad cognitiva y rendimiento de LLMs al consumir contexto.

**3. Crear subcarpetas dentro de Research para distinguir niveles**
- **Descartada porque:** Añade complejidad innecesaria. La separación en carpetas independientes es más clara y sigue la estructura ya establecida en `Documentos/00-start-here/README.md`.

**4. Establecer separación explícita y normativa entre Research, Estudios y Decisiones**
- **Seleccionada porque:** Proporciona claridad cognitiva, mejora rendimiento de LLMs, y separa claramente entre pensar, analizar y decidir. Mantiene estructura existente mientras añade claridad normativa.

## Consecuencias

### Positivas

- **Mayor claridad cognitiva:** Al crear y consultar información, es inmediatamente claro si se trata de exploración temprana, análisis estructurado o decisión tomada
- **Mejor rendimiento de LLMs:** Al consumir contexto estructurado, los LLMs pueden distinguir entre hipótesis, evidencia y decisiones, mejorando calidad de outputs
- **Separación clara entre pensar, analizar y decidir:** Establece flujo cognitivo claro: Research → Estudios → Decisiones
- **Trazabilidad mejorada:** Facilita seguir evolución de pensamiento desde exploración hasta decisión
- **Reducción de confusión:** Elimina ambigüedad sobre dónde ubicar documentos nuevos

### Negativas / Riesgos

- **Requiere disciplina inicial:** Necesita esfuerzo consciente para clasificar correctamente el contenido al crear documentos
- **Fricción inicial:** Puede generar trabajo adicional al mover documentos existentes que no estén correctamente clasificados
- **Curva de aprendizaje:** Requiere tiempo para internalizar las distinciones y aplicarlas consistentemente
- **Riesgo de clasificación incorrecta:** Sin disciplina, documentos pueden terminar en carpetas incorrectas, reduciendo beneficios de la separación
- **Mantenimiento continuo:** Requiere revisión periódica para mantener separación correcta

## Notas

- Esta decisión establece normas para uso de las carpetas `Research/`, `Estudios/` y `Decisiones/ADRs/` en el Segundo Cerebro
- Los documentos existentes que no cumplan esta separación deben revisarse y moverse según corresponda
- Esta separación debe documentarse en `Documentos/00-start-here/README.md` para referencia futura
- Los LLMs que trabajen con el repositorio deben ser instruidos a respetar esta separación al crear nuevos documentos
- La carpeta `Decisiones/ADRs/` es la única fuente de verdad para decisiones arquitectónicas; no debe haber decisiones documentadas en Research o Estudios

---

**Referencias:**
- `Documentos/00-start-here/README.md` - Estructura oficial del repositorio
- `Documentos/Research/` - Carpeta para exploración temprana
- `Documentos/Estudios/` - Carpeta para análisis estructurados
- `Documentos/Decisiones/ADRs/` - Carpeta para decisiones arquitectónicas
- `Plantillas/adr-plantilla.md` - Plantilla para ADRs
