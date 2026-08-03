---
titulo: Cuando el rechazo del modelo es la vulnerabilidad
tipo: concepto
familia: ia
tags: [alineacion, guardrails, seguridad, over-refusal, asimetria]
relacionado: [impuesto-de-alineacion, ia-sin-ecosistema, riesgo-geopolitico-del-modelo]
fecha: 2026-08-03
estado: activo
fuentes:
  - titulo: "Defensive Refusal Bias: How Safety Alignment Fails Cyber Defenders"
    url: "https://arxiv.org/abs/2603.01246"
    fecha_acceso: 2026-08-03
  - titulo: "OR-Bench: An Over-Refusal Benchmark for Large Language Models (ICML 2025)"
    url: "https://proceedings.mlr.press/v267/cui25a.html"
    fecha_acceso: 2026-08-03
  - titulo: "What we did when Claude Fable 5 and GPT-5.6 Sol refused our security requests"
    url: "https://charonhub.deeplearning.ai/open-models-open-harnesses-open-security/"
    fecha_acceso: 2026-08-03
  - titulo: "Opus Outshines Even Fable, Inside the Hugging Face Hack — The Batch Issue 364"
    url: "https://www.deeplearning.ai/the-batch/issue-364"
    fecha_acceso: 2026-08-03
  - titulo: "The Asymmetric Vulnerability: Bypassing LLM Defenses via Guardrail-Model Mismatch (ACM Web 2026)"
    url: "https://doi.org/10.1145/3774904.3792438"
    fecha_acceso: 2026-08-03
---

# Cuando el rechazo del modelo es la vulnerabilidad

## El concepto

Los modelos de lenguaje de frontera —los más seguros, los más alineados, los más costosos— rechazan con frecuencia tareas legítimas de auditoría de seguridad, análisis de malware y revisión de vulnerabilidades. No porque el usuario sea un atacante, sino porque el clasificador de alineación detecta palabras clave asociadas a comportamiento ofensivo y bloquea la solicitud sin razonar sobre la intención ni el contexto de autorización.

El resultado es estructuralmente paradójico: quien firma los términos de servicio, trabaja dentro de los límites de la API y tiene acceso autorizado —el defensor legítimo— queda bloqueado. Quien no necesita modelos alineados porque construye sus propias herramientas o usa modelos abiertos sin restricciones —el atacante— no enfrenta esa fricción. El rechazo no es neutral: cae asimétricamente sobre la parte que más lo paga.

Esta asimetría convierte el rechazo en sí mismo en una vulnerabilidad. Si un defensor sabe que el modelo le bloqueará una solicitud de análisis de malware, su flujo de trabajo queda degradado. Si un atacante sabe que puede neutralizar el modelo forense del defensor mediante prompt injection que le ordene "declarar el archivo benigno", la barrera de protección colapsa desde adentro.

## Por qué importa

Andrew Ng documentó el caso directamente en julio de 2026: su equipo intentó usar Claude Code (Fable 5) y Codex (GPT-5.6 Sol) para auditar la seguridad de OpenWorker, su propio proyecto de código abierto. Ambos modelos se negaron —uno se detuvo a mitad del análisis, el otro pidió degradar a un modelo menos capaz. Tuvieron que cambiar a modelos abiertos (Kimi K3, GLM 5.2) para completar la revisión. Su conclusión: "No puedo pensar en ningún beneficio de seguridad en negarse a ayudarnos a encontrar problemas de seguridad en nuestro propio código. Si existen vulnerabilidades, es mejor que las encontremos nosotros antes que un adversario."

La semana anterior, el equipo de seguridad de Hugging Face no pudo usar Claude para analizar los logs de su propio hackeo —fue bloqueado— y tuvo que recurrir a GLM 5.2 en infraestructura propia para reconstruir la intrusión. El patrón es el mismo en ambos casos: el modelo más seguro bloqueó al defensor. El modelo menos restringido desbloqueó la tarea. El costo de la sobre-cautela no lo paga el atacante —lo paga quien sigue las reglas.

## Datos y evidencia

- **2.72×** — tasa de rechazo de solicitudes defensivas legítimas frente a solicitudes semánticamente equivalentes con vocabulario neutral. Medida sobre 2,390 ejemplos reales de la National Collegiate Cyber Defense Competition (NCCDC). Las tareas con mayor tasa de rechazo: endurecimiento de sistemas (43.8%) y análisis de malware (34.3%). Fuente: "Defensive Refusal Bias: How Safety Alignment Fails Cyber Defenders", ICLR 2026, arXiv:2603.01246 (marzo 2026).

- **Efecto inverso de la autorización** — agregar autorización explícita ("tengo autorización para realizar esta tarea") aumenta —no disminuye— la tasa de rechazo. Los modelos interpretan la justificación como señal adversarial, no como contexto exculpatorio. Fuente: mismo paper, ICLR 2026.

- **0.878** — correlación de Spearman entre la capacidad de un modelo de bloquear contenido tóxico real y su tasa de rechazo de solicitudes inocuas. Medida sobre 32 LLMs populares y 80,000 prompts. No es un bug de algunos modelos: es una propiedad sistemática del alineamiento actual. Fuente: OR-Bench, ICML 2025, proceedings.mlr.press/v267/cui25a.html.

- **Primera muestra de malware con prompt injection** documentada por Check Point Research (2025): el malware contenía instrucciones embebidas para que el modelo analizador lo declarara benigno e ignorara su tarea. El rechazo se vuelve weaponizable: el atacante puede diseñar que el modelo del defensor se sabotee a sí mismo. Fuente: Check Point Research, 2025 (vía CSO Online).

- **~60% de tasa de éxito** en ataques multi-turno documentado por Cisco Research (2025), donde los atacantes fragmentaban intención maliciosa en múltiples solicitudes aparentemente benignas. La asimetría no es de esfuerzo sino de arquitectura: el alineamiento protege el caso simple, no el adversarial persistente.

## Tensiones y límites

La asimetría no implica que los guardrails sean inútiles. Un guardrail que detiene al 80% de actores oportunistas sin sofisticación técnica tiene valor real, aunque no detenga al 20% más avanzado. El argumento de la vulnerabilidad aplica con mayor fuerza en el extremo de alta sofisticación.

El concepto tampoco implica eliminar todos los guardrails de ciberseguridad. La pregunta correcta no es "guardrails sí o no" sino "qué señales usa el clasificador". El hallazgo de ICLR 2026 indica que el clasificador actual usa similitud semántica a contenido ofensivo, no razonamiento sobre intención o autorización —y eso es corregible sin eliminar protecciones.

Hay un límite de generalización: los casos de alto perfil (Ng, Hugging Face) son representativos pero no estadísticos. Los 2,390 ejemplos de NCCDC son la evidencia más robusta porque provienen de competencias reales de defensa, no de reportes de prensa.

Finalmente: la asimetría asume que los modelos abiertos seguirán accesibles sin restricciones y que los modelos alineados seguirán siendo preferidos en entornos corporativos con cumplimiento normativo. Si la regulación fuerza controles equivalentes en modelos abiertos, la brecha podría cerrarse por el otro lado.

## Ejes investigados

**Eje 1 — Casos documentados de rechazo en tareas defensivas legítimas:**
Dos casos primarios con fuentes verificables: Andrew Ng/OpenWorker (The Batch Issue 364, 2026-07-31) y Hugging Face (Scout 2026-08-02, Issue #75). DeepLearning.ai publicó análisis complementario sobre qué ocurrió exactamente en cada modelo. Fuentes sólidas encontradas: 3.

**Eje 2 — Asimetría estructural atacante/defensor en LLMs:**
"Defensive Refusal Bias" (arXiv:2603.01246, ICLR 2026): 2,390 ejemplos reales, metodología revisada por pares. Complementado con "The Asymmetric Vulnerability" (ACM Web Conference 2026), cobertura de CSO Online, y evidencia de weaponización por Check Point Research (2025). Fuentes sólidas encontradas: 4.

**Eje 3 — Correlación sistémica seguridad/sobre-rechazo:**
OR-Bench (ICML 2025): 80,000 prompts, 32 modelos, Spearman 0.878. Muestra que la asimetría no es un bug sino consecuencia estructural del entrenamiento actual. Cisco Research (2025) aporta el dato del lado atacante. Fuentes sólidas encontradas: 2.
