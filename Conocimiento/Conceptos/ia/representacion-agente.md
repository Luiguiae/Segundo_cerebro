---
titulo: "Representación agente"
tipo: concepto
fecha: 2026-06-13
familia: agencia-ia
categorias_secundarias: [diseno]
tags: [agentes, ia, etica, control, diseño]
estado: activo
relacionado: [arnes-del-agente, espectro-autonomia-agente, agencia-humana-como-imperativo-ux]
fuentes:
  - titulo: "Sequoia Ascent 2026 summary — Andrej Karpathy"
    url: "https://karpathy.bearblog.dev/sequoia-ascent-2026/"
    fecha_acceso: 2026-06-13
  - titulo: "AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A"
    url: "https://arxiv.org/abs/2603.24775"
    fecha_acceso: 2026-06-13
  - titulo: "Mimetic Alignment with ASPECT: Evaluation of AI-inferred Personal Profiles"
    url: "https://arxiv.org/abs/2603.26922"
    fecha_acceso: 2026-06-13
  - titulo: "Interoperable Architecture for Digital Identity Delegation for AI Agents"
    url: "https://arxiv.org/abs/2601.14982"
    fecha_acceso: 2026-06-13
  - titulo: "AI and My Values: User Perceptions of LLMs' Ability to Extract and Embody Human Values"
    url: "https://arxiv.org/pdf/2601.22440"
    fecha_acceso: 2026-06-13
---

# Representación agente

## El concepto

Cuando un agente actúa en nombre de una persona ante otros agentes — negocia, decide, se compromete — el problema de diseño se bifurca en dos capas que los sistemas actuales no distinguen. La primera es técnica: ¿es este agente quien dice ser? ¿Qué puede hacer? ¿Con qué alcance opera? Los protocolos que emergieron en 2025-2026 (A2A, AIP, Delegation Grants) resuelven esta capa con criptografía, tokens verificables y scope attenuation. La segunda es de representación: ¿a quién representa este agente y con qué fidelidad? Esa capa no tiene aún su artefacto de diseño formalizado.

La diferencia es estructural. El `arnes-del-agente` es un contrato de capacidades: define el espacio de acción del agente, sus herramientas, permisos y guardrails. La representación agente requiere algo distinto — un contrato de identidad: codificar quién es el principal humano con suficiente fidelidad para que el agente actúe en su nombre en situaciones que ese humano no anticipó, ante agentes de otras personas que igualmente operan sin supervisión en tiempo real. Karpathy lo formuló en Sequoia Ascent 2026: "people and organizations will have agent representation — my agent will talk to your agent." El problema no es la técnica de la interacción; es qué lleva el agente de tu parte cuando habla.

El Agent Card de A2A — el artefacto que representa a un agente frente a otros — contiene: nombre, versión, endpoints, skills, modos de input/output, autenticación. No contiene: los valores del humano en un contexto de negociación, su estilo de comunicación, su jerarquía de prioridades ante trade-offs imprevistos, o sus límites no delegables. Un agente puede ser criptográficamente verificable como "el agente de X" sin saber qué habría elegido X cuando los parámetros de la negociación cambiaron a mitad del proceso.

## Por qué importa

El vault tiene `arnes-del-agente` como artefacto central del diseño agéntico y `espectro-autonomia-agente` para diseñar el nivel de autonomía. Pero ninguno resuelve el modo representación: cuando el agente opera en nombre del humano ante otros agentes, la pregunta ya no es "¿qué puede hacer?" ni "¿cuánta autonomía tiene?". Es "¿a quién representa y con qué fidelidad?".

Las consecuencias son asimétricas respecto a los errores del arnés. Un arnés mal diseñado ejecuta acciones incorrectas a velocidad de máquina — el daño es visible, técnico, corregible. Un contrato de identidad ausente produce algo más difícil de detectar: el agente actúa "en tu nombre" con valores promediados, con estilo de negociación genérico, con límites que nunca elegiste. El resultado no es un error técnico — es una representación inauténtica que genera compromisos que no son tuyos, en sistemas donde el humano no estaba presente para corregirlos.

La escalabilidad agrava el problema. Cuando tu agente negocia con cien agentes simultáneamente — cada uno representando a otra persona — la falta de un contrato de identidad no es un gap de diseño en un flujo: es la condición base de un sistema que opera sin identidad de sus principales.

## Datos y evidencia

- **A2A Protocol v0.3.0** (Google, 2026): el Agent Card incluye skills, capabilities, endpoints y autenticación. No existe campo para valores del principal ni estilo de negociación. La especificación es intencional sobre identidad técnica, silenciosa sobre identidad de representación.

- **AIP: Agent Identity Protocol** (arXiv 2603.24775, Sunil Prakash, marzo 2026): scan de ~2,000 servidores MCP — todos sin autenticación. AIP introduce Invocation-Bound Capability Tokens (IBCTs) para resolver identidad y delegación verificable. Resuelve autenticación, scope attenuation, cadena de delegación. No resuelve quién es el humano detrás del token ni qué valores porta.

- **Delegation Grants** (arXiv 2601.14982, enero 2026): framework para transferencia de autoridad con scope reduction — cada paso de delegación reduce el conjunto de acciones permitidas (monotone attenuation). La identidad codificada es de alcance (scope), no de valores.

- **ASPECT** (Microsoft Research, arXiv 2603.26922, Ruoxi Shang et al., marzo 2026): pipeline que infiere perfiles de comunicación personal sin entrenamiento per-persona. En estudio con 20 participantes, 1,840 evaluaciones pareadas y 600 evaluaciones de escenario: alineación moderada con autoevaluaciones, preferido sobre baseline genérico en agregado, pero con **variación sustancial entre individuos y escenarios**. Primer intento verificado de construir perfiles individuales de representación — con la limitación de que opera sobre comportamiento observable pasado, no sobre valores declarados o jerarquías de prioridad ante escenarios nuevos.

- **AI and My Values** (arXiv 2601.22440, 2026): **85%** de participantes expresaron preocupación por que organizaciones creen perfiles de valores sin su conocimiento. El estudio distingue tres capas distintas de representación: style (cómo comunica), preference alignment (qué output prefiere) y values alignment (qué principios guían decisiones en trade-offs). Los enfoques RLHF actuales promedian colectivamente, marginalizando diferencias individuales.

## Tensiones y límites

La tensión central: codificar la identidad de una persona con suficiente fidelidad para representarla requiere o bien datos masivos de comportamiento observable — con el riesgo de que el perfil sea un promedio de comportamientos pasados, no de valores futuros — o bien declaración explícita de valores por parte del humano, que introduce el problema inverso: nadie declara sus valores con la granularidad necesaria para anticipar todos los trade-offs. ASPECT (2026) demuestra que la inferencia automatizada alcanza alineación moderada pero con variación sustancial entre personas — suficiente para tareas de estilo, insuficiente para trade-offs de valores en negociaciones de alta consecuencia.

La segunda tensión: quién controla el contrato de identidad. Si lo controla el proveedor del agente, el humano delega su representación a quien tiene interés comercial en el resultado. Si lo controla el humano, hay que resolver el mantenimiento: los valores y prioridades cambian; el contrato codificado hace seis meses puede no reflejar quién eres hoy. Esta tensión conecta directamente con `agencia-humana-como-imperativo-ux`: preservar la agencia del humano sobre su propia representación es el nuevo imperativo, no solo sobre sus acciones directas.

No aplica en escenarios de ejecución pura (automatización de tareas predefinidas sin negociación) o donde los compromisos son completamente reversibles. El problema de representación es más agudo donde los compromisos son irreversibles y el humano no estará presente para corregirlos.

## Ejes investigados

**Eje 1 — Protocolos actuales de identidad técnica de agentes (gap de representación):** A2A v0.3.0, AIP (arXiv 2603.24775), Delegation Grants (arXiv 2601.14982). Los tres resuelven la capa técnica con solidez creciente. Ninguno aborda la capa de representación de valores del principal. Hallazgo clave: el Agent Card de A2A, siendo el artefacto de "identidad" más estandarizado del ecosistema, no tiene campo para valores ni preferencias. 3 fuentes técnicas primarias.

**Eje 2 — Codificación de valores/preferencias personales en agentes:** ASPECT (Microsoft Research, arXiv 2603.26922) y "AI and My Values" (arXiv 2601.22440). ASPECT es el trabajo empírico más concreto: infiere perfiles de comunicación individual usando LLMs sobre datos observados. Resultado: alineación moderada, variación sustancial. Identifica style / preference / values como tres capas distintas. El gap: RLHF promedia colectivamente; perfiles individuales requieren datos que la mayoría no tiene estructurados. 2 fuentes académicas con datos empíricos.

**Eje 3 — Negociación agente-a-agente y fidelidad de representación:** Trabajos sobre negociación LLM-a-LLM y arquitecturas de delegation chains verificables. Los agentes pueden imitar estilo humano y ser percibidos como más razonables. Pero imitar el estilo no es representar los valores: la distinción entre "negociar como X" (imitar patrones) y "negociar por X" (defender sus prioridades en trade-offs imprevistos) no está resuelta en ningún sistema actual. 2 fuentes con casos de negociación documentados.
