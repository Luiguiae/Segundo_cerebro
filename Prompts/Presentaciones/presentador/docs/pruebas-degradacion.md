# Pruebas manuales de degradación (T15) — 2026-09-27

Hechas con Luigui presente, con la guía en pantalla (`tests/manual/vivo/`, guion `degradacion`; resultados en `tests/manual/vivo/resultados/degradacion-*.json`). Cubren los 4 puntos de "Errores" del SPEC §4. Micrófono integrado (no había Bluetooth conectado).

| # | Prueba | Cómo se hizo | Resultado |
|---|---|---|---|
| 1 | **Página sin Reveal.js** | `servir_vivo.py degradacion --variante sinreveal --deck tests/manual/vivo/deck-sin-reveal`. Se espera 15 s, se comprueba que la página se ve igual y que el indicador dice "no usa Reveal.js — inactivo", y se pulsan `M` y `E` | ✅ 5/5 tras corregir un fallo (ver abajo) |
| 2 | **Sin permiso de cámara** (activando los gestos con `M`) | Origen nuevo (`localhost:8773`): permitir micrófono, pulsar `M` UNA vez y **bloquear** la cámara; luego "LeIA, siguiente" y la flecha → | ✅ 5/5: indicador "sin permiso de cámara"; voz y teclado siguen funcionando; sin mensajes intrusivos |
| 3 | **Sin internet** (Wi-Fi apagado a mano) | Gestos encendidos con `M`; Wi-Fi apagado; se dice varias veces "LeIA, siguiente"; swipe; flecha; Wi-Fi encendido | ✅ 8/8: la voz avisa "sin internet — reintentando" y no cambia nada; el swipe y la flecha funcionan sin internet; al volver el Wi-Fi la voz se recupera sola y "LeIA, siguiente" funciona |
| 4 | **Comando de voz no reconocido** | "LeIA, bailemos un vals", "LeIA, qué hora es", un murmullo y solo "LeIA" | ✅ 5/5: no cambia nada; la pantalla queda limpia (Luigui lo confirmó) |

## Fallos encontrados y corregidos durante la prueba
- **Prueba 1 (fallo real):** en una página sin Reveal, pulsar `M` **encendía la cámara** (30 fps) aunque el SPEC exige que el presentador no se active. Corregido en `presentador.js`: sin Reveal (o antes de que esté listo) las teclas solo cambian el deseo, no abren cámara ni micrófono, y el indicador dice "inactivo (sin Reveal)". Verificado en Chrome: 0 llamadas a `getUserMedia` y 0 reconocedores creados. La ejecución fallida (D1d) queda como evidencia en `degradacion-20260927-000601.json`.
- **Prueba 2, primer intento:** `M` se pulsó dos veces (el modelo tarda unos segundos en cargar antes de que Chrome pida la cámara), lo que apagó los gestos antes del permiso. No era un fallo del código; se ajustó el texto de la guía ("pulsa M UNA vez y espera") y se repitió.
- **Prueba 1, repetición:** la primera repetición no llegó a empezar (no se pulsó ESPACIO a tiempo); se repitió sola.

## Notas
- **Audio ambiente:** el micrófono transcribió conversaciones de fondo (voces ajenas) durante algunas pruebas. La guía ya **no guarda transcripciones fuera de los pasos de voz** y en estos trunca a 40 caracteres; los resultados ya guardados se limpiaron (`gestos-*` y `degradacion-*`). Ojo en el ensayo: con audio de fondo la voz transcribe lo que oiga (y puede fallar con "gratis gratis" en lugar de "LeIA, siguiente").
- Variantes de "LeIA" vistas en estas pruebas: *leía, leí A, ella, autosos leía…* Sin cambios en `VARIANTES_LEIA` (solo `de ella`, calibrada en T13).
