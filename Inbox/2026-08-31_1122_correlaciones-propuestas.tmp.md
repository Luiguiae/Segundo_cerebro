# Correlaciones propuestas — 2026-08-31

Candidatos evaluados: 20 (top 20 por score entre 1,429 pares con señal ≥2, tras excluir pares ya en `Correlaciones/`, los 3 pendientes de revisión en `Inbox/2026-08-25_0811_correlaciones-propuestas.tmp.md`, y los 15 descartados en la corrida anterior del 2026-08-25 — sin cambios en el vault desde entonces, así que evaluarlos de nuevo habría repetido el mismo veredicto)
Sobrevivientes autocrítica adversarial: 2
Descartados: 18 (mayoría por relación de ejemplificación o co-ocurrencia temática sin contradicción real — el par comparte `relacionado` en frontmatter pero no revela una tensión que no sea obvia leyendo ambos conceptos por separado)

---

## 1. El criterio de reversibilidad protege el resultado, no el juicio

**Par:** `agencia-humana-como-imperativo-ux` × `soberania-epistemica`
**Señales:** ambos se listan mutuamente en `relacionado` + 5 tags compartidos (diseño, ux, agentes, etica, control) + misma familia (agencia-ia)

**Justificación de la tensión real:** `agencia-humana-como-imperativo-ux` calibra cuándo se necesita agencia humana explícita con un solo criterio: reversibilidad — irreversible/alto impacto requiere intervención, reversible/bajo riesgo puede ejecutarse autónomamente. `soberania-epistemica` muestra que la rendición cognitiva (cognitive miserliness) opera con más fuerza exactamente en las decisiones de bajo riesgo y alta frecuencia — el segmento que el otro concepto exime de intervención. El criterio de calibración de uno es el punto ciego del otro.

---

### La tensión

`agencia-humana-como-imperativo-ux` resuelve "¿cuándo necesito un humano en el loop?" con una regla orientada a la consecuencia de la acción: si es reversible y de bajo impacto, el agente ejecuta sin agencia humana explícita; si es irreversible o de alto impacto, requiere intervención.

`soberania-epistemica` mide algo distinto: no el riesgo de la acción, sino el estado cognitivo de quien la evalúa. Su propio texto es explícito sobre dónde el problema es más agudo: "en checkpoints de alto volumen y baja consecuencia percibida... que en checkpoints ante decisiones irreversibles de alta consecuencia, donde el usuario activa naturalmente el Sistema 2". Es decir: las dos reglas señalan en direcciones opuestas para el mismo tipo de decisión. Aprobar un resumen generado por IA, aceptar una sugerencia de código, confirmar una recomendación — reversible, bajo riesgo — es precisamente donde `agencia-humana-como-imperativo-ux` dice "no hace falta intervención explícita" y donde `soberania-epistemica` dice "aquí es donde más se necesita forzar el pensamiento, porque nada en la situación lo va a activar por sí solo".

### El insight no obvio

Leídos por separado, ambos conceptos suenan compatibles — los dos dicen "protege la agencia humana frente a la IA". El insight no obvio es que el criterio operacional de uno (reversibilidad, una propiedad de la acción) es un mal proxy para lo que el otro mide (activación del Sistema 2, un estado mental del usuario). No son la misma variable, y optimizar por una no garantiza la otra.

Un sistema puede cumplir perfectamente el criterio de `agencia-humana-como-imperativo-ux` — calibra fricción según reversibilidad — y fallar por completo el objetivo de `soberania-epistemica`: nunca activa pensamiento deliberado en las decisiones reversibles, que son la mayoría del volumen de interacción diario. El daño no es un evento único y grave — es la erosión acumulada de una capacidad de juicio que nunca se ejercita porque cada decisión individual "no vale la pena pensar". La reversibilidad protege contra el error catastrófico; no protege contra la atrofia del criterio.

### El límite

Esto no invalida la reversibilidad como criterio — sigue siendo necesaria para decidir dónde el error es tolerable. El punto es que es insuficiente como único eje: hace falta un segundo criterio, ortogonal, sobre frecuencia y esfuerzo cognitivo esperado. Pero añadir ese segundo eje tiene costo real: no es viable activar el Sistema 2 en cada una de cientos de microdecisiones diarias de baja consecuencia sin paralizar el flujo. Ninguno de los dos conceptos resuelve cómo elegir el subconjunto de decisiones reversibles de alto volumen donde vale la pena pagar el costo de fricción epistémica deliberada, sin volver el sistema inservible por exceso de checkpoints.

---

## 2. El impuesto no se paga parejo: el atacante lo evade, el defensor lo hereda

**Par:** `impuesto-de-alineacion` × `seguridad-asimetrica-de-modelos-abiertos`
**Señales:** 4 tags compartidos (ia, gobernanza-ia, etica, control) + misma familia (agencia-ia) + relación declarada en `relacionado` (unidireccional: `seguridad-asimetrica-de-modelos-abiertos` → `impuesto-de-alineacion`) + eco léxico directo — `seguridad-asimetrica-de-modelos-abiertos` titula una de sus secciones "El impuesto medido" sin nombrar formalmente el concepto emparejado

**Justificación de la tensión real:** `impuesto-de-alineacion` describe la degradación de capacidad por entrenamiento de seguridad como un costo estructural que paga cualquiera que use un modelo alineado — la metáfora del "impuesto" implica una carga compartida, inevitable si usas la API. `seguridad-asimetrica-de-modelos-abiertos` muestra que en ciberseguridad ese impuesto no se distribuye parejo: el atacante tiene una vía de escape que el defensor no tiene (migrar a un modelo abierto sin restricciones), mientras que el defensor legítimo, atado a cumplimiento y cadena de custodia, no puede evadirlo de la misma forma. La metáfora fiscal, que sugiere universalidad, oculta una transferencia selectiva de capacidad.

---

### La tensión

`impuesto-de-alineacion` plantea el alignment tax como costo estructural inevitable: cualquiera que use un modelo alineado por API "hereda el impuesto sin haberlo elegido", y lo documenta con datos generales de degradación de capacidad (accuracy en razonamiento cayendo de 56.6% a 16.4% con más safety training).

`seguridad-asimetrica-de-modelos-abiertos` toma el mismo tipo de medición — literalmente titula una sección "El impuesto medido", citando el dato análogo de su propio dominio (2.72× tasa de rechazo en trabajo de ciberseguridad legítimo, "Defensive Refusal Bias", ICLR 2026) — y muestra que ese impuesto tiene una vía de escape que el concepto original no contempla: el atacante puede simplemente cambiar de modelo. El caso Unit 42 (julio 2026) lo documenta de forma literal: el mismo actor que Claude Code y Codex bloquearon completó el ataque migrando a DeepSeek vía Hermes Agent, sin fricción. El defensor, en el caso paralelo de Hugging Face, no tuvo esa misma libertad: necesitaba un modelo igual de abierto para hacer forense, pero sigue atado a estándares de auditabilidad y cadena de custodia que el atacante no respeta.

### El insight no obvio

La palabra "impuesto" implica, sin que el concepto original lo declare explícitamente, una carga compartida — algo que se paga porque no hay alternativa, como un impuesto real aplicado a toda una categoría de contribuyentes. `seguridad-asimetrica-de-modelos-abiertos` revela que en ciberseguridad esa premisa es falsa: existe una alternativa (modelos abiertos sin alineación) y solo un lado del conflicto puede tomarla sin costo. El atacante no paga el impuesto — lo evade por diseño, porque no tiene ningún motivo para preferir un modelo alineado. El defensor no puede evadirlo de la misma forma porque su legitimidad depende precisamente de operar dentro de las estructuras de cumplimiento que el impuesto protege.

El resultado no es una carga distribuida — es una transferencia neta de capacidad desde quien cumple las reglas de alineación hacia quien no las cumple. Cada punto de "impuesto" que un proveedor cobra en nombre de la seguridad, en ciberseguridad ofensiva/defensiva, se convierte en ventaja de capacidad relativa para el actor que no está sujeto a ese proveedor — invirtiendo el propósito declarado del impuesto: en vez de reducir el riesgo agregado, lo redistribuye desde el lado que se suponía debía proteger.

### El límite

La inversión de la metáfora aplica específicamente donde atacante y defensor requieren el mismo tipo de contenido para operar (exploits, malware, artefactos C2) y donde el defensor no puede migrar libremente a un modelo sin restricciones sin comprometer su propia legitimidad operacional — el límite que `seguridad-asimetrica-de-modelos-abiertos` ya declara para sí mismo. No aplica igual a dominios donde el impuesto de alineación afecta capacidad general (research, code generation) sin un actor adversarial activo explotando la asimetría; ahí sigue siendo, más literalmente, una carga compartida sin mecanismo de evasión unilateral. Los programas de verificación de identidad (Cyber Verification Program de Anthropic, Trusted Access de OpenAI) son el intento institucional de restaurar la metáfora fiscal — permitir excepciones para defensores verificados — pero ambos conceptos documentan que esa verificación impone su propia fricción asimétrica sobre quien ya estaba en desventaja.

---

## Descartados y razón (resumen — top 18 restantes del batch de 20)

Patrón dominante: el par ya se declara mutuamente en `relacionado`, comparte 3+ tags y misma familia, pero al leer ambos cuerpos completos la conexión es de **ejemplificación o co-ocurrencia temática**, no de tensión — uno de los dos ya es, en esencia, un caso particular o una extensión directa del otro, sin contradecirlo:

- `agencia-humana-como-imperativo-ux` × `ux-checkpoints` — el segundo es la implementación de diseño del primero (`ux-checkpoints` es, literalmente, el mecanismo que `agencia-humana-como-imperativo-ux` pide); no hay contradicción, hay especificación.
- `ux-checkpoints` × `arquitectura-de-confianza` — mismo patrón: confianza es la consecuencia declarada de checkpoints bien diseñados, no una fuerza en tensión con ellos.
- `metricas-post-pantalla` × `arnes-del-agente` — co-ocurrencia temática (ambos sobre gobernar agentes) sin mecanismo de contradicción específico entre los dos.
- `las-tres-caras-del-producto-agentico` × `legibilidad-de-maquina` — relación de dependencia (una cara del producto requiere legibilidad), no tensión.
- `las-tres-caras-del-producto-agentico` × `arnes-del-agente` — mismo patrón de dependencia.
- `ia-sin-ecosistema` × `gobernanza-ia-performativa` — `gobernanza-ia-performativa` es un caso particular del argumento de "activos complementarios" que `ia-sin-ecosistema` ya nombra explícitamente (la "gobernanza real" es uno de los complementos que cita) — ejemplificación, no tensión nueva.
- `web-bifurcada` × `legibilidad-de-maquina` — co-ocurrencia: ambos describen el mismo fenómeno (internet dividida por accesibilidad a agentes) desde ángulos complementarios, sin contradecirse.
- `impuesto-de-alineacion` × `agente-que-escapa-obedeciendo` — ya hay mención cruzada literal en el cuerpo (`impuesto-de-alineacion` referencia el caso); la síntesis ya está semi-explícita.
- `seguridad-asimetrica-de-modelos-abiertos` × `riesgo-geopolitico-del-modelo` — ambos describen riesgos de modelos abiertos/geopolítica desde ángulos que se refuerzan, no se contradicen; síntesis obvia ("los modelos abiertos generan más de un tipo de riesgo").
- `automatizacion-vs-ampliacion` × `ia-como-filtro-de-entrada` — relación de aplicación (uno es un caso del otro), sin tensión nueva no obtenible de cada uno por separado.
- `arquitectura-de-inteligencia` × `capital-de-contexto` — co-ocurrencia estructural (misma familia, mismo tema de fondo); `capital-de-contexto` ya se apoya explícitamente en el marco de `arquitectura-de-inteligencia` en su propio texto.
- `sistema-de-mentalidades-futuras` × `colonizar-el-manana-con-hoy` — el segundo es prácticamente un caso aplicado del primero; título reducible a "[A] y [B]" sin pérdida.
- `disenador-a-constructor` × `diseno-dos-velocidades` — relación de precedencia/complemento ya asumida por ambos textos, no contradicción.
- `disenador-a-constructor` × `diseno-uxui-y-ia` — mismo patrón.
- `metacognicion-del-disenador` × `autoautomatizacion-del-disenador` — dependencia causal (uno es condición del otro), no tensión.
- `metricas-post-pantalla` × `las-tres-caras-del-producto-agentico` — co-ocurrencia temática sin mecanismo de contradicción específico.
- `las-tres-caras-del-producto-agentico` × `cuello-de-botella-del-flujo` — relación de causa-efecto, no tensión real.
- `ia-sin-ecosistema` × `condicion-redespliegue` — ambos describen el mismo patrón general (valor requiere complementos organizacionales) desde dos ángulos del mismo argumento; síntesis ya obtenible leyendo cada uno.

---

_Propuestas generadas automáticamente por Jarvis. Requieren revisión y aprobación de Luigui antes de escribir en `Correlaciones/`._
_Para aprobar: `Jarvis, revisa propuestas pendientes`_
_Nota: sigue pendiente de revisión `Inbox/2026-08-25_0811_correlaciones-propuestas.tmp.md` (3 propuestas de la corrida anterior, sin tocar)._
