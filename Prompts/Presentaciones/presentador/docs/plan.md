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
| **Teclas** | En Reveal 6.0.2 **`H` = "Previous slide / Navigate left"** y **`G` = "Jump to slide"**. `V` no tiene atajo por defecto. Ver decisión D1. |
| Plantillas del vault | `Plantillas/presentaciones/html-base.md` no menciona Reveal: el pipeline actual de presentaciones **no genera Reveal.js**. Ver riesgo R9. |

## 3. Decisiones que necesito que apruebes (desvían o interpretan el SPEC)

- **D1 — Teclas.** Las teclas `G`/`H` del SPEC chocan con Reveal, y `H` de la peor manera: al pulsarla para ocultar el indicador **retrocedería un slide**. El SPEC dice "si alguno choca, se reasigna". Propongo **`M` = gestos (mano), `V` = voz, `I` = indicador**, libres en los atajos por defecto de Reveal 6.0.2 (se vuelve a verificar en el spike con el deck real). Se cambian también en el checklist de ensayo. **Condición de la aprobación:** antes de T12, comprobar en `vendor/reveal/dist/reveal.js` si el `keyCode` 86 (`V`) está entre las teclas que activan la pausa / pantalla negra (no solo en la ayuda); si choca, se propone otra tecla libre, se verifica igual y se actualizan SPEC, tasks y checklist. Alternativa descartada: interceptar `G`/`H` en fase de captura — anula atajos nativos de Reveal, contra "las teclas nativas siguen funcionando siempre".
- **D2 — Archivos extra sobre la estructura del SPEC**: `swipe.js` (detector puro, testeable con trazas reales), `tests/` (`comandos.test.js`, `swipe.test.js`, `test_presentar.py`, `manual/spike-gestos.html`) y `setup_vendor.py`. El SPEC ya pide que `comandos.js` sea testeable por separado; este plan lo extiende a `swipe.js`, el punto de mayor riesgo. No cambian el comportamiento.
- **D3 — `vendor/` no se versiona en git** (≈ 50 MB, engordaría el repo para siempre). `setup_vendor.py` (solo librería estándar) lo reconstruye con versiones y hashes fijos. **Se corre el sábado, con internet, no el lunes.** Alternativa: versionarlo (más simple de reconstruir, repo más pesado).
- **D4 — Interpretación de "con prefijo LeIA".** El prefijo debe ir **seguido inmediatamente** del comando ("… bueno, leia siguiente, gracias"), no comando suelto en cualquier parte del enunciado. Razón: "lea" es también el verbo ("que lea el siguiente párrafo"); con adyacencia no dispara.
- **D5 — Interinos ambiguos.** Con prefijo se evalúan resultados intermedios, pero "avanza" puede ser el inicio de "avanza 3" y "avanza 1" el de "avanza 12". Regla: las palabras sin número posible (`siguiente`, `anterior`, `atrás`, `adelante`, `vuelve al inicio`) disparan al instante; las que admiten número (`avanza`, `adelanta`, `retrocede`, `regresa`) esperan ~500 ms de texto estable o el resultado final. Sigue dentro de "latencia < 1.5 s". Sin esto habría avances de 1 en lugar de 3.
- **D6 — Audio de la voz sale a Google.** La Web Speech API de Chrome manda el audio al servicio de reconocimiento de Google mientras la voz está activa. El SPEC lo acepta implícitamente (Chrome + internet), pero la charla es de trabajo. Si el contenido es sensible, se usa `V` para apagar la voz (o se presenta solo con gestos + teclado). **Aprobado tal cual:** el aviso va en el README y la decisión de usar voz la toma Luigui el día de la charla. Los frames de la cámara **no** salen: MediaPipe corre local en WASM (se verifica en el spike: 0 requests salientes en la pestaña Network).

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
| **R7** | **Choque de teclas `G`/`V`/`H`** | Confirmado en el código de Reveal 6.0.2: `H` retrocede un slide y `G` abre "Jump to slide" | Decisión D1 (`M`/`V`/`I`). Los atajos se ignoran si el foco está en un campo de texto y no se cancela ninguna tecla que no sea la nuestra. Se re-verifica con el deck real (plugins de Reveal pueden añadir atajos) |
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
