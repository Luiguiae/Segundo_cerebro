---
titulo: "Marea creciente de automatización"
tipo: concepto
familia: transicion-ia
fecha: 2026-05-19
estado: activo
tags: [automatizacion, trabajo, ia, cambio, transicion]
relacionado:
  - ia-como-filtro-de-entrada
  - automatizacion-vs-ampliacion
  - ia-sin-ecosistema
fuentes:
  - titulo: "Crashing Waves vs. Rising Tides: Preliminary Findings on AI Automation from Thousands of Worker Evaluations of Labor Market Tasks"
    url: "https://arxiv.org/abs/2604.01363"
    fecha_acceso: 2026-05-19
---

# Marea creciente de automatización

## El concepto

La automatización por IA no ocurre como una ola que golpea súbitamente tareas específicas y deja el resto intacto — ocurre como una marea que sube gradual y simultáneamente en casi todo el trabajo texto-dirigible. MIT FutureTech propone esta distinción como un continuo entre dos patrones: *crashing waves* (capacidades que surgen abruptamente sobre conjuntos pequeños de tareas) y *rising tides* (mejora continua y de base amplia). Los datos apuntan al segundo patrón como dominante. La consecuencia: la disrupcción laboral no llega como un evento predecible por sector — llega como elevación de umbral en todos los dominios al mismo tiempo.

## Por qué importa

El modelo mental de "la IA reemplaza primero X tipo de trabajo" asume crashing waves. Si la marea es la forma real, entonces la estrategia de adaptación cambia: no hay sector texto-dirigible que pueda asumir que tiene tiempo mientras otros absorben el impacto primero. Para el diseñador-constructor, esto significa que la ventaja no está en el dominio elegido sino en la capa que la marea no toca: el juicio sobre qué construir, el contexto acumulado sobre el problema, y la capacidad de convertir output de IA en workflow confiable. El execution gap — la brecha entre un prompt exitoso y un flujo de trabajo autónomo confiable — es el único terreno donde la marea no sube sola.

## Datos y evidencia

- MIT FutureTech (arXiv 2604.01363, Mertens et al., abril 2026): 41 modelos evaluados contra 3,000+ tareas laborales del O\*NET del Departamento de Trabajo de EE.UU.; más de 17,000 evaluaciones doble ciego por expertos humanos del dominio.
- En Q2-2024, modelos frontier completaban tareas de 3-4 horas humanas con ~**50% de tasa de éxito**; para Q3-2025 había subido a ~**65%**.
- La duración de tarea alcanzable a una tasa de éxito dada se **duplica cada 3.8 meses**.
- La tasa de aceptación promedio de managers sobre tareas evaluadas ya se ubica en **60%** en el corte transversal del estudio.
- Hallazgo sobre escala vs. novedad: modelos más **nuevos** mejoran el desempeño uniformemente en todo el espectro de duración de tarea; modelos más **grandes** (>100B parámetros) dominan tareas cortas pero pierden ventaja comparativa conforme aumenta la dependencia secuencial.
- En contraste con METR (que reporta 50% de éxito en tareas de software de 8-15 minutos), este paper documenta 50% de éxito en tareas laborales generales de ~3 horas — lo que sugiere que los benchmarks de código subestiman sistemáticamente la utilidad de los modelos en trabajo texto-dirigible corporativo.
- Limitación estructural del estudio: todas las tareas son auto-contenidas (el contexto está en el prompt). Los flujos de trabajo reales requieren contexto organizacional no explicitado, artefactos externos y recuperación dinámica de información — fricciones que el benchmark abstrae.

## Tensiones y límites

**Tensión con `ia-como-filtro-de-entrada`:** ese concepto asume que la IA golpea selectivamente tareas de entrada y deja intactas las de mayor experiencia. El rising tide sugiere que la elevación es amplia — no hay categoría de trabajo texto-dirigible con inmunidad temporal. Pueden ser compatibles si el filtro de entrada describe la primera zona en saturarse, no la única.

**Tensión con `automatizacion-vs-ampliacion`:** la distinción automatización/ampliación sigue siendo válida para describir el *modo de impacto* sobre un individuo, pero el rising tide describe la *distribución del impacto* sobre el mercado. Son dimensiones distintas, no contradictorias.

**Límite del execution gap:** la brecha entre prompt exitoso y workflow autónomo confiable es el verdadero cuello de botella — y el paper lo deja como variable exógena. La marea puede subir en capacidades de razonamiento mientras el terreno de integración de sistemas permanece sin resolver. Esto es exactamente el argumento de `ia-sin-ecosistema`.

**Límite metodológico:** las proyecciones a 2029 asumen tendencia lineal en log-odds, ignorando restricciones físicas de escala de cómputo y límites de datos de entrenamiento.

## Ejes investigados

- Distinción empírica entre crashing waves y rising tides como patrones alternativos de automatización
- Benchmark O\*NET aplicado a evaluación de capacidades de LLMs en trabajo laboral real (no código)
- Relación entre tamaño de modelo vs. novedad de modelo y su efecto diferencial en el espectro de duración de tarea
- El execution gap como variable no resuelta: distancia entre output exitoso y workflow autónomo confiable
- Comparación metodológica con METR y SWE-bench: por qué los benchmarks de código subestiman el impacto en trabajo texto-dirigible general
