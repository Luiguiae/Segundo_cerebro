---
tipo: plan
id: mejora-006
titulo: Memoria y Conciencia Contextual de Jarvis
fecha: 2026-07-04
estado: pendiente-aprobacion
---

# Plan — Memoria y Conciencia Contextual de Jarvis

> Basado en `mejora-006-spec.md`. Numeración del sistema de mejoras del vault — sin
> colisión real con `mejora_006_filesystem.py` (numeración de módulos Python internos,
> un espacio de nombres distinto). Corregido tras aclaración de Luigui.

---

## Hallazgos previos a la implementación

Antes de tocar código, esto es lo que encontré leyendo `jarvis.py` y `jarvis_daemon.py` tal como están hoy (post auditoría del 2026-07-04), que cambia el alcance de 2 de los 6 módulos de la spec.

### 1. Módulo 2 (`que_hicimos`) se solapa con algo que ya funciona

`jarvis.py` ya tiene un intent `consulta_simple` con esta lógica (líneas ~560-577):

```python
_LOG_KEYWORDS = ("hoy", "hicimos", "cambios", "actualizaciones", "historial", "hiciste", "resumen del día", "resumen del dia")

def cargar_contenido_vault_por_pregunta(instruccion: str) -> str:
    if any(k in instruccion.lower() for k in _LOG_KEYWORDS):
        # lee las últimas 100 líneas de JARVIS_LOG.md y se las pasa a Groq
```

Es decir: "Jarvis, qué hicimos hoy" **ya** dispara esto, ya lee el log, y ya responde por voz. Lo que falta es específicamente el filtro por período (ayer vs. hoy vs. esta semana) — hoy toma ciegamente las últimas 100 líneas sin mirar la fecha.

**Recomendación:** en vez de crear un intent nuevo `que_hicimos` (que competiría con `consulta_simple` por las mismas frases y obligaría a desambiguar en el prompt de clasificación de Groq), extiendo la función existente para parsear "ayer"/"hoy"/"esta semana" de la instrucción y filtrar las entradas de `JARVIS_LOG.md` por su encabezado de fecha (`### YYYY-MM-DD` o `## YYYY-MM-DD`) antes de pasarlas a Groq. Cero intents nuevos, cero riesgo de desambiguación, reusa el 100% del wiring que ya existe.

### 2. Módulo 5 no tiene el bug que describe la spec — ya funciona

La spec dice: *"el watcher llama despachar_intent('operacion_archivo', ...) pero el dispatch de 'sí' del usuario no está conectado al flujo de reevaluación."*

Leí el código real (`jarvis_daemon.py`, `on_concepto_modificado` + `_ejecutar_accion_pendiente_con_lock` + `_ejecutar_accion_pendiente`) y **esa conexión ya existe y ya funciona**:

```
Watcher detecta cambio → on_concepto_modificado()
  → hablar("¿Quieres que lo re-evalúe?")
  → escuchar_respuesta()
  → si afirmación → _ejecutar_accion_pendiente_con_lock("reevaluar_concepto", slug)
    → ejecutar_claude("Re-evalúa el concepto X contra la rúbrica...")
    → hablar(resumen del resultado)
```

Y hay evidencia real en `JARVIS_LOG.md` del 2026-06-25: `## 2026-06-25 18:20 — WATCHER / Concepto modificado: gestion-del-tiempo / Resultado: Re-evaluado` — funcionó, quedó registrado.

**Lo que la spec realmente pide (y eso sí falta)** es una conversación de varios turnos: evaluar → reportar hallazgos en voz → preguntar "¿guardo?" → guardar → preguntar "¿profundizo con fuentes externas?" → investigar → preguntar "¿guardo la versión enriquecida?". Hoy es una sola pregunta y una sola acción atómica vía `ejecutar_claude` (que tarda hasta 600s y no permite ese ida-y-vuelta). Esto **no es un fix, es una capacidad nueva** construida sobre wiring que ya está sano. Lo trato como tal en las fases de abajo.

### 3. Profundización externa — vía HTTP a `/evaluar`, no importación directa

Correcto: el VPS está desplegado en `https://jarvis-luigui.duckdns.org` (verificado en vivo — `GET /health` responde `{"status":"ok","conceptos":77,"vault_commit":"e13e5dd"}`, y ese `vault_commit` coincide exactamente con el último commit pusheado desde esta Mac, así que el vault del VPS está sincronizado). Las API keys de Tavily/DeepSeek viven en `/home/jarvis/server/.env` del VPS — se quedan ahí, la laptop nunca las necesita.

Leí el contrato real de `POST /evaluar` en `jarvis_server.py`:

```
Request  EvaluarBody   { tipo: "texto"|"url"|"imagen", contenido: str, mime_type: str|None }
Response EvaluarResponse { estado: "candidato_aprobado"|"candidato_rechazado",
                           concepto_borrador: dict|None, resumen_voz: str,
                           razon_rechazo: str|None, correlaciones_sugeridas: list[str] }
Auth: Authorization: Bearer <JARVIS_TOKEN>  (secrets.compare_digest, 401 si no coincide)
```

`resumen_voz` ya viene listo para `hablar()` — el pipeline interno del VPS (extracción → resumen → rúbrica → Tavily → DeepSeek → borrador Gen-4) es exactamente lo que Módulo 5 pide como "profundizar con fuentes externas".

**Ojo con `/confirmar` — no sirve para este caso.** `/confirmar` (el endpoint hermano que escribe el `.md` y hace push) rechaza con `409` si el archivo destino **ya existe** (`jarvis_server.py:258-262: "Ya existe el concepto '{slug}'... No se sobreescribe"`). Tiene sentido para su caso de uso real — crear conceptos nuevos desde la PWA — pero Fase 5b está **enriqueciendo un concepto que ya existe**. Si llamara a `/confirmar` con el `concepto_borrador` que devuelve `/evaluar`, el VPS lo rechazaría siempre (409) porque el slug ya está en el vault.

**Diseño correcto:** uso `/evaluar` solo para obtener la investigación (fuentes + síntesis + resumen de voz) — nunca llamo a `/confirmar`. Si Luigui confirma que quiere guardar la versión enriquecida, tomo las secciones enriquecidas del `concepto_borrador` devuelto (`## Datos y evidencia`, `## Ejes investigados`, fuentes) y las fusiono **localmente** en el archivo existente — mismo mecanismo de escritura que Fase 5a, preservando slug/familia/tags/relacionado del concepto original. El guardado real sigue pasando por el flujo local (escribir, `generar_index.py`, commit), nunca por el VPS.

**Nota aparte — verificar despliegue actual:** el `/health` en vivo devuelve `conceptos`/`vault_commit` en el body — pero hoy mismo corregí `jarvis_server.py` para que `/health` devuelva solo `{"status": "ok"}` (hallazgo de seguridad, ya commiteado y pusheado a GitHub). Que el VPS siga devolviendo la versión vieja significa que el servidor corriendo **no tiene desplegado el código más reciente** — probablemente falta un `git pull` + reinicio del servicio en el VPS. No es bloqueante para Fase 5b (el endpoint `/evaluar` que voy a usar no cambió de contrato), pero vale la pena que redespliegues cuando puedas para que las correcciones de seguridad de hoy (fuga de token, SSRF, etc.) queden activas en producción.

---

## Arquitectura

### Archivos que se tocan

| archivo | qué cambia |
|---|---|
| `Prompts/Meta/jarvis/jarvis.py` | 3 intents nuevos (`recordar_hecho`, `subir_cambios`, `reevaluar_concepto` como intent directo) + extensión de `cargar_contenido_vault_por_pregunta` + carga de `memoria.md` en prompts de Groq |
| `Prompts/Meta/jarvis/jarvis_daemon.py` | Rutina de arranque: sync diario + saludo proactivo, antes de `loop_principal()` |
| `Prompts/Meta/jarvis/memoria.md` | Archivo nuevo — creado vacío con la estructura de la spec |
| `Prompts/Meta/jarvis/rubrica_local.py` *(nuevo)* | Reimplementación ligera de evaluación de rúbrica con Groq (Fase 5a) — lee `Plantillas/rubrica.md` y `Plantillas/taxonomia.md` reales en vez de hardcodear una copia (evita el problema de divergencia que ya existe entre `evaluador.py` y `jarvis_server.py` en el VPS) |
| `~/Library/Application Support/Jarvis/env` | Se agrega `JARVIS_TOKEN=...` — mismo archivo protegido (chmod 600) donde ya vive `GROQ_API_KEY` desde hoy. Necesito que me pases el valor real (vive en `/home/jarvis/server/.env` del VPS) — no tengo acceso SSH configurado para leerlo yo mismo. |

### Por qué no reutilizar `ejecutar_claude` para Módulo 5

`ejecutar_claude` dispara un proceso `claude --print` completo (hasta 600s, sin diálogo intermedio). El flujo de Módulo 5 necesita hablar, escuchar una confirmación, y solo entonces actuar — eso requiere llamadas Groq directas y rápidas (`responder_con_groq`, ya existe), no un subproceso atómico. Es coherente con lo que la spec ya pide explícitamente en "Restricciones técnicas": *"la evaluación de rúbrica se reimplementa localmente con Groq"*.

---

## Fases

Ordenadas de menor a mayor riesgo/dependencia. Cada fase es un commit independiente — puedes aprobar y ejecutar por fases si prefieres no hacer las 5 de una vez.

### Fase 1 — Memoria personal (Módulo 1)
Nuevo intent `recordar_hecho`. Crea `memoria.md`. Carga su contenido en el system prompt de `conversacion_libre` y `consulta_simple`. Sin dependencias de otras fases.
**Riesgo:** bajo. **Valor:** alto (lo pediste primero en la spec, y es la base de "conciencia contextual" para las demás fases).

### Fase 2 — Qué hicimos (Módulo 2, con el alcance recortado del hallazgo 2)
Extiende `cargar_contenido_vault_por_pregunta` con filtro de período. Sin intent nuevo.
**Riesgo:** bajo. **Depende de:** nada.

### Fase 3 — Subir cambios (Módulo 6)
Nuevo intent `subir_cambios`, calco casi exacto del patrón de `sincronizar_vault` que ya existe (mismo manejo de `GIT_TERMINAL_PROMPT`, mismo `stdin=DEVNULL`), pero con `git status --porcelain` antes de comprometer (para poder decir "no había cambios pendientes" con precisión, mismo patrón que usé hoy en `git_sync.py` del VPS).
**Riesgo:** bajo — reusa código que ya está probado en producción.
**Nota de concurrencia:** verifiqué que esto no introduce una race nueva — tanto este intent como las escrituras del watcher pasan por el mismo `lock_interaccion` que ya serializa el acceso (confirmado hoy mismo: vi al watcher auto-commitear un concepto mientras yo trabajaba, sin pisarse con nada).

### Fase 4 — Saludo proactivo + sync al arrancar (Módulos 3 + 4, combinados)
La propia spec dice que deben combinarse en un solo mensaje — los implemento como una sola rutina `_saludo_proactivo_y_sync()` en `jarvis_daemon.py`, llamada una vez en `main()` antes de `loop_principal()`:
1. Si `~/.jarvis_last_sync` no es hoy → `git pull origin main` silencioso (reusa la secuencia fetch/diff/pull que ya existe en `sincronizar_vault`).
2. Lee `git log --since=<~/.jarvis_last_boot>` sobre el repo YA actualizado — esto cubre en una sola consulta tanto lo que se acaba de traer de GitHub como cualquier commit local del watcher desde el último arranque.
3. Arma un solo saludo con `hablar(...)` antes de que `loop_principal` empiece a escuchar wake word.
4. Todo el bloque en try/except — si git falla, saludo estándar, el daemon arranca igual.
**Riesgo:** medio — toca la secuencia de arranque del daemon, que hoy no tiene ningún `hablar()` antes de `loop_principal`. Hay que verificar que el saludo no se confunda con eco al abrir el micrófono (debería ser seguro: `hablar()` ya actualiza `_last_hablar_end_time` y `esperar_wake_word` ya respeta ese buffer antes de abrir el stream).

### Fase 5a — Watcher conversacional: evaluar, reportar, confirmar, guardar
La parte de Módulo 5 que no depende del VPS. Nuevo `rubrica_local.py` con una función `evaluar_concepto_con_groq(ruta) -> dict` que lee el `.md`, arma el prompt desde `Plantillas/rubrica.md` + `Plantillas/taxonomia.md` reales (no copia hardcodeada), llama a Groq, y devuelve hallazgos + propuesta de cambios estructurada. Nuevo intent `reevaluar_concepto` (accesible por voz directa, no solo desde el watcher — reusa `_ultimo_slug_de_historial()` si no se especifica cuál). El flujo:
```
"Jarvis, reevalúa esto" / watcher detecta cambio
→ evaluar_concepto_con_groq(ruta)
→ Jarvis reporta hallazgos en voz
→ "¿guardo los cambios?"
→ si sí: escribe el .md, corre generar_index.py, git commit
→ "¿quieres que profundice con fuentes externas?"
→ [Fase 5b — ver abajo]
```
**Riesgo:** alto — es la fase más grande, con más superficie nueva (parsing de respuesta de Groq, escritura de archivo, diálogo de 2 turnos).
**Depende de:** Fase 1 (para que Groq tenga memoria.md como contexto de las decisiones que toma) — no estrictamente necesario pero más coherente si va después.

### Fase 5b — Profundización con fuentes externas vía VPS
Nueva función `_profundizar_via_vps(contenido: str) -> dict | None` en `jarvis.py`:
```
"¿quieres que profundice con fuentes externas?" → sí
→ hablar("Investigando con fuentes externas, esto puede tardar un minuto...")
→ POST https://jarvis-luigui.duckdns.org/evaluar
    headers: Authorization: Bearer <JARVIS_TOKEN>
    body: {"tipo": "texto", "contenido": <cuerpo del concepto>}
    timeout: 120s
→ si estado == "candidato_rechazado": hablar(resumen_voz) y terminar sin escribir nada
→ si estado == "candidato_aprobado":
    hablar(resumen_voz)  ← ya viene listo para TTS, no hace falta resumir de nuevo
    "¿guardo la versión enriquecida?"
    → si sí: fusiono localmente las secciones enriquecidas (Datos y evidencia,
      Ejes investigados, fuentes) del concepto_borrador recibido DENTRO del
      archivo existente — preservando slug/familia/tags/relacionado originales.
      NUNCA llamo a /confirmar (rechaza con 409 porque el concepto ya existe —
      ver hallazgo 3). Guardo con el mismo mecanismo local de Fase 5a:
      escribir → generar_index.py → git commit.
```
**Riesgo:** medio — la superficie nueva es acotada (una llamada HTTP + un merge de secciones), pero depende de una API externa con latencia real (~30-90s) y de que el `JARVIS_TOKEN` esté correctamente guardado localmente. Manejo explícito de: timeout, error de conexión (VPS caído/DNS), y respuesta `candidato_rechazado`.
**Depende de:** Fase 5a (usa el mismo mecanismo de escritura local) y de que Luigui provea el valor de `JARVIS_TOKEN` para guardarlo en `~/Library/Application Support/Jarvis/env`.

---

## Riesgos generales

- **`memoria.md` sin cota de crecimiento** — la spec no pide límite y no lo agrego por iniciativa propia, pero lo señalo: con uso diario puede crecer indefinidamente. Si te molesta en el futuro, es un ajuste menor (podar por fecha).
- **Fase 4 es la única que toca la secuencia de arranque del daemon** — la más fácil de romper de forma silenciosa (un error ahí podría dejar al daemon sin saludo, sin crashear — bajo impacto real, pero avísame si prefieres que la deje para el final en vez de en medio).
- **Fase 5a introduce una segunda vía para editar conceptos** (además de `ejecutar_claude`/Claude Code) — dos caminos que escriben `.md` y hacen `git commit` de formas ligeramente distintas. Vale la pena que ambos escriban al log con el mismo formato (ya lo contemplo en las tasks) para no perder trazabilidad.

---

## Qué necesito confirmar

1. ¿De acuerdo con recortar Módulo 2 a una extensión de `consulta_simple` en vez de un intent nuevo?
2. ¿De acuerdo con el diseño de Fase 5b (usar `/evaluar` solo para investigar, nunca `/confirmar`, guardar siempre en local)?
3. Necesito el valor real de `JARVIS_TOKEN` (vive en `/home/jarvis/server/.env` del VPS) para guardarlo en el archivo protegido de la laptop — pégamelo cuando apruebes, o dime si prefieres que lo pida por otro canal.
4. ¿Quieres las 6 fases (1, 2, 3, 4, 5a, 5b) en un solo lote, o las apruebas y ejecutas de a una?

Si no dices nada puntual sobre 1-2, asumo que las recomendaciones de arriba están bien y genero `tasks-006.md` sobre esa base.
