---
titulo: "El peaje del acceso agéntico"
tipo: concepto
familia: agencia-ia
tags: [ia, agentes, infraestructura, web, gobernanza-ia]
relacionado: [web-bifurcada, presupuesto-ia-como-restriccion, costo-marginal-cero-como-disruptor]
fecha: 2026-07-26
estado: borrador
fuentes:
  - titulo: "Your site, your rules: new AI traffic options for all customers"
    url: "https://blog.cloudflare.com/content-independence-day-ai-options/"
    fecha_acceso: 2026-07-26
  - titulo: "10,300 to 1: How AI Crawlers Are Quietly Draining the Web Economy"
    url: "https://www.alphamatch.ai/blog/ai-crawlers-drain-web-economy-on-premise-ai-2026"
    fecha_acceso: 2026-07-26
  - titulo: "AI Bot Traffic Is Now 40% of the Web. Publishers, Pay Attention."
    url: "https://www.playwire.com/blog/ai-bot-traffic-is-now-40-of-the-web-publishers-pay-attention"
    fecha_acceso: 2026-07-26
  - titulo: "The Agentic Web Requires New Normative Infrastructure"
    url: "https://arxiv.org/html/2606.10711v2"
    fecha_acceso: 2026-07-26
  - titulo: "Cloudflare Separates AI Crawlers by Purpose and Opens Door to Charging Them Directly"
    url: "https://www.techtimes.com/articles/319554/20260702/cloudflare-separates-ai-crawlers-purpose-opens-door-charging-them-directly.htm"
    fecha_acceso: 2026-07-26
---

# El peaje del acceso agéntico

## El concepto

La web operó durante tres décadas bajo un contrato implícito: los crawlers podían indexar cualquier contenido público porque a cambio enviaban tráfico de referencia. El motor de búsqueda extraía valor del contenido; el publisher recibía visitantes. El ciclo era simétrico, aunque nunca se firmó.

Los agentes IA rompen ese contrato. Un agente que navega la web en nombre de un usuario extrae el valor del contenido —la respuesta, el precio, el resumen— sin que exista un clic de retorno. El publisher asume el costo de servir la solicitud; el agente captura el beneficio. La simetría se invierte.

Cloudflare respondió a este quiebre formalizando, por primera vez, una taxonomía de propósito para el tráfico de bots: tres categorías distinguibles —Search (indexa y refiere tráfico), Training (extrae para entrenar modelos), Agent (actúa en tiempo real en nombre de un usuario)— y un esquema de permisos distinto para cada una. A partir del 15 de septiembre de 2026, los dominios nuevos que muestren publicidad tendrán Training y Agent bloqueados por defecto. Search permanece permitido: es el único tipo que todavía devuelve algo al publisher.

El resultado es que Cloudflare —empresa que procesa aproximadamente el 20% del tráfico de internet— se convierte en árbitro de qué bots sobreviven y bajo qué condiciones. El peaje ya no es metafórico.

## Por qué importa

La fractura que Cloudflare formaliza no es solo técnica: es la primera codificación explícita de que el valor que un bot extrae depende de su propósito, y que ese propósito puede y debe tener consecuencias económicas.

Para los constructores de productos agénticos, esto significa que el acceso a datos web en tiempo real —uno de los insumos más valiosos de los agentes— deja de ser un recurso libre. El "internet abierto" que los modelos asumieron como infraestructura de entrenamiento y operación empieza a cerrar compuertas. Los agentes que dependen de scraping directo enfrentan un entorno donde el permission layer está en la capa de red, no en el robots.txt.

Para los publishers, la clasificación abre la posibilidad de monetizar el acceso en lugar de solo bloquearlo. Herramientas como TollBit y el estándar Know Your Agent están construyendo la plomería para un modelo pay-per-crawl: en vez de un muro de bloqueo, un peaje medido donde cada tipo de bot paga según el valor que extrae.

La pregunta de fondo no es técnica. Es sobre quién controla el arbitraje: si Cloudflare puede clasificar un bot como "entrenamiento" vs. "agente" con consecuencias de acceso tan distintas, quien controla esa clasificación controla qué productos agénticos son viables a escala.

## Datos y evidencia

- **Cloudflare (julio 2026):** nueva política activa desde el 1 de julio. Desde el 15 de septiembre de 2026, Training y Agent bloqueados por defecto en páginas con anuncios para todos los dominios nuevos. Disponible para todos los clientes, incluyendo plan gratuito. Afecta también a multi-purpose crawlers (Googlebot, Applebot, BingBot) si el usuario elige bloquear Training.
- **Ratio crawl-to-referral (AlphaMatch.ai, 2026):** el crawler de Anthropic (Claude) genera 10,300 scrapes por cada visitante humano referido. GPTBot de OpenAI: 903.8:1. Bot de Perplexity: 192.9:1. Googlebot: 5.2:1. DuckDuckGo: 1.5:1.
- **Volumen de bot traffic (Playwire / Thunderbit, 2026):** los bots representan el 57.5% del tráfico HTML —primera vez en la historia de internet que el tráfico automatizado supera al humano—. El 51.8% de las solicitudes de AI crawlers son para entrenamiento de modelos.
- **Caso Digital Trends (AlphaMatch.ai, 2026):** 4.1 millones de scrapes de bots en una semana generaron solo 4,200 referrals humanos —ratio de 966:1—.
- **Litigación (2025-2026):** Bartz v. Anthropic (2025) estableció que entrenar con libros obtenidos legalmente es fair use transformativo. NYT v. OpenAI testea si la "regurgitación" del output derrota ese fair use. Google v. SerpApi (audiencia mayo 2026) pivota de copyright hacia DMCA Section 1201 anti-circumvention —lo que podría criminalizar el scraping proxy-basado independientemente del fair use—.

## Tensiones y límites

**Tensión con `costo-marginal-cero-como-disruptor`:** el mecanismo de los agentes como eliminadores de fricción asume acceso libre a la web. Si el peaje se generaliza, el costo marginal de operar un agente web deja de ser cercano a cero —no por el modelo, sino por la capa de acceso—. La disrupción que los agentes prometen está condicionada a la permeabilidad de la infraestructura.

**La paradoja de la clasificación:** para distinguir entre un bot de búsqueda, uno de entrenamiento y uno agéntico, Cloudflare necesita inspeccionar la intención del crawl —y la intención no es siempre declarada honestamente—. Un bot de entrenamiento puede disfrazarse de agente; un agente legítimo puede parecer un scraper masivo. La clasificación está sujeta a gaming.

**Límite geopolítico y de concentración:** la política de Cloudflare aplica donde Cloudflare tiene presencia (~20% del internet). El 80% restante puede operar sin este filtro. Y una empresa privada que controla el acceso de bots a ese porcentaje del internet concentra un poder de arbitraje que ninguna regulación todavía toca.

**La solución de peaje no es neutral:** TollBit y modelos pay-per-crawl favorecen a agentes con presupuesto —grandes corporaciones— y penalizan a agentes experimentales, open source o de investigación. El mercado de datos web accesibles se redistribuye, no se democratiza.

## Ejes investigados

**Eje 1 — Cloudflare como árbitro técnico:** mecanismo de clasificación de bots en tres categorías, calendario de implementación, alcance (todos los clientes), y qué pasa con multi-purpose crawlers. 3 fuentes sólidas encontradas (Cloudflare Blog, TechTimes, HelpNetSecurity).

**Eje 2 — La fractura económica del contrato implícito:** datos de crawl-to-referral ratio por crawler, volumen de bot traffic vs. tráfico humano, impacto en revenue de publishers, modelos emergentes de monetización (TollBit, Know Your Agent). 3 fuentes sólidas encontradas (AlphaMatch.ai, Playwire, SecurityBoulevard).

**Eje 3 — Fair use y regulación de la infraestructura agéntica:** litigación activa (Bartz v. Anthropic, NYT v. OpenAI, Google v. SerpApi), cambio de argumento de copyright a anti-circumvention DMCA, AI AGENT Act y acceso no discriminatorio. 3 fuentes sólidas encontradas (DataImpulse, IPWAY, arXiv 2606.10711).
