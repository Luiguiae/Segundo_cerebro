# SPEC — Presentador por gestos y voz (LeIA)

> Proyecto: `~/Documents/Segundo_cerebro/Prompts/Presentaciones/presentador/` · Deadline: lunes 2026-09-28 (presentación de trabajo)

> **Revisión 2026-09-27 (4.ª, tras la prueba en vivo de T14; aprobada por Luigui):** el **swipe queda EXPERIMENTAL en v1 y los gestos están APAGADOS por defecto** (se activan con `M`). Motivo: en la prueba en vivo, a la distancia real y con un solo intento por paso, hubo **2 disparos inversos en 10 swipes a la izquierda** (además de 13/20 aciertos). La voz y el teclado son los canales de v1. Las metas de swipe de §7 pasan a ser objetivo de una versión posterior, no criterio de aceptación de v1. Ver `plan.md` §13–14.
>
> **Revisión 2026-09-26 (3.ª, tras la ronda 2 del spike; aprobada por Luigui):** el swipe pasa a ser un **canal secundario en v1** y se detecta con el **detector v2**: categoría `Open_Palm` como condición de armado **más mano abierta y casi quieta justo antes del trazo** (≥200 ms). Umbral por defecto **8 %** del ancho (rango de trabajo ~8–12 %). Meta **8/10 por lado en intentos válidos** (antes 9/10); voz y teclado cubren los fallos. Se mantiene estricto: **0 cambios no intencionales y 0 disparos inversos**; ante cualquier conflicto entre tasa de acierto y falsos positivos, gana 0 falsos positivos (ver `plan.md` §12).
>
> **Revisión 2026-09-26 (2.ª, tras el spike T06; aprobada por Luigui):** el swipe se mide con **~10–12 % del ancho del cuadro en <500 ms** (antes ~25 % en ~400 ms: a la distancia real un swipe recorre 13–21 % del ancho; ver `plan.md` §9), **con la mano abierta como condición de armado** (el método —categoría `Open_Palm` o dedos extendidos por landmarks— se fija con la comparación offline de la ronda 2), y la resolución de cámara por defecto es **640×480**. Además `presentador.js` **bloquea** la telemetría de MediaPipe hacia `odml.pa.googleapis.com` (`fetch`/XHR/`sendBeacon`).

> **Revisión 2026-09-26 (aprobada por Luigui):** las teclas de control pasan de `G`/`V`/`H` a **`M` (gestos) / `E` (voz, "escuchar") / `I` (indicador)**. Verificado en `vendor/reveal/dist/reveal.js` (6.0.2): `H` = slide anterior, `G` = saltar a slide y **`V` (keyCode 86) = pausa / pantalla negra** (no figura en la ayuda de Reveal, solo en el código). `M`, `E` e `I` no las usa Reveal ni sus plugins (notes = `S`, search = Ctrl+Shift+F, zoom = Esc). El SPEC ya preveía reasignar si había choque (CU5).

## 1. Problema
Al presentar, Luigui necesita navegar los slides sin tocar la laptop ni depender de un clicker, usando swipes de mano o comandos de voz indistintamente.

## 2. Usuario objetivo
Luigui presentando en el trabajo, de pie a menos de 2 m de su MacBook Pro Intel (2019), con la presentación proyectada desde esa laptop y un micrófono Bluetooth conectado. Las presentaciones están construidas en HTML puro con Reveal.js (texto, estilos y estructura reales; no imágenes de slides).

## 3. Casos de uso principales
1. Como presentador, quiero hacer un swipe en el aire con la mano abierta hacia mi derecha para avanzar, y hacia mi izquierda para retroceder.
2. Como presentador, quiero decir "LeIA siguiente" o "LeIA retrocede" (o solo "siguiente" / "retrocede") para moverme un paso.
3. Como presentador, quiero decir "avanza 3 slides" o "retrocede 2 slides" para saltar varios slides de una vez.
4. Como presentador, quiero decir "vuelve al inicio" para ir al primer slide.
5. Como presentador, quiero apagar gestos o voz con una tecla si empiezan a dar falsos positivos, sin perder el control por teclado.

## 4. Criterios de aceptación

**Semántica de navegación**
- "Un paso" (swipe, "siguiente", "retrocede") equivale a la flecha derecha/izquierda: `Reveal.next()` / `Reveal.prev()`. Si el slide tiene fragments, avanza el siguiente fragment.
- Saltos de N slides mueven N slides horizontales completos (ignoran fragments): `Reveal.slide(h ± N)`.
- "Vuelve al inicio": `Reveal.slide(0, 0)`.
- Si el salto excede los límites, se detiene en el primer o último slide.

**CU1 — Swipe**
- DADO que la cámara ve mi mano abierta (`Open_Palm`) a ≤2 m, CUANDO la desplazo horizontalmente hacia mi derecha más de ~8–12% del ancho del cuadro en menos de ~500 ms con poco desplazamiento vertical, y la mano llevaba al menos ~200 ms abierta y casi quieta justo antes del trazo, ENTONCES avanza un paso exactamente una vez.
- CUANDO hago el mismo movimiento hacia mi izquierda, ENTONCES retrocede un paso exactamente una vez.
- La dirección se calcula desde la perspectiva del presentador (la imagen de la webcam viene en espejo y se invierte).
- DADO que acaba de ocurrir un cambio por cualquier canal, CUANDO pasan menos de 1500 ms, ENTONCES se ignora todo movimiento y comando (cooldown compartido). Esto evita que el regreso de la mano después de un swipe dispare el sentido contrario.
- DADO que hablo gesticulando normalmente (mano no abierta, movimiento lento o vertical), ENTONCES no cambia el slide.

**CU2/CU3/CU4 — Voz**
- Vocabulario (sin distinguir tildes ni mayúsculas; "slide", "slides", "diapositiva", "lámina" opcionales al final):
  - Avanzar 1: `siguiente | avanza | adelante`
  - Retroceder 1: `retrocede | atrás | anterior | regresa`
  - Avanzar N: `avanza N` / `adelanta N`
  - Retroceder N: `retrocede N` / `regresa N`
  - Inicio: `vuelve al inicio | al inicio | primer slide`
- N se entiende en dígitos ("3") o en palabras ("tres", "un", "una"), de 1 a 20.
- **Con prefijo "LeIA":** la frase dispara aunque vaya dentro de un enunciado más largo, y se evalúa sobre resultados intermedios para reducir latencia.
- **Sin prefijo (a secas):** solo dispara si el enunciado completo, como resultado final, es exactamente un comando del vocabulario. "Siguiente" dicho solo, con pausa, avanza; "veamos el siguiente punto" no hace nada.
- Variantes de transcripción de "LeIA" aceptadas: `leia`, `leía`, `lea`, `le ia`, `lelia`, `leya`. La lista final se ajusta en el ensayo con lo que realmente transcriba Chrome.
- Un mismo enunciado dispara una sola acción (sin doble disparo entre resultado intermedio y final).
- Chrome corta el reconocimiento continuo tras silencios; el sistema lo reinicia automáticamente en `onend`/`onerror` sin intervención.

**CU5 — Control y feedback**
- Tecla `M` activa/desactiva gestos (**apagados por defecto**: experimentales en v1); `E` activa/desactiva voz; `I` oculta/muestra el indicador. Las teclas nativas de Reveal (flechas, espacio) y el clicker siguen funcionando siempre. `M`, `E` e `I` no deben chocar con atajos de Reveal (verificado; ver la revisión del 2026-09-26 arriba).
- Indicador discreto en una esquina, por encima del contenido de la presentación sin alterar su layout: estado de cámara y micrófono, y último comando ejecutado con el slide resultante (ej. `+3 → 7/20`).

**Arranque**
- DADO una presentación HTML con Reveal.js en una carpeta (`index.html` + sus assets), CUANDO ejecuto `python3.11 presentar.py ~/Presentaciones/<carpeta>`, ENTONCES se abre en Chrome en `http://localhost:8765` con el presentador activo.
- El HTML de la presentación no se modifica en disco: `presentar.py` inyecta los `<script>` del presentador antes de `</body>` al servir `index.html` (mismo patrón que la inyección del token en jarvis-server).
- El presentador espera a que Reveal esté listo (`Reveal.isReady()` / evento `ready`) antes de activarse.

**Errores**
- La página no usa Reveal.js → la presentación se muestra igual, el presentador no se activa y el indicador lo avisa.
- Sin permiso de cámara → funciona con voz y teclado; el indicador lo muestra. (Con los gestos apagados por defecto, la cámara solo se pide al pulsar `M`.)
- Sin internet (Web Speech falla) → funciona con gestos y teclado; el indicador lo muestra.
- Comando de voz no reconocido → no pasa nada; no hay mensajes intrusivos en pantalla.

## 5. Fuera de alcance
- Crear el contenido de la presentación del lunes (se construye aparte, en HTML con Reveal.js).
- Presentaciones que no sean Reveal.js (PPT, Keynote, PDF, imágenes de slides).
- Navegación vertical de Reveal (slides anidados): la navegación es lineal, igual que las flechas.
- El asistente LeIA como tal: aquí "LeIA" es solo una palabra de activación dentro del navegador.
- Que Jarvis o LeIA controlen los slides desde un daemon (posible v2).
- Integración con `jarvis.py`, sus intents, el RESOLVER (T1–T7) o el `.zshrc`.
- "Ir al slide N" por número absoluto, "ve al final", zoom, puntero láser.
- Cualquier cambio a conceptos, ATLAS o archivos del vault fuera de la carpeta del proyecto.

## 6. Stack / arquitectura
- **Presentación:** HTML + Reveal.js. El proyecto trae Reveal.js en `vendor/` y `presentar.py` lo sirve en `/vendor/`, para que las presentaciones puedan referenciarlo localmente en vez de depender de un CDN el día de la charla.
- **Gestos:** MediaPipe Tasks Vision `GestureRecognizer` (JS/WASM). La condición de armado es la categoría `Open_Palm` con la mano casi quieta justo antes del trazo (elegida con datos: la geometría de dedos extendidos no la superó; ver `plan.md` §11–12) y los landmarks de la mano (centro de palma) miden la trayectoria horizontal del swipe. Cámara a 640×480. Librería y modelo `gesture_recognizer.task` descargados en `vendor/` durante el setup (sin CDN en runtime).
- **Voz:** Web Speech API de Chrome (`continuous`, `interimResults`, `lang: es-PE`). Parser de comandos en el cliente (normalización de tildes, variantes de "LeIA", números en palabras), sin Groq.
- **Servidor:** `presentar.py` con librería estándar de Python 3.11 (`http.server`) en `localhost:8765`. `localhost` es contexto seguro, requisito de `getUserMedia`. Sirve la carpeta de la presentación en `/`, el presentador en `/presentador/` y las librerías en `/vendor/`, e inyecta los scripts en `index.html`.
- **Convivencia con Jarvis:** Jarvis local solo se activa con "Jarvis" y macOS permite que ambos usen el micrófono a la vez, así que no hay que pausarlo.
- **Confidencialidad:** las presentaciones son material de trabajo. Viven fuera del repo (`~/Presentaciones/`) y nunca se copian al vault. El proyecto no contiene ninguna presentación; como ejemplo de prueba incluye un deck de demo genérico (`demo/index.html`) sin contenido de trabajo.

Estructura:
```
Prompts/Presentaciones/presentador/
├── docs/SPEC.md
├── presentar.py        ← servidor local + inyección de scripts
├── presentador.js      ← swipe + voz + cooldown + teclas + indicador
├── comandos.js         ← parser de voz (testeable por separado)
├── demo/index.html     ← deck Reveal.js genérico para probar
├── vendor/             ← reveal.js, tasks-vision, gesture_recognizer.task
├── .gitignore
└── README.md           ← uso + cómo referenciar /vendor/ desde un deck + checklist de ensayo
```

## 7. Métricas de éxito
- En ensayo de 10 min hablando y gesticulando normalmente: 0 cambios de slide no intencionales.
- **[Experimental en v1 — objetivo, no criterio de aceptación]** Swipe (canal secundario): **8/10 a la derecha y 8/10 a la izquierda en intentos válidos** (mano abierta y quieta antes del trazo, a 1–2 m con luz de oficina), **0 disparos inversos** al regresar la mano. Los swipes que no se reconocen los cubren la voz y el teclado.
- Prioridad: ante cualquier conflicto entre tasa de acierto y falsos positivos, se prioriza **0 falsos positivos**.
- 9/10 comandos de voz reconocidos a la primera, incluidos saltos de N slides.
- Latencia percibida < 1 s en swipe y < 1.5 s en voz.
- El lunes la presentación completa se navega sin tocar la laptop.

## 8. Preguntas abiertas
- Ninguna bloqueante. Las variantes de transcripción de "LeIA" se calibran en el ensayo.

---

## Checklist de ensayo (domingo)
- [ ] Presentación del lunes en `~/Presentaciones/2026-09-28/index.html`, con Reveal.js referenciado desde `/vendor/` (no CDN)
- [ ] macOS: micrófono Bluetooth como entrada por defecto; si el audio de salida también va por ese dispositivo, verificar que no baje de calidad
- [ ] Chrome: aceptar permisos de cámara y micrófono para `localhost:8765`
- [ ] Decir "LeIA siguiente" varias veces y revisar en el indicador cómo transcribe Chrome "LeIA"; agregar variantes si hace falta
- [ ] Probar "siguiente" a secas y frases como "veamos el siguiente punto" (esta última no debe disparar)
- [ ] Probar "avanza 3", "retrocede dos slides", "vuelve al inicio", y un slide con fragments
- [ ] Probar swipes con la luz real o la más parecida, a la distancia en la que vas a estar; revisar que el regreso de la mano no retroceda
- [ ] Probar en la red donde vas a presentar o con hotspot (la voz necesita internet)
- [ ] Probar `M`, `E`, `I` y el clicker/flechas como fallback (y confirmar que `V` NO hace nada útil: en Reveal es pausa/pantalla negra)
- [ ] Opcional: pausar Jarvis local por precaución si no lo vas a usar durante la charla
