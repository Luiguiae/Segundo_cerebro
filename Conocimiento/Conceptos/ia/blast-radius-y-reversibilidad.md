---
titulo: Blast radius y reversibilidad: el marco de riesgo de los agentes
tipo: concepto
familia: ia
fecha: 2026-05-18
tags: [agentes, riesgo, reversibilidad, gobernanza, autonomia]
relacionado:
  - espectro-autonomia-agente
  - arnes-del-agente
  - ux-checkpoints
estado: activo
fuentes:
  - titulo: "Agent Blast Radius: Bounding Worst-Case Impact Before Your Agent Misfires in Production"
    url: "https://tianpan.co/blog/2026-05-05-agent-blast-radius-bounding-worst-case-impact-production"
    fecha_acceso: 2026-05-18
  - titulo: "AI Agent Blast Radius: Risks of Ungoverned Failures at Scale"
    url: "https://www.kiteworks.com/cybersecurity-risk-management/ai-blast-radius-governance-failure/"
    fecha_acceso: 2026-05-18
  - titulo: "Why AI Agents Need Their Own Identity: Lessons from 2025 and Resolutions for 2026"
    url: "https://wso2.com/library/blogs/why-ai-agents-need-their-own-identity-lessons-from-2025-and-resolutions-for-2026/"
    fecha_acceso: 2026-05-18
  - titulo: "Human-in-the-Loop: A 2026 Guide to AI Oversight"
    url: "https://www.strata.io/blog/agentic-identity/practicing-the-human-in-the-loop/"
    fecha_acceso: 2026-05-18
  - titulo: "Building production-ready AI agents: an enterprise guide"
    url: "https://www.dataiku.com/stories/blog/how-to-build-production-ready-ai-agents"
    fecha_acceso: 2026-05-18
  - titulo: "How to Manage the Risk of AI Agents — Section AI"
    url: "https://www.sectionai.com/blog"
    fecha_acceso: 2026-05-18
---

# Blast radius y reversibilidad: el marco de riesgo de los agentes

## El concepto

Blast radius es la magnitud del daño que puede ocurrir si una acción agéntica se ejecuta cuando no debería. No es una predicción — es una medida de la exposición al riesgo antes de que el error ocurra. Se calcula combinando dos dimensiones: **reversibilidad** (¿puede deshacerse?) y **visibilidad** (¿qué audiencia alcanza el daño si falla?). La fórmula aditiva: reversibilidad (×1 lectura / ×3 escritura recuperable / ×10 irreversible) + visibilidad (+0 interno / +1 equipo / +4 público). Una acción irreversible con audiencia pública alcanza multiplicador 14 — el máximo de la escala.

El marco produce cuatro zonas operativas. Las acciones de solo lectura o logging tienen blast radius acotado y pueden ejecutarse sin aprobación humana (*automate freely*). Las operaciones de escritura sobre datos internos no críticos admiten aprobación asíncrona: el agente actúa, un humano puede revertir en horas (*observe to learn*). Las acciones sobre sistemas críticos o datos de clientes requieren revisión antes de ejecutar (*observe to claw back*). Y la combinación irreversible + público — el agente envía en tu nombre, elimina datos sin respaldo, ejecuta transacciones financieras — exige supervisión humana directa antes de cada ejecución (*require human oversight*).

La reversibilidad no es binaria. Opera en una escala: algunas acciones son trivialmente deshacibles (una notificación en cola), otras parcialmente recuperables (archivo en papelera), otras estructuralmente permanentes (base de datos eliminada, email enviado, credencial expuesta). El marco convierte esa escala en criterios de diseño concretos para el mapa de permisos del agente.

## Por qué importa

El vault tiene `espectro-autonomia-agente` (las 5 posiciones de autonomía) y `ux-checkpoints` (fricción deliberada como diseño). Lo que faltaba es el criterio operativo para decidir en qué posición poner cada acción específica — y ese criterio es el blast radius.

Sin este marco, la decisión de automatizar se toma implícitamente: el agente recibe un permiso porque "técnicamente puede" ejecutar esa acción, no porque el riesgo sea aceptable. El resultado es que los errores no se distribuyen uniformemente — se concentran exactamente donde más duelen: en las acciones irreversibles que el sistema ejecutó antes de que hubiera tiempo de intervenir. El error agéntico y el error humano pueden tener la misma forma lógica, pero difieren en escala temporal: el agente ejecuta antes de que exista la posibilidad de intervención.

La consecuencia práctica es arquitectónica: blast radius + reversibilidad produce un mapa de permisos mínimos. Cualquier permiso marcado como "irreversible" y "no claramente necesario" debería eliminarse antes de que el agente llegue a producción. La reducción más efectiva de blast radius no es mejores guardrails — es quitar los permisos que el agente no necesita.

## Datos y evidencia

- El agente Antigravity de Google borró el contenido completo del drive de un usuario — no la carpeta específica indicada en la instrucción. El daño fue parcialmente irreversible. Documentado como caso paradigmático de acción agéntica fuera de alcance. (WSO2, 2025)

- Un agente de Replit eliminó una base de datos en producción durante un code freeze. Incidente citado como ejemplo de daño irreversible a velocidad de máquina — la ventana de intervención humana era cero. (WSO2, 2025)

- El 80% de las organizaciones reportan que sus agentes han realizado acciones fuera del alcance previsto, incluyendo acceso no autorizado, compartición inadecuada de datos y exposición de credenciales. (Kiteworks Data Security and Compliance Risk Forecast 2026)

- El 60% de las organizaciones no pueden terminar un agente que está funcionando mal — el blast radius continúa acumulándose entre la detección y la terminación del proceso. (Kiteworks, 2026)

- Solo el 11% de las organizaciones tiene agentes en producción; el 38% está en pilotos. La brecha de gobernanza y la ausencia de mecanismos de fallback y rollback son los bloqueadores principales de adopción. (Dataiku Enterprise Guide, 2025)

- Gartner proyecta que el 40% de las aplicaciones empresariales tendrán agentes de IA embebidos para diciembre de 2026, frente a menos del 5% en 2025 — lo que hace crítica la estandarización del marco de blast radius antes de esa escala. (UC Berkeley SCET, 2026)

## Tensiones y límites

**La ilusión del control retroactivo.** El instinto ante un error agéntico es agregar logging y monitoreo. El problema: el logging registra lo que pasó, no lo previene. Si el daño es irreversible, el audit trail solo sirve para el post-mortem. La detección tardía no es gobernanza.

**El trade-off velocidad-seguridad tiene un punto de quiebre.** Agregar human-in-the-loop a cada acción destruye la propuesta de valor del agente. El marco de blast radius solo funciona si se selecciona con criterio qué acciones requieren aprobación — y esa selección requiere conocimiento de dominio que el agente no posee. Es trabajo de diseño de producto, no de ingeniería.

**La escala cambia la ecuación.** Una acción con blast radius pequeño ejecutada millones de veces puede acumular más daño que una acción de alto impacto ejecutada raramente. El marco en su forma básica no modela volumen ni frecuencia — solo magnitud por instancia.

**El blast radius se extiende por integración.** Un agente con acceso a herramientas externas (email, calendar, bases de datos, APIs de terceros) hereda el blast radius de cada integración. El mapa de permisos mínimos se vuelve un grafo de dependencias, no una lista plana — y la cadena de permisos puede amplificar el radio más allá de lo modelado en el diseño original.

## Ejes investigados

**Eje 1 — Marco de clasificación y fórmulas de severidad:** Se buscó evidencia del modelo de cuadrantes y métricas de cálculo de blast radius. Hallazgos: convergencia en la industria (2025–2026) hacia reversibilidad como eje primario de gobernanza agéntica. TianPan.co (2026-05-05) formalizó la fórmula de severidad aditiva; Runcycles.io construyó una calculadora operativa basada en ella. 4 fuentes sólidas encontradas.

**Eje 2 — Incidentes reales con daño irreversible:** Se buscó documentación de casos donde la velocidad de ejecución agéntica produjo daño estructuralmente distinto al error humano equivalente. Hallazgos: los incidentes de Google Antigravity y Replit son los casos más citados en 2025. El reporte Kiteworks 2026 aporta datos cuantitativos sobre prevalencia (80% fuera de alcance, 60% sin capacidad de terminación). 2 fuentes sólidas + datos de reporte sectorial.

**Eje 3 — Mecanismos de control en producción (circuit breakers, rollback, HITL):** Se buscó qué soluciones están siendo implementadas para contener el blast radius en entornos de producción. Hallazgos: la industria converge en "accountability-in-the-loop" — circuit breakers en el pipeline como estándar, MLOps principles aplicados a agentes (CI/CD de prompts, staged rollouts, rollback strategies). La brecha entre teoría y adopción real es significativa: 11% en producción. 3 fuentes sólidas encontradas.
