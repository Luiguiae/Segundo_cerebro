---
tipo: plan
mejora: 012
titulo: "Modo taller — análisis de sesión (segunda lente sobre el transcript)"
fecha: 2026-09-02
estado: implementado
---

# mejora-012 — Análisis de sesión en modo taller

## Objetivo

Modo taller (mejora-010) hoy solo mira el transcript crudo con una lente: minería
de candidatos a concepto atómico. Esta mejora agrega una **segunda lente**, sobre
el mismo transcript, sin cambiar la primera: análisis de la sesión como reunión —
tópicos, prioridad, acuerdos/responsables, nivel de información, y cruce con
otras sesiones y con el vault.

## Decisiones confirmadas (2026-09-02)

| decisión | resultado |
|---|---|
| Activación | Siempre corre junto a la extracción de candidatos, al cerrar modo taller — mismo transcript, antes de decidir si se borra |
| Destino del output | `Inbox/*.tmp.md`, mismo patrón que los candidatos — queda como propuesta a revisar |
| Nombres reales | Genéricos por rol/área ("el arquitecto", "un funcionario de banca empresas") — nunca un nombre propio |
| Profundidad del cruce | Solo coincidencias fuertes (mismo tópico ya visto en otra sesión o ya instalado en el vault) — no relaciones vagas |

## Estructura del archivo de análisis

`Inbox/YYYY-MM-DD_HHMM_modo-taller_analisis.tmp.md`:

```markdown
# Análisis de sesión — Taller YYYY-MM-DD HH:MM

## Tópicos principales
[tema]: 1-2 líneas

## Priorización por gravedad
| tópico | gravedad (alta/media/baja) | por qué |

## Acuerdos y responsables
| acuerdo | responsable (rol/área, nunca nombre propio) | condición/cuándo |
(o "Sin acuerdos explícitos detectados.")

## Nivel de información por tópico
| tópico | suficiente / necesita profundizar | qué falta si aplica |

## Cruce con otras sesiones de modo taller
[tópico] ya apareció en [archivo de sesión anterior]
(o "Sin coincidencias fuertes con sesiones anteriores.")

## Cruce con el vault
[tópico] se relaciona con concepto existente `[slug]`
(o "Sin coincidencias fuertes con conceptos existentes.")
```

## Cambios de código (`jarvis_daemon.py`)

1. **Nueva función `_analizar_sesion_taller(transcript_path: Path) -> bool`** — mismo
   patrón que `_extraer_candidatos_taller()`: arma una instrucción para
   `ejecutar_claude()`, el proceso headless lee el transcript, busca por su cuenta
   (Glob/Read — ya tiene las tools) otros `Inbox/*_modo-taller_*.tmp.md` y los
   conceptos `activo` del vault para el cruce, y escribe el `.tmp.md` de análisis.
   Devuelve si se generó o no (para el resumen de voz).
2. **`modo_taller_captura()`**: en el bloque que hoy solo llama a
   `_extraer_candidatos_taller()`, se agrega la llamada a `_analizar_sesion_taller()`
   **en paralelo** (mismo transcript, cada uno escribe un archivo de salida
   distinto — no hay conflicto de escritura entre ellos; el conflicto que evita
   `lock_interaccion` es con OTRA interacción de voz no relacionada, no entre
   estos dos). Se usa `concurrent.futures.ThreadPoolExecutor` — reduce el tiempo
   de espera de Luigui a la mitad frente a correrlos en serie.
   - Import nuevo: `concurrent.futures` (no estaba en el archivo)
3. El resumen de voz combina ambos resultados: "Encontré N candidatos y dejé el
   análisis de la sesión en la bandeja de entrada."
4. El log combinado (`registrar_en_jarvis_log`) reporta ambos resultados en una
   entrada.
5. **Sin cambio a la política de borrado del transcript** — sigue gobernada solo
   por `n_candidatos > 0` (Regla ya existente de mejora-010). El análisis se
   genera antes de esa decisión, así que nunca depende de si el transcript
   sobrevive o no.

## Riesgos

| riesgo | mitigación |
|---|---|
| El modelo escribe un nombre propio real pese a la instrucción | instrucción explícita y repetida en el prompt ("nunca escribas un nombre propio"); no hay verificación automática post-hoc — si aparece uno, se reporta como hallazgo a corregir en una iteración futura (regex de detección de nombres es poco confiable en español, no se intenta ahora) |
| Cruce con vault/otras sesiones consume más tokens/tiempo que la extracción de candidatos | acotado a "coincidencias fuertes" únicamente (decisión ya confirmada) — no es un análisis exhaustivo |
| Tiempo total de espera tras cerrar modo taller sube (dos análisis en vez de uno) | mitigado corriendo ambos en paralelo (concurrent.futures) en vez de en serie |
| El archivo de análisis se acumula en Inbox/ sin revisión, igual que ya pasa con los candidatos | mismo comportamiento aceptado que los candidatos hoy — no se resuelve en este alcance |

---

## Implementación (2026-09-02)

- `jarvis_daemon.py`: agregado `import concurrent.futures`, nueva función
  `_analizar_sesion_taller(transcript_path) -> bool` (mismo patrón que
  `_extraer_candidatos_taller`, prompt con las 6 secciones confirmadas), y
  `modo_taller_captura()` ahora corre ambas extracciones en paralelo vía
  `ThreadPoolExecutor` y combina el resumen de voz y la entrada de log
- Validado `py_compile`
- Confirmado que no había sesión de modo taller activa antes de reiniciar
  (última sesión del día cerró a las 12:00 por tope de 90min)
- Daemon reiniciado (`kill -TERM` + relanzado por `launchd`)
- Nota lateral descubierta al reiniciar: la rutina cloud semanal de mejora-011
  ya había corrido el 2026-08-31 y funcionó en producción — 2 correlaciones
  propuestas (18 descartadas por la autocrítica) y 1 borrador graduado
  (`rutina-trabajo-enfocada`), todo commiteado y pusheado automáticamente por
  la rutina. Mergeado al integrar este trabajo.
