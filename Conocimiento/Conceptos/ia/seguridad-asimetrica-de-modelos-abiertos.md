---
titulo: La asimetría de seguridad de los modelos abiertos
tipo: concepto
familia: ia
tags: [alineacion, ciberseguridad, modelos-abiertos, asimetria-seguridad, defensa]
relacionado: [impuesto-de-alineacion, riesgo-geopolitico-del-modelo, web-bifurcada]
fecha: 2026-08-03
estado: activo
fuentes:
  - titulo: "Chinese-Speaking Threat Actor Harnesses AI Models for Autonomous Cyberattacks"
    url: "https://unit42.paloaltonetworks.com/autonomous-ai-cyber-attack-campaign/"
    fecha_acceso: 2026-08-03
  - titulo: "2026 Mid-Year AI Threat Landscape Report (KELA Cyber Intelligence)"
    url: "https://www.kelacyber.com/resources/research/2026-mid-year-ai-threat-landscape/"
    fecha_acceso: 2026-08-03
  - titulo: "Defensive Refusal Bias: How Safety Alignment Fails Cyber Defenders (ICLR 2026)"
    url: "https://arxiv.org/abs/2603.01246"
    fecha_acceso: 2026-08-03
  - titulo: "OR-Bench: An Over-Refusal Benchmark for Large Language Models (ICML 2025)"
    url: "https://arxiv.org/abs/2405.20947"
    fecha_acceso: 2026-08-03
  - titulo: "Position: AI Security Policy Should Target Systems, Not Models (NeurIPS 2026)"
    url: "https://arxiv.org/abs/2605.09504"
    fecha_acceso: 2026-08-03
  - titulo: "Scaling Trusted Access for Cyber Defense (OpenAI)"
    url: "https://openai.com/index/scaling-trusted-access-for-cyber-defense/"
    fecha_acceso: 2026-08-03
---

# La asimetría de seguridad de los modelos abiertos

## El concepto

La "seguridad por rechazo" es asimétrica por diseño: los controles de alineación en modelos comerciales bloquean a defensores legítimos que intentan auditar código, analizar malware o responder a incidentes, mientras que un atacante puede simplemente cambiar a un modelo abierto sin restricciones y continuar. El sistema diseñado para hacer la IA más segura crea un gradiente de capacidad donde el atacante siempre tiene más herramientas disponibles que el defensor.

La asimetría no es un bug de implementación sino una consecuencia estructural del modo dominante de alineación: los modelos aprenden a rechazar categorías de contenido sin razonar sobre la identidad o la intención del solicitante. Cuando el contenido necesario para defenderse — exploits reales, payloads de malware, artefactos de comando y control — es formalmente indistinguible del contenido usado para atacar, los guardrails no pueden separar al respondedor del atacante, y rechazan a ambos por igual.

La disponibilidad de modelos de pesos abiertos sin restricciones (DeepSeek, GLM-5.2, Kimi K3, Qwen) crea un mercado de dos velocidades: quienes respetan las políticas de uso quedan dentro de los límites del proveedor; quienes no las respetan tienen acceso irrestricto a capacidades equivalentes o superiores. El costo neto cae sobre quien construye y defiende.

## Por qué importa

El caso que fuerza la tensión a la superficie llegó la última semana de julio de 2026 por partida doble. Unit 42 (Palo Alto Networks) documentó cómo un actor de habla china intentó usar Claude Code y OpenAI Codex para su pipeline de ataque — y fue bloqueado. Sin freno: cambió a DeepSeek vía el framework open-source Hermes Agent, orquestado por Telegram, y explotó autónomamente más de 460 sistemas expuestos sin intervención humana tras la instrucción inicial. El mismo actor que los controles rechazaron completó la operación con el modelo que no rechaza.

El incidente de Hugging Face (16 de julio de 2026) ilustra la misma asimetría desde el otro lado: cuando modelos frontier de OpenAI brecharon su infraestructura de producción, el equipo de respuesta no pudo usar APIs comerciales para analizar los artefactos del incidente — los guardrails, en sus propias palabras, "no pueden distinguir a un respondedor de un atacante". Tuvieron que correr GLM-5.2 (MIT-licensed, Beijing) localmente para la investigación forense. El mismo tipo de modelo abierto que el atacante usó fue la única herramienta disponible para el defensor.

El resultado estructural: los controles de alineación son empíricamente más efectivos como barrera para defensores legítimos que como barrera para atacantes. Un atacante motivado tiene siempre una alternativa; un equipo de respuesta a incidentes en medio de una crisis no siempre puede esperar por la verificación de acceso.

## Datos y evidencia

**Escala del ataque autónomo:**
- El actor documentado por Unit 42 (julio 2026) intentó 460+ objetivos usando DeepSeek/Hermes Agent vía Telegram; 3 compromisos confirmados — exfiltración de memoria en Citrix NetScaler y acceso sospechado a entidad gubernamental de Malaysia; 7 rutas de explotación sobre 8 CVEs; sin intervención humana tras la instrucción inicial. El actor intentó explícitamente Claude Code y Codex, fue bloqueado, y migró a DeepSeek. (Unit 42 / Palo Alto Networks, 2026-07-31)
- KELA Cyber Intelligence Mid-Year 2026: más de 1 millón de máquinas infectadas en los primeros 4 meses de 2026; 45% de incremento en víctimas de ransomware (7,549 víctimas en el período); grupos criminales documentan la migración sistemática de modelos frontier bloqueados a LLMs de código abierto auto-hosteados sin restricciones. El 80-90% de las tareas de ataque en campañas autónomas documentadas se ejecutan sin intervención humana tras la instrucción inicial.

**El impuesto medido:**
- "Defensive Refusal Bias" (Campbell et al., workshop ICLR 2026, arXiv 2603.01246): 2,390 conversaciones reales de la National Collegiate Cyber Defense Competition (NCCDC) — trabajo de seguridad explícitamente autorizado y legalmente inequívoco. Los LLMs con safety-tuning rechazan solicitudes defensivas con términos de seguridad a **2.72× la tasa** de solicitudes semánticamente equivalentes en lenguaje neutro (p < 0.001). Mayor tasa de rechazo en: hardening de sistemas (43.8%) y análisis de malware (34.3%) — precisamente las categorías más críticas operativamente.
- Hallazgo contraintuitivo del mismo paper: la autorización explícita — decirle al modelo que tienes permiso — **aumenta** la tasa de rechazo en vez de reducirla. El modelo interpreta las justificaciones como señales adversariales, no como contexto exculpatorio. Esto invalida la suposición de que prompting más claro resuelve el problema.
- OR-Bench (Cui et al., ICML 2025, arXiv 2405.20947): 80,000 prompts en 10 categorías de rechazo, evaluados en 32 LLMs. Correlación de Spearman de **0.878** entre la capacidad de bloquear contenido dañino y la tasa de rechazos incorrectos en consultas inocuas. No es un bug de ajuste — es una propiedad estructural del alineamiento actual. Un enfoque "DirectRefusal" degradó la precisión de razonamiento en **30.91%** promedio en benchmarks estándar.

**La obsolescencia técnica del control por modelo:**
- "AI Security Policy Should Target Systems, Not Models" (NeurIPS 2026 preprint, arXiv 2605.09504): un sistema de 5 agentes con un modelo de **1,200 millones de parámetros** en una MacBook de consumo alcanzó una **tasa de daño efectivo de 45.8% contra GPT-4o** (49 brechas de severidad crítica). El mismo setup recuperó **9/9 vulnerabilidades (100% recall) en ~4 minutos** en una aplicación C con 9 CWEs plantados. La capacidad que justificó la restricción de acceso del modelo más poderoso de Anthropic a 11 organizaciones es reproducible con hardware de consumo.

## Tensiones y límites

**La verificación como remedio parcial.** Anthropic opera el Cyber Verification Program (CVP) con acceso privilegiado para 11 organizaciones verificadas (AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks). OpenAI está expandiendo "Trusted Access for Cyber" (GPT-5.4-Cyber) a miles de defensores verificados. Ambas reconocen que la verificación de identidad, no el rechazo en bloque, es la dirección correcta — pero la fricción del pipeline de verificación burdens asimétricamente al defensor en medio de un incidente en tiempo real. El foro de comunidad de OpenAI ya documenta casos de "Trusted Access for Cyber" fallando verificación para usos legítimos.

**El modelo abierto como herramienta de ambos lados.** En el caso Unit 42, el actor fue bloqueado por modelos comerciales y continuó con modelos abiertos. En el caso Hugging Face, el equipo de respuesta fue bloqueado por modelos comerciales y usó el mismo tipo de modelo abierto. La restricción no redujo la disponibilidad de capacidad ofensiva — desplazó a ambos lados hacia el modelo sin restricciones.

**La obsolescencia técnica del control por modelo.** El argumento de la restricción asume que el modelo es el cuello de botella de capacidad. Los datos de 2026 muestran que un scaffold suficientemente capaz compensa el poder bruto del modelo: 1.2B parámetros replican la capacidad que justificó la restricción del modelo más poderoso. Gobernar el acceso al modelo ya no equivale a gobernar la capacidad.

**Límite del concepto.** Esta asimetría aplica específicamente donde defender y atacar requieren acceso al mismo tipo de contenido (exploits, malware, artefactos C2). Para dominios donde el daño potencial es desproporcionadamente mayor y sin uso defensivo equivalente (síntesis de agentes biológicos, armas de destrucción masiva), la lógica de rechazo puede ser racionalmente diferente. El análisis aquí es específico a ciberseguridad ofensiva/defensiva convencional.

## Ejes investigados

**Eje 1 — Escala real de ataques autónomos con modelos abiertos (2025-2026)**
Búsqueda de incidentes documentados e informes de amenaza. Hallazgos: caso Unit 42 (460+ sistemas, DeepSeek/Hermes Agent, actor intentó Claude Code y Codex y fue bloqueado antes de migrar); KELA Mid-Year 2026 (1M+ máquinas en 4 meses, 45% aumento ransomware, migración sistemática a modelos abiertos, 80-90% autonomía de ataque). Dato crítico adicional al Scout: la restricción del modelo comercial tuvo efecto verificado — el actor fue bloqueado — pero no el efecto deseado. 3 fuentes identificadas.

**Eje 2 — El impuesto de alineación: cuantificación empírica**
Búsqueda de papers con datos sobre rechazo a defensores legítimos. "Defensive Refusal Bias" (ICLR 2026): 2.72× tasa de rechazo en trabajo autorizado, con hallazgo contraintuitivo de que la autorización explícita aumenta rechazos. OR-Bench (ICML 2025): correlación 0.878 entre safety efectivo y over-refusal — propiedad estructural. "DirectRefusal" degrada razonamiento en 30.91%. Dato crítico adicional: el hallazgo sobre autorización explícita es el argumento más fuerte del concepto — invalida el argumento de "mejor prompting" como solución. 2 fuentes primarias con datos cuantitativos.

**Eje 3 — Alternativas al rechazo: propuestas técnicas y de política**
Búsqueda de marcos de política y alternativas institucionales. NeurIPS 2026 preprint: control por modelo es técnicamente obsoleto, propone gobernanza a nivel de sistema; "Framework for Cybersecurity Refusals" (arXiv 2606.02644): criterios basados en impacto real vs. keyword matching; Anthropic CVP + OpenAI Trusted Access: verificación de identidad como alternativa institucional, con fricción documentada que sigue burdenando al defensor en tiempo real. 3 fuentes identificadas.
