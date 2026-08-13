---
concepto: vigilancia-involuntaria-por-cumplimiento
instalado_en: Conocimiento/Conceptos/ia/vigilancia-involuntaria-por-cumplimiento.md
score: 23/30
motivo_contingencia: Gmail no disponible — el conector solo expone create_draft, sin herramienta de envío real. Se creó borrador en Gmail. Concepto instalado directamente en vault en modo contingencia.
fecha: 2026-08-13
---

## Nota de contingencia — Profundizador-1

El concepto **vigilancia-involuntaria-por-cumplimiento** fue profundizado y guardado directamente en el vault porque Gmail no pudo enviarse (solo disponible `create_draft`, no herramienta de envío real).

Se dejó un borrador en Gmail con el .md completo y las instrucciones de instalación.

**Revisar antes del próximo git pull:**
- Verificar que el frontmatter pasa Gate 0
- Cambiar `estado: borrador` → `estado: activo` si aprueba la rúbrica
- Correr `generar_index.py` para regenerar el ATLAS
