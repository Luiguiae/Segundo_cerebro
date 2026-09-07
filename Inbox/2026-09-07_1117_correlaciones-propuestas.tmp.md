# Correlaciones propuestas — 2026-09-07

Candidatos evaluados: 20 (generados por señales objetivas — mención cruzada, tags compartidos, misma familia — sobre el pool de conceptos activo no cubierto por corridas anteriores del 2026-08-25 y 2026-08-31)
Sobrevivientes autocrítica adversarial: 1
Descartados: 19 (patrón dominante — distinto al de corridas previas: en esta corrida, 17 de los 19 descartes no fallan por ser co-ocurrencia superficial, sino porque uno de los dos archivos fuente ya contiene, en su propia sección "Tensiones y límites" o "Ejes investigados", la síntesis completa o casi completa de la relación entre ambos conceptos — al punto de citar al otro por nombre y resolver la tensión ahí mismo. Leer ambos conceptos por separado ya entrega la conclusión.)

---

## 1. Los tests en verde no son el pit stop

**Par:** `comprehension-debt` × `pit-stop-cognitivo`

**Señales:** mención cruzada explícita (pit-stop-cognitivo cita literalmente a comprehension-debt: "Equipos que no hacen pit stops cognitivos acumulan comprehension-debt hasta que el sistema colapsa") + 5 tags compartidos (conocimiento, criterio, equipo, ia, velocidad) + misma familia (velocidad-output) + contradicción verificada al leer ambos cuerpos completos: pit-stop-cognitivo declara una excepción explícita a su propia práctica que comprehension-debt refuta con su mecanismo central.

**Justificación de la tensión real:** pit-stop-cognitivo, en su propia sección de límites, declara: *"No aplica si el equipo ya tiene pruebas automatizadas robustas que funcionan como pit stop continuo — en ese caso el pit stop cognitivo ya está integrado en el proceso."* Comprehension-debt define su fenómeno central como exactamente lo contrario de lo que esa excepción asume: la deuda de comprensión se acumula *detrás* de un test suite en verde — *"El código se ve limpio. Los tests están en verde. El ajuste de cuentas llega en silencio, normalmente en el peor momento posible."* No es que los dos conceptos hablen de temas relacionados: uno declara una condición de exención que el otro documenta empíricamente como el escenario de mayor riesgo, no de mayor seguridad.

---

### La tensión

pit-stop-cognitivo presenta la pausa deliberada — revisar el código generado, ejecutar los tests, confirmar que el sistema se comporta como se esperaba — como el mecanismo que hace sostenible la velocidad de desarrollo con IA. Pero incluye una cláusula de salida: si el equipo ya tiene "pruebas automatizadas robustas", esas pruebas *son* el pit stop, y la pausa deliberada deja de ser necesaria porque "ya está integrada en el proceso".

comprehension-debt describe el caso documentado por Margaret-Anne Storey de un equipo que chocó contra la comprehension debt en la semana siete: no podían hacer cambios simples sin romper algo inesperado, y el motivo no era código sucio ni tests fallando — era que nadie en el equipo podía explicar por qué se habían tomado las decisiones de diseño ni cómo las partes del sistema estaban supuestas a funcionar juntas. Los tests de ese equipo, hasta la semana siete, seguían en verde. El artículo lo nombra directamente: *"A diferencia de la deuda técnica — que se manifiesta como fricción visible... la comprehension debt produce falsa confianza."*

Los datos que comprehension-debt cita refuerzan el punto con precisión quirúrgica: el estudio arXiv 2603.28592 encontró que el código generado con IA tiene 40% de vulnerabilidades críticas en contextos sensibles a seguridad — código que, por definición, pasaba los tests que existían, o no habría llegado a producción. Un test suite verifica que el comportamiento observado coincide con lo que el test especifica. No verifica que un humano entienda por qué el sistema se comporta así, ni que ese comportamiento sea la decisión de diseño correcta. Eso es precisamente lo que comprehension-debt mide y lo que la cláusula de exención de pit-stop-cognitivo trata como equivalente.

### El insight no obvio

pit-stop-cognitivo y comprehension-debt no compiten por la misma pregunta — pero el primero, sin proponérselo, ofrece una vía de escape (”ya tenemos tests, no necesitamos pausar”) que el segundo demuestra que es exactamente la puerta por la que la comprehension debt entra sin ser detectada. Un equipo que lee solo pit-stop-cognitivo concluye razonablemente que invertir en CI robusto lo exime de la disciplina de la pausa cognitiva. Un equipo que lee solo comprehension-debt aprende que los tests en verde son una señal de falsa confianza, pero no tiene ningún motivo para dudar de la cláusula de exención de una práctica que ni siquiera menciona.

Hay además una asimetría más fina: comprehension-debt identifica el único patrón mitigador validado empíricamente por la investigación de Glasgow (arXiv 2604.13277) — "rewrite before commit", es decir, forzar la reescritura del código generado antes de aceptarlo, no solo revisarlo o correr sus tests. El pit stop cognitivo, tal como está definido ("revisar el código generado, ejecutar los tests, confirmar que el sistema se comporta como se esperaba"), es una práctica de verificación de comportamiento — más cercana a un QA gate que a un ejercicio de reescritura forzada. Si "rewrite before commit" es el único patrón que la evidencia valida, un pit stop que consiste en revisar y correr tests sin reescribir puede no alcanzar el umbral que comprehension-debt exige para hablar de mitigación real — incluso cuando el equipo cree estar haciendo la pausa correcta.

### El límite

Esto no invalida el pit stop cognitivo como práctica — sigue siendo mejor que no pausar en absoluto, y sigue capturando clases de error que ninguna suite de tests detecta por diseño (deriva del modelo mental, decisiones arquitectónicas no explicadas). El límite es específico a la cláusula de exención: la existencia de tests robustos no es evidencia de comprensión, es evidencia de cobertura de comportamiento — dos cosas que comprehension-debt muestra que pueden divergir completamente durante meses (la etapa "Drift", días 30-180, según el staging de Allstacks que cita el propio pit-stop-cognitivo).

Tampoco se sigue que la solución sea eliminar la cláusula de exención sin más: comprehension-debt es explícito en que el problema es en última instancia organizacional — las métricas de equipo (velocity, story points, PRs merged) no miden comprensión, y ningún ritual individual, pit stop o rewrite-before-commit, resuelve un incentivo desalineado a nivel de equipo. El pit stop cognitivo, incluso en su versión más exigente (reescribir, no solo revisar), sigue siendo una táctica que un incentivo organizacional mal diseñado puede vaciar de contenido.

---

## Descartados y razón

- `agencia-humana-como-imperativo-ux` × `representacion-agente` — la tensión específica (el criterio de reversibilidad de uno se vuelve inaplicable en el escenario de negociación agente-a-agente del otro, porque el humano está estructuralmente ausente) ya está enunciada por representacion-agente: *"El problema de representación es más agudo donde los compromisos son irreversibles y el humano no estará presente para corregirlos"*, y su sección de tensiones cierra remitiendo directamente a agencia-humana-como-imperativo-ux. Síntesis ya explícita en el archivo fuente.
- `disenador-a-constructor` × `copiloto-de-producto` — copiloto-de-producto ya plantea y resuelve esta tensión en su propio texto: *"Tensiona con disenador-a-constructor: si el diseñador ya puede construir directamente, ¿sigue necesitando un rol de copiloto separado o lo integra? La respuesta depende del tamaño del sistema..."* — nada que agregar no esté ya ahí.
- `ia-como-filtro-de-entrada` × `marea-creciente-de-automatizacion` — marea-creciente-de-automatizacion ya declara la tensión y su resolución ("pueden ser compatibles si el filtro de entrada describe la primera zona en saturarse, no la única") en su propia sección de tensiones.
- `ia-como-filtro-de-entrada` × `juicio-como-trabajo-completo` — juicio-como-trabajo-completo se describe a sí mismo como extensión directa de ia-como-filtro-de-entrada ("este concepto extiende la consecuencia al largo plazo organizacional"); relación de extensión ya declarada, no tensión nueva.
- `inversion-sesgo-tecnologico` × `automatizacion-vs-ampliacion` — el propio eje investigado de inversion-sesgo-tecnologico ya nombra la síntesis: "conecta con automatizacion-vs-ampliacion (el seniority ya no garantiza el modo amplificación)". La conclusión central ya está puesta encima de la mesa por la fuente misma.
- `presupuesto-ia-como-restriccion` × `impuesto-de-verificacion` — presupuesto-ia-como-restriccion ya integra la conexión de forma explícita: "El impuesto-de-verificacion se extiende aquí: no solo verificas el output, también debes verificar el modelo que lo produjo."
- `presupuesto-ia-como-restriccion` × `ia-sin-ecosistema` — mismo archivo, misma sección: "ia-sin-ecosistema ya captura que el ROI de la IA requiere activos complementarios; este concepto agrega que uno de esos activos complementarios es ahora la gobernanza del propio gasto en IA" — síntesis ya resuelta por la fuente.
- `arquitectura-de-inteligencia` × `conocimiento-autoorganizado-por-llm` — este es el caso más extremo: conocimiento-autoorganizado-por-llm dedica un párrafo completo de "El concepto" a declarar la tensión de forma explícita ("Son respuestas opuestas a la misma pregunta") y la retoma en "Tensiones y límites". El archivo ya es, en esencia, la correlación.
- `agente-como-carpeta` × `arnes-del-agente` — agente-como-carpeta declara la relación explícitamente como complementariedad, no tensión: "No son el mismo concepto con nombres distintos... Diseñar bien el arnés no garantiza una buena arquitectura de carpeta, y viceversa."
- `arnes-del-agente` × `espectro-autonomia-agente` — arnes-del-agente ya desarrolla esta tensión completa en su propia sección de límites, incluyendo la conclusión ("el diseño del arnés es inherentemente un problema de calibración continua, no de configuración única").
- `arnes-del-agente` × `limite-de-las-jaulas-digitales` — limite-de-las-jaulas-digitales dedica un párrafo entero a esta tensión específica, con la conclusión ya cerrada: "el arnés reduce el riesgo, no lo elimina."
- `arnes-del-agente` × `representacion-agente` — representacion-agente construye toda su sección "El concepto" sobre esta distinción ("El arnes-del-agente es un contrato de capacidades... La representación agente requiere algo distinto — un contrato de identidad"). Ya es la correlación completa.
- `autoautomatizacion-del-disenador` × `automatizacion-vs-ampliacion` — autoautomatizacion-del-disenador resuelve esta tensión explícitamente en su propio texto: "La autoautomatización es el modo en que un senior... activa el modo automatización sobre sus propias funciones cognitivas más valiosas."
- `inteligencia-como-utilidad` × `riesgo-geopolitico-del-modelo` — riesgo-geopolitico-del-modelo ya declara la conexión ("si la inferencia frontier se comodifica más rápido de lo que avanza la regulación, la ventana de este riesgo puede cerrarse"); el ángulo adicional explorado (que el umbral regulatorio y el umbral de no-comoditización coinciden en el mismo tramo frontier) no tiene respaldo textual directo en ninguno de los dos archivos — es extensión especulativa, no tensión verificable en el texto.
- `inteligencia-como-utilidad` × `ia-sin-ecosistema` — inteligencia-como-utilidad ya se define a sí mismo como "el mecanismo inverso" de ia-sin-ecosistema, explícitamente, en su sección "Por qué importa". Síntesis ya resuelta por la fuente.
- `poblaciones-sinteticas` × `usuarios-sinteticos` — poblaciones-sinteticas abre su propio texto con la distinción completa ("La distinción... es de nivel, no de grado"); es una aclaración de escala ya resuelta por la fuente, no una tensión pendiente de descubrir.
- `cambio-como-estado-permanente` × `cultura-de-tinkering` — cambio-como-estado-permanente ya plantea y resuelve la tensión: "La cultura de tinkering es una forma de institucionalizar el espacio de experimentación dentro del cambio permanente, no a pesar de él."
- `quien-controla-el-prompt` × `capital-de-contexto` — capital-de-contexto ya desarrolla esta relación en detalle ("El prompt controller sin capital de contexto maduro reinventa cada interacción. El capital de contexto sin un prompt controller con criterio produce artefactos técnicamente bien formados pero sin juicio de dominio") — la correlación ya está escrita ahí, casi palabra por palabra.
- `soberania-epistemica` × `sycophancy-como-riesgo-de-diseno` — caso extremo de duplicación: ambos archivos contienen la misma frase, casi verbatim ("optimizar para satisfacción de usuario y para bienestar/optimizar para bienestar de usuario no son la misma cosa"). La síntesis no solo es obvia — ya está copiada en los dos lados.

---

_Propuestas generadas automáticamente por Jarvis. Requieren revisión y aprobación de Luigui antes de escribir en `Correlaciones/`._
_Para aprobar: `Jarvis, revisa propuestas pendientes`_
