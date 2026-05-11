# Taxonomía del Segundo Cerebro

> Jarvis lee este archivo antes de crear o modificar cualquier concepto.
> Define las reglas del sistema: qué tipos de nodos existen, qué tags son válidos,
> y qué relaciones están permitidas.

---

## Tipos de nodo

Cada archivo `.md` en `Conocimiento/` debe declarar su `tipo` en el frontmatter YAML.
Los tipos válidos son:

| tipo | carpeta | descripción |
|------|---------|-------------|
| `concepto` | `Conocimiento/Conceptos/` | Una idea atómica: un principio, patrón, fenómeno o marco mental. No es un resumen de fuente ni un proyecto. |
| `correlacion` | `Conocimiento/Correlaciones/` | La tensión productiva entre dos o tres conceptos. Generada por el skill `correlacion-conceptos`. |
| `fuente` | `Conocimiento/Fuentes/` | Transcripción o extracto procesado de una fuente externa (YouTube, artículo, podcast). No es el concepto — es la materia prima. |

---

## Estructura obligatoria de un concepto atómico

### Plantilla canónica (Gen-3)

Todo archivo de tipo `concepto` debe seguir exactamente esta plantilla:

```markdown
---
titulo: "Nombre legible del concepto"
tipo: concepto
familia: [ver familias abajo]
tags: [máximo 5, ver tags controlados abajo]
relacionado: [kebab-case de otros conceptos, máximo 3]
fecha: YYYY-MM-DD
estado: borrador | activo | archivado
fuentes:                          ← opcional, pero obligatorio si hay datos verificados
  - titulo: "Título de la fuente"
    autor: "Nombre del autor"     ← opcional
    url: "https://..."
    fecha_acceso: YYYY-MM-DD
---

## El concepto
[La idea central: qué es, qué mecanismo opera, cómo funciona.]

## Por qué importa
[Consecuencias, impacto, por qué este concepto cambia algo.]

## Tensiones y límites
[Paradojas, cuándo no aplica, fuerzas que lo contradicen.]
```

Si el concepto tiene datos verificados con fuentes externas (Gen-4), se agregan dos secciones adicionales al final del cuerpo:

```markdown
## Datos y evidencia
[Cifras con: número + fecha + fuente por cada dato.]

## Ejes investigados
[Transparencia sobre qué líneas se investigaron y cuántas fuentes sólidas se encontraron por eje.]
```

### Reglas de frontmatter

- `titulo`: legible, en español, con artículo si aplica; sin signos de exclamación ni mayúsculas innecesarias
- `tipo`: siempre `concepto` para archivos en `Conceptos/`
- `familia`: exactamente una de las familias definidas abajo
- `tags`: máximo 5, en minúsculas, en español, sin acentos, de la lista controlada
- `relacionado`: solo conceptos que ya existen como archivos en `Conceptos/`; no inventar; máximo 3
- `fecha`: fecha de creación en formato `YYYY-MM-DD`
- `estado`: `borrador` cuando se crea, `activo` cuando pasa la rúbrica, `archivado` si queda obsoleto
- `fuentes`: array obligatorio cuando el cuerpo contiene datos numéricos o afirmaciones de terceros verificables

### Campos prohibidos en el frontmatter

Los siguientes campos **no pueden aparecer** en conceptos del vault. Si Jarvis los encuentra al auditar, los elimina:

| campo | razón |
|-------|-------|
| `alias` | Redundante; el slug del filename es la referencia única |
| `proyectos` | Los conceptos no pertenecen a proyectos — esa relación va en el proyecto |
| `slug` | Ya está codificado en el nombre del archivo |
| `categoria` | Reemplazado por `familia` |
| `fuente` (string u objeto) | Reemplazado por `fuentes` (array) |

---

## Familias de conceptos

Las familias agrupan conceptos por dominio temático. Cada concepto pertenece a **una sola** familia.

| familia | descripción | ejemplos de conceptos que ya existen |
|---------|-------------|--------------------------------------|
| `transicion-ia` | Cómo el trabajo, el rol y las herramientas cambian con IA | `disenador-a-constructor`, `momento-liminal`, `fundamentales-vs-flux` |
| `velocidad-output` | Sistemas, procesos y mentalidades que aceleran de idea a resultado | `mvp-a-prototipo-en-produccion`, `vibe-coding`, `quien-controla-el-prompt` |
| `sistemas-conocimiento` | Arquitecturas para capturar, indexar y activar conocimiento | *(este archivo describe esa familia)* |
| `equipos-impacto` | Cómo equipos pequeños logran resultados desproporcionados con IA | `equipos-pequenos-alto-impacto`, `usuarios-sinteticos` |
| `agencia-ia` | Agentes, autonomía, orquestación y límites de la IA | `agentes-ia` |
| `epistemologia-practica` | Cómo sabemos lo que sabemos y cómo eso cambia con IA | `arquitectura-de-inteligencia`, `claridad-antes-de-velocidad` |

---

## Tags controlados

Solo estos tags están permitidos. Si un concepto necesita un tag que no está aquí,
Jarvis debe proponer agregarlo a esta lista antes de usarlo.

### Dominio
`ia`, `diseño`, `producto`, `sistemas`, `conocimiento`, `agentes`, `codigo`, `automatizacion`, `estrategia`, `organizacion`, `prompts`, `educacion`, `habilidades`, `herramientas`, `desarrollo`, `escala`, `startups`, `mvp`, `cultura`, `colonialismo`, `descolonizacion`, `trabajo`, `productividad`, `mcp`, `infraestructura`, `web`, `ux`

### Proceso
`captura`, `indexacion`, `activacion`, `correlacion`, `evaluacion`, `iteracion`, `prototipado`, `construccion`, `research`, `validacion`, `aprendizaje`

### Perfil / audiencia
`disenador`, `builder`, `lider`, `equipo`, `latam`, `liderazgo`, `usuarios`, `roles`

### Temporalidad
`transicion`, `momentum`, `velocidad`, `largo-plazo`, `ahora`, `cambio`, `transformacion`, `historia`

### Postura epistémica
`tension`, `paradoja`, `principio`, `patron`, `hipotesis`, `marco`, `poder`, `incertidumbre`, `fundamentos`, `criterio`, `confianza`, `transparencia`, `control`, `etica`

---

## Relaciones permitidas

El campo `relacionado` en el frontmatter solo puede contener conceptos con estas relaciones implícitas:

| tipo de relación | cuándo usarla |
|------------------|---------------|
| Amplifica | El concepto A hace más poderoso al B |
| Tensiona | El concepto A contradice o limita al B |
| Precede | El concepto A es condición para entender el B |
| Complementa | A y B cubren ángulos distintos del mismo fenómeno |

No es necesario declarar el tipo de relación en el frontmatter — solo listar el concepto relacionado.
La relación específica se declara en los archivos de `Correlaciones/`.

---

## Convenciones de nombre de archivo

| tipo | convención | ejemplo |
|------|-----------|---------|
| concepto | `kebab-case`, sin acentos, sin artículos | `claridad-antes-de-velocidad.md` |
| correlacion | `YYYY-MM-DD_concepto-a--concepto-b.md` | `2026-04-07_vibe-coding--agentes-ia.md` |
| fuente | `YYYY-MM-DD_kebab-titulo-fuente.md` | `2026-03-27_finding-our-way-jorge-arango.md` |

---

## Lo que Jarvis NO puede hacer con la taxonomía

- No puede crear un tag fuera de la lista controlada sin reportarlo en `JARVIS_LOG.md`
- No puede asignar más de una familia a un concepto
- No puede crear un archivo de tipo `correlacion` en `Conceptos/` ni viceversa
- No puede marcar un concepto como `activo` sin que haya pasado la rúbrica
- No puede modificar este archivo por iniciativa propia — solo lo edita cuando Luigui lo solicita explícitamente
