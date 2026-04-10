# Segundo Cerebro — Mapa del Repositorio (Fuente de Verdad)

Este repositorio es una base de conocimiento personal versionada, operada por **Jarvis**
(agente de mantenimiento definido en `CLAUDE.md`), y diseñada para trabajar con Claude Code
como entorno principal de desarrollo y pensamiento.

---

## Archivos raíz

| Archivo | Rol |
|---------|-----|
| `CLAUDE.md` | Identidad y reglas de Jarvis — define cómo opera el agente |
| `JARVIS_LOG.md` | Registro cronológico de todas las acciones del agente |
| `Conocimiento/ATLAS.md` | Mapa de relaciones auto-generado — Context Layer del sistema |

---

## Estructura oficial del repositorio

### Conocimiento/
**El núcleo del sistema.** Contiene el conocimiento estructurado y el ATLAS.

```
Conocimiento/
├── ATLAS.md              ← índice auto-generado (ejecutar generar_index.py para regenerar)
├── Conceptos/            ← conceptos atómicos .md (taxonomía + rúbrica obligatorias)
├── Correlaciones/        ← tensiones productivas entre pares de conceptos
└── Fuentes/
    ├── YouTube/          ← transcripciones procesadas
    └── Sesiones/         ← resúmenes de sesiones de trabajo (últimas 5)
```

Cada concepto en `Conceptos/` sigue la plantilla `Plantillas/concepto-atomico.md` y pasa
la rúbrica de dos gates antes de entrar al vault. `ATLAS.md` se regenera automáticamente
después de cada cambio.

### Plantillas/
Plantillas reutilizables obligatorias para todos los tipos de documento del sistema.

| Archivo | Para qué |
|---------|----------|
| `concepto-atomico.md` | Conceptos en `Conocimiento/Conceptos/` |
| `taxonomia.md` | Ontología del sistema — tags, familias, tipos (solo lectura) |
| `rubrica.md` | Criterios de calidad Gate 1 y Gate 2 (solo lectura) |
| `prd-plantilla.md` | Nuevos PRDs en `Documentos/PRDS/` |
| `adr-plantilla.md` | Decisiones arquitectónicas en `Documentos/Decisiones/ADRs/` |
| `bench-plantilla.md` | Benchmarks comparativos en `Documentos/Benchmarks/` |

### Documentos/
Conocimiento estable y reusable. No es el lugar para experimentación — eso va en `Proyectos/`.

```
Documentos/
├── 00-start-here/        ← este archivo y guías del sistema
├── PRDS/                 ← PRDs creados desde prd-plantilla.md
├── Research/             ← investigación, hallazgos, insights (exploración temprana)
├── Estudios/             ← análisis profundos y exploratorios
│   └── simulaciones/     ← simulaciones con usuarios sintéticos
├── Decisiones/ADRs/      ← decisiones arquitectónicas documentadas
├── Benchmarks/           ← comparativas y evaluaciones
├── Procesos/             ← flujos, procesos, BPMN, Mermaid
└── Presentaciones/       ← decks, charlas, workshops
    ├── 00-plantillas/
    ├── charlas/
    ├── decks/
    ├── html/
    └── workshops/
```

### Proyectos/
Estado y documentación de proyectos activos. Cada proyecto tiene su carpeta propia.

Proyectos actuales:
- `Wayta_IA/` — proyecto principal
- `correlacion-conceptos/` — skill para detectar y generar correlaciones entre conceptos
- `rastreador-conocimiento/` — agente que rastrea y genera conceptos desde fuentes externas

### Prompts/
Prompts reutilizables organizados por dominio.

```
Prompts/
├── Jarvis/               ← prompts-jarvis.md — catálogo completo de comandos de Jarvis
├── Meta/                 ← scripts de mantenimiento del sistema
│   ├── generar_index.py  ← regenera ATLAS.md desde Conocimiento/Conceptos/
│   └── generar_presentacion.py ← genera outline de presentación con API de Claude
├── ADRs/
├── Estudios/
├── Git/
├── PRDs/
├── Presentaciones/
└── Usuarios-sinteticos/
```

El archivo `Prompts/Jarvis/prompts-jarvis.md` es la referencia principal para invocar
a Jarvis: contiene prompts listos para auditar, agregar conceptos, correlacionar,
generar entregables y gestionar sesiones.

### Iniciativas/
Trabajo activo por iniciativa o proyecto. Puede referenciar documentos y PRDs existentes.

---

## Jarvis — el agente del vault

Jarvis opera sobre el vault vía Claude Code. Se invoca desde la raíz del repositorio:

```bash
claude "Jarvis, [instrucción]"
```

**Comandos principales:**

| Comando | Qué hace |
|---------|----------|
| `Jarvis, agrega el concepto [nombre]` | Crea concepto atómico, aplica rúbrica, actualiza ATLAS |
| `Jarvis, correlaciona [a] y [b]` | Genera correlación si hay tensión productiva real |
| `Jarvis, audita el vault` | Evalúa todos los conceptos contra la rúbrica, actualiza estados |
| `Jarvis, actualiza el ATLAS` | Regenera ATLAS.md desde los conceptos existentes |
| `Jarvis, procesa esta fuente: [url/texto]` | Crea archivo de fuente y extrae candidatos a concepto |
| `Jarvis, cierra la sesión` | Guarda resumen de sesión, mantiene últimas 5, regenera ATLAS |

Ver catálogo completo en `Prompts/Jarvis/prompts-jarvis.md`.

---

## Rituales de sesión

**Inicio:** Al abrir Claude Code, Jarvis lee las últimas 3 sesiones en
`Conocimiento/Fuentes/Sesiones/` y reporta el contexto pendiente antes de actuar.

**Cierre:** `"Jarvis, cierra la sesión"` genera `Conocimiento/Fuentes/Sesiones/YYYY-MM-DD.md`
con qué se hizo, decisiones tomadas, pendientes y estado del vault.

---

## Reglas obligatorias para uso con LLM

- **NO inventar carpetas ni rutas.** Usar únicamente las definidas aquí.
- **Usar siempre los nombres exactos** — incluyendo mayúsculas/minúsculas.
- **Leer `Plantillas/taxonomia.md` y `Plantillas/rubrica.md`** antes de crear cualquier concepto.
- **Ningún concepto entra al vault sin pasar la rúbrica** (Gate 1 + Gate 2).
- **El campo `relacionado` solo apunta a archivos que existen** en `Conocimiento/Conceptos/`.
- **Regenerar ATLAS.md después de cada cambio** en `Conocimiento/`.
- **Todo queda en `JARVIS_LOG.md`** — exitoso o rechazado.
- Todo documento nuevo usa frontmatter YAML con campos obligatorios.
- Nombres de archivos en kebab-case, sin acentos, sin espacios.
- `Plantillas/taxonomia.md` y `Plantillas/rubrica.md` son de solo lectura — no modificar.
