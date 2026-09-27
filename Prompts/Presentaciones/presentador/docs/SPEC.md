# SPEC — Presentador por gestos y voz (LeIA)

> Proyecto: `~/Documents/Segundo_cerebro/Prompts/Presentaciones/presentador/` · Deadline: lunes 2026-09-28 (presentación de trabajo)

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
- DADO que la cámara ve mi mano abierta (`Open_Palm`) a ≤2 m, CUANDO la desplazo horizontalmente hacia mi derecha más de ~25% del ancho del cuadro en menos de ~400 ms con poco desplazamiento vertical, ENTONCES avanza un paso exactamente una vez.
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
- Tecla `M` activa/desactiva gestos; `E` activa/desactiva voz; `I` oculta/muestra el indicador. Las teclas nativas de Reveal (flechas, espacio) y el clicker siguen funcionando siempre. `M`, `E` e `I` no deben chocar con atajos de Reveal (verificado; ver la revisión del 2026-09-26 arriba).
- Indicador discreto en una esquina, por encima del contenido de la presentación sin alterar su layout: estado de cámara y micrófono, y último comando ejecutado con el slide resultante (ej. `+3 → 7/20`).

**Arranque**
- DADO una presentación HTML con Reveal.js en una carpeta (`index.html` + sus assets), CUANDO ejecuto `python3.11 presentar.py ~/Presentaciones/<carpeta>`, ENTONCES se abre en Chrome en `http://localhost:8765` con el presentador activo.
- El HTML de la presentación no se modifica en disco: `presentar.py` inyecta los `<script>` del presentador antes de `</body>` al servir `index.html` (mismo patrón que la inyección del token en jarvis-server).
- El presentador espera a que Reveal esté listo (`Reveal.isReady()` / evento `ready`) antes de activarse.

**Errores**
- La página no usa Reveal.js → la presentación se muestra igual, el presentador no se activa y el indicador lo avisa.
- Sin permiso de cámara → funciona con voz y teclado; el indicador lo muestra.
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
- **Gestos:** MediaPipe Tasks Vision `GestureRecognizer` (JS/WASM). Se usa la categoría `Open_Palm` como condición y los landmarks de la mano (centro de palma) para medir la trayectoria horizontal del swipe. Librería y modelo `gesture_recognizer.task` descargados en `vendor/` durante el setup (sin CDN en runtime).
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
- 9/10 swipes a la derecha y 9/10 a la izquierda reconocidos a 1–2 m con luz de oficina, sin disparo inverso al regresar la mano.
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
