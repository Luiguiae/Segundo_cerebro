# Plantilla — Business Case HTML

Mapa narrativo para generar un business case a partir de un concepto del vault.
Se usa junto con `html-base.md` (sistema visual) y el concepto fuente.

---

## Arco narrativo

Un business case defiende **una decisión de inversión** con evidencia. El arco es:

> *¿Por qué este problema es caro? → ¿Por qué esta solución funciona? → ¿Cuánto regresa? → ¿Qué se aprueba hoy?*

Cada sección debe responder exactamente una pregunta. No hay sección decorativa.

---

## Secciones y su fuente en el vault

### 1. Nav
- Links a: `#problema`, `#solucion`, `#evidencia`, `#roi`, `#aprobacion`
- Nombre del proyecto: extraer del `titulo:` del frontmatter
- Label del CTA del nav: `"Aprobar →"`

---

### 2. Hero `id="inicio"`
**Fondo:** `var(--ink)` (oscuro)

**Contenido:**
- **Eyebrow:** nombre de la organización o área que propone (inferir del contexto o usar "COE · [categoría]")
- **Título:** el `titulo:` del concepto, formulado como oportunidad
  - Patrón: *"[verbo de acción] + [resultado esperado] con [nombre del concepto]"*
  - Ejemplo: *"Comprimir ciclos de investigación un 80% con Poblaciones Sintéticas"*
- **Subtítulo:** primera oración de `## El concepto`
- **Stats grid (3-4 stat cards):** extraer del `## Datos y evidencia` — cifras concretas con unidad, fuente y año
  - Priorizar: porcentajes de mejora, tiempo ahorrado, cobertura, costo evitado

---

### 3. Resumen ejecutivo `id="resumen"`
**Fondo:** `var(--canvas)` (claro)

Grid 2×2 con 4 celdas:

| Celda | Contenido |
|-------|-----------|
| **El problema** | Primera tensión de `## Tensiones y límites` + costo actual inferido |
| **La solución** | Párrafo 1-2 de `## El concepto` resumido en 2-3 líneas |
| **Evidencia** | 2-3 hallazgos clave de `## Datos y evidencia` |
| **El ask** | Qué se aprueba: presupuesto, piloto, equipo, timeline |

---

### 4. El problema `id="problema"`
**Fondo:** `var(--ink)` (oscuro)

**Contenido:**
- **Eyebrow:** `"// diagnóstico"`
- **Título:** formulado como pregunta o costo (`"¿Por qué el método actual es insostenible?"`)
- **Lead:** costo del status quo — extraer de `## Por qué importa`
- **Pain cards (3-4 tarjetas):** cada una = una fricción o costo específico del proceso actual
  - Fuente: tensiones de `## Tensiones y límites` + datos de `## Por qué importa`
  - Estructura de cada card: ícono + título del dolor + descripción + dato cuantitativo si existe

---

### 5. La solución `id="solucion"`
**Fondo:** `var(--canvas)` (claro)

**Contenido:**
- **Eyebrow:** `"// propuesta"`
- **Título:** cómo resuelve el problema
- **Lead:** párrafo central de `## El concepto`
- **Feature grid (3-4 cards):** capacidades o componentes de la solución
  - Extraer de `## El concepto` — buscar sub-mecanismos, casos de uso, capacidades diferenciadas
- **Diagrama opcional:** flujo antes/después en texto estructurado o ASCII si hay proceso claro

---

### 6. Evidencia `id="evidencia"`
**Fondo:** `var(--ink)` (oscuro)

**Contenido:**
- **Eyebrow:** `"// evidencia"`
- **Título:** `"Lo que la evidencia dice"`
- **Hallazgos principales (3-4):** de `## Datos y evidencia`
  - Cada hallazgo: número grande + descripción + fuente (autor + año)
- **Quote destacado (si existe):** cita textual o hallazgo impactante como blockquote
- **Tabla de fuentes:** si hay `fuentes:` en frontmatter — titulo, institución, año

---

### 7. Análisis de opciones `id="opciones"` *(opcional)*
**Fondo:** `var(--canvas)` (claro) — incluir solo si hay alternativas claras

**Contenido:**
- **Tabla de comparación:** la solución propuesta vs. 2-3 alternativas (mantener status quo, herramienta competidora, enfoque manual)
- Criterios: tiempo, costo, cobertura, riesgo, escalabilidad
- La solución propuesta siempre en la columna marcada con ★

---

### 8. ROI `id="roi"`
**Fondo:** `var(--canvas)` (claro)

**Contenido:**
- **Eyebrow:** `"// retorno"`
- **Título:** cifra principal de retorno o ahorro
- **3 stat cards:** cifras clave (tiempo comprimido, costo evitado, capacidad ganada)
  - Fuente: calcular desde `## Datos y evidencia` o inferir conservadoramente
  - Etiquetar los valores inferidos como `"estimado conservador"`
- **Tabla ROI:** inversión vs. retorno por año (Año 0, Año 1, Año 2)
- **Nota:** si no hay datos suficientes para ROI cuantitativo, usar comparativo cualitativo

---

### 9. Inversión / TCO `id="inversion"`
**Fondo:** `var(--ink)` (oscuro)

**Contenido:**
- **Eyebrow:** `"// inversión"`
- **3 columnas de costo:** Setup inicial / Operación mensual / Escalado
  - Estimar desde contexto del concepto y categoría de solución
  - Siempre etiquetar como `"referencial"` si son estimados
- **Nota de variabilidad:** qué factores cambian el costo

---

### 10. Riesgos `id="riesgos"`
**Fondo:** `var(--canvas)` (claro)

**Contenido:**
- **Eyebrow:** `"// riesgos"`
- **3-4 risk cards:** extraer de `## Tensiones y límites`
  - Clasificar cada tensión como riesgo BAJO / MEDIO / ALTO
  - Cada card: badge de nivel + nombre del riesgo + descripción + mitigación propuesta

---

### 11. Roadmap `id="roadmap"`
**Fondo:** `var(--ink)` (oscuro)

**Contenido:**
- **Eyebrow:** `"// plan"`
- **3-4 fases:** inferir desde la naturaleza del concepto
  - Fase 1 (Mes 1-2): Setup, infraestructura, piloto acotado
  - Fase 2 (Mes 2-3): Validación, ajuste, ampliación
  - Fase 3 (Mes 4-6): Escala, institucionalización
  - Fase 4 (Mes 6+): Mantenimiento / iteración continua (si aplica)
- Cada fase: nombre + milestones + KPI objetivo

---

### 12. CTA / Aprobación `id="aprobacion"`
**Fondo:** `var(--teal)` o gradiente ink→teal

**Contenido:**
- **Eyebrow:** `"// decisión"`
- **Título:** `"¿Qué se aprueba hoy?"` o similar
- **El ask específico:** 2-4 bullets concretos (presupuesto, equipo, timeline, alcance del piloto)
- **Dos botones de acción:** `"Aprobar piloto →"` y `"Agendar revisión"`
- **Footer:** fecha de presentación + autor + versión

---

## Reglas de generación

1. **Siempre en español.** Incluidos los textos de UI (botones, labels, tooltips).

2. **Datos del vault son autoritativos.** No inventar cifras. Si falta un dato, usar placeholder visible: `[PENDIENTE: estimar con equipo]` o etiquetar como `"estimado conservador"`.

3. **Máximo 2 niveles de jerarquía por sección.** Título → contenido. Sin sub-subsecciones.

4. **Cada stat lleva su fuente.** Formato: `(Autor/Institución, año)` en texto pequeño bajo el número.

5. **El ask del CTA es específico.** No `"implementar la solución"` — sino `"aprobar presupuesto de $X para piloto de 60 días con equipo de N personas"`.

6. **Tono:** ejecutivo, directo, basado en evidencia. Sin jerga de startup. Sin palabras como "disruptivo", "innovador", "transformador" sin dato que las respalde.

7. **Secciones opcionales:** `#opciones` y `#evidencia-externa` se omiten si el concepto no tiene datos suficientes para poblarlas.

---

## Mapping rápido: sección → campo del vault

| Sección HTML | Campo del concepto |
|---|---|
| Hero título | `titulo:` + reformulación |
| Hero stats | `## Datos y evidencia` — cifras |
| Resumen exec | Síntesis de las 3 secciones principales |
| Problema | `## Por qué importa` + `## Tensiones y límites` |
| Solución | `## El concepto` |
| Evidencia | `## Datos y evidencia` + `fuentes:` |
| Riesgos | `## Tensiones y límites` |
| Roadmap | Inferido del tipo de solución |
| CTA ask | `## Por qué importa` — urgencia + acción |
