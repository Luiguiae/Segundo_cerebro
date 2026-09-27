# Presentador por voz (y gestos experimentales) para decks Reveal.js

Navega una presentación Reveal.js sin tocar la laptop: **por voz** ("LeIA, siguiente", "avanza tres slides", "vuelve al inicio") y, de forma **experimental**, con swipes de mano. Corre en `localhost`, en Chrome, y **no modifica tu HTML en disco**: `presentar.py` inyecta los scripts al servir `index.html`.

> **Estado de la v1 (2026-09-27)** — **La voz y el teclado son los canales de la v1.** **Los gestos están APAGADOS por defecto** y son **experimentales**: en la prueba en vivo hubo 2 disparos inversos en 10 swipes a la izquierda (ver [Gestos](#gestos-experimentales-apagados-por-defecto)). Se encienden con la tecla **`M`**, solo si quieres ensayarlos.

Especificación y decisiones: [`docs/SPEC.md`](docs/SPEC.md) · [`docs/plan.md`](docs/plan.md) · [`docs/tasks.md`](docs/tasks.md) · [`docs/pruebas-degradacion.md`](docs/pruebas-degradacion.md).

---

## Requisitos

- macOS con **Google Chrome** (probado con Chrome 153) y **Python 3.11** (solo librería estándar).
- **Internet para la voz** (Web Speech API de Chrome). Los gestos y el teclado no lo necesitan.
- Node ≥ 20 solo para correr los tests.
- Un deck **Reveal.js** que cargue Reveal desde `/vendor/` (ver [abajo](#cómo-referenciar-reveal-desde-tu-deck)).

## Instalación (una vez, **con internet y antes de la charla, no el mismo día**)

```bash
cd ~/Documents/Segundo_cerebro/Prompts/Presentaciones/presentador
python3.11 setup_vendor.py
```

Descarga a `vendor/` (≈ 47 MB, fuera de git): Reveal.js 6.0.2, MediaPipe Tasks Vision 1.0.1 y el modelo `gesture_recognizer.task`, todo con **hashes verificados**. Es idempotente. Si `vendor/` falta o está incompleto, `presentar.py` se detiene y te dice que lo corras.

## Uso

```bash
python3.11 presentar.py ~/Presentaciones/2026-09-28          # abre Chrome en http://localhost:8765
python3.11 presentar.py ~/Presentaciones/2026-09-28 --debug  # muestra en el indicador lo que Chrome entiende de tu voz
```

| Opción | Para qué |
|---|---|
| `--port N` | Puerto (por defecto **8765**; los permisos de cámara/micrófono son **por puerto**, así que conviene no cambiarlo) |
| `--debug` | Indicador con la transcripción cruda de la voz y el estado de la mano |
| `--lang es-MX` | Idioma del reconocimiento (por defecto `es-PE`; prueba `es-MX`/`es-ES` si transcribe mal) |
| `--sin-inyeccion` | Sirve la carpeta tal cual, sin el presentador |
| `--no-abrir` | No abre Chrome |

Las presentaciones son material de trabajo: viven **fuera del repo** (`~/Presentaciones/`) y nunca se copian al vault. El proyecto solo incluye `demo/index.html`, un deck genérico para probar.

### Cómo referenciar Reveal desde tu deck

Para no depender de un CDN el día de la charla, carga Reveal desde `/vendor/`, con **script clásico** (no módulo ESM: si Reveal se carga como módulo no existe `window.Reveal` y el presentador se queda inactivo):

```html
<link rel="stylesheet" href="/vendor/reveal/dist/reset.css">
<link rel="stylesheet" href="/vendor/reveal/dist/reveal.css">
<link rel="stylesheet" href="/vendor/reveal/dist/theme/black.css">
...
<script src="/vendor/reveal/dist/reveal.js"></script>
<script>Reveal.initialize({ hash: false });</script>
```

Si la página **no** usa Reveal, se muestra igual y el presentador no se activa (el indicador lo dice).

## Teclas

| Tecla | Hace | Nota |
|---|---|---|
| **`M`** | Enciende / apaga los **gestos** | **Apagados por defecto.** La cámara solo se pide al pulsarla. Espera unos segundos: primero carga el modelo |
| **`E`** | Enciende / apaga la **voz** (*escuchar*) | Encendida por defecto |
| **`I`** | Muestra / oculta el **indicador** | |
| Flechas, espacio, clicker | Navegación nativa de Reveal | **Nunca se bloquean** |

`M`, `E` e `I` se eligieron porque Reveal 6.0.2 usa `H` (slide anterior), `G` (saltar a slide) y **`V` (pausa / pantalla negra: no figura en su ayuda, solo en su código)**. **`V` sigue siendo la pausa de Reveal.** Las teclas se ignoran si escribes en un campo de texto o usas Ctrl / ⌘ / Alt / Shift.

## Voz

Vocabulario (sin distinguir tildes ni mayúsculas; "slide", "slides", "diapositiva", "lámina" son opcionales al final):

| Para… | Di… |
|---|---|
| Avanzar un paso (respeta *fragments*) | `siguiente` · `avanza` · `adelante` |
| Retroceder un paso | `retrocede` · `atrás` · `anterior` · `regresa` |
| Saltar N slides completos (1–20; ignora *fragments*) | `avanza 3` · `adelanta dos` · `retrocede 2 slides` · `regresa cinco` |
| Ir al primer slide | `vuelve al inicio` · `al inicio` · `primer slide` |

- **Con "LeIA" delante** ("LeIA, siguiente"): funciona incluso dentro de una frase más larga, pero la palabra de activación debe ir **pegada al comando** (así "que lea el siguiente párrafo" no dispara).
- **A secas** ("siguiente"): solo dispara si **toda** la frase es exactamente un comando. "Veamos el siguiente punto" no hace nada.
- Una misma frase dispara **una sola acción**; tras cualquier cambio se ignora todo durante **1,5 s** (cooldown compartido con teclado, clicker y gestos).
- "avanza" puede ser el inicio de "avanza tres": esos comandos esperan ~0,5 s a que el texto se estabilice.
- Chrome corta el reconocimiento tras silencios: el presentador lo **reinicia solo**.

**Cómo transcribe Chrome "LeIA"** varía. Medido en la prueba en vivo: *leia, leía, ley, de ella, bella…* Las variantes aceptadas están en `VARIANTES_LEIA` de [`comandos.js`](comandos.js) (`leia`, `lea`, `le ia`, `lelia`, `leya`, `de ella`). **`ley` y `bella` no están** a propósito: "la ley siguiente…" cambiaría el slide sin querer (prioridad: 0 falsos positivos). Calibra con `--debug` en el ensayo y, si quieres, añade variantes sabiendo ese riesgo.

## Gestos (EXPERIMENTALES, apagados por defecto)

Se encienden con **`M`**. Un swipe con la mano abierta hacia tu derecha avanza y hacia tu izquierda retrocede. MediaPipe corre **en tu Mac** (WASM); la cámara va a 640×480 y se libera al pulsar `M` de nuevo.

**Por qué son experimentales.** En la prueba en vivo, a la distancia real y con un solo intento por paso: derecha 6/10, izquierda 7/10 **con 2 disparos inversos**, ida y vuelta rápido 2/3; y **0 cambios** en gesticulación (20 s), mano abierta quieta (8 s), puño (6 s) y saludo con vaivén (6 s). No cumple el "0 disparos inversos" del proyecto, así que no es un canal de aceptación en v1.

### Reglas de uso (si los enciendes)

1. **Después de un swipe, baja o cierra la mano.** No la regreses en horizontal con la palma abierta: ese regreso rápido puede leerse como un swipe en sentido contrario (es exactamente lo que dio los disparos inversos).
2. **No saludes ni hagas vaivenes con la palma abierta.** Un vaivén lento (~1 Hz) con la palma abierta es indistinguible de swipes repetidos. Si vas a gesticular con la mano abierta, **apaga los gestos con `M`**.

Cómo decide el detector (v2): un trazo horizontal de ≥ 8 % del ancho en ≤ 0,5 s **precedido de ≥ 0,2 s de mano abierta (`Open_Palm`) casi quieta**, con cooldown de 1,5 s, **bloqueo del sentido contrario durante 3 s** tras un swipe y una guardia contra vaivenes. Sobre las 102 trazas grabadas: 0 falsos positivos y 0 inversos, pero en vivo aparecieron 2 (ver arriba). Detalle en [`docs/plan.md`](docs/plan.md) §11–13. Hay una **ronda de diagnóstico opcional** pendiente (§14) para intentar arreglar los inversos; no se hace salvo que se pida.

## Indicador

Una cajita discreta en la esquina inferior derecha, encima del contenido y **sin alterar el layout** (Shadow DOM, `pointer-events: none`): estado de la cámara y del micrófono, y el último comando (`+3 → 7/12 voz`). Con `--debug` añade la transcripción cruda. `I` lo oculta.

## Qué pasa cuando algo falla (degradación)

Probado en vivo el 2026-09-27 ([`docs/pruebas-degradacion.md`](docs/pruebas-degradacion.md)):

| Situación | Qué ves | Qué sigue funcionando |
|---|---|---|
| La página **no usa Reveal.js** | Se ve igual; indicador "no usa Reveal.js — inactivo"; `M`/`E` no abren cámara ni micrófono | Todo lo nativo de la página |
| **Sin permiso de cámara** (al pulsar `M`) | "Cámara (M) sin permiso de cámara" | Voz y teclado |
| **Sin internet** | "Micrófono (E) sin internet — reintentando" y la voz no cambia nada | Teclado y gestos; la voz se recupera sola al volver la conexión |
| **Comando no reconocido** | Nada: sin mensajes ni avisos | Todo |

## Privacidad — léelo antes de la charla

- **El audio de la voz sale de tu Mac.** La Web Speech API de Chrome envía el audio al servicio de reconocimiento de Google **mientras la voz está activa**. Si el contenido es sensible, apaga la voz con **`E`** o presenta con teclado. **La decisión de usar voz es tuya el día de la charla.** (Pendiente v2: reconocimiento local, p. ej. Vosk, para no enviar audio ni depender de internet.)
- **La cámara no sube nada.** El reconocimiento de gestos corre localmente.
- **Telemetría de MediaPipe bloqueada.** MediaPipe Tasks Vision 1.0.1 trata de enviar métricas de uso a `odml.pa.googleapis.com` cada 60 s (sin opción para desactivarlo). `presentador.js` bloquea esas peticiones (`fetch`, XHR y `sendBeacon`); verificado: 0 peticiones externas con MediaPipe activo.
- **Audio ambiente:** la voz transcribe lo que oiga, también la tele o las voces de fondo.

## Solución de problemas

| Síntoma | Qué hacer |
|---|---|
| Chrome no pide (o ya negó) el micrófono/cámara | Es **por puerto**: `localhost:8765` → icono del candado → Configuración del sitio. Mantén siempre el mismo puerto |
| La voz no dispara o oye otra cosa | Arranca con `--debug` y mira cómo transcribe tu "LeIA". Prueba `--lang es-MX`. Acércate al micrófono y quita el audio de fondo |
| **Micrófono Bluetooth** | Elígelo como **entrada** en Ajustes del Sistema → Sonido. Si la **salida** también va por Bluetooth, macOS puede pasar a un perfil de baja calidad y bajar la exactitud: comprueba en el ensayo (9/10 comandos a la primera) |
| Los gestos no se encienden | Pulsa `M` **una vez** y espera unos segundos (carga del modelo antes de pedir la cámara). Si no hay permiso, el indicador lo dice |
| **Jarvis** (daemon local) | Comparte el micrófono sin problema, pero **cierra sus ojos** ("Jarvis, cierra los ojos") para que no compita por la cámara, y no digas "Jarvis" durante la charla |
| `vendor/ falta o está incompleto` | `python3.11 setup_vendor.py` (con internet) |
| El puerto está ocupado | Otra instancia de `presentar.py`: ciérrala. Si usas otro puerto, tendrás que dar los permisos de nuevo |
| Reveal "pausa" la pantalla (negro) | Pulsaste `V`, `B` o `.`: es la pausa de Reveal. Púlsala otra vez |

## Checklist de ensayo (domingo)

- [ ] Presentación del lunes en `~/Presentaciones/2026-09-28/index.html`, con Reveal cargado como **script clásico** desde `/vendor/` (no CDN, no ESM)
- [ ] `python3.11 setup_vendor.py` corrido **con internet** (no el lunes)
- [ ] macOS: **micrófono Bluetooth como entrada por defecto**; si la salida también va por ese dispositivo, comprobar que la calidad no baja
- [ ] Chrome: aceptar el permiso de micrófono para `localhost:8765` (y el de cámara solo si vas a ensayar los gestos)
- [ ] Arrancar con `--debug` y decir "LeIA, siguiente" varias veces: mira cómo transcribe Chrome "LeIA" y ajusta las variantes o `--lang` si hace falta
- [ ] Probar "siguiente" a secas y frases como "veamos el siguiente punto" (esta última **no** debe disparar)
- [ ] Probar "avanza 3", "retrocede dos slides", "vuelve al inicio" y un slide con *fragments*
- [ ] **30 s de silencio** y luego un comando: la voz debe seguir viva
- [ ] Probar en la **red donde vas a presentar** o con hotspot (la voz necesita internet); probar también con el Wi-Fi apagado: la voz avisa y el teclado sigue
- [ ] Probar `E`, `I` y el clicker/flechas como respaldo; comprobar que **`V` es la pausa de Reveal** (no hace otra cosa) y que `M`, `E`, `I` no chocan con nada de tu deck
- [ ] **Gestos: apagados por defecto.** Si quieres ensayarlos, pulsa `M`, y recuerda las **dos reglas de uso**: (1) tras un swipe, **baja o cierra la mano** en vez de regresarla horizontal con la palma abierta; (2) **no saludes ni hagas vaivenes con la palma abierta** — usa `M` para apagarlos si hace falta
- [ ] Ensayo de 10 min hablando y gesticulando normal: **0 cambios de slide no intencionales**
- [ ] Decidir el mediodía del domingo si se presenta con voz, con teclado, o ambos (el audio de la voz va a Google)
- [ ] Cerrar los ojos de Jarvis o pausarlo si no lo vas a usar; cerrar apps que suenen (audio de fondo)
- [ ] **Congelar el código el domingo a las 22:00.** El lunes solo se ejecuta

## Estructura y tests

```
presentar.py        servidor local + inyección de scripts (--debug, --lang, --port…)
presentador.js      bloqueo de telemetría · navegación · cooldown · teclas · indicador · voz · gestos
comandos.js         parser de voz (módulo dual navegador/Node)
swipe.js            detector de swipe v2 (módulo dual)
setup_vendor.py     descarga Reveal, MediaPipe y el modelo con hashes verificados
demo/index.html     deck Reveal genérico para probar
vendor/             (no versionado) reveal.js, tasks-vision, gesture_recognizer.task
docs/               SPEC · plan · tasks · pruebas de degradación
tests/              unittest (Python) y node --test (comandos, swipe) + trazas reales
tests/manual/       spike de gestos (T06) y guías de pruebas en vivo (T13–T15)
```

```bash
python3.11 -m unittest discover -s tests -p "test_*.py"      # servidor, inyección, setup_vendor
node --test tests/comandos.test.js tests/swipe.test.js       # parser de voz y detector de swipe
```

Pruebas en vivo guiadas (en pantalla, con tonos y verificación automática): `python3.11 tests/manual/vivo/servir_vivo.py <voz|gestos|degradacion> [--variante …]`.

## Límites conocidos

- **Gestos experimentales** (ver arriba): 2 inversos en 10 swipes a la izquierda; ~65 % de aciertos a un solo intento.
- El detector **no distingue** un swipe deliberado a la izquierda de un retorno rápido tras ≥ 3 s de reposo con la palma abierta.
- Un **vaivén lento (~1 Hz) con la palma abierta** puede disparar; `M` apaga los gestos.
- La voz depende de internet y transcribe el audio ambiente; las variantes de "LeIA" varían por voz y micrófono. **El micrófono Bluetooth aún no se ha medido** (queda para el ensayo).
- Datos de una sola persona y sesión; los umbrales se afinaron sobre los mismos datos. Los 10 min sin cambios no intencionales se miden en el ensayo.
