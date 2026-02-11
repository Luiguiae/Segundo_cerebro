# Segundo Cerebro — Mapa del Repositorio (Fuente de Verdad)

Este repositorio es una base de conocimiento personal versionada para trabajar con LLMs
(Cursor, Claude Code) y documentar pensamiento, decisiones y diseño.

## Estructura oficial del repositorio

### Plantillas/
Contiene **plantillas reutilizables obligatorias**.
- prd-plantilla.md → para nuevos PRDs
- adr-plantilla.md → para decisiones (ADR)
- bench-plantilla.md → para benchmarks comparativos

### Documentos/
Contiene **conocimiento estable y reusable**.

- 00-start-here/ → guias, reglas y mapa del repo
- PRDS/ → PRDs creados a partir de prd-plantilla.md
- Research/ → investigacion, hallazgos, insights (exploracion temprana)
- Estudios/ → analisis profundos o exploratorios (conocimiento estructurado)
- Estudios/simulaciones/ → simulaciones con usuarios sinteticos
- Decisiones/ADRs/ → decisiones arquitectonicas documentadas
- Benchmarks/ → comparativas y evaluaciones
- Procesos/ → flujos, procesos, BPMN, Mermaid
- Presentaciones/ → decks, charlas, workshops y plantillas de presentacion

### Proyectos/
Estado y seguimiento de proyectos activos.
Cada proyecto tiene su carpeta con documentos de estado y backlog.

### Prompts/
Prompts reutilizables para trabajar con Cursor, LLMs y agentes.
Organizados por dominio: ADRs, PRDs, Estudios, Git, Meta, Presentaciones, Usuarios-sinteticos.

### Iniciativas/
Trabajo activo por iniciativa o proyecto.
Cada iniciativa puede referenciar documentos y PRDs existentes.

## Reglas obligatorias para uso con LLM

- NO inventar carpetas ni rutas.
- Usar SIEMPRE los nombres exactos definidos arriba.
- Citar rutas reales del repositorio.
- Usar las plantillas en Plantillas/ como base obligatoria.
- Si falta una carpeta, proponerla explicitamente antes de asumirla.
- Todo documento nuevo debe usar frontmatter YAML con campos obligatorios (ADR-003).
- Nombres de archivos en kebab-case, sin acentos, sin espacios (ADR-004).
