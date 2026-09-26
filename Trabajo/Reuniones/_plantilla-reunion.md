---
fecha: YYYY-MM-DD
titulo: Nombre de la reunión
acciones:
  - accion: Qué hay que hacer (verbo + resultado concreto)
    responsable: Quién, tal como se mencionó en la reunión
    fecha: YYYY-MM-DD
---

<!--
Un .md por reunión. Nombre de archivo sugerido: YYYY-MM-DD_titulo-en-kebab-case.md

Reglas (paquete de mejoras 2026-09-26, Mejora C — spec: 2026-09-26_paquete-mejoras-vault.md):
- `acciones`: MÁXIMO 3 entradas, cada una con accion + responsable + fecha.
- No asignar responsables que no se hayan mencionado explícitamente en la reunión.
  Si no se mencionó responsable o fecha, dejar el campo vacío en vez de inventarlo.
- No reemplaza un acta completa: 3 acciones deben bastar para actuar sin releer el transcript.
- v1: el input es solo texto pegado (audio/video queda fuera por decisión de foco).
- Sin integración a calendario ni Slack en v1.
La skill transcript → acciones que rellena este archivo se construye en una sesión aparte.
-->

## Notas
Opcional. Contexto mínimo que ayude a entender las acciones; no es un acta.
