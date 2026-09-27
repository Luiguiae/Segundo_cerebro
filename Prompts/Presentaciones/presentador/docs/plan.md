# Plan — Presentador por gestos y voz (LeIA)

> Estado: **aprobado por Luigui el 2026-09-26** (D1–D6, con las condiciones de la sección 3). Ejecución en curso; ver `docs/tasks.md` para el avance.
> Fuente: `docs/SPEC.md` (sin modificar). Deadline: lunes 2026-09-28.

## 1. Objetivo

Navegar un deck Reveal.js sin tocar la laptop: swipe de mano abierta y comandos de voz ("LeIA siguiente", "avanza 3 slides", "vuelve al inicio"), con teclas para apagar cada canal y un indicador discreto. `presentar.py` sirve la carpeta del deck e inyecta los scripts al servir, sin tocar el HTML en disco.

**Definición de "listo para el lunes":** el checklist de ensayo del SPEC pasa el domingo y el código queda congelado esa noche. Lunes solo se ejecuta, no se programa.

## 2. Hallazgos verificados hoy (2026-09-26, en esta máquina)

| Qué | Resultado |
|---|---|
| Equipo | MacBook Pro Intel i7-9750H, 16 GB, GPU dual (Intel UHD 630 + AMD Radeon Pro 5300M), cámara FaceTime HD. Es el equipo del SPEC, así que el spike de gestos se mide en el hardware real. |
| Software | Chrome 153.0.8010.53 · Python 3.11.15 · Node v24.13.0 (sirve para los tests de `comandos.js` sin dependencias). |
| Reveal.js | Última en npm: **6.0.2** (`dist/` = 5.0 MB). API confirmada leyendo su código: `isReady()`, evento `ready`, `slide()`, `getIndices()`, `getTotalSlides()`. |
| MediaPipe | `@mediapipe/tasks-vision` **1.0.1** (bundle ESM `vision_bundle.mjs` + `wasm/` con 3 variantes de ~11 MB: simd, module, nosimd). Modelo `gesture_recognizer.task` float16 v1: 8 373 440 bytes, URL responde 200. Total `vendor/` estimado ≈ 45–50 MB. |
| MIME en Python 3.11 | `.mjs` → `text/javascript`, `.wasm` → `application/wasm`. `.task` no tiene tipo: hay que fijarlo (`application/octet-stream`). |
| **Teclas** | En Reveal 6.0.2 (leyendo el manejador de teclado, no solo la ayuda): `H` = slide anterior, `G` = saltar a slide y **`V` (keyCode 86) = pausa / pantalla negra**. *Corrección:* la primera versión de este plan dio `V` por libre porque no aparece en la ayuda de Reveal; la condición que puso Luigui al aprobar D1 lo detectó. Libres en el núcleo y en los 6 plugins: `M`, `E`, `I`. Ver D1. |
| Plantillas del vault | `Plantillas/presentaciones/html-base.md` no menciona Reveal: el pipeline actual de presentaciones **no genera Reveal.js**. Ver riesgo R9. |

## 3. Decisiones que necesito que apruebes (desvían o interpretan el SPEC)

- **D1 — Teclas.** Las teclas `G`/`H` del SPEC chocan con Reveal, y `H` de la peor manera: al pulsarla para ocultar el indicador **retrocedería un slide**. El SPEC dice "si alguno choca, se reasigna". Aprobado con **`M` = gestos (mano), `E` = voz (escuchar), `I` = indicador** — `V` se descartó tras la verificación (ver abajo); `M`, `E` e `I` verificadas libres en el núcleo y los plugins de Reveal 6.0.2 (se vuelve a verificar con el deck real en el ensayo). Se cambian también en el checklist de ensayo. **Condición de la aprobación — resultado (2026-09-26): `V` CHOCA.** En el manejador de teclado de Reveal 6.0.2, `[58,59,66,86,190].includes(keyCode) → togglePause()`: `V` dejaría la pantalla proyectada en negro. Reemplazo: `E` ("escuchar"), verificada libre (keyCodes que maneja el núcleo: 13, 27, 32–40, 58, 59, 63, 65, 66, 67, 70, 71, 72, 74, 75, 76, 78, 79, 80, 86, 112, 190, 191; plugins: notes = `S`, search = Ctrl+Shift+F, zoom = Esc). SPEC, tasks y checklist ya actualizados. Alternativa descartada: interceptar `G`/`H` en fase de captura — anula atajos nativos de Reveal, contra "las teclas nativas siguen funcionando siempre".
- **D2 — Archivos extra sobre la estructura del SPEC**: `swipe.js` (detector puro, testeable con trazas reales), `tests/` (`comandos.test.js`, `swipe.test.js`, `test_presentar.py`, `manual/spike-gestos.html`) y `setup_vendor.py`. El SPEC ya pide que `comandos.js` sea testeable por separado; este plan lo extiende a `swipe.js`, el punto de mayor riesgo. No cambian el comportamiento.
- **D3 — `vendor/` no se versiona en git** (≈ 50 MB, engordaría el repo para siempre). `setup_vendor.py` (solo librería estándar) lo reconstruye con versiones y hashes fijos. **Se corre el sábado, con internet, no el lunes.** Alternativa: versionarlo (más simple de reconstruir, repo más pesado).
- **D4 — Interpretación de "con prefijo LeIA".** El prefijo debe ir **seguido inmediatamente** del comando ("… bueno, leia siguiente, gracias"), no comando suelto en cualquier parte del enunciado. Razón: "lea" es también el verbo ("que lea el siguiente párrafo"); con adyacencia no dispara.
- **D5 — Interinos ambiguos.** Con prefijo se evalúan resultados intermedios, pero "avanza" puede ser el inicio de "avanza 3" y "avanza 1" el de "avanza 12". Regla: las palabras sin número posible (`siguiente`, `anterior`, `atrás`, `adelante`, `vuelve al inicio`) disparan al instante; las que admiten número (`avanza`, `adelanta`, `retrocede`, `regresa`) esperan ~500 ms de texto estable o el resultado final. Sigue dentro de "latencia < 1.5 s". Sin esto habría avances de 1 en lugar de 3.
- **D6 — Audio de la voz sale a Google.** La Web Speech API de Chrome manda el audio al servicio de reconocimiento de Google mientras la voz está activa. El SPEC lo acepta implícitamente (Chrome + internet), pero la charla es de trabajo. Si el contenido es sensible, se usa `E` para apagar la voz (o se presenta solo con gestos + teclado). **Aprobado tal cual:** el aviso va en el README y la decisión de usar voz la toma Luigui el día de la charla. Los frames de la cámara **no** salen: MediaPipe corre local en WASM (se verifica en el spike: 0 requests salientes en la pestaña Network).

## 4. Fases (en orden) y dependencias

Ordenadas por **riesgo primero**: el spike de gestos va antes de construir sobre él.

| Fase | Contenido | Depende de | Salida |
|---|---|---|---|
| **F0 Andamiaje** | Estructura, `.gitignore`, `setup_vendor.py`, `vendor/`, `demo/index.html` | — | `vendor/` reproducible; demo navegable con teclado |
| **F1 Servidor** | `presentar.py`: servir, inyectar, abrir Chrome | F0 | `python3.11 presentar.py demo/` abre el demo en `localhost:8765` con el script inyectado |
| **F2 Spike de gestos (go / no-go)** | Medir MediaPipe en este Mac/Chrome y **grabar trazas reales** | F0, F1 | Decisión: gestos siguen / se mitigan / quedan fuera del lunes |
| **F3 Parser de voz** | Casos de prueba primero, luego `comandos.js` | — (puede ir en paralelo a F1–F2) | `node --test` verde |
| **F4 Detector de swipe** | `swipe.js` + tests con trazas de F2 | F2 | 0 disparos inversos en las trazas |
| **F5 Integración** | `presentador.js`: arranque, navegación, cooldown, teclas, indicador, voz, gestos | F1, F3, F4 | Los 5 casos de uso funcionando en el demo |
| **F6 Degradación** | Sin Reveal / sin cámara / sin internet / comando no reconocido | F5 | Matriz de errores del SPEC pasada |
| **F7 Docs, ensayo y cierre** | README, checklist, ensayo con métricas del SPEC §7, congelamiento | F6 | Checklist completo; log + push |

**Calendario propuesto** (hoy sábado 26 por la noche): sábado noche F0–F1 (+ arrancar F2 si alcanza) · domingo mañana F2–F5 · domingo tarde F6 + ensayo completo · **domingo 22:00 congelar código** · lunes solo ejecutar. El plan es ajustable a tu ritmo de revisión: cada tarea espera tu visto bueno.

**Punto de decisión del domingo (plan B):** si a mediodía los gestos no pasan el ensayo, se presenta con **voz + teclado/clicker**, que ya cubre los CU2–CU5; los gestos quedan para v2. No hay que decidirlo hoy.

## 5. Riesgos y mitigaciones

| # | Riesgo | Qué lo causa | Mitigación |
|---|---|---|---|
| **R1** | **Swipe inverso al regresar la mano** (el más probable) | El brazo vuelve tras el swipe y es también un desplazamiento rápido en sentido contrario | Tres capas: (1) cooldown compartido 1500 ms tras cualquier cambio (SPEC); (2) **re-armado**: tras un disparo, no se acepta otro hasta que la mano quede casi quieta o salga del cuadro; (3) el criterio de velocidad (≥25 % del ancho en <400 ms) descarta retornos lentos. Se prueba **offline contra trazas reales** de F2 (incluyendo el retorno natural), no solo a ojo. Dirección: la imagen viene en espejo → se invierte `x`; se comprueba con una traza real de "swipe a mi derecha" |
| **R2** | **MediaPipe Tasks Vision en Chrome sobre Mac Intel 2019** | WASM+WebGL en un equipo con GPU dual; sin garantía de fps; carga del bundle ESM y de los `.wasm` con rutas locales | Spike F2 medido en este equipo: fps sostenidos, CPU, latencia, `delegate` GPU vs CPU, resolución reducida (320×240 / 640×480), 1 mano (`numHands: 1`), detección cada N frames. Umbral propuesto de go: **≥15 fps sostenidos** (con 15 fps caben ≥6 muestras en la ventana de 400 ms). Si no llega → mitigaciones; si aún no → plan B (sin gestos el lunes). Carga desde `/vendor/` con MIME correcto (`.wasm`, `.mjs`) |
| **R3** | **Web Speech se corta solo** | Chrome termina el reconocimiento continuo tras silencios; también `no-speech`, `network`, `audio-capture` | Reinicio automático en `onend`/`onerror` con espera creciente (evita bucle rápido si el error es persistente); `not-allowed` / `service-not-allowed` se tratan como fallo permanente (indicador, sin reintentos infinitos); reinicio limpia el estado de dedupe |
| **R4** | **Doble disparo interim/final** | El mismo enunciado produce resultados intermedios y uno final | Cada resultado se identifica por su **índice** en la lista de Web Speech; al disparar se marca ese índice como consumido y se ignoran sus siguientes actualizaciones (incluido el final). Segunda capa: el cooldown compartido. Con D5 se evitan además los disparos parciales |
| **R5** | **Variantes de transcripción de "LeIA"** | Chrome puede escribir "leia", "Leia", "lea", "le ya", "Lía"… | Lista en un solo arreglo editable en `comandos.js`; modo `--debug` en `presentar.py` muestra la **transcripción cruda** en el indicador para calibrar en el ensayo (lo que pide el checklist). Adyacencia obligatoria (D4) para que "lea" como verbo no dispare. Si `es-PE` transcribe mal, probar `es-MX`/`es-ES` (constante de configuración) |
| **R6** | **Inyección en `index.html` y espera a Reveal** | Reveal puede inicializarse antes o después de nuestro script; el deck puede cargarlo como módulo ESM (entonces no hay `window.Reveal`) | Inyectar antes del **último** `</body>` (o al final si no existe), solo en `/` y `/index.html`, sobre **bytes** (sin decodificar), idempotente, `Content-Length` recalculado; el HTML en disco no se toca (se verifica con hash antes/después). En el navegador: comprobar `Reveal.isReady()` **y** escuchar `ready` (puede haber ocurrido ya), con sondeo y tiempo límite; si vence → indicador "sin Reveal" y la presentación sigue intacta. El README indica cargar Reveal como script clásico desde `/vendor/` |
| **R7** | **Choque de teclas `G`/`V`/`H`** | Confirmado en el código de Reveal 6.0.2: `H` retrocede un slide, `G` abre "Jump to slide" y **`V` pausa (pantalla negra)** | Decisión D1 (`M`/`E`/`I`). Los atajos se ignoran si el foco está en un campo de texto y no se cancela ninguna tecla que no sea la nuestra. Se re-verifica con el deck real (plugins de Reveal pueden añadir atajos) |
| **R8** | **Jarvis local y la cámara/CPU** | El daemon de Jarvis tiene un hilo de visión (ojos cerrados por defecto) y el wake word usa el micrófono; MediaPipe + Chrome + Web Speech en un i7 con Jarvis corriendo puede subir la carga | El SPEC dice que el micrófono se comparte sin problema. Se **mide CPU en el spike con Jarvis corriendo**, y el checklist añade "verificar que los ojos de Jarvis están cerrados" |
| **R9** | **El deck del lunes no es Reveal.js (o usa CDN)** | La plantilla actual del vault no es Reveal; el SPEC deja el contenido del deck fuera de alcance | Es una **dependencia externa** que bloquea el uso, no el desarrollo: confirmar el sábado que el deck del lunes se construye con Reveal y referencia `/vendor/reveal/dist/reveal.js`. Sin Reveal, el presentador solo avisa y no hace nada (SPEC). `demo/` sirve para ensayar mientras tanto |
| **R10** | **Micrófono Bluetooth** | Al usar el micro del auricular, macOS puede pasar a perfil de baja calidad (también para la salida); baja la exactitud del reconocimiento | Ya está en el checklist del SPEC; se mide la exactitud de voz (9/10) con ese micrófono, no con el integrado |
| **R11** | **Deadline** | Dos días y varios canales | Riesgo primero (F2), plan B explícito, congelamiento el domingo 22:00, lunes sin cambios de código |

## 6. Qué NO se toca

`jarvis.py`, `jarvis_daemon.py`, `.zshrc`, `RESOLVER.md`, `ATLAS.md`, conceptos y cualquier archivo del vault fuera de `Prompts/Presentaciones/presentador/` (más `JARVIS_LOG.md`, que solo se añade). Ninguna presentación de trabajo entra al repo: solo `demo/index.html` genérico.

## 7. Verificación de la entrega

Cada tarea de `docs/tasks.md` trae su criterio de done ligado al SPEC. El cierre mide las métricas del SPEC §7 en el ensayo y las registra en `docs/ensayo.md`.

## 8. Pendientes v2 (fuera del alcance del lunes)

- **Reconocimiento de voz local en el navegador** (p. ej. Vosk, WASM) para no enviar audio a Google ni depender de internet (ver D6 y R3). Hoy la voz usa Web Speech API de Chrome porque es lo que fija el SPEC; esto es una mejora posterior, no se hace antes del lunes.
- Que Jarvis/LeIA controlen los slides desde un daemon (ya listado como posible v2 en el SPEC §5).

## 9. Resultados del spike de gestos — T06 (2026-09-26)

Medido en este Mac (i7-9750H, Chrome 153, Intel UHD 630 vía Metal), de pie a la distancia real de presentar, con Jarvis corriendo. Datos crudos en `tests/traces/` (54 trazas + `_resumen.json` + `_cpu.json`; solo coordenadas, sin imágenes).

| Medida | Resultado |
|---|---|
| fps sostenidos (10 s medidos + 3 s de calentamiento) | GPU 640×480: **28.1** (mín 26/s) · GPU 320×240: **29.9** (mín 28) · CPU 640×480: 23.6 (mín 19) · CPU 320×240: 23.2 (mín 22). 100 % de los segundos ≥15 fps en las 4. La cámara entrega 30 fps |
| Latencia cuadro → resultado | GPU: 15–21 ms de media (p95 21–38 ms) · CPU: ≈60 ms (p95 76–90 ms) |
| CPU | Chrome ≈0.3–0.4 núcleos con GPU (0.2 solo con la cámara abierta) y ≈0.9–1.1 con el delegado CPU; equipo completo ≈13 % (12 núcleos lógicos); **Jarvis ≈3.7 % de un núcleo** (sin interferencia apreciable) |
| Red | 0 recursos externos, pero **2 intentos de `POST https://odml.pa.googleapis.com/v1/log`** (bloqueados por la CSP del spike). Ver corrección de D6 abajo |
| Espejo | **Confirmado**: 20/20 swipes válidos se leen en la dirección correcta al invertir `x` |
| Amplitud del swipe | En el cuadro, un swipe real recorre **13–21 % del ancho** (mediana; máx 28 %) en ~230–300 ms, no el ~25 % del SPEC |
| Reconocimiento de la categoría | `Open_Palm` en solo 30–51 % de los cuadros con mano durante un swipe (el resto `None`); en gesticulación normal `Open_Palm` ≈0 % |
| Trazas | derecha 20 intentos (8 válidos con el criterio del spike) · izquierda 20 (7) · retorno 8 (5) · puño/dedo 3 · gesticulación 3 (60 s) |

**Prototipo offline** (solo para dimensionar; sobre los mismos datos, no es evidencia independiente): umbral Δx ≥ 10–12 % en ≤ 500 ms, armado por 3 cuadros de `Open_Palm` en 600 ms, cooldown 1500 ms y re-armado con nueva palma → derecha 15–17/20, izquierda 12–13/20, retorno 5/8, direcciones inversas 1 en 48, y 0–1 falso positivo en 60 s de gesticulación. Sin armado por palma: 4 falsos positivos en 60 s y 3 con puño/dedo.

**Correcciones a este plan a raíz del spike (pendientes de tu decisión):**
- **D6 corregida:** el plan decía que los frames de la cámara no salen y que se verificaría "0 requests salientes". Se verificó y **no es cierto del todo**: `vision_bundle.mjs` (1.0.1) crea siempre un registrador de uso que envía a Google cada 60 s, por HTTP POST en protobuf, métricas del task (tipo `GestureRecognizer`, modo y contadores/latencias según el código; no hay imágenes ni landmarks en ese mensaje, pero no pude decodificar el payload real). No tiene opción para desactivarlo. Propuesta: `presentador.js` bloquea (`fetch`/XHR/`sendBeacon`) las peticiones a `odml.pa.googleapis.com`; el registrador se apaga solo tras el primer fallo. Criterio de done nuevo en T14: 0 peticiones externas con MediaPipe activo.
- **Resolución:** el spike eligió 320×240 solo por fps (todas superan 15 con holgura). La baja resolución es la sospecha principal del bajo reconocimiento de `Open_Palm`; hay que probar 640×480 (28 fps) o 1280×720 antes de dar el diseño del detector por bueno.
- **Umbral del swipe (CU1):** ~25 % del ancho no es alcanzable a esta distancia y campo de visión; los datos apuntan a ~10–12 %, con la palma abierta como condición de armado. Es una desviación del SPEC (que dice "~25 %" y "~400 ms") y requiere tu aprobación.

## 10. Decisiones tras el spike (Luigui, 2026-09-26)

1. **Aprobado:** umbral de swipe ~10–12 % del ancho con la mano abierta como condición de armado, ventana de 500 ms y resolución 640×480 por defecto (SPEC, plan y tasks actualizados).
2. **Aprobado:** `presentador.js` bloquea `fetch`/XHR/`sendBeacon` hacia `odml.pa.googleapis.com` (se instala en T11, antes de cargar MediaPipe); criterio "0 peticiones externas con MediaPipe activo" en T14. Corrige D6: los *frames* no salen, pero MediaPipe intenta enviar telemetría de uso; el bloqueo lo evita.
3. **Ronda 2 del spike** a 640×480 guardando los **21 landmarks** de cada cuadro, para comparar offline dos formas de detectar mano abierta (categoría `Open_Palm` vs. dedos extendidos por geometría) y elegir la de mejor tasa por lado sin falsos positivos en gesticulación. Regla de continuidad: si el resultado es igual o mejor que el prototipo de §9 (derecha ~85 %, izquierda ~65 %, 0–1 falsos positivos) se sigue con T09–T12 y se para antes de T13; si es peor, se detiene y se presentan las cifras antes de T09.
4. La decisión de plan B (voz + teclado) sigue siendo de Luigui al mediodía del domingo.

## 11. Resultados de la ronda 2 del spike (640×480, con 21 landmarks) — Luigui frente a la cámara, 2026-09-26

49 trazas nuevas (`tests/traces/r2-*.json`, con los 21 landmarks por cuadro y lateralidad) + `r2-resumen.json` + `r2-cpu.json`. 30 fps sostenidos a 640×480 con GPU; durante la grabación Chrome ≈0.44 núcleos, equipo 13 %, Jarvis 3.6 % de un núcleo. Sigue habiendo 2 intentos de telemetría a `odml.pa.googleapis.com` (bloqueados por la CSP del spike).

**Comparación offline de "mano abierta"** (mismo detector; solo cambia el predicado de armado). Script reproducible: `tests/manual/spike/comparar_metodos.py`.
- **A · categoría `Open_Palm`** del clasificador.
- **B · geometría con landmarks** (dedos extendidos, y variantes con palma hacia la cámara [signo del producto vectorial según lateralidad] y mano erguida).

Hallazgos:
1. **La resolución NO mejoró el reconocimiento de `Open_Palm`** (durante swipes: derecha 51 %→28 %, izquierda 45 %→43 %, retorno 30 %→31 %; 320×240→640×480). La hipótesis de la ronda 1 queda **refutada**.
2. **La geometría sola no sirve como armado:** "dedos extendidos" está activa en 76–83 % de los cuadros de gesticulación (la gente gesticula con la mano abierta). Añadiendo palma-a-cámara baja a 4 % y con erguida a 0 %, pero **no supera** a la categoría en swipes detectados y da más falsos positivos. **Método elegido: A (categoría `Open_Palm`)**, que es además el más simple.
3. **Qué hace fallar al detector v1 (armado por 3 cuadros de palma):** el **retorno de la mano** es a veces más amplio que el propio swipe corto (izquierda, intentos 1 y 6) y dispara el sentido contrario; y el único falso positivo (en ambos métodos) fue mover la mano abierta ~16 % del ancho al colocarla al inicio de un "reposo".
4. **Detector v2 (mano abierta quieta justo antes del trazo, ≥3 cuadros y dispersión ≤0.08 en 200 ms):** 0 inversos y 0 falsos positivos en 27/27 configuraciones probadas del método A.
5. **Asimetría:** usaste una mano distinta para cada dirección (lateralidad de MediaPipe: 90 % `Right` en derecha, 78 % `Left` en izquierda). El swipe hacia adentro del cuerpo es más corto.

| Configuración | Derecha | Izquierda | Ida y vuelta | Inversos | Falsos positivos (106 s de gesticulación, reposo y puño) |
|---|---|---|---|---|---|
| *Prototipo de la ronda 1 (320×240, v1, TH .10)* | 17/20 (85 %) | 13/20 (65 %) | 5/8 | 1 | 1 (en 60 s) |
| Ronda 2 · A · v1 (TH .10) — todos los intentos | 12/13 (92 %) | 8/19 (42 %) | 7/8 | 1 | 1 |
| Ronda 2 · A · v1 (TH .08, K2) — todos los intentos | 12/13 (92 %) | 11/19 (58 %) | 6/8 | 2 | 1 |
| Ronda 2 · A · **v2** (TH .08) — todos los intentos | 10/13 (77 %) | 10/19 (53 %) | 7/8 | **0** | **0** |
| Ronda 2 · A · v1 (TH .10) — solo intentos válidos* | 9/10 (90 %) | 6/10 (60 %) | 2/2 | 1 | 1 |
| Ronda 2 · A · **v2** (TH .08) — solo intentos válidos* | 8/10 (80 %) | **8/10 (80 %)** | 2/2 | **0** | **0** |
| Ronda 2 · B (geometría) · v2 — todos los intentos | 8/13 (62 %) | 10/19 (53 %) | 3/8 | 0 | 0 |

\* "Válido" = mano vista en ≥50 % de los cuadros y algún movimiento ≥8 % (swipes realmente hechos). Con validación cruzada (afinar en intentos impares, probar en pares) el método A · v2 da 69 % derecha / 53 % izquierda, 0 inversos, 0 falsos positivos; el B da lo mismo con 1 falso positivo.

**Lectura honesta:** sobre la misma base que el prototipo (todos los intentos), el resultado **no es claramente igual o mejor**: derecha sube, pero izquierda queda por debajo del ~65 % (42–58 % con v1, 53 % con v2). Con solo los intentos válidos, v2 llega a 80 %/80 % sin inversos ni falsos positivos, pero sigue por debajo del 9/10 del SPEC. Por eso se **detuvo el avance a T09** y se presentaron las cifras. Límites: n ≤ 19 por lado, una persona, una sesión, parámetros afinados sobre los mismos datos; 106 s de no-swipe (el SPEC pide 10 min sin cambios no intencionales).
