---
titulo: Vault brief — Segundo Cerebro
actualizado: 2026-09-26
conceptos_baseline: 103
categorias_baseline: [diseno, economia, filosofia, ia, organizaciones, producto]
---

## 1. Quién soy / qué construyo
- Luigui Avila, diseñador-constructor (diseño + producto + IA). Español.
- Segundo Cerebro: conocimiento atómico en Obsidian para presentaciones, propuestas y charlas. Proyecto visible: Wayta IA.
- Jarvis = agente de mantenimiento: Claude Code (CLAUDE.md) + daemon de voz macOS. Conciso: actúa y reporta.

## 2. Estructura (al 2026-09-26)
- Conocimiento/Conceptos/: 103 en 6 carpetas — ia 41 · filosofia 17 · diseno 15 · organizaciones 12 · producto 12 · economia 6.
- Conocimiento/: Correlaciones/ (29), Fuentes/Sesiones/, ATLAS.md (índice auto-generado).
- Inbox/ (.tmp.md por decidir) · Backlog/ (ideas de proyecto) · docs/ (planes) · Plantillas/ (taxonomia.md, rubrica.md: solo lectura) · Trabajo/Reuniones/ (plantilla de reunión; material de trabajo, no conocimiento atómico) · Prompts/Meta/.

## 3. Decisiones ya tomadas
- 1 concepto = 1 idea atómica; Gate 0 (estructura) + rúbrica Gate 1/2 antes de escribir.
- taxonomia.md y rubrica.md solo se editan si Luigui lo pide.
- Los agentes proponen, Luigui aprueba: candidatos, correlaciones y graduaciones van a Inbox/*.tmp.md.
- Todo queda en JARVIS_LOG.md (append-only, reciente arriba). El watcher regenera el ATLAS solo.
- Ver pantalla: OCR local si es texto, DeepSeek Vision si hay imagen. Intents: Groq (openai/gpt-oss-20b).
- "Archivar" = marcar, no mover ni borrar. Este brief es manual: el watcher solo avisa si se desactualiza.

## 4. Enfoques descartados
- Remotion (video): src perdido; hoy /presentacion-html.
- Claude Vision para ver pantalla: nunca hubo ANTHROPIC_API_KEY (2026-09-15).
- Watcher con confirmación por voz: cuelga el daemon (2026-07-06).
- Groq llama-3.3-70b-versatile: deprecado, 404 (2026-08-25).
- Agentes que escriben al vault sin aprobación · campo nuevo en conceptos (rompe schema) · brief dentro de generar_index.py.

## 5. Rutas clave (raíz ~/Documents/Segundo_cerebro/)
- CLAUDE.md, AGENTS.md (reglas) · CONTEXTO_SEGUNDO_CEREBRO.md (exhaustivo) · context.md (sesión) · JARVIS_LOG.md.
- Plantillas/taxonomia.md, rubrica.md · Conocimiento/ATLAS.md · Prompts/Meta/generar_index.py.
- Prompts/Meta/jarvis/: jarvis.py, jarvis_daemon.py, jarvis.log (log activo).
