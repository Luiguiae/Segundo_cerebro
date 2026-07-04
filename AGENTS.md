# AGENTS.md — Instrucciones para agentes que operan sobre este vault

> Este archivo es la primera lectura obligatoria para cualquier agente
> (Jarvis, Claude Code, o cualquier herramienta MCP) que interactúe
> con el Segundo Cerebro de Luigui Avila.

## Identidad del vault

- **Propietario:** Luigui Avila (luiguiavilae@gmail.com)
- **Proyecto:** Segundo Cerebro — infraestructura de conocimiento personal
- **Idioma:** Español en todo el contenido. Inglés solo en nombres de archivo
  del sistema (README.md, ATLAS.md, AGENTS.md, CLAUDE.md).

## Estructura de carpetas

```
Segundo_cerebro/
├── Conocimiento/
│   ├── Conceptos/          ← conceptos atómicos por categoría
│   │   ├── ia/
│   │   ├── diseno/
│   │   ├── producto/
│   │   ├── organizaciones/
│   │   ├── economia/
│   │   └── filosofia/
│   └── Correlaciones/      ← relaciones entre conceptos
├── Backlog/                ← ideas de proyectos construibles (SDD)
├── Inbox/                  ← fuentes sin procesar (NO tocar sin instrucción)
└── Prompts/Meta/           ← scripts de Jarvis (NO tocar sin instrucción)
    └── jarvis/
```

## Zonas de acceso

| Zona | Lectura | Escritura | Notas |
|---|---|---|---|
| `Conocimiento/Conceptos/` | ✅ | ✅ | Solo con schema correcto |
| `Conocimiento/Correlaciones/` | ✅ | ✅ | Solo con schema correcto |
| `Backlog/` | ✅ | ✅ | Solo ideas en estado borrador |
| `Inbox/` | ✅ | ⚠️ | Solo Jarvis scout-nocturno escribe aquí |
| `Prompts/Meta/jarvis/` | ✅ | ⚠️ | Solo con instrucción explícita |
| `Conocimiento/ATLAS.md` | ✅ | ⚠️ | Regenerar con generar_index.py |
| `AGENTS.md` | ✅ | ⚠️ | Solo con instrucción explícita |

## Schema obligatorio para conceptos atómicos

Todo archivo en `Conocimiento/Conceptos/[categoria]/` DEBE seguir la plantilla canónica
definida en `Plantillas/taxonomia.md`:

```yaml
---
titulo: "[string]"
tipo: concepto
familia: [string]
tags: []               # máximo 5
relacionado: []        # solo slugs que existen como archivos reales, máximo 3
fecha: YYYY-MM-DD
estado: borrador | activo | archivado
fuentes:               # opcional — obligatorio solo si hay datos verificados
  - titulo: "[string]"
    url: "[url]"
    fecha_acceso: YYYY-MM-DD
---
```

**Regla crítica sobre `relacionado`:** nunca incluir slugs especulativos.
Solo referencias a archivos que existen físicamente en el vault.

## Secciones del body

Obligatorias, siempre:

1. `## El concepto`
2. `## Por qué importa`
3. `## Tensiones y límites`

Opcionales — solo si el concepto tiene datos verificados con fuentes externas (Gen-4):

4. `## Datos y evidencia`
5. `## Ejes investigados`

## Nombrado de archivos

- Siempre kebab-case: `nombre-del-concepto.md`
- Sin caracteres especiales, acentos ni espacios en el nombre de archivo
- El título dentro del frontmatter sí puede tener acentos

## Lo que NUNCA debe hacer un agente

- Crear conceptos fuera de las 6 carpetas canónicas sin instrucción explícita
- Agregar slugs en `relacionado` que no existen en el vault
- Modificar archivos en `Prompts/Meta/jarvis/` sin instrucción explícita
- Sobreescribir `AGENTS.md` o `CLAUDE.md` sin instrucción explícita
- Eliminar archivos (solo el propietario puede eliminar)
