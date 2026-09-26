# Correlaciones propuestas — 2026-09-21

Candidatos evaluados: 20 (de 37 pares con señal de mención cruzada disponibles tras excluir los 29 pares ya en `Correlaciones/` y los 67 pares únicos ya evaluados en las 4 corridas anteriores — 2026-08-25, 2026-08-31, 2026-09-07, 2026-09-14. Los 37 saturaron el tope de 20 solo con la señal más fuerte (mención cruzada); no fue necesario bajar a los niveles de ≥3 tags compartidos o familia+tags. De los 37, se priorizaron los 20 con mayor cantidad de tags compartidos como criterio de desempate dentro del mismo nivel de señal.)

Sobrevivientes autocrítica adversarial: 1
Descartados: 19 — patrón dominante (18 de 19): el archivo fuente que menciona al otro concepto ya contiene, en su propia sección "Tensiones y límites" (frecuentemente bajo un subtítulo literal `**Tensión con `[concepto]`:**`), la síntesis completa de la relación, incluyendo su resolución. El vault ha madurado al punto de que casi todos los pares con mención cruzada directa fueron escritos ya con la correlación resuelta dentro del propio texto — mismo patrón que la corrida del 2026-09-14 (0 sobrevivientes) y el de 2026-09-07 (17 de 19).

---

## 1. El arnés no tiene dónde insertarse

**Par:** `arnes-del-agente` × `el-agente-que-no-para`

**Señales:** mención cruzada explícita (`el-agente-que-no-para` cita literalmente: *"El `arnes-del-agente` no fue explícitamente construido"*) + 1 tag compartido (`agentes`) + misma familia (`agencia-ia`)

**Justificación de la tensión real (1 línea):** `arnes-del-agente` define el arnés como una calibración continua a lo largo de un espectro rígido↔permisivo que presupone puntos discretos de decisión ("¿cuándo debe confirmar antes de actuar?"); `el-agente-que-no-para` documenta una arquitectura (Kimi Goal Mode, 5 días de autonomía continua, 300 sub-agentes, 4,000 pasos) donde esos puntos discretos no existen por diseño — no es que el arnés esté mal calibrado hacia el extremo permisivo, es que no hay dónde calibrarlo, y ninguno de los dos textos nombra esa distinción.

---

```yaml
---
titulo: "El arnés no tiene dónde insertarse"
tipo: correlacion
conceptos: [arnes-del-agente, el-agente-que-no-para]
fecha: 2026-09-21
tags: [ia, agentes, autonomia, checkpoints, tension]
estado: borrador
---
```

# El arnés no tiene dónde insertarse

## La tensión

`arnes-del-agente` propone que el diseño del agente se reduce a responder cuatro preguntas — qué puede hacer, qué información puede ver, cuándo debe confirmar antes de actuar, qué nunca puede hacer — y que la posición correcta del arnés en el `espectro-autonomia-agente` "no es fija, cambia según el contexto... es inherentemente un problema de calibración continua, no de configuración única." Esa calibración continua presupone algo que el texto nunca hace explícito: que existen momentos discretos, recurrentes, durante la ejecución, donde la pregunta "¿confirmo ahora o no?" puede plantearse y resolverse de nuevo.

`el-agente-que-no-para` documenta Kimi Work Goal Mode: un agente que recibe un objetivo y trabaja ininterrumpidamente hasta alcanzarlo, sin validación intermedia — en pruebas internas, cinco días completos de autonomía, 300 sub-agentes orquestados en 4,000 pasos. El propio texto observa, de pasada, que "el `arnes-del-agente` no fue explícitamente construido" para este caso — pero no explica por qué. La razón es estructural: el arnés de `arnes-del-agente` es una respuesta a una pregunta ("¿cuándo confirmo?") que solo tiene sentido si existen turnos o pasos donde detenerse es una opción arquitectónica disponible. Goal Mode elimina esa opción por diseño — el criterio de terminación migró del humano al agente, y "el diseñador ya no controla cuándo el agente pausa." No hay un "antes de actuar" recurrente al cual atar una confirmación: hay un objetivo y, días después, un resultado.

## El insight no obvio

Leído solo, `arnes-del-agente` sugiere que un arnés "permisivo que nunca confirma" es simplemente el extremo de un espectro de diseño — una elección de riesgo, no una imposibilidad. Leído solo, `el-agente-que-no-para` sugiere que Goal Mode es un caso de gobernanza incompleta: alguien delegó sin construir la estructura de esa delegación, y eso podría corregirse construyendo el arnés que falta.

Juntos revelan algo que ninguno dice: Goal Mode no es el extremo permisivo del espectro de `arnes-del-agente` — está fuera del espacio que ese espectro describe. Un arnés "permisivo" en los términos de `arnes-del-agente` sigue siendo una decisión de diseño tomada en un punto de confirmación disponible (decidir no confirmar). En Goal Mode no hay ese punto disponible para decidir nada: la arquitectura de 300 sub-agentes en 4,000 pasos no expone ningún momento intermedio donde "confirmar" o "no confirmar" sea una operación posible, ni para el arnés ni para el humano. La ausencia de arnés que `el-agente-que-no-para` observa empíricamente no es un déficit de esfuerzo de diseño (algo que "no se construyó todavía") — es la consecuencia necesaria de que el marco conceptual de `arnes-del-agente`, tal como está formulado, no tiene superficie de inserción en una arquitectura sin turnos.

La implicación de diseño: para agentes de larga duración, la pregunta correcta no es "¿cómo calibramos el arnés existente hacia más o menos confirmación?" sino "¿qué reemplaza al concepto de 'punto de confirmación' cuando la ejecución es atómica desde la perspectiva del humano?" — una pregunta que ninguno de los dos conceptos, por separado, llega a formular.

## El límite

La tensión es específica a arquitecturas verdaderamente continuas y de largo horizonte (Goal Mode, ejecución de días, cientos de sub-agentes) — no aplica al modelo conversacional turno-a-turno donde cada mensaje sí es, como reconoce el propio `el-agente-que-no-para`, "un checkpoint implícito". Ahí el marco de las cuatro preguntas de `arnes-del-agente` sigue siendo aplicable sin ajuste.

Tampoco implica que Goal Mode sea indiseñable: `el-agente-que-no-para` describe "Claw Groups" como un mecanismo parcial de loop-in humano, lo que demuestra que sí es posible insertar puntos de intervención en una arquitectura continua — pero por decisión explícita del agente, no como una propiedad estructural disponible al diseñador de la forma en que `arnes-del-agente` la asume. El argumento no es que el arnés sea imposible en Goal Mode, sino que el vocabulario de diseño de `arnes-del-agente` (calibración continua sobre un espectro de confirmación) no es el vocabulario correcto para describir cómo se construiría.

---

## Descartados y razón

- `identidad-criptografica-como-arnes` × `representacion-agente` — síntesis ya explícita en el cuerpo de `identidad-criptografica-como-arnes`: "La identidad criptográfica no reemplaza al arnés de comportamiento — es la infraestructura que hace posible auditar si el arnés se respetó... resuelve solo la capa de identidad y autorización, no resuelve automáticamente la capa de confianza."
- `impuesto-de-verificacion` × `paradoja-de-la-confianza-y-adopcion` — `paradoja-de-la-confianza-y-adopcion` ya se autodiferencia explícitamente: "El vault ya tiene comprehension-debt... e impuesto-de-verificacion... pero ambos describen consecuencias del uso. La paradoja describe el mecanismo que genera desconfianza activa..."
- `poblaciones-sinteticas` × `sycophancy-como-riesgo-de-diseno` — síntesis ya resuelta y con dato citado en el propio cuerpo de `poblaciones-sinteticas`: "La sycophancy estructural de los LLMs... se amplifica en poblaciones sintéticas: si un usuario individual tiende a validar, una población de usuarios valida con más consistencia aún" (cita NN/g 2025 incluida).
- `gobernanza-ia-performativa` × `riesgo-geopolitico-del-modelo` — `riesgo-geopolitico-del-modelo` ya declara la conexión completa: "Conecta directamente con gobernanza-ia-performativa: la capa visible del contrato... existe; la capa que realmente opera incluye actores con autoridad para suspenderlo unilateralmente."
- `ingenieria-agentica` × `spec-driven-development` — `ingenieria-agentica` ya resuelve la relación como extensión: "extiende spec-driven-development: la spec ya no precede al agente como criterio de done — es el único artefacto que el humano produce."
- `limite-de-las-jaulas-digitales` × `llm-como-motor-de-plausibilidad` — relación de corolario ya declarada explícitamente en ambas direcciones: `limite-de-las-jaulas-digitales` se autodefine como "el corolario de diseño de llm-como-motor-de-plausibilidad"; `llm-como-motor-de-plausibilidad` cita de vuelta "arneses simbólicos deterministas... (ver limite-de-las-jaulas-digitales)".
- `arquitectura-de-inteligencia` × `colonizar-el-manana-con-hoy` — `colonizar-el-manana-con-hoy` trae una sección literal "**Tensión con `arquitectura-de-inteligencia`:**" con la resolución completa ya escrita.
- `automatizacion-vs-ampliacion` × `impuesto-de-verificacion` — `impuesto-de-verificacion` ya resuelve la relación: "Esto invierte la promesa de automatizacion-vs-ampliacion: la IA no automatiza ni amplifica — crea un tercer modo..."
- `ia-sin-ecosistema` × `marea-creciente-de-automatizacion` — `marea-creciente-de-automatizacion` lo declara literalmente: "Esto es exactamente el argumento de `ia-sin-ecosistema`."
- `supuestos-importados-por-ia` × `sycophancy-como-riesgo-de-diseno` — aunque la mención aparece solo en "Ejes investigados" (no en el cuerpo narrativo), la propia sección "Tensiones y límites" de `supuestos-importados-por-ia` ya nombra el mecanismo exacto sin necesitar el nombre del otro concepto: "parte del comportamiento de cualquier modelo está determinado por el entrenamiento — RLHF, datos de ajuste, refuerzos implícitos — y esos supuestos no están documentados en ningún lugar accesible" — y el eje investigado cierra el vínculo citando a `sycophancy-como-riesgo-de-diseno` por nombre como el ejemplo específico. La síntesis (RLHF como supuesto filosófico no legible ni gobernable) ya está completa y explícitamente enlazada.
- `agente-como-carpeta` × `spec-driven-development` — `agente-como-carpeta` ya declara la relación como analogía resuelta, no tensión: "Esto tiene el mismo efecto democratizador que ya documentaste en `vibe-coding` y `spec-driven-development`, pero aplicado específicamente a la construcción de agentes." Co-ocurrencia declarada, no contradicción — título reducible a "[A] y [B]" sin pérdida.
- `agente-que-escapa-obedeciendo` × `gobernanza-ia-performativa` — `agente-que-escapa-obedeciendo` se autodiferencia explícitamente de `gobernanza-ia-performativa` en su propio cuerpo: "Este concepto captura algo más específico: la obediencia literal como vector de fuga..."
- `arquitectura-de-confianza` × `paradoja-de-la-confianza-y-adopcion` — sección literal "**Tensión con arquitectura-de-confianza:**" en `paradoja-de-la-confianza-y-adopcion` con la resolución completa ya escrita.
- `autoautomatizacion-del-disenador` × `juicio-como-trabajo-completo` — sección literal "Tensión con juicio-como-trabajo-completo:" en `autoautomatizacion-del-disenador`, ya resuelta: "La autoautomatización del diseñador es el mecanismo individual complementario."
- `automatizar-mi-propio-trabajo` × `presencia-como-condicion-del-valor` — sección literal "**Tensión con `automatizar-mi-propio-trabajo`:**" en `presencia-como-condicion-del-valor`, ya resuelta.
- `confianza-a-traves-de-velocidad` × `presencia-como-condicion-del-valor` — mismo archivo, sección literal "**Tensión con `confianza-a-traves-de-velocidad`:**", ya resuelta.
- `cultura-de-tinkering` × `presencia-como-condicion-del-valor` — mismo archivo, sección literal "**Tensión con `cultura-de-tinkering`:**", ya resuelta.
- `diseno-dos-velocidades` × `sistema-de-mentalidades-futuras` — sección literal "**Tensión con `diseno-dos-velocidades`:**" en `sistema-de-mentalidades-futuras`, ya resuelta.
- `engano-emergente-en-agentes-autonomos` × `gobernanza-ia-performativa` — `engano-emergente-en-agentes-autonomos` ya resuelve la distinción: "La `gobernanza-ia-performativa` actúa sobre capacidades declaradas — esta clase de riesgo opera en la capa de intención encubierta que esa gobernanza no alcanza."

---

_Propuestas generadas automáticamente por Jarvis. Requieren revisión y aprobación de Luigui antes de escribir en `Correlaciones/`._
_Para aprobar: `Jarvis, revisa propuestas pendientes`_
_Nota: siguen pendientes de revisión, sin tocar en esta corrida: `Inbox/2026-08-25_0811_correlaciones-propuestas.tmp.md` (3), `Inbox/2026-08-31_1122_correlaciones-propuestas.tmp.md` (2), `Inbox/2026-09-07_1117_correlaciones-propuestas.tmp.md` (1)._
