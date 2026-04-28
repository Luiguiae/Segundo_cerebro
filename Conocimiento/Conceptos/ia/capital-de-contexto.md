---
titulo: "Capital de contexto"
tipo: concepto
familia: epistemologia-practica
categoria: ia
fecha: 2026-04-18
tags: [ia, conocimiento, prompts, estrategia, criterio]
relacionado: [quien-controla-el-prompt, feedback-que-escala, arquitectura-de-inteligencia]
estado: activo
fuentes:
  - titulo: "An AI state of the union: hoarding pattern – Simon Willison, Lenny's Podcast"
    url: "https://www.lennysnewsletter.com/p/an-ai-state-of-the-union"
    fecha_acceso: 2026-04-18
  - titulo: "When Every Company Can Use the Same AI Models, Context Becomes a Competitive Advantage – HBR"
    url: "https://hbr.org/2026/02/when-every-company-can-use-the-same-ai-models-context-becomes-a-competitive-advantage"
    fecha_acceso: 2026-04-18
  - titulo: "Context Engineering Is Replacing Prompt Engineering – Mia Platform"
    url: "https://mia-platform.eu/blog/context-engineering/"
    fecha_acceso: 2026-04-18
  - titulo: "AI's trillion-dollar opportunity: Context graphs – Foundation Capital"
    url: "https://foundationcapital.com/ideas/context-graphs-ais-trillion-dollar-opportunity"
    fecha_acceso: 2026-04-18
  - titulo: "Compounding AI Advantage – Dual Boot Partners"
    url: "https://www.dualbootpartners.com/insights/compounding-ai/"
    fecha_acceso: 2026-04-18
  - titulo: "Context Engineering: From Prompts to Corporate Multi-Agent Architecture – arXiv 2603.09619"
    url: "https://arxiv.org/pdf/2603.09619"
    fecha_acceso: 2026-04-18
---

# Capital de contexto

## El concepto
Los mejores practicantes de IA no tratan los prompts como interacciones desechables —
construyen un *hoard*: colecciones curadas de prompts de alta calidad, cadenas de
razonamiento probadas, ejemplos few-shot calibrados, y contextos que producen outputs
consistentes y confiables. Esta acumulación compone: quien más tiene, más puede
producir con menos esfuerzo marginal.

Simon Willison nombra el patrón *hoarding* como una de las prácticas centrales de
los equipos que obtienen resultados sostenidos con IA. La paradoja que el concepto
expone: tratamos el prompting como trabajo efímero cuando debería tratarse como
capital acumulable. El hoard de contexto de un equipo experto es tan difícil de
replicar como el conocimiento tácito institucional — no porque esté protegido, sino
porque se tarda meses en construirlo con resultados reales.

## Por qué importa
Cuando todos los equipos tienen acceso a los mismos modelos de lenguaje, la ventaja
competitiva migra al contexto que alimenta esos modelos. HBR (Feb 2026) documenta
este cambio: el diferenciador ya no es qué modelo usas — es la calidad del contexto
que le proporcionas. Las organizaciones que convirtieron su conocimiento institucional
en contexto reutilizable y gobernado están separándose del resto.

El capital de contexto es el mecanismo por el cual el conocimiento tácito de un
equipo se vuelve operacionalmente transferible a los agentes que trabajan con él.

## Datos y evidencia

**Context engineering: la evolución del prompting.**
En mid-2025, Gartner declaró que "context engineering is in, and prompt engineering
is out." La distinción es precisa: prompt engineering trata cada interacción como
una nueva instrucción; context engineering construye la infraestructura de información
que hace que las instrucciones sean consistentemente efectivas.

Gartner predice que para 2028, el context engineering estará en el 80% de las
herramientas de IA, mejorando la precisión de los agentes en al menos un 30%.

**El contexto como registro de decisiones.**
Foundation Capital (2026) introduce el concepto de *context graph*: la estructura
acumulada formada por trazas de decisión — no la cadena de razonamiento del modelo,
sino un registro vivo de decisiones reales tomadas a través del tiempo, con sus
contextos y excepciones. Este grafo se convierte en la fuente de verdad de la
autonomía agéntica: no solo documenta qué ocurrió, sino por qué fue permitido ocurrir.

La implicación: el capital de contexto no es solo una colección de prompts — es
una arquitectura de precedentes que permite a los agentes tomar decisiones
consistentes con el criterio del equipo sin que cada interacción requiera instrucción
explícita.

**El efecto compuesto del capital de contexto.**
Dual Boot Partners documenta el patrón de ventaja compuesta: las primeras
implementaciones de IA generan ganancias de productividad; esas ganancias financian
mejores inversiones en datos y contexto; ese contexto mejorado produce outputs de
mayor calidad; que generan más datos y precedentes. El capital de contexto no
decae con el tiempo — crece, y el costo de replicarlo para un competidor aumenta
conforme el capital madura.

Este es el mismo mecanismo que hace valioso el conocimiento tácito institucional:
no está protegido legalmente, pero los años de decisiones reales que lo construyeron
no pueden copiarse. Un competidor puede replicar el modelo y la interfaz — no puede
replicar los años de ejemplos calibrados, cadenas de razonamiento validadas, y
contextos que producen el output correcto para ese dominio específico.

**El hoard como infraestructura, no como colección.**
La distinción entre un hoard amateur y capital de contexto maduro es arquitectónica.
Un hoard amateur es una carpeta de prompts que funcionaron. Capital de contexto maduro
es un sistema donde: los prompts están versionados, cada ejemplo incluye trazabilidad
de por qué funcionó, el contexto es recuperable por agentes en tiempo de ejecución,
y el feedback de cada uso retroalimenta la calidad de los prompts futuros.
Esto conecta directamente con `feedback-que-escala`: el capital de contexto es el
repositorio donde el feedback sistémico se materializa como activo reutilizable.

## Tensiones y límites
Tensiona con `quien-controla-el-prompt`: quien controla el prompt accede
individualmente al contexto correcto; el capital de contexto es la pregunta de quién
posee y mantiene el contexto que hace que ese prompt funcione. El prompt controller
sin capital de contexto maduro reinventa cada interacción. El capital de contexto
sin un prompt controller con criterio produce artefactos técnicamente bien formados
pero sin juicio de dominio.

El capital de contexto como activo organizacional crea dependencia: un equipo
altamente optimizado para un modelo específico puede encontrar que su capital de
contexto pierde valor si el modelo cambia radicalmente. La portabilidad del contexto
entre modelos es un problema no resuelto.

No aplica en la misma medida a tareas que requieren creatividad divergente — donde
la riqueza del contexto puede actuar como ancla que limita el espacio de soluciones
en lugar de enriquecerlo.

## Ejes investigados
- **Eje 1:** Hoarding pattern (Willison) y context engineering como evolución — Lenny's, Mia Platform, Gartner
- **Eje 2:** Contexto como ventaja competitiva — HBR Feb 2026, Foundation Capital context graphs
- **Eje 3:** Efecto compuesto del capital de contexto — Dual Boot Partners, arXiv 2603.09619
