# JARVIS_LOG

---

### 2026-04-18 — correlaciones generadas: top 3 conceptos del scout

**Instrucción:** "correlaciona el top 3" (espectro-autonomia-agente, fabrica-oscura-de-software, capital-de-contexto)

**Acciones:**
- Evaluadas 3 pares posibles — todos aprueban Gate 1 + Gate 2
- Escritas 3 correlaciones en `Correlaciones/`

**Resultados:**
- `2026-04-18_espectro-autonomia-agente--fabrica-oscura-de-software.md`: OK — "El operador que no está"
- `2026-04-18_espectro-autonomia-agente--capital-de-contexto.md`: OK — "El precio de entrada para cada posición"
- `2026-04-18_fabrica-oscura-de-software--capital-de-contexto.md`: OK — "El único activo que queda"

**ATLAS regenerado:** sí — 34 conceptos procesados

---

### 2026-04-18 — correlaciones generadas: 3 nuevas

**Instrucción:** "sugiere correlaciones entre los 3 nuevos conceptos y los que ya existen → ejecuta top 3"

**Acciones:**
- Leídos conceptos relevantes: `confianza-a-traves-de-velocidad`, `quien-controla-el-prompt`, `expertise-de-dominio-en-producto`, `vibe-coding`, `feedback-que-escala`, `claridad-antes-de-velocidad`
- 6 correlaciones candidatas evaluadas; top 3 seleccionadas por Luigui
- Rúbrica aplicada — las 3 aprueban Gate 1 + Gate 2

**Resultados:**
- `2026-04-18_pit-stop-cognitivo--confianza-a-traves-de-velocidad.md`: OK — "La pausa que sostiene la velocidad"
- `2026-04-18_copiloto-de-producto--quien-controla-el-prompt.md`: OK — "El mapa y el volante"
- `2026-04-18_pit-stop-cognitivo--feedback-que-escala.md`: OK — "Lo que el sistema no puede enseñarse a sí mismo"

**ATLAS regenerado:** sí — 29 conceptos procesados

---

### 2026-04-18 — profundizar: restriccion-de-tiempo-como-ventaja, copiloto-de-producto, pit-stop-cognitivo

**Instrucción:** "profundiza estos conceptos: restriccion-de-tiempo-como-ventaja, copiloto-de-producto, pit-stop-cognitivo"

**Acciones:**
- Leídos los 3 borradores desde `Conocimiento/Conceptos/`
- 9 búsquedas web ejecutadas (3 ejes × 3 conceptos)
- Generados 3 `.md` enriquecidos entregados en chat (no guardados en disco)

**Ejes investigados por concepto:**

*restriccion-de-tiempo-como-ventaja*
- Eje 1: Parkinson's Law + investigación en creatividad bajo restricciones (Acar et al. 2019, Cromwell 2024) — 3 fuentes sólidas
- Eje 2: Datos empíricos velocidad IA vs comprensión humana (CodeRabbit 2025, 470 PRs) — 2 fuentes sólidas
- Eje 3: Investigación en ingeniería y diseño sobre restricciones deliberadas (ResearchGate, SAGE) — 2 fuentes sólidas

*copiloto-de-producto*
- Eje 1: Pair programming navigator/driver — Cockburn & Williams, ScienceDirect 2006 — 2 fuentes sólidas
- Eje 2: Supervisión humana en aviación, EASA AI framework 2025, MDPI — 2 fuentes sólidas
- Eje 3: Evolución rol PM en equipos AI-native — Product School, Maven, HBR 2026 — 3 fuentes sólidas

*pit-stop-cognitivo*
- Eje 1: Leslie Lamport — Microsoft Research, Quanta Magazine — 2 fuentes sólidas
- Eje 2: Comprehension debt empírico — arxiv 2604.13277 y 2603.28592, Addy Osmani — 3 fuentes sólidas
- Eje 3: Cognitive offloading y pérdida de comprensión — Frontiers Psychology 2025, RCT ScienceDirect 2025 — 2 fuentes sólidas

**Resultados:**
- 3 `.md` enriquecidos generados — entregados en chat, pendientes de guardar por Luigui
- Dato nuevo más relevante por concepto:
  - *restriccion-tiempo*: código IA produce 1.7x más issues; solo 30% del código Copilot es aceptado (CodeRabbit 2025)
  - *copiloto-de-producto*: EASA formaliza que IA debe ofrecer recomendaciones, no directivas; over-reliance erode habilidades
  - *pit-stop-cognitivo*: RCT 2026 — IA asistida = mismo tiempo, 17% menos comprensión; comprehension debt ya es término académico formal

**Correcciones de frontmatter aplicadas al guardar:**
- Tags fuera de lista controlada reemplazados: `decision-making` → `criterio`, `equipos` → `equipo`, `agentes-ia` → `agentes`, `calidad` → `criterio`, `comprension` → `conocimiento`, `sostenibilidad` → omitido (excedía máx 5)
- Campos `familia` y `estado: activo` agregados a los 3 archivos (faltaban en borradores)
- Campo `relacionado` en copiloto-de-producto y pit-stop-cognitivo reducido a máx 3 (tenían 4)

**ATLAS regenerado:** sí — 29 conceptos procesados

---

### 2026-04-16 00:00 — concepto agregado: inversion-sesgo-tecnologico

**Instrucción:** "Jarvis, agrega los conceptos aprobados con tensión Fuerte (McKinsey PDF)"

**Acciones:**
- Leídos `taxonomia.md` y `rubrica.md`
- Verificados archivos relacionados: `ia-como-filtro-de-entrada`, `automatizacion-vs-ampliacion`, `fundamentales-vs-flux` — todos existen ✓
- Tags no controlados sustituidos: `trabajo` → omitido, `inversion` → omitido. Tags finales: [ia, automatizacion, educacion, habilidades, transicion]

**Resultados:**
- `inversion-sesgo-tecnologico.md`: OK — Gate 1: ✓✓✓✓ | Gate 2: ✓✓✓✓ → estado: activo

**Criterios evaluados:**
- Gate 1.1 Atómico: ✓ — una idea: inversión del sesgo de automatización en estratos altos
- Gate 1.2 Propio: ✓ — destilación con interpretación, no resumen del reporte
- Gate 1.3 Frontmatter completo: ✓
- Gate 1.4 Nombre de archivo: ✓ — kebab-case, sin acentos, sin artículos
- Gate 2.1 No es resumen: ✓
- Gate 2.2 Tensión interna: ✓ — efecto no uniforme, potencial vs. trayectoria real
- Gate 2.3 Relacionable: ✓ — 3 conceptos existentes
- Gate 2.4 Transferible: ✓ — autocontenido con datos y contexto

**[PROPUESTA]** Tags `trabajo` e `inversion` no están en la lista controlada. Se omitieron; propuesta: agregar `trabajo` a la lista de tags de dominio en `taxonomia.md`.

---

### 2026-04-16 00:00 — concepto agregado: condicion-redespliegue

**Instrucción:** (mismo comando de sesión McKinsey)

**Acciones:**
- Verificados archivos relacionados: `automatizar-mi-propio-trabajo`, `feedback-que-escala`, `equipos-pequenos-alto-impacto` — todos existen ✓
- Tags no controlados sustituidos: `productividad`, `condicion` → omitidos. Tags finales: [ia, automatizacion, organizacion, sistemas, transicion]
- Familia cambiada de `sistemas-conocimiento` a `transicion-ia` — el concepto trata el cambio organizacional post-automatización, no arquitecturas de conocimiento

**Resultados:**
- `condicion-redespliegue.md`: OK — Gate 1: ✓✓✓✓ | Gate 2: ✓✓✓✓ → estado: activo

**Criterios evaluados:**
- Gate 1.1 Atómico: ✓ — una idea: el redespliegue como condición no automática de la promesa de productividad IA
- Gate 1.2 Propio: ✓ — el supuesto implícito del modelo McKinsey es interpretación propia
- Gate 1.3 Frontmatter completo: ✓
- Gate 1.4 Nombre de archivo: ✓
- Gate 2.1 No es resumen: ✓
- Gate 2.2 Tensión interna: ✓ — no todos pueden redesplazarse, puede usarse como excusa para no actuar
- Gate 2.3 Relacionable: ✓ — 3 conceptos existentes
- Gate 2.4 Transferible: ✓

**[PROPUESTA]** Tags `productividad` y `condicion` no están en la lista controlada. Propuesta: agregar `productividad` a dominio en `taxonomia.md`.

**ATLAS regenerado:** sí — 26 conceptos procesados

---

### 2026-04-15 17:00 — concepto profundizado: colonialismo-cultural-digital

**Instrucción:** "Profundiza en el concepto" (borrador colonialismo-cultural-digital)

**Ejes investigados:**
1. Legibilidad algorítmica como mecanismo de dominación — 4 fuentes (arXiv, Springer, Cultural Survival, Sagepub)
2. Distinción entre marcos teóricos adyacentes (Kwet, Couldry & Mejias, Zuboff) — 3 fuentes (LSE, Oxford JoC, Lawfare)
3. Resistencia y apropiación — 4 fuentes (Tierra Común, UNESCO Courier, Institute of Network Cultures, Milan & Treré 2024)

**Acciones:**
- Archivo sobreescrito con concepto enriquecido: 5 fuentes en frontmatter, sección nueva `## Datos y evidencia`, `## Ejes investigados`
- Estado actualizado: `borrador` → `activo`
- Eliminados campos no estándar (`alias`, `proyectos`, `fuente` estructurado)
- ATLAS regenerado

**Resultados:**
- `colonialismo-cultural-digital.md`: OK — activo

**ATLAS regenerado:** sí — 24 conceptos procesados

---

### 2026-04-15 16:30 — auditoría completa del vault

**Instrucción:** "Jarvis, audita el vault completo"

---

#### CONCEPTOS — 24 evaluados

| archivo | Gate 1 | Gate 2 | resultado |
|---|---|---|---|
| claridad-antes-de-velocidad | ✓✓✓✓ | ✓✓✓✓ | OK |
| spec-driven-development | ✓✓✓✓ | ✓✓✓✓ | OK |
| usuarios-sinteticos | ✓✓✓✓ | ✓✓✓✓ | OK |
| quien-controla-el-prompt | ✓✓✓✓ | ✓✓✓✓ | OK |
| momento-liminal | ✓✓✓✓ | ✓✓✓✓ | OK |
| fundamentales-vs-flux | ✓✓✓✓ | ✓✓✓✓ | OK |
| **colonialismo-cultural-digital** | ✓✓✓✓ | ✗✓✓✓ | **ADVERTENCIA** |
| diseno-uxui-y-ia | ✓✓✓✓ | ✓✓✓✓ | OK |
| disenador-a-constructor | ✓✓✓✓ | ✓✓✓✓ | OK |
| vibe-coding | ✓✓✓✓ | ✓✓✓✓ | OK |
| agentes-ia | ✓✓✓✓ | ✓✓✓✓ | OK |
| mvp-a-prototipo-en-produccion | ✓✓✓✓ | ✓✓✓✓ | OK |
| equipos-pequenos-alto-impacto | ✓✓✓✓ | ✓✓✓✓ | OK |
| arquitectura-de-inteligencia | ✓✓✓✓ | ✓✓✓✓ | OK |
| automatizar-mi-propio-trabajo | ✓✓✓✓ | ✓✓✓✓ | OK |
| expertise-de-dominio-en-producto | ✓✓✓✓ | ✓✓✓✓ | OK |
| feedback-que-escala | ✓✓✓✓ | ✓✓✓✓ | OK |
| confianza-a-traves-de-velocidad | ✓✓✓✓ | ✓✓✓✓ | OK |
| diseno-dos-velocidades | ✓✓✓✓ | ✓✓✓✓ | OK |
| lo-ilegible-como-senal | ✓✓✓✓ | ✓✓✓✓ | OK |
| gobernanza-ia-performativa | ✓✓✓✓ | ✓✓✓✓ | OK |
| ia-como-filtro-de-entrada | ✓✓✓✓ | ✓✓✓✓ | OK |
| automatizacion-vs-ampliacion | ✓✓✓✓ | ✓✓✓✓ | OK |
| senal-anticipada-mercado-laboral | ✓✓✓✓ | ✓✓✓✓ | OK |

**Resumen conceptos:** 23 activo · 1 borrador

**Falla Gate 2.1 — colonialismo-cultural-digital:**
Cuerpo descriptivo ("Es importante destacar que..."), secciones "¿Cómo funciona?" y "Mis notas" leen como resumen del artículo fuente, no como concepto destilado con voz propia. Estado degradado a `borrador`.
**Propuesta de mejora:** reescribir "¿Cómo funciona?" con mecanismo propio interpretado; eliminar "Es importante destacar que..."; reformular "Mis notas" con observación original, no con repetición de la definición.

---

#### CORRELACIONES — 8 evaluadas

| archivo | Gate 2.1 | Gate 2.2 | Gate 2.3 | titulo | resultado |
|---|---|---|---|---|---|
| vibe-coding--spec-driven-development | ✓ | ✓ | ✓ | agregado | ADVERTENCIA→OK |
| claridad-antes-de-velocidad--momento-liminal | ✓ | ✓ | ✓ | agregado | ADVERTENCIA→OK |
| fundamentales-vs-flux--disenador-a-constructor | ✓ | ✓ | ✓ | agregado | ADVERTENCIA→OK |
| automatizar-mi-propio-trabajo--expertise-de-dominio | ✓ | ✓ | ✓ | agregado | ADVERTENCIA→OK |
| ia-como-filtro-de-entrada--agentes-ia | ✓ | ✓ | ✓ | presente | OK |
| automatizacion-vs-ampliacion--fundamentales-vs-flux | ✓ | ✓ | ✓ | presente | OK |
| senal-anticipada--gobernanza-ia-performativa | ✓ | ✓ | ✓ | presente | OK |
| ia-como-filtro-de-entrada--disenador-a-constructor | ✓ | ✓ | ✓ | presente | OK |

**Acciones sobre correlaciones:**
- Agregado campo `titulo` a las 4 correlaciones antiguas (inconsistencia con las nuevas)
- Reemplazadas 2 referencias rotas (`[[prototipo]]`, `[[intencion-de-diseno]]`) en `vibe-coding--spec-driven-development` por conceptos existentes (`claridad-antes-de-velocidad`, `agentes-ia`)

---

**Acciones ejecutadas:** 6 archivos modificados, 1 concepto degradado a borrador, ATLAS regenerado
**ATLAS regenerado:** sí — 24 conceptos procesados

---

### 2026-04-15 16:00 — 4 correlaciones generadas desde conceptos canaries-coal-mine

**Instrucción:** "encuentra correlaciones entre estos 3 nuevos conceptos atómicos y la información que ya tenemos en Conceptos"

**Pares evaluados con tensión real:**
1. `ia-como-filtro-de-entrada` ↔ `agentes-ia` — OK
2. `automatizacion-vs-ampliacion` ↔ `fundamentales-vs-flux` — OK
3. `senal-anticipada-mercado-laboral` ↔ `gobernanza-ia-performativa` — OK
4. `ia-como-filtro-de-entrada` ↔ `disenador-a-constructor` — OK

**Pares descartados (co-ocurrencia sin tensión productiva):**
- `senal-anticipada` ↔ `momento-liminal` — comparten frame temporal pero no se contradicen
- `automatizacion-vs-ampliacion` ↔ `equipos-pequenos-alto-impacto` — relación de causa-efecto, no tensión

**Resultados:**
- `2026-04-15_ia-como-filtro-de-entrada--agentes-ia.md`: OK — "El multiplicador que cierra la puerta"
- `2026-04-15_automatizacion-vs-ampliacion--fundamentales-vs-flux.md`: OK — "La misma línea divisoria, dos mapas"
- `2026-04-15_senal-anticipada-mercado-laboral--gobernanza-ia-performativa.md`: OK — "Gobernar la señal sin verla"
- `2026-04-15_ia-como-filtro-de-entrada--disenador-a-constructor.md`: OK — "La salida de emergencia también se cierra"

**ATLAS regenerado:** sí — 24 conceptos procesados

---

### 2026-04-15 15:30 — 3 conceptos atómicos creados desde fuente canaries-coal-mine

**Instrucción:** "Confirmado. Crea los conceptos atómicos que encuentres"

**Rúbrica — ia-como-filtro-de-entrada:**
- Gate 1: ✓✓✓✓ — Gate 2: ✓✓✓✓ — **OK → activo**

**Rúbrica — automatizacion-vs-ampliacion:**
- Gate 1: ✓✓✓✓ — Gate 2: ✓✓✓✓ — **OK → activo**

**Rúbrica — senal-anticipada-mercado-laboral:**
- Gate 1: ✓✓✓✓ — Gate 2: ✓✓✓✓ — **OK → activo**

**Acciones:**
- Creados 3 archivos en `Conocimiento/Conceptos/`
- ATLAS regenerado

**Resultados:**
- `ia-como-filtro-de-entrada.md`: OK
- `automatizacion-vs-ampliacion.md`: OK
- `senal-anticipada-mercado-laboral.md`: OK

**ATLAS regenerado:** sí — 24 conceptos procesados (era 21)

---

### 2026-04-15 15:00 — fuente procesada + concepto profundizado: canaries-coal-mine

**Instrucción:** "profundiza y guarda el paper en Conocimiento/Fuentes/"

**Ejes investigados:**
1. Impacto de IA en trabajadores junior/entry-level — 6 fuentes encontradas, todas consistentes
2. Automatización vs. amplificación — 4 fuentes (MIT Sloan, arXiv 2025, WEF, BCG)
3. Destrucción de la rampa de aprendizaje laboral — 4 fuentes (CNBC, Focused Chaos, Veris Insights, rezi.ai)

**Fuentes por eje:** 6 / 4 / 4 — mínimo de 2 cumplido en los 3 ejes

**Acciones:**
- Lectura de taxonomia.md y rubrica.md
- Creación de `Conocimiento/Fuentes/2025-11-13_canaries-coal-mine-brynjolfsson.md`
- Rúbrica fuente: Gate 1 ✓✓✓✓ · Gate 2 ✓✓✓ — resultado: OK
- Concepto enriquecido `ia-como-filtro-de-entrada` generado y entregado en chat
- Concepto NO guardado en disco — pendiente confirmación de Luigui

**Resultados:**
- `Conocimiento/Fuentes/2025-11-13_canaries-coal-mine-brynjolfsson.md`: OK — 3 candidatos en Conceptos a extraer
- `ia-como-filtro-de-entrada.md`: PENDIENTE — listo para guardar, espera instrucción

**ATLAS regenerado:** pendiente — sin escritura en Conceptos/ todavía

---

### 2026-04-15 14:30 — comando documentado: profundizar-concepto

**Instrucción:** "Agrega la sección Profundizar concepto a CLAUDE.md y prompts-jarvis.md"

**Acciones:**
- Lectura de CLAUDE.md y Prompts/Jarvis/prompts-jarvis.md para mapear estructura existente
- Inserción de sección `### Profundizar concepto` en bloque "Comandos que entiendes" de CLAUDE.md (línea 170)
- Inserción de entrada `### 1.6 Profundizar concepto` en Sección 1 de prompts-jarvis.md (línea 86)
- Adición de fila en tabla de Referencia rápida de prompts-jarvis.md (línea 362)

**Resultados:**
- CLAUDE.md: OK — sección agregada con flujo completo de 8 pasos y restricciones v1
- Prompts/Jarvis/prompts-jarvis.md: OK — entrada 1.6 con prompt de uso + fila en referencia rápida

**ATLAS regenerado:** no — cambio solo en archivos de configuración/prompts, no en Conocimiento/

---

### 2026-04-15 12:00 — concepto agregado: gobernanza-ia-performativa

**Instrucción:** "Jarvis, agrega el concepto gobernanza-ia-performativa"

**Rúbrica:**
- Gate 1.1 Atómico: ✓ — una sola idea: gobernanza visible ≠ control real
- Gate 1.2 Propio: ✓ — redactado en voz del sistema, no copiado de fuentes
- Gate 1.3 Frontmatter: ✓ — todos los campos completos y válidos
- Gate 1.4 Nombre archivo: ✓ — kebab-case, sin acentos
- Gate 2.1 No es resumen: ✓ — agrega interpretación, señal diagnóstica y estructura de 4 capas
- Gate 2.2 Tensión interna: ✓ — paradoja 56%→12% entre declaración e implementación real
- Gate 2.3 Relacionable: ✓ — agentes-ia, quien-controla-el-prompt, arquitectura-de-inteligencia
- Gate 2.4 Transferible: ✓ — autocontenido, no requiere contexto del post original

**Resultado:** OK — estado: activo

**Acciones:**
- Escrito: `Conocimiento/Conceptos/gobernanza-ia-performativa.md`
- Respaldado con investigación web (shadow AI stats, FTC AI-washing, brecha 56%→12%)

**ATLAS regenerado:** sí — 21 conceptos procesados

---

### 2026-04-13 — concepto rechazado y eliminado: etica-en-la-ia

**Instrucción:** "descartalo"

**Resultado:** RECHAZADO — eliminado permanentemente

**Razones:**
- Gate 1.2: cuerpo es paráfrasis del artículo fuente, sin interpretación propia
- Gate 1.3: falta `familia`; tags `etica` y `filosofia` no están en lista controlada
- Gate 2.1: reemplazable con el link — no agrega perspectiva
- Gate 2.2: tensión declarada como "es complejo", sin paradoja real
- Gate 2.3: `relacionado: []`

**ATLAS regenerado:** no — vault sin cambios (20 conceptos)

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
