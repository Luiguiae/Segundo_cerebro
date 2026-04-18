# Backlog de Soluciones Construibles

Sistema para capturar, madurar y convertir ideas de proyectos en prompts listos para Jarvis.

## Ciclo de vida de una idea

```
CAPTURA (borrador) → MADURACIÓN (SDD) → LISTO → EN CONSTRUCCIÓN → COMPLETADO
```

## Cómo usar

1. **Captura rápida:** Copia `_plantilla-idea.md` → llena encabezado + Problema → guarda en `ideas/` con estado `borrador`
2. **Maduración:** En Claude.ai, completa las 8 secciones SDD hasta tener SPEC.md + prompt para Jarvis
3. **Arranque:** Cuando la idea está en estado `listo`, crea la carpeta del proyecto fuera del Segundo Cerebro y pega el prompt en Jarvis
4. **Registro:** Actualiza el estado en el frontmatter y en las listas correspondientes

## Estados válidos

| Estado | Descripción |
|---|---|
| `borrador` | Capturada, sin spec completo |
| `en-maduración` | SDD en progreso |
| `listo` | SDD completo, prompt validado |
| `en-construcción` | Jarvis trabajando en el proyecto |
| `completado` | Terminado o descartado |

## Convención de nombres

`YYYY-MM-DD_slug-de-la-idea.md`
