---
titulo: "El cumplimiento que se volvió vigilancia"
tipo: concepto
familia: agencia-ia
tags: [gobernanza-ia, ia, transparencia, control, etica]
relacionado: [gobernanza-ia-performativa, legibilidad-de-maquina, arquitectura-de-confianza]
fecha: 2026-08-13
estado: borrador
fuentes:
  - titulo: "Claude Now Watermarks Text Everywhere; Mark Proves Processing, Not Authorship"
    url: "https://www.techtimes.com/articles/323873/20260811/claude-now-watermarks-text-everywhere-mark-proves-processing-not-authorship.htm"
    fecha_acceso: 2026-08-13
  - titulo: "EU AI Act Article 50: Transparency Obligations Take Effect"
    url: "https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/"
    fecha_acceso: 2026-08-13
  - titulo: "Four Cents Strips Claude Watermark; Anthropic Detection API Confirms Evasion Oracle"
    url: "https://www.techtimes.com/articles/324183/20260812/four-cents-strips-claude-watermark-anthropic-detection-api-confirms-evasion-oracle.htm"
    fecha_acceso: 2026-08-13
  - titulo: "Some Claude users are mad that Anthropic's new watermarks will catch them cheating at their jobs, classes"
    url: "https://techcrunch.com/2026/08/12/some-claude-users-are-mad-that-anthropics-new-watermarks-will-catch-them-cheating-at-their-jobs-classes/"
    fecha_acceso: 2026-08-13
  - titulo: "Adoption of Watermarking for Generative AI Systems in Practice and Implications under the new EU AI Act"
    url: "https://arxiv.org/pdf/2503.18156"
    fecha_acceso: 2026-08-13
  - titulo: "Anthropic's text watermarks signal new front in AI detection"
    url: "https://www.axios.com/2026/08/12/anthropic-claude-watermarks-ai-detection"
    fecha_acceso: 2026-08-13
---

## El concepto

Anthropic empezó a marcar todo el texto generado por Claude con un watermark invisible el 2 de agosto de 2026, en respuesta al Artículo 50 del EU AI Act. La marca es un sesgo estadístico en las elecciones de palabras del modelo: entre múltiples palabras igualmente plausibles en cada posición, el modelo selecciona preferentemente un subconjunto que codifica un patrón secreto detectable. El resultado es texto ordinario que un lector humano no distingue del no-marcado, pero que un detector computacional puede identificar como proveniente de Claude.

La norma que obliga al watermark fue diseñada para un nivel específico de la cadena regulatoria: los proveedores (Anthropic) deben marcar sus outputs para que plataformas, desplegadores profesionales y autoridades de vigilancia de mercado puedan verificar la proveniencia del contenido a escala. El individuo final —el estudiante, el empleado, el investigador que usa Claude en su trabajo cotidiano— no es el objetivo del Artículo 50 del EU AI Act. La regulación apunta a la transparencia del mercado, no al control de la persona.

Pero el mecanismo técnico no distingue niveles de la cadena. Al implementar el watermark de forma global y sin opt-out, y al anunciar una API de detección de acceso público, Anthropic creó la infraestructura para que cualquier institución que actúe como "desplegador" —una universidad, un empleador, una editorial— pueda detectar si un texto fue procesado por Claude. Nadie decidió explícitamente convertir la transparencia de mercado en vigilancia disciplinaria. Pero ese es el efecto que la arquitectura de la implementación produce.

## Por qué importa

Este caso documenta un mecanismo de transferencia de nivel que el vault todavía no tiene nombrado: la infraestructura de gobernanza construida para operar en un nivel de la cadena regulatoria (mercado → autoridad de vigilancia) se filtra hacia abajo (individuo → institución disciplinaria) sin que nadie lo haya decidido como política explícita. No es que el Artículo 50 falle en su objetivo original; es que la implementación técnica necesaria para cumplirlo habilita un caso de uso que la norma nunca tuvo intención de crear.

La queja más fuerte ante el anuncio de Anthropic no vino de estudiantes intentando hacer trampa, sino de abogados, académicos e investigadores que usan Claude para revisar, editar o reformatear texto que escribieron ellos mismos. Su trabajo ahora lleva la marca de Claude aunque las ideas, el argumento y la investigación son enteramente suyos. Para cualquier institución que lea una detección positiva como prueba de "autoría IA", esa distinción desaparece: el watermark detecta que Claude *procesó* el texto, no que Claude lo *autoró*. Una persona que le pidió a Claude que revisara su puntuación recibe de vuelta un documento marcado como "procesado por IA" aunque el contenido sea 100% propio.

Este concepto extiende `gobernanza-ia-performativa` con un mecanismo técnico específico y fechado: no es solo que la gobernanza sea gesto, es que los gestos de cumplimiento construyen infraestructura que luego opera independientemente de su propósito original, activando efectos que ningún actor de la cadena eligió explícitamente.

## Datos y evidencia

- **Fecha de entrada en vigor del EU AI Act Art. 50**: 2 de agosto de 2026 para sistemas recién lanzados; período de gracia hasta diciembre de 2026 para sistemas anteriores. Fines de hasta €15 millones o el 3% de la facturación global por incumplimiento. [EU AI Act Article 50 — Cloud Security Alliance, 2026-07-29]
- **Implementación de Anthropic**: watermark activo desde el 2 de agosto de 2026 en todos los modelos Claude nuevos, globalmente, sin opt-out. Aplica a Claude.ai, API, Claude Code, Claude Cowork, Claude Tag, y a través de AWS, Google Cloud y Microsoft Foundry. [Anthropic, agosto 2026]
- **Robustez adversarial**: una evaluación forense de julio de 2026 encontró que paráfrasis que preserva significado eliminó la marca en el 100% de textos previamente detectados para dos esquemas de watermarking, y en el 98,3% para SynthID. [citado en TechCrunch, 2026-08-12]
- **Costo de evasión**: aproximadamente $0,04 por pasada usando la propia API de detección de Anthropic como oráculo de evasión — quien tiene conocimiento técnico, escapa en segundos y por centavos. [TechCrunch / TechTimes, 2026-08-12]
- **Falsa atribución como problema documentado**: el watermark no distingue entre "Claude generó este texto" y "Claude revisó/editó/tradujo texto de autoría humana". Quienes usan Claude para proofreading, traducción o reformateo de su propio trabajo quedan marcados de forma idéntica a quienes generaron el texto desde cero. [TechCrunch / The Decoder, 2026-08-12]
- **Diseño regulatorio original**: el Artículo 50 estructura la cadena como proveedor → desplegador profesional → autoridad de vigilancia de mercado. El individuo final no aparece como actor en la cadena de detección intencionada por la norma. [EU AI Act Article 50(1) y 50(2), 2024]

## Tensiones y límites

**La marca detecta procesamiento, no autoría.** La misma señal que identifica "Claude generó esto" identifica también "Claude corrigió esto", "Claude tradujo esto" y "Claude reformateó esto". Para el sistema de detección, todos estos casos son técnicamente indistinguibles. Una institución que usa la detección como proxy de "autoría IA" comete un error de categoría que la señal técnica no puede —ni pretende— corregir.

**La vulnerabilidad es asimétrica.** El watermark es adversarialmente débil: $0,04 y una pasada de paráfrasis eliminan la marca. Los usuarios que tienen el conocimiento técnico y el incentivo para evadir, lo hacen. Quienes quedan expuestos son los usuarios de buena fe —el académico que pidió una revisión de estilo, el abogado que usó Claude para limpiar su redacción— que no saben que son rastreables ni cómo dejar de serlo. La vigilancia disciplina al inocente técnico, no al sofisticado.

**El patrón de creep de infraestructura de cumplimiento no es exclusivo de IA.** KYC/AML fue diseñado para vigilancia de crimen financiero a nivel de mercado y se convirtió en infraestructura de vigilancia individual masiva con monitoreo continuo de transacciones personales. El GDPR, pensado para proteger al individuo, creó estructuras que actores de plataforma usaron para consolidar posición regulatoria. La transferencia de nivel no es un accidente de la IA: es un patrón recurrente en cómo las normas de cumplimiento se implementan técnicamente y luego migran hacia usos no declarados.

**El límite del concepto**: no todo watermark produce vigilancia individual. El problema específico emerge de la combinación de tres elementos: (1) API de detección públicamente accesible para cualquier institución + (2) incapacidad técnica de distinguir autoría de asistencia + (3) instituciones con incentivos disciplinarios preexistentes que ahora tienen acceso a la señal. Si la API fuera de acceso restringido exclusivamente a autoridades regulatorias de mercado, el efecto de vigilancia individual no ocurriría. La vigilancia no es una propiedad del watermark: es una propiedad de la arquitectura de acceso a su detección.

## Ejes investigados

**Eje 1 — Mecanismo técnico y arquitectura de acceso a la detección**: investigué cómo funciona el watermark estadístico de Claude y quién tiene acceso a detectarlo. Hallazgo clave: la API de detección planificada es públicamente accesible, no restringida a reguladores; la robustez adversarial es baja ($0,04 de evasión en ~100% de casos); y el watermark captura *procesamiento* IA, no *autoría* IA — una distinción que la señal técnica no puede hacer. 4 fuentes sólidas encontradas.

**Eje 2 — Brecha regulatoria mercado/individuo en el EU AI Act**: investigué el texto del Artículo 50 y su cadena de implementación intencionada. Hallazgo clave: el Artículo 50 diseña una cadena proveedor → desplegador profesional → autoridad de vigilancia de mercado. El individuo final no aparece como actor en esa cadena. La implementación técnica de Anthropic cortocircuita esa cadena al hacer la detección públicamente accesible para cualquier institución. 3 fuentes sólidas encontradas.

**Eje 3 — Patrón histórico de compliance creep**: investigué precedentes de infraestructura de cumplimiento que deriva de vigilancia de mercado a vigilancia individual. Hallazgo clave: KYC/AML y GDPR son casos documentados con el mismo patrón estructural. El fenómeno tiene nombre en literatura de policy ("compliance drift", "function creep"). El corpus académico en español es escaso; el patrón está mejor documentado en literatura anglosajona de regulación e infraestructura institucional. 2 fuentes sólidas encontradas.
