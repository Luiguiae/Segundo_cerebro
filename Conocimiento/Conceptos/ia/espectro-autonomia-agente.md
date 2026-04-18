---
titulo: espectro-autonomia-agente
tipo: concepto
familia: agencia-ia
categoria: ia
fecha: 2026-04-18
tags: [ia, agentes, roles, criterio, poder]
relacionado: [agentes-ia, gobernanza-ia-performativa, quien-controla-el-prompt]
estado: activo
fuentes:
  - titulo: "Levels of Autonomy for AI Agents – arXiv 2506.12469 (Feng, McDonald, Zhang – U. Washington)"
    url: "https://arxiv.org/abs/2506.12469"
    fecha_acceso: 2026-04-18
  - titulo: "Levels of Autonomy for AI Agents – Knight First Amendment Institute"
    url: "https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1"
    fecha_acceso: 2026-04-18
  - titulo: "Human-in-the-Loop: A 2026 Guide to AI Oversight"
    url: "https://www.strata.io/blog/agentic-identity/practicing-the-human-in-the-loop/"
    fecha_acceso: 2026-04-18
  - titulo: "Measuring AI agent autonomy in practice – Anthropic Research"
    url: "https://www.anthropic.com/research/measuring-agent-autonomy"
    fecha_acceso: 2026-04-18
  - titulo: "Human-in-the-Loop AI: Systematic Review – MDPI Entropy"
    url: "https://www.mdpi.com/1099-4300/28/4/377"
    fecha_acceso: 2026-04-18
---

# Espectro de autonomía del agente

## El concepto
"Human in the loop" es una trampa conceptual binaria: sugiere que existe solo un modo
de intervención humana — estar adentro o afuera del ciclo. El paper "Levels of Autonomy
for AI Agents" (Feng, McDonald, Zhang — University of Washington / Knight First
Amendment Institute, 2025) define cinco posiciones distintas que un humano puede ocupar:

1. **Operador** — diseña el sistema, define los objetivos y las restricciones
2. **Colaborador** — trabaja junto al agente en tiempo real, toma decisiones conjuntas
3. **Consultor** — responde preguntas del agente cuando este las solicita
4. **Aprobador** — revisa y autoriza antes de que el agente ejecute
5. **Observador** — solo vigila métricas y puede intervenir post-facto

Cada posición implica consecuencias radicalmente distintas para el control, la
responsabilidad y la calidad del output. La autonomía del agente no es una consecuencia
de su capacidad técnica — es una decisión de diseño deliberada.

## Por qué importa
La posición que un humano ocupa respecto a un agente determina qué trabajo todavía
es del humano. Un equipo que se posiciona como *observador* mientras cree que se
posiciona como *operador* está cediendo control sin saberlo — exactamente el patrón
que `gobernanza-ia-performativa` documenta a nivel organizacional.

La decisión de posicionamiento en el espectro no es técnica. Es una decisión de
diseño con consecuencias para la responsabilidad legal, la calidad del output, y la
capacidad del humano de intervenir cuando el agente se equivoca.

## Datos y evidencia

**El paper: autonomía como diseño, no como capacidad.**
Feng, McDonald y Zhang (arXiv 2506.12469) argumentan que la autonomía del agente puede
tratarse como una variable de diseño independiente de su capacidad. Un agente altamente
capaz puede configurarse para pedir confirmación constantemente; un agente menos capaz
puede correr completamente autónomo en tareas simples y de bajo riesgo. El nivel de
autonomía correcto no es el máximo técnicamente posible — es el adecuado para el
riesgo y el contexto.

Esto invierte la narrativa dominante de que "más IA = más autonomía = mejor". La
pregunta correcta es: ¿qué posición en el espectro produce el output de mayor calidad
para este problema específico?

**HITL vs. HOTL vs. HAOL.**
La literatura de supervisión identifica tres paradigmas distintos:
- **Human-in-the-loop (HITL)**: el humano aprueba antes de que el agente ejecute
- **Human-on-the-loop (HOTL)**: el agente actúa autónomamente; el humano puede
  intervenir después
- **Human-out-of-the-loop**: el agente opera sin supervisión en tiempo real

La regulación (EU AI Act, EASA para aviación) está empujando hacia HITL o HOTL para
sistemas de alto riesgo, con documentación explícita de qué posición ocupa el humano
y qué acciones puede tomar. La interacción granular varía: coarse-grained (humano
aprueba o rechaza outputs a nivel de batch) vs. fine-grained (humano interviene en
cada decisión del agente).

**La trampa del observador performativo.**
Anthropic Research (2026) documenta que la métrica más fácil de manipular en
sistemas agénticos es la "supervisión humana" — equipos reportan que tienen humanos
"en el loop" cuando en realidad están en posición de observador sin capacidad real
de intervención. El indicador: ¿cuánto tiempo tiene el humano para revisar antes de
que el agente ejecute? Si la ventana de veto es menor al tiempo necesario para
comprender el output, el "aprobador" es un observador con interfaz de aprobador.

## Tensiones y límites
Tensiona con la narrativa de velocidad: posicionarse como colaborador o aprobador
en lugar de observador reduce la velocidad de ejecución del agente. La heurística
emergente de la investigación es que el nivel de autonomía correcto es función del
riesgo — no de la conveniencia o la velocidad.

Tensiona con `quien-controla-el-prompt`: el espectro agrega una dimensión que
quien-controla-el-prompt no captura. El control del prompt es una forma de ser
operador, pero la posición en el espectro también define qué pasa después del
prompt — quién aprueba, quién puede vetar, quién solo observa.

No aplica uniformemente dentro del mismo sistema: el mismo agente puede requerir
posiciones distintas para distintas categorías de decisión. Un equipo puede ser
colaborador para decisiones de arquitectura y observador para decisiones de
implementación — y el diseño del sistema debe hacer esas posiciones explícitas.

## Ejes investigados
- **Eje 1:** arXiv 2506.12469 — framework de 5 niveles, autonomía como decisión de diseño
- **Eje 2:** HITL vs. HOTL — taxonomías de supervisión humana, MDPI Entropy, Strata.io
- **Eje 3:** Supervisión performativa vs. real — Anthropic Research, EU AI Act
