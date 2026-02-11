# Segundo Cerebro — Instrucciones para LLM

Este repositorio es una base de conocimiento personal versionada.
La fuente de verdad de la estructura es: `Documentos/00-start-here/README.md`

## Estructura del repositorio

```
Plantillas/          → plantillas obligatorias (adr, prd, bench)
Documentos/
  00-start-here/     → mapa del repo (fuente de verdad)
  PRDS/              → PRDs de producto
  Research/          → exploracion temprana, hipotesis
  Estudios/          → analisis estructurados, conocimiento estable
  Estudios/simulaciones/ → simulaciones con usuarios sinteticos
  Decisiones/ADRs/   → decisiones arquitectonicas
  Benchmarks/        → comparativas
  Procesos/          → flujos y procesos
  Presentaciones/    → decks, charlas, workshops
Proyectos/           → estado de proyectos activos
Prompts/             → prompts reutilizables por dominio
Iniciativas/         → trabajo activo por iniciativa
```

## Reglas obligatorias

1. NO inventar carpetas ni rutas. Usar solo las definidas arriba.
2. Usar nombres exactos. Si falta una carpeta, proponerla antes de crearla.
3. Todo documento nuevo debe tener frontmatter YAML con estos campos:
   - titulo, tipo, estado, autor, fecha, updated, tags, fuentes
4. Nombres de archivos en kebab-case, sin acentos, sin espacios, sin mayusculas innecesarias.
5. Prefijos obligatorios por tipo: `prd-`, `benchmark-`, `proceso-`, `presentacion-`, `workshop-`, `ADR-00X-`.
6. Prohibido: sufijos de version (v2, final), indicadores temporales (ok, listo), nombres genericos.
7. Usar plantillas de `Plantillas/` como base obligatoria al crear documentos nuevos.
8. Citar siempre rutas reales del repositorio.

## Flujo cognitivo

Research/ (explorar) → Estudios/ (analizar) → Decisiones/ADRs/ (decidir)

- Research: hipotesis, preguntas abiertas, exploracion temprana
- Estudios: analisis profundos, sintesis, evidencia trabajada
- Decisiones/ADRs: decisiones explicitas tomadas con alternativas y consecuencias

## Convenciones de commit

Formato: `tipo: descripcion breve en espanol`
Tipos: docs, feat, fix, chore, refactor

## Proyecto activo: Wayta IA

Floreria virtual con inspiracion ancestral andina. El motor decide (reglas deterministas), la IA solo narra.
- PRD: `Documentos/PRDS/prd-wayta-ia.md`
- Estado MVP: `Proyectos/Wayta_IA/WAYTA-IA-001-estado-mvp.md`
- ADR inicio: `Documentos/Decisiones/ADRs/ADR-000-inicio-wayta-ia.md`
