# Candidatos de concepto — Transcript Taller 2026-09-02

> Extraídos de `Inbox/2026-09-02_1005_modo-taller_transcript.tmp.md`.
> Sin evaluación de rúbrica. Sin instalación en vault. Solo candidatos crudos.

---

## Agente como emulador de segmento

Un agente de IA construido para responder como lo haría un cliente de un segmento específico — no como un bot genérico, sino como una persona con perfil demográfico, historia financiera y comportamiento de uso conocido. La idea central es que el agente "es" el cliente, no que habla sobre él.

> "básicamente es un agente que funciona para emular respuestas... lo que queremos en estos ejercicios evaluar al momento de entrevistar a una persona como lo haría" — 10:08:45 / 10:09:21

---

## Triangulación de datos para construir un usuario sintético

Práctica de combinar tres capas de datos — cualitativa (entrevistas), cuantitativa (encuestas) y datos de uso real — para construir una persona sintética con mayor fidelidad que la que daría cualquiera de las tres fuentes por separado. La triangulación es lo que distingue al usuario sintético de un personaje ficticio.

> "combine con 25 segmentos ahorita ya tenemos la cualitativa cuantitativa y datos que usa la gente" — 10:09:02

---

## "¿Se sintió real?" como criterio de evaluación

Usar la percepción subjetiva de verosimilitud — no la precisión técnica ni la cobertura de datos — como métrica primaria de calidad de un usuario sintético. Si el evaluador no puede distinguir si habló con un humano o un agente, el agente pasó. Es una forma de Turing test aplicada a investigación de usuarios.

> "voy a andar feedback de esto se sintió real" — 10:10:41

---

## Homogeneización de respuestas entre segmentos distintos

Cuando usuarios sintéticos de diferentes segmentos empiezan a dar respuestas parecidas, es una señal de que el modelo no está diferenciando suficientemente los perfiles — está colapsando hacia respuestas promedio o genéricas. La homogeneización es un síntoma de subentrenamiento o de datos de segmento insuficientemente distintos.

> "las las respuestas de cada uno son parecidos porque... digital" — 10:22:38

---

## Doble caso de uso de los usuarios sintéticos

Los usuarios sintéticos sirven para dos propósitos distintos que se usan en momentos distintos del proceso: (1) entrenamiento de equipos en técnicas de entrevista antes de salir al campo, y (2) afinación de propuestas comerciales antes de presentarlas a clientes reales. Son el mismo artefacto con dos contextos de activación diferentes.

> "los dos casos de uso son como entrenamiento o previo... afinando tu propuesta antes de ir a la" — 10:31:11 / 10:31:33

---

## Ruptura de personaje ante meta-preguntas

El usuario sintético falla — sale del personaje — cuando se le pregunta sobre cómo fue construido o cómo funciona el sistema. Es una fragilidad estructural: el agente puede sostener el rol de "cliente" pero no puede responder preguntas sobre su propia arquitectura sin revelar que es un modelo. La línea que rompe el personaje es la meta-pregunta.

> "oye cómo se construye este flujo así... responde como que ya no el modelo... cómo se tiene arma este flujo de compensación" — 10:33:24 / 10:33:41
