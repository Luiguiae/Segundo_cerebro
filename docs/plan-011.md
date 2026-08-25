---
tipo: plan
mejora: 011
titulo: "Buscador proactivo de correlaciones + Agente graduador de borradores"
fecha: 2026-08-24
estado: implementado
---

# mejora-011 — Buscador de correlaciones + Graduador de borradores

## Objetivo

Dos agentes nuevos que cierran huecos expuestos por la auditoría del 2026-08-24:

1. **Buscador proactivo de correlaciones** — hoy `correlacion-conceptos` es reactivo (Luigui pide el par exacto). Con 101 conceptos y solo 29 correlaciones, hay huecos de grafo sin mapear.
2. **Agente graduador de borradores** — hoy "profundiza este concepto" es manual, uno por uno. Los `borrador` se acumulan sin que nadie los revisite salvo auditoría completa.

## Decisiones confirmadas (2026-08-24)

| decisión | resultado |
|---|---|
| Disparo | Ambos: comando de voz bajo demanda + rutina programada de respaldo (`schedule`) |
| Buscador — escritura | **Nunca auto-escribe.** Propone en `Inbox/*.tmp.md`, Luigui aprueba |
| Graduador — escritura | **Nunca auto-actualiza.** Propone versión enriquecida en `Inbox/*.tmp.md`, Luigui aprueba |

Consecuencia directa de estas 3 decisiones: **ninguno de los dos agentes toca `Conocimiento/Conceptos/` ni `Conocimiento/Correlaciones/` directamente.** Ambos escriben exclusivamente a `Inbox/`, igual que ya hace `modo_taller_captura()`. Se necesita un tercer comando que cierre el loop — sin él, las propuestas se acumulan sin destino, igual que ya pasó con los 8 candidatos del taller.

## Comandos nuevos (documentados en CLAUDE.md, ejecutados vía `ejecutar_claude()` headless — igual que el resto de comandos de vault)

### `Jarvis, busca correlaciones`

1. Lee todos los conceptos `activo` de `Conocimiento/Conceptos/`
2. Identifica sub-conectados: conceptos con 0 o 1 entradas en `relacionado`
3. Genera candidatos de pareja por señales objetivas (no todos los pares — con 101 conceptos son ~5,050 combinaciones):
   - misma `familia`
   - ≥2 tags compartidos
   - mención cruzada literal en el cuerpo de uno hacia el otro
   - **tope: máx. 20 candidatos evaluados por corrida**, priorizados por señal más fuerte (mención cruzada > tags compartidos ≥3 > familia+tags)
4. Por cada candidato, redacta la correlación completa (mismo formato que `correlacion-conceptos`: `## La tensión` / `## El insight no obvio` / `## El límite`)
5. **Autocrítica adversarial antes de proponer** — para cada borrador de correlación, responde explícitamente:
   - ¿El título podría ser "[A] y [B]" sin perder nada? → si sí, descarta (no es tensión real)
   - ¿Alguien que leyó los dos conceptos por separado ya sabe esta conclusión? → si sí, descarta (síntesis obvia)
   - Este paso es el que faltó el 2026-06-25 y produjo las 2 correlaciones truismo que la auditoría de hoy rechazó
6. Escribe `Inbox/YYYY-MM-DD_HHMM_correlaciones-propuestas.tmp.md` con las que sobreviven la autocrítica: contenido completo listo para copiar + 1 línea de justificación de por qué la tensión es real
7. Reporta por voz: "Encontré N propuestas de correlación, quedaron en el Inbox"
8. Registra en `JARVIS_LOG.md`: candidatos evaluados, cuántos sobrevivieron la autocrítica, cuántos se descartaron y por qué

### `Jarvis, gradúa los borradores`

1. Lista todo `estado: borrador` en `Conceptos/` y `Correlaciones/`
2. Por cada uno, busca en `JARVIS_LOG.md` la entrada de auditoría más reciente que lo tocó, para saber el criterio específico que falló (no adivina — si no hay razón registrada, lo reporta como "sin diagnóstico, requiere revisión manual" y no lo toca)
3. **Salta archivos con un intento de graduación en los últimos 14 días** (busca en `JARVIS_LOG.md` entradas `"graduador"` + nombre de archivo) — evita reintentos en loop sobre el mismo borrador débil
4. Corre profundización dirigida al hueco específico (mismo motor que "Jarvis, profundiza este concepto": 1-2 ejes de investigación acotados al criterio fallido, no una reescritura genérica)
5. Re-evalúa Gate 2 sobre la versión enriquecida
6. Si ahora pasa (≥3/4 concepto, 3/3 correlación): añade a `Inbox/YYYY-MM-DD_HHMM_borradores-graduados.tmp.md` — diff antes/después + qué cambió + evaluación Gate 2 nueva
7. Si sigue sin pasar: dentro del mismo archivo `.tmp.md`, sección separada "sin graduar" — qué se intentó y qué sigue faltando (esto también evita reintentos silenciosos en la próxima corrida, aunque el chequeo de 14 días ya lo cubre)
8. Reporta por voz: "Revisé N borradores, M están listos para aprobar en el Inbox"
9. Registra en `JARVIS_LOG.md`

### `Jarvis, revisa propuestas pendientes` (comando nuevo que cierra el loop)

1. Lista todos los `Inbox/*_correlaciones-propuestas.tmp.md` y `Inbox/*_borradores-graduados.tmp.md` sin procesar
2. Presenta cada propuesta (resumen corto por voz si se invoca hablando; contenido completo si se invoca en sesión de texto)
3. Por cada una, espera confirmación explícita antes de escribir — aprobar una correlación la escribe en `Correlaciones/` con `estado: activo` (ya pasó Gate 1+2 en el paso 5 del buscador); aprobar una graduación sobrescribe el concepto/correlación original con `estado: activo`
4. Al aprobar o descartar cada item, lo quita del `.tmp.md`; si el archivo queda vacío, lo borra
5. Regenera ATLAS si hubo escrituras, registra en log

## Rutina programada de respaldo

Vía skill `schedule`: cron semanal (ej. lunes 06:00) que invoca `claude --print --permission-mode bypassPermissions` con la instrucción "Jarvis, busca correlaciones. Luego, Jarvis, gradúa los borradores." — mismo mecanismo que ya usa `ejecutar_claude()`, corriendo sin el daemon de voz activo. Como ninguno de los dos escribe al vault directamente (decisión confirmada), este cron es seguro de dejar desatendido: en el peor caso, llena el Inbox de propuestas sin usar.

Pendiente decidir en la implementación: si el saludo proactivo del daemon debe mencionar "tienes N propuestas pendientes en el Inbox" al arrancar — parece consistente con cómo ya reporta conceptos nuevos, se confirma cuando se implemente.

## Cambios de código

- `CLAUDE.md`: 3 secciones nuevas de comando (arriba) + entrada en "Comandos que entiendes"
- `jarvis.py` / `jarvis_daemon.py`: patrones de intent para las 3 frases nuevas ("busca correlaciones", "gradúa los borradores"/"gradua borradores", "revisa propuestas pendientes"), dispatch a `ejecutar_claude()` igual que los comandos de vault existentes — sin lógica Python nueva, es prompt engineering + intent matching, como el resto de `accion_directa`
- `schedule`: 1 rutina cron nueva (weekly)

## Riesgos

| riesgo | mitigación |
|---|---|
| Coste de evaluar candidatos de correlación (headless Claude corriendo autocrítica sobre hasta 20 pares) | tope explícito de 20/corrida; corre en horario de bajo uso si es cron |
| Graduador reintentando indefinidamente sobre borradores irrecuperables | tope de 14 días entre intentos + límite de 1 intento por corrida por archivo |
| Inbox acumulando `.tmp.md` de propuestas si Luigui no las revisa | el saludo proactivo puede recordarlas (pendiente de decidir en implementación); no es bloqueante — el `.tmp.md` no afecta Gate 0 del resto del vault |
| Candidatos de correlación de baja señal (familia+tags sin relación real) colando por la autocrítica | la autocrítica es el mismo criterio Gate 2 ya validado hoy contra las 2 correlaciones truismo — no es una heurística nueva sin probar |

---

## Implementación (2026-08-24)

- `CLAUDE.md`: agregadas las 3 secciones de comando (`Buscar correlaciones`, `Graduar borradores`, `Revisar propuestas pendientes`) entre "Correlacionar conceptos" y "Auditar el vault"
- `jarvis.py`: agregados los 3 comandos a los ejemplos de `accion_directa` en el prompt del clasificador Groq + regla de desambiguación explícita ("REGLA MEJORA-011") para que no se confundan con `razonamiento_profundo` pese a sonar como pregunta. Sin lógica Python nueva — `accion_directa` ya es un passthrough genérico a `ejecutar_claude()`, confirmado leyendo el dispatch existente
- `jarvis_daemon.py`: sin cambios — reutiliza `detectar_intent`/`despachar_intent` de `jarvis.py` vía `_mod`, confirmado por grep antes de tocar nada
- Validado con `py_compile` en ambos archivos
- Rutina cloud semanal creada vía `RemoteTrigger` (routine id `trig_01EUK43fDMVyeJGNx9adjN1t`, cron `0 11 * * 1` UTC = lunes 06:00 America/Lima, próxima corrida 2026-08-31). **Nota de diseño respecto al plan original:** la skill `schedule` de este entorno solo ofrece rutinas **cloud** (sesión aislada con su propio git checkout), no cron local sobre `ejecutar_claude()` como se asumió al escribir el plan. El prompt de la rutina instruye a la sesión cloud a leer `CLAUDE.md`, ejecutar ambos comandos, y si generó algo en `Inbox/`, hacer `git add/commit/push` directo a `main` — seguro porque ninguno de los dos comandos toca `Conceptos/`/`Correlaciones/` ni cambia `estado` de nada existente, solo agrega archivos de propuesta nuevos.
- El saludo proactivo del daemon **no** se modificó para mencionar propuestas pendientes en Inbox — quedó fuera de este alcance, pendiente de decidir si vale la pena en una iteración futura
