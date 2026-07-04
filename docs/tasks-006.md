---
tipo: tasks
id: mejora-006
titulo: Tareas — Memoria y Conciencia Contextual de Jarvis
fecha: 2026-07-04
estado: completado
---

# Tareas — mejora-006

> Depende de la aprobación de `plan-006.md`. Cada tarea es lo bastante chica para un commit propio.
> "Hecho cuando" usa el mismo formato DADO/CUANDO/ENTONCES que ya usa la spec y la rúbrica del vault.

---

## Fase 1 — Memoria personal

### 1.1 — Crear `memoria.md`
Archivo nuevo en `Prompts/Meta/jarvis/memoria.md`, con la estructura exacta de la spec (`## Hechos personales`, `## Preferencias`, `## Notas de contexto`), vacío salvo el encabezado.
**Hecho cuando:** el archivo existe y `cargar_memoria()` (tarea 1.5) lo lee sin error incluso vacío.

### 1.2 — Intent `recordar_hecho` en el clasificador Groq
Agregar la categoría al system prompt de `detectar_intent_groq` (mismo lugar donde vive `sincronizar_vault`), con señales: "recuerda que...", "mi [dato] es...", "olvida que...". Params: `accion` (`agregar` | `olvidar`), `hecho` (texto literal).
**Hecho cuando:** decir "Jarvis, recuerda que mi mascota se llama Nama" clasifica como `recordar_hecho` con `accion=agregar`.

### 1.3 — Keyword fallback para `recordar_hecho`
Mismo patrón que el bloque `SINCRONIZAR` en `detectar_intent_keywords` — activa con "recuerda que", "olvida que", sin depender de Groq.
**Hecho cuando:** con `GROQ_API_KEY` invalidada temporalmente, el mismo comando de 1.2 sigue clasificando correctamente.

### 1.4 — Handler del intent en `_despachar_intent_impl`
- `accion=agregar`: agrega línea `- [YYYY-MM-DD] {hecho}` a `## Hechos personales` de `memoria.md`. Confirma: "Anotado, lo recordaré."
- `accion=olvidar`: envía el contenido actual de `memoria.md` + la instrucción a Groq, pide que devuelva el archivo completo con la línea correspondiente removida (más robusto que regex — el usuario no repite el texto exacto). Sobreescribe el archivo. Confirma: "Listo, lo olvidé." o "No encontré eso en mi memoria." si Groq no encuentra coincidencia.
**Hecho cuando:** los 3 ejemplos de la spec ("recuerda que mi mascota...", "mi cumpleaños es...", "olvida que tengo dos gatos") funcionan de punta a punta y persisten en el archivo.

### 1.5 — Cargar `memoria.md` como contexto
Función `cargar_memoria() -> str` (mismo patrón que `cargar_contenido_vault_por_pregunta`). Inyectarla en el `system_prompt_override` de `conversacion_libre` y `consulta_simple`.
**Hecho cuando:** tras recordar un hecho, una pregunta en una sesión nueva ("Jarvis, cómo se llama mi mascota") lo devuelve correctamente — el criterio de aceptación literal del Módulo 1 de la spec.

### 1.6 — Log
`registrar_en_jarvis_log("MEMORIA", instruccion, resultado)` en ambas ramas del handler.

---

## Fase 2 — Qué hicimos (extensión de `consulta_simple`)

### 2.1 — Parser de período
Función `_parsear_periodo(instruccion: str) -> tuple[date, date] | None` — reconoce "ayer" (día calendario anterior), "hoy" (día actual), "esta semana" (últimos 7 días), retorna `None` si no hay período explícito (comportamiento actual: últimas 100 líneas sin filtrar).
**Hecho cuando:** las 4 frases de ejemplo de la spec ("qué hicimos ayer", "qué hicimos esta semana", "resumen de actividad reciente", "qué cambios hice al vault") producen el rango correcto o `None` según corresponda.

### 2.2 — Filtrar `JARVIS_LOG.md` por período
Extender `cargar_contenido_vault_por_pregunta`: si `_parsear_periodo` devuelve un rango, parsear los encabezados de entrada (`### YYYY-MM-DD` / `## YYYY-MM-DD HH:MM`) y quedarse solo con las entradas dentro del rango, antes de pasarlas a Groq. Si el rango no tiene entradas, decirlo explícitamente en vez de que Groq alucine actividad.
**Hecho cuando:** "qué hicimos ayer" en un día sin actividad registrada responde "no encontré actividad registrada ayer" en vez de inventar algo con las últimas 100 líneas genéricas.

### 2.3 — Verificación manual
Probar los 4 ejemplos de la spec contra el log real del vault (que ya tiene meses de historial) y confirmar que el resumen hablado es coherente con lo que dice `git log` para esas fechas.

---

## Fase 3 — Subir cambios

### 3.1 — Intent `subir_cambios`
Categoría nueva en el clasificador Groq + keyword fallback (mismo patrón que `sincronizar_vault`/`SINCRONIZAR`), señales: "sube los cambios", "sincroniza hacia arriba", "push al servidor". Sin params adicionales.

### 3.2 — Handler
```
git status --porcelain  → si vacío: hablar("No había cambios pendientes.") y salir
git add -A
git commit -m "feat: cambios via Jarvis [timestamp]"
git pull --rebase origin main   ← agregado respecto a la spec: evita el mismo problema
                                    de push no-fast-forward que corregí hoy en git_sync.py
git push origin main
```
Mismo `GIT_TERMINAL_PROMPT=0` + `stdin=subprocess.DEVNULL` que ya usa `sincronizar_vault`. Éxito: "Listo, cambios subidos al servidor." Sin cambios: mensaje de 3.1. Error: "Hubo un problema al subir los cambios. Revisa la conexión."
**Hecho cuando:** con cambios reales pendientes en el vault, decir "Jarvis, sube los cambios al servidor" los publica en GitHub y lo confirma por voz; repetirlo inmediatamente después dice "no había cambios pendientes".

### 3.3 — Log
`registrar_en_jarvis_log("SYNC", instruccion, resultado)` — mismo tipo que usa `sincronizar_vault`, para que ambos queden juntos en cualquier futura consulta de "qué hicimos" (Fase 2).

---

## Fase 4 — Saludo proactivo + sync diario al arrancar

### 4.1 — Utilidades de timestamp
`_leer_timestamp(path: Path) -> str | None` / `_escribir_timestamp(path: Path) -> None` — ISO en la primera línea, `None` si el archivo no existe (primer arranque). Ubicación: `~/.jarvis_last_boot`, `~/.jarvis_last_sync`.

### 4.2 — Sync diario
`_sync_diario_si_corresponde() -> list[str]` — si la fecha de `~/.jarvis_last_sync` no es hoy (o el archivo no existe), corre `git pull origin main` (mismo patrón fetch/pull que `sincronizar_vault`, sin el paso de `diff` previo porque aquí no hace falta reportarlo por separado — el log-since de 4.3 ya lo cubre). Actualiza el timestamp. Retorna lista vacía si ya se sincronizó hoy o si falla (silencioso, sin bloquear).

### 4.3 — Saludo con novedades
`_saludo_con_novedades() -> str` — corre `git log --since=<~/.jarvis_last_boot o "24 hours ago" si no existe> --oneline` sobre el repo ya actualizado por 4.2, extrae slugs de los mensajes de commit, arma: "Buenos días Luigui. Desde la última vez que hablamos, se agregaron N conceptos nuevos: [slugs]. ¿Quieres que los revisemos?" o el saludo estándar si no hay nada. Actualiza `~/.jarvis_last_boot`.

### 4.4 — Integrar en el arranque
Llamar `_sync_diario_si_corresponde()` y `_saludo_con_novedades()` (todo el bloque en un solo try/except) en `main()` de `jarvis_daemon.py`, después de `_iniciar_dashboard()` y antes de `loop_principal(lock_interaccion)`. Si cualquier paso falla: log del error, saludo estándar ("Jarvis listo. ¿En qué te ayudo?"), el daemon sigue arrancando igual.
**Hecho cuando:** matar el daemon, crear un concepto de prueba con otra sesión de Claude Code (o esperar una sincronización real), y volver a levantar el daemon — el saludo lo menciona. Sin novedades, saluda estándar. Con git roto a propósito (ej. permisos), el daemon arranca igual y saluda estándar.

### 4.5 — Verificación de no-bloqueo
Confirmar con un timeout corto en las llamadas git de 4.2/4.3 (ej. 15s) que un git colgado (mismo síntoma que el bug de `sincronizar_vault` que arreglamos hoy con `GIT_TERMINAL_PROMPT=0`) no deja al daemon sin arrancar indefinidamente.

---

## Fase 5a — Watcher conversacional (evaluar → reportar → confirmar → guardar)

### 5a.1 — `rubrica_local.py` — builder de prompt desde archivos reales
Función `_construir_prompt_rubrica() -> str` que lee `Plantillas/rubrica.md` y `Plantillas/taxonomia.md` completos y arma el system prompt de evaluación a partir de su contenido real — no una copia hardcodeada (evita repetir el problema de divergencia que encontré hoy entre `evaluador.py` y `jarvis_server.py` en el VPS).

### 5a.2 — Función de evaluación
`evaluar_concepto_con_groq(ruta: Path) -> dict` — lee el `.md`, llama a Groq con el prompt de 5a.1 pidiendo JSON estructurado: `{"pasa_gate1": bool, "pasa_gate2": bool, "hallazgos": [...], "propuesta_frontmatter": {...} | null, "propuesta_cuerpo": str | null}`. Reusa el patrón de `response_format: json_object` que ya usa `detectar_intent_groq`.

### 5a.3 — Intent `reevaluar_concepto` (voz directa, no solo watcher)
Nueva categoría Groq + keyword fallback. Sin `slug` explícito → usa `_ultimo_slug_de_historial()` (ya existe en `jarvis.py`, mismo patrón que "léelo sin contexto").
**Hecho cuando:** "Jarvis, reevalúa este concepto" después de leer uno por voz lo identifica correctamente.

### 5a.4 — Diálogo de confirmación
Reemplaza el cuerpo de `_ejecutar_accion_pendiente`'s ramas `"reevaluar_concepto"`/`"evaluar_concepto"` (hoy llaman a `ejecutar_claude`) por:
```
resultado = evaluar_concepto_con_groq(ruta)
hablar(resumen de resultado["hallazgos"])
if hay propuesta:
    hablar("¿Guardo estos cambios?")
    respuesta = escuchar_respuesta()
    si afirmación → tarea 5a.5
hablar("¿Quieres que profundice con fuentes externas?")
respuesta = escuchar_respuesta()
si afirmación → Fase 5b
```
**Importante:** esto reemplaza el uso de `ejecutar_claude` SOLO en este flujo del watcher — no toca `accion_directa` ni el resto de intents que sí lo siguen usando.

### 5a.5 — Guardar cambios confirmados
Escribe `propuesta_frontmatter`/`propuesta_cuerpo` al archivo, corre `generar_index.py`, hace `git add <ruta> && git commit`. Reusa `_sanitizar_slug`-equivalente si aplica. Confirma por voz.

### 5a.6 — Log
Mismo formato `registrar_en_jarvis_log("WATCHER", ...)` que ya usa el flujo actual, para no romper la trazabilidad existente.

---

## Fase 5b — Profundización externa vía VPS

### 5b.1 — Guardar `JARVIS_TOKEN` localmente
Agregar `JARVIS_TOKEN=<valor real, provisto por Luigui>` a `~/Library/Application Support/Jarvis/env` (mismo archivo protegido, chmod 600, donde ya vive `GROQ_API_KEY` desde la corrección de hoy). El launcher de `Jarvis.app` ya hace `source` de ese archivo — no hace falta tocar el launcher de nuevo.
**Hecho cuando:** `os.environ.get("JARVIS_TOKEN")` devuelve el valor correcto dentro del daemon corriendo.

### 5b.2 — Función `_profundizar_via_vps(contenido: str) -> dict | None`
En `jarvis.py`. `POST https://jarvis-luigui.duckdns.org/evaluar` con `Authorization: Bearer <JARVIS_TOKEN>`, body `{"tipo": "texto", "contenido": contenido}`, `timeout=120`. Maneja: `requests.Timeout` → habla "El servidor tardó demasiado, Luigui." y retorna `None`; `requests.ConnectionError` → habla "No pude conectar con el servidor, Luigui." y retorna `None`; `401` → habla "El token del servidor no es válido, Luigui." (señal de que 5b.1 quedó mal) y retorna `None`. Éxito: retorna el JSON de `EvaluarResponse` tal cual.
**Hecho cuando:** con el VPS real (`https://jarvis-luigui.duckdns.org/health` ya verificado arriba), pasar el cuerpo de un concepto real devuelve un `EvaluarResponse` válido con `estado="candidato_aprobado"` y `resumen_voz` no vacío.

### 5b.3 — Integrar en el diálogo de Fase 5a
Después de "¿guardo los cambios?" (5a.4), agregar: "¿quieres que profundice con fuentes externas?" → si sí → `hablar("Investigando con fuentes externas, esto puede tardar un minuto...")` → `_profundizar_via_vps(cuerpo_actual_del_concepto)`.
- Si `None` (error ya hablado en 5b.2): terminar el flujo sin tocar el archivo.
- Si `estado == "candidato_rechazado"`: `hablar(resumen_voz)` y terminar sin escribir nada.
- Si `estado == "candidato_aprobado"`: `hablar(resumen_voz)`, preguntar "¿guardo la versión enriquecida?".

### 5b.4 — Fusión local de las secciones enriquecidas
Si el usuario confirma en 5b.3: tomar `concepto_borrador["el_concepto"]`/`["por_que_importa"]`/`["tensiones_y_limites"]`/`["datos_y_evidencia"]`/`["ejes_investigados"]`/`["fuentes"]` del JSON recibido (verificar nombres exactos de campos contra `_construir_md_gen4` en `jarvis_server.py` antes de implementar) y reemplazar/agregar esas secciones en el archivo **existente**, preservando su frontmatter original (`titulo`, `slug` vía nombre de archivo, `familia`, `tags`, `relacionado`, `edges`, `estado`). **Nunca** invocar `/confirmar` — ver hallazgo 3 del plan (rechaza con 409 porque el concepto ya existe). Corre `generar_index.py`, `git add <ruta>`, `git commit -m "feat: profundiza {slug} con fuentes externas via Jarvis"`.
**Hecho cuando:** al confirmar, el archivo local queda con secciones nuevas basadas en investigación real (fuentes verificables con URL), el frontmatter original no cambió, y el commit queda registrado.

### 5b.5 — Log
`registrar_en_jarvis_log("WATCHER", f"Profundización externa: {slug}", resultado)` — mismo formato que el resto del flujo de Fase 5a/watcher.

### 5b.6 — Verificación manual de red
Probar explícitamente: (a) VPS accesible → flujo completo funciona; (b) `JARVIS_TOKEN` incorrecto a propósito → mensaje de error claro, nada se rompe; (c) desconectar el wifi antes de confirmar "profundiza" → mensaje de error de conexión, el daemon sigue vivo y responde al siguiente wake word.

---

## Nota — despliegue del VPS desactualizado

`GET https://jarvis-luigui.duckdns.org/health` responde con `conceptos`/`vault_commit` en el body — la versión corregida de hoy (auditoría de seguridad) reduce `/health` a solo `{"status":"ok"}`. Esto no bloquea ninguna tarea de aquí (el contrato de `/evaluar` no cambió), pero confirma que el servidor en producción no tiene el código más reciente desplegado. Redesplegar (`git pull` + reiniciar el servicio en el VPS) queda fuera del alcance de mejora-006 — es una tarea de operaciones aparte.

---

## Orden recomendado de ejecución

Fase 1 → Fase 2 → Fase 3 → Fase 4 → Fase 5a → Fase 5b. Cada una es un commit independiente y funcional por sí sola — no hay que esperar a tener todas para probar valor real.
