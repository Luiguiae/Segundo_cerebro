# Tasks — Presentador por gestos y voz (LeIA)

> Estado: **aprobado 2026-09-26** (D1–D6). Ligado a `docs/plan.md` (decisiones D1–D6) y `docs/SPEC.md`.
> Protocolo aprobado: T01–T05 y T07–T08 seguidas sin detenerse mientras cada criterio de done se cumpla (un commit + push por tarea); resumen por tarea al terminar T08 y **parada antes de T06** (requiere a Luigui frente a la cámara). Ante un done que falle sin solución, o cualquier desvío del SPEC o de D1–D6: detenerse y avisar. Desde T09 en adelante, revisión tarea por tarea.
> Convención de referencias: **CA-x** = criterio de aceptación del SPEC §4 (Nav = semántica de navegación, CU1…CU5, Arranque, Errores); **M-x** = métrica del SPEC §7.

## Avance (actualizado 2026-09-26)

| Tarea | Estado | Commit |
|---|---|---|
| T01 estructura y `.gitignore` | ✅ | `24e806d` |
| T02 `setup_vendor.py` | ✅ | `7047c5a` |
| T03 `demo/index.html` | ✅ | `1121998` |
| T04 `presentar.py` (servidor + comprobación de `vendor/`) | ✅ | `afa63c4` |
| T05 inyección de scripts | ✅ | `b4ec34a` |
| T06 spike de gestos (go / no-go) | ✅ rondas 1 y 2 medidas; comparación offline hecha (plan.md §11); **T09 detenida a la espera de decisión de Luigui** | `2c4fb13` + ronda 2 |
| T07 casos de prueba del parser (147) | ✅ | `b17c891` |
| T08 `comandos.js` | ✅ 147/147 | `a542334` |
| T09 `swipe.js` (detector v2) | ✅ | `242ce0d` + ajustes en T10 |
| T10 tests del detector (49) | ✅ | `aa8b2b6` |
| T11 `presentador.js` (arranque, navegación, cooldown, bloqueo de telemetría) | ✅ | `04aa3b9` |
| T12 teclas M/E/I e indicador | ✅ | `5a298dc` |
| T13 voz en el navegador | ✅ 14/16 en vivo + 4/4 tras calibrar "de ella" | `72e78ae` |
| T14 gestos en el navegador | 🟡 **código listo y probado; criterio en vivo NO cumplido** (2/10 inversos a la izquierda, 13/20 aciertos a un intento) — a la espera de decisión | (ver git log) |
| T15–T18 | pendientes | — |

Verificación previa de D1 (tecla `V` = pausa) resuelta el 2026-09-26: `V` → `E` (commit `4d4c1dd`).

Contrato compartido que usan varias tareas (ver T07/T09):
- `interpretar(texto, esFinal)` → `null` | `{ accion: 'paso'|'salto'|'inicio', delta, definitivo, conPrefijo }`. `paso` = `Reveal.next()/prev()` (delta ±1, respeta fragments); `salto` = `Reveal.slide(h ± N)` (ignora fragments, con tope en primer/último slide); `inicio` = `Reveal.slide(0, 0)`.
- Detector de swipe: muestras `{ t, x, y, categoria }` con `x`,`y` normalizados (0–1) del centro de palma en el cuadro **sin espejar**; el detector invierte `x` (perspectiva del presentador) y devuelve `null` | `'derecha'` | `'izquierda'`.

---

## F0 — Andamiaje

### T01 · Estructura del proyecto y `.gitignore`
- **Descripción:** crear las carpetas `docs/`, `demo/`, `tests/`, `tests/manual/` y el `.gitignore` (`vendor/`, `__pycache__/`, `*.pyc`, `.DS_Store`, `*.log`). `docs/SPEC.md`, `docs/plan.md` y `docs/tasks.md` ya existen.
- **Archivos:** `.gitignore`, carpetas vacías con `.gitkeep` donde haga falta.
- **Done:** el árbol coincide con el SPEC §6 más lo aprobado en D2; `git status` no muestra `vendor/`. (Soporta D2, D3.)

### T02 · `setup_vendor.py` — dependencias sin CDN
- **Descripción:** script de librería estándar que descarga a `vendor/`: `reveal.js` 6.0.2 (`dist/` y `plugin/`) y `@mediapipe/tasks-vision` 1.0.1 (`vision_bundle.mjs` + `wasm/`) desde los tarballs de npm, y `gesture_recognizer.task` float16 v1. **Verifica integridad**: `dist.integrity` (sha512) de cada tarball de npm y sha256 fijo del modelo (`97952348…0482`); aborta si no coincide. Idempotente (no re-descarga lo ya verificado). Fija los `.task` sin tipo MIME (lo resuelve T04).
- **Archivos:** `setup_vendor.py`, `vendor/` (ignorado en git).
- **Done:** `python3.11 setup_vendor.py` deja `vendor/reveal/dist/reveal.js`, `vendor/tasks-vision/vision_bundle.mjs`, `vendor/tasks-vision/wasm/*` y `vendor/models/gesture_recognizer.task` (8 373 440 bytes); un segundo run no descarga nada; un hash alterado a propósito hace fallar el script. Cubre la restricción "Reveal + MediaPipe en `vendor/`, sin CDN en runtime" y R2.

### T03 · `demo/index.html` — deck Reveal genérico
- **Descripción:** deck de prueba **sin contenido de trabajo**: ~12 slides horizontales, dos con fragments, uno con texto largo, referenciando Reveal **solo** desde `/vendor/reveal/dist/...` (script clásico, no ESM). Sirve para el ensayo y las pruebas manuales.
- **Archivos:** `demo/index.html`.
- **Done:** abierto con `python3.11 -m http.server` desde una carpeta que exponga `/vendor/`, navega con flechas y muestra fragments; no contiene texto de trabajo. Ancla: CA-Nav (fragments), CA-Arranque.

---

## F1 — Servidor

### T04 · `presentar.py` — servidor local
- **Descripción:** `python3.11 presentar.py <carpeta> [--debug] [--port 8765]`. Sirve la carpeta en `/`, los archivos del presentador (lista blanca: `presentador.js`, `comandos.js`, `swipe.js`) en `/presentador/`, y `vendor/` en `/vendor/`. Solo `127.0.0.1` (`localhost` = contexto seguro para `getUserMedia`). Protección contra `..` y rutas absolutas (resolver y verificar que quede dentro de la raíz); `Cache-Control: no-store`; MIME correcto (`.mjs`, `.wasm`, `.task` = `application/octet-stream`); errores claros si la carpeta no existe, no tiene `index.html` o el puerto está ocupado. Abre Chrome (`open -a "Google Chrome"`, con respaldo a `webbrowser`). `--debug` activa la transcripción cruda en el indicador (T13). `--sin-inyeccion` sirve la carpeta tal cual (para el spike de F2, cuando `presentador.js` aún no existe). Solo librería estándar. **Si `vendor/` falta o está incompleto, se detiene con un mensaje claro que indica correr `python3.11 setup_vendor.py`** (la lista de archivos requeridos vive en `setup_vendor.py` y `presentar.py` la importa: una sola fuente de verdad). No escribe nada en la carpeta de la presentación.
- **Archivos:** `presentar.py`.
- **Done:** con `vendor/` ausente o incompleto, sale con código ≠ 0 y el mensaje que apunta a `setup_vendor.py`; con `demo/` abre `http://localhost:8765` en Chrome; `curl` a `/../presentar.py` y a `/presentador/presentar.py` devuelve 404; `.wasm` sale como `application/wasm`; el hash de la carpeta `demo/` es idéntico antes y después. Ancla: CA-Arranque (1.º y 2.º punto), restricciones de Python 3.11 y stdlib.

### T05 · Inyección de scripts al servir
- **Descripción:** función pura `inyectar(html_bytes) -> bytes` que agrega los `<script>` del presentador **antes del último `</body>`** (sin distinguir mayúsculas; si no hay `</body>`, al final), trabajando sobre bytes, **idempotente** (no inyecta dos veces) y con `Content-Length` correcto. Solo para `/` y `/index.html`. Antes de los scripts va un bloque inline `window.PRESENTADOR_CONFIG = {...}` (p. ej. `debug`), y luego, en orden: `comandos.js`, `swipe.js`, `presentador.js`.
- **Archivos:** `presentar.py`, `tests/test_presentar.py` (`unittest`).
- **Done:** tests verdes para: con `</body>`, con `</BODY>`, sin `</body>`, dos `</body>` (usa el último), doble llamada, HTML en UTF-8 con tildes intacto, HTML no-UTF-8 (bytes intactos). En vivo: el *view-source* de `localhost:8765` muestra los scripts y `demo/index.html` en disco no cambia (hash). Ancla: CA-Arranque (2.º punto), R6.

---

## F2 — Spike de gestos (go / no-go)

### T06 · Spike MediaPipe en este Mac + grabación de trazas
- **Descripción:** página de desarrollo (no forma parte de la entrega final) que carga `GestureRecognizer` desde `/vendor/` en modo `VIDEO` y mide en vivo: (a) carga sin errores en Chrome 153; (b) fps sostenidos y latencia cuadro→detección con `delegate` GPU vs CPU y con 640×480 / 320×240, `numHands: 1`; (c) CPU en Activity Monitor **con Jarvis corriendo**; (d) que `Open_Palm` se reconozca a 1–2 m con la luz disponible; (e) pestaña Network: **0 requests salientes** durante la detección. Incluye un botón que **graba trazas** `{t, x, y, categoria}` del centro de palma y las descarga como JSON (sin imágenes), etiquetadas por ti (swipe derecha, izquierda, retorno natural, gesticulación normal).
- **Archivos:** `tests/manual/spike/index.html` (se sirve con `python3.11 presentar.py tests/manual/spike --sin-inyeccion`), `tests/traces/*.json`.
- **Done / criterio de go:** **≥15 fps sostenidos** en la configuración elegida, sin errores de WASM/modelo, 0 requests salientes, y ≥10 trazas de swipe derecha, ≥10 izquierda, ≥5 retornos naturales y ≥3 de gesticulación grabadas. **Entregable de decisión:** te presento las cifras y recomiendo *seguir*, *seguir con mitigaciones* (resolución/frecuencia/CPU) o *plan B sin gestos el lunes*. No avanzo a F4 sin tu decisión. Ancla: R2, M-latencia swipe.

---

## F3 — Parser de voz (independiente de F1/F2)

### T07 · Casos de prueba del parser (primero los tests)
- **Descripción:** escribir `tests/comandos.test.js` (`node --test`, sin dependencias) con los casos de abajo **antes** de implementar. Cada caso: entrada, `esFinal` y resultado esperado.
- **Archivos:** `tests/comandos.test.js`.
- **Done:** el archivo corre y **falla** limpiamente contra un `comandos.js` vacío (rojo antes del verde); los casos cubren todo el vocabulario del SPEC, los rechazos y D4/D5. Ancla: CA-Voz completo.

**Casos (resumen; el archivo los tendrá todos, incluidos tildes/mayúsculas/puntuación):**

| Grupo | Entrada (`esFinal`) | Esperado |
|---|---|---|
| Sin prefijo, paso | "siguiente" · "Siguiente." · "  SIGUIENTE  " · "avanza" · "adelante" (final) | `paso +1` |
| | "retrocede" · "atrás" · "atras" · "anterior" · "regresa" (final) | `paso −1` |
| Sin prefijo, salto | "avanza 3" · "avanza tres slides" · "avanza 3 diapositivas" (final) | `salto +3` |
| | "adelanta 2" · "adelanta dos láminas" · "adelanta dos laminas" (final) | `salto +2` |
| | "retrocede 2 slides" · "regresa cinco" (final) | `salto −2` · `salto −5` |
| | "retrocede un slide" · "avanza una diapositiva" (final) | `salto −1` · `salto +1` (un/una = 1; salto ignora fragments) |
| | "avanza veinte" · "avanza 20" · "avanza dieciséis" (final) | `+20` · `+20` · `+16` |
| | "avanza 21" · "avanza 0" · "avanza 25" (final) | `null` (fuera de 1–20; no cae a `paso`) |
| Inicio | "vuelve al inicio" · "al inicio" · "primer slide" (final) | `inicio` |
| Sin prefijo, rechazos | "veamos el siguiente punto" · "el siguiente" · "siguiente por favor" · "adelante con el tema" · "avanza y retrocede" · "hola" · "" (final) | `null` |
| Sin prefijo, interino | "siguiente" · "avanza 3" (**no** final) | `null` (solo finales) |
| Prefijo, paso | "leia siguiente" (interino y final) | `paso +1`, `definitivo: true` |
| | "LeIA, siguiente" · "LEÍA ATRÁS" · "leía retrocede" (final) | `+1` · `−1` · `−1` |
| Variantes de "LeIA" | "lea siguiente" · "le ia siguiente" · "lelia atrás" · "leya vuelve al inicio" | `+1` · `+1` · `−1` · `inicio` |
| Dentro de un enunciado | "bueno leia siguiente gracias" · "ok leia avanza tres" (interino) | `paso +1` definitivo · `salto +3` |
| D5 (interino ambiguo) | "leia avanza" · "leia retrocede" (interino) | `paso ±1`, `definitivo: false` |
| | "leia avanza 3" · "leia regresa 2" (interino) | `salto`, `definitivo: false` |
| | "leia avanza" · "leia avanza 3 slides" (final) | `definitivo: true` |
| | "leia adelante" · "leia vuelve al inicio" · "leia primer slide" (interino) | `definitivo: true` (sin número posible) |
| D4 (adyacencia) | "leia" · "leia qué hora es" · "lea el siguiente párrafo" · "que lea el siguiente" | `null` |
| Un enunciado, una acción | "leia siguiente leia siguiente" · "leia siguiente, retrocede" (final) | un solo resultado (el primero: `+1`) |
| Sufijo opcional | "leia siguiente slide" (final) | `paso +1` |

### T08 · Implementar `comandos.js`
- **Descripción:** `normalizar(texto)` (minúsculas, sin tildes, sin puntuación, espacios colapsados), lista editable de variantes de "LeIA", números 1–20 en dígitos y palabras (incluye `un`/`una`), `interpretar(texto, esFinal)` según el contrato y D4/D5. Módulo dual: global en el navegador y `module.exports` en Node. Sin dependencias.
- **Archivos:** `comandos.js`.
- **Done:** `node --test tests/comandos.test.js` **verde en todos los casos de T07**. Ancla: CA-Voz (vocabulario, prefijo/a secas, variantes, un enunciado = una acción), M-voz.

---

## F4 — Detector de swipe

### T09 · `swipe.js` — detector puro (v2)
- **Descripción:** `crearDetector(config)` → `{ procesar(muestra), notificarCambio(t), reiniciar(), config }`. Muestras `{t, x, y, categoria}` con `x`,`y` normalizados del centro de palma en el cuadro **sin espejar**; `x`/`y` nulos = sin mano. **Detector v2** (aprobado, plan.md §12): hay evento si existe un trazo horizontal de **≥8 % del ancho en ≤500 ms** (relación vertical ≤0.6) **precedido de ≥200 ms de mano abierta y casi quieta** (≥3 cuadros, ≥60 % con `Open_Palm`, dispersión x/y ≤8 %); la mano **no** tiene que ser `Open_Palm` durante el trazo. Dirección invertida por el espejo (raw `x` decreciente = **derecha** del presentador). **Cooldown 1500 ms** tras un evento; `notificarCambio(t)` inicia el mismo cooldown y limpia el historial cuando el cambio vino de **otro canal** (cooldown compartido con la voz). Un hueco de detección **>400 ms** limpia el historial (mano que sale y entra ≠ swipe; 250 ms costaba swipes reales porque la mano se pierde 250–300 ms por desenfoque a mitad del trazo). **Reglas añadidas al medir con datos (T10):** la quietud previa debe **abarcar ≥150 ms** (3 cuadros pueden ser solo 66 ms); el **sentido contrario se bloquea 3 s** tras un evento y el trazo bloqueado se consume (una mano que reposó 2.3 s abierta en el destino y volvió rápido disparó el inverso en la ronda 1); **guardia de vaivén** (≥3 inversiones de sentido ≥4 % en 1 s no arma). **Límite conocido:** un vaivén lento (~1 Hz) con la palma abierta y quietud en cada giro es indistinguible de swipes repetidos; la tecla `M` apaga los gestos. Umbrales en `CONFIG_POR_DEFECTO` al inicio del archivo. Módulo dual (navegador `window.Swipe` / Node). Prototipo de referencia: `tests/manual/spike/comparar_metodos.py` (`detector2`).
- **Archivos:** `swipe.js`.
- **Done:** produce **exactamente los mismos eventos** que el prototipo `detector2` de Python (actualizado con las mismas reglas) sobre las 102 trazas reales de las dos rondas (verificación de equivalencia), y pasa T10. Ancla: CU1 (todos los puntos), R1.

### T10 · Tests del detector (sintéticos + trazas reales)
- **Descripción:** `tests/swipe.test.js` (`node --test`) con casos sintéticos y con las trazas reales grabadas en T06 (rondas 1 y 2).
- **Archivos:** `tests/swipe.test.js`.
- **Done:** sintéticos — swipe derecha limpio (raw `x` decreciente tras mano abierta quieta) = `'derecha'`; izquierda limpio = `'izquierda'` (verifica el espejo); lento (2 s) = `null`; corto (5 %) = `null`; vertical dominante = `null`; mano no abierta todo el movimiento = `null`; **trazo con la categoría perdida durante el movimiento sí dispara** (armado solo por la quietud previa); swipe + retorno rápido dentro de 1500 ms = **1** evento; retorno a los 1600 ms sin haber quedado quieta = `null`, y tras quedarse quieta 300 ms un nuevo swipe sí dispara; vaivén continuo = `null`; temblor ±2 % = `null`; mano que sale y entra = `null`; muestreo irregular (66–100 ms) sigue detectando; dos cuadros seguidos tras el disparo = 1 evento; `notificarCambio` bloquea 1500 ms y exige nueva quietud. Trazas reales — **0 disparos en gesticulación, reposo y puño (rondas 1 y 2); 0 eventos antes del YA; 0 disparos con dirección inversa como primer evento; 0 eventos extra; en la ronda 2, ≥8/10 derecha y ≥8/10 izquierda en intentos válidos**. Prioridad: si hay conflicto entre tasa y falsos positivos, gana 0 falsos positivos. Ancla: CU1, SPEC §7 (swipe).

---

## F5 — Integración en el navegador

### T11 · `presentador.js` — arranque, navegación y cooldown
- **Descripción:** al cargarse, espera a Reveal (sondeo con tiempo límite + `Reveal.isReady()` + evento `ready`); si no aparece, deja un aviso en el indicador y no hace nada más. Expone `navegar(accion)` con la semántica del SPEC (`paso` → `next()/prev()`, `salto` → `slide(h±N)` con tope, `inicio` → `slide(0,0)`) y el **cooldown compartido de 1500 ms** para voz y gestos (usa `performance.now()`).
- **Archivos:** `presentador.js`.
- **Además (aprobado tras T06):** instala **antes de cualquier otra cosa** el bloqueo de `fetch`/XHR/`sendBeacon` hacia `odml.pa.googleapis.com` (telemetría de MediaPipe 1.0.1; ver plan.md §9–10), para que esté activo antes de que se cargue MediaPipe. Las peticiones bloqueadas se cuentan (visible en `--debug`).
- **Done:** en el demo, desde la consola, `navegar` mueve un fragment, N slides, al inicio, y se detiene en los extremos; un `fetch` a `https://odml.pa.googleapis.com/v1/log` queda bloqueado y contado (y `fetch('/')` sigue funcionando); una segunda llamada dentro de 1500 ms se ignora; con una página sin Reveal no lanza errores y muestra el aviso. Ancla: CA-Nav (todos), CA-Arranque (3.er punto), CA-Errores (sin Reveal), R6.

### T12 · Teclas de control e indicador
- **Descripción:** *(verificación previa de la condición de D1 ya hecha el 2026-09-26: `V` (keyCode 86) activa la pausa/pantalla negra en Reveal 6.0.2 → reemplazada por `E`; ver plan.md §3 D1).* Teclas **`M`** gestos, **`E`** voz ("escuchar"), **`I`** indicador, ignoradas si el foco está en un campo de texto y sin cancelar ninguna otra tecla; las flechas/espacio/clicker de Reveal no se tocan. Indicador con **Shadow DOM** (no lo afecta el CSS del deck), `position: fixed` en una esquina, `pointer-events: none`, sin alterar el layout: estado de cámara y micrófono y último comando (`+3 → 7/20`). Con `--debug`, una línea extra con la transcripción cruda.
- **Archivos:** `presentador.js`.
- **Done:** las tres teclas alternan (y `V` sigue siendo la pausa nativa de Reveal, sin interferencia) y el indicador lo refleja; el layout del demo no cambia con el indicador visible ni oculto (medición del alto/ancho de `.reveal`); flechas y espacio siguen funcionando con gestos y voz apagados. Ancla: CU5 (ambos puntos), R7.

### T13 · Voz en el navegador
- **Descripción:** `webkitSpeechRecognition` con `continuous`, `interimResults`, `lang` = constante (`es-PE`). Cada resultado se procesa con `interpretar()`; **dedupe por índice de resultado** (índice consumido = se ignoran sus siguientes actualizaciones); los `definitivo: false` se despachan tras ~500 ms de texto estable o al llegar el final (D5); cooldown compartido. Reinicio automático en `onend`/`onerror` con espera creciente; `not-allowed`/`service-not-allowed` son permanentes (indicador, sin reintentos infinitos); el reinicio limpia el dedupe. Voz apagada con `E` detiene el reconocimiento.
- **Archivos:** `presentador.js`.
- **Done:** "leia siguiente", "avanza tres slides", "vuelve al inicio" y "avanza 3" con y sin prefijo se comportan como los casos de T07 en vivo; **un enunciado = una acción** (el contador de acciones lo prueba); tras 30 s de silencio la voz sigue viva; "veamos el siguiente punto" no hace nada; en `--debug` se ve cómo transcribe Chrome "LeIA". Ancla: CU2, CU3, CU4, CA-Voz (dedupe, reinicio), R3, R4, R5, M-voz.

### T14 · Gestos en el navegador
- **Descripción:** `getUserMedia` a **640×480** (aprobado tras T06), video oculto, bucle de `GestureRecognizer` con los parámetros que salgan del spike, alimentando `swipe.js`; el evento pasa por `navegar()` con el cooldown compartido. Gestos apagados con `M` **liberan la cámara** (se detienen los tracks: se apaga la luz y baja el CPU).
- **Archivos:** `presentador.js`.
- **Done:** swipe a la derecha avanza un paso una sola vez, a la izquierda retrocede, el regreso de la mano no dispara, hablar gesticulando no cambia slides; `M` apaga y enciende la cámara; latencia percibida < 1 s; **0 peticiones externas con MediaPipe activo** (el bloqueo de `odml.pa.googleapis.com` está en `presentador.js`; ver plan.md §9). Ancla: CU1, CU5, R1, R2, M-swipe.

---

## F6 — Degradación

### T15 · Matriz de errores del SPEC
- **Descripción:** revisar y completar el manejo de: página sin Reveal, cámara denegada, sin internet (Web Speech falla), comando no reconocido, foco en campo de texto. Ningún mensaje intrusivo en pantalla; solo el indicador.
- **Archivos:** `presentador.js`.
- **Done:** cuatro pruebas manuales documentadas — (1) `<html>` sin Reveal: la página se ve igual, indicador avisa; (2) permiso de cámara denegado: voz y teclado funcionan, indicador lo dice; (3) Wi-Fi apagado: gestos y teclado funcionan, indicador lo dice; (4) frase no reconocida: sin efecto ni mensaje. Ancla: CA-Errores (los 4 puntos).

---

## F7 — Documentación, ensayo y cierre

### T16 · `README.md`
- **Descripción:** uso (`setup_vendor.py`, `presentar.py`, `--debug`), cómo referenciar `/vendor/reveal/dist/reveal.js` desde un deck (script clásico), tabla de teclas (con la nota de por qué `M`/`E`/`I` y que `V` es la pausa de Reveal), el aviso de D6 (audio de voz → Google), solución de problemas (permisos, Bluetooth, `es-PE`→`es-MX`, ojos de Jarvis cerrados) y el **checklist de ensayo** del SPEC (ya con `M`/`E`/`I`).
- **Archivos:** `README.md`.
- **Done:** alguien que no conozca el proyecto puede correr el demo y ensayar solo con el README. Ancla: SPEC §6 (README) y checklist de ensayo.

### T17 · Ensayo guiado y métricas
- **Descripción:** ejecutar el checklist completo contigo (domingo) y medir el SPEC §7 con el micrófono Bluetooth y la distancia real; registrar resultados y ajustes en `docs/ensayo.md`.
- **Archivos:** `docs/ensayo.md`, ajustes puntuales de constantes (variantes de "LeIA", idioma, umbrales).
- **Además (aprobado tras la ronda 2):** grabar trazas de swipe con **la mano que Luigui use naturalmente al presentar** y **re-afinar los umbrales de `swipe.js` solo si mejora la tasa sin introducir falsos positivos ni disparos inversos** (se valida con `tests/swipe.test.js` + las trazas nuevas), y **siempre antes del congelamiento** (T18).
- **Done:** 10 min hablando y gesticulando con **0** cambios no intencionales y **0** disparos inversos; swipe **8/10** por lado en intentos válidos (canal secundario); **9/10** comandos de voz; latencias < 1 s (swipe) y < 1.5 s (voz); el deck completo se navega sin tocar la laptop. Si algo no pasa, se decide plan B con esos números. Ancla: SPEC §7 completo.

### T18 · Congelamiento y cierre
- **Descripción:** congelar el código (domingo 22:00), registrar en `JARVIS_LOG.md` (append, formato de `CLAUDE.md`) y `git push`.
- **Archivos:** `JARVIS_LOG.md`; commit de todo el proyecto (sin `vendor/`).
- **Done:** entrada de log con lo hecho, resultados del ensayo y pendientes; `git status` limpio en el proyecto; origin al día. No se tocó `jarvis.py`, `jarvis_daemon.py`, `.zshrc`, `RESOLVER.md`, `ATLAS.md` ni conceptos (verificado con `git diff --stat` contra la lista).

---

## Resumen de dependencias

`T01 → T02 → T03 → T04 → T05 → T06 (go/no-go) → T09 → T10 → T11 → T12 → T13 → T14 → T15 → T16 → T17 → T18` con **T07–T08 (voz)** movibles en cualquier momento antes de T13.
