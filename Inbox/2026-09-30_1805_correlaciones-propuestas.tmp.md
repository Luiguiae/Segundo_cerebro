# Correlaciones propuestas — 2026-09-30

Pedido explícito de Luigui: "dame 3 correlaciones a partir de este nuevo concepto" (`sistemas-para-humanos-saturados-por-agentes`, instalado hoy). **Alcance distinto de una corrida normal de "busca correlaciones":** no fue un barrido de todo el vault — los 3 candidatos evaluados son exactamente los 3 conceptos que el propio concepto ya declara en `relacionado` (`web-bifurcada`, `legibilidad-de-maquina`, `identidad-criptografica-como-arnes`), que además son los más fuertes posibles por familia compartida (`agencia-ia`) y tags compartidos (`agentes`, `sistemas`). Verificado que ninguno de los 3 pares tiene ya un archivo en `Correlaciones/` ni aparece en ningún `Inbox/*_correlaciones-propuestas.tmp.md` pendiente.

Sobrevivientes autocrítica adversarial: **3 de 3**
Descartados: 0

---

## 1. Firmar a tu propio agente no identifica al que toca la puerta

**Par:** `sistemas-para-humanos-saturados-por-agentes` × `identidad-criptografica-como-arnes`

**Señales:** misma familia (`agencia-ia`) + 2 tags compartidos (`agentes`, `identidad`) + mención cruzada literal (el concepto nuevo nombra explícitamente "identidad criptográfica — HTTP Message Signatures (RFC 9421)... Web Bot Auth" en su sección de Tensiones y límites).

**Justificación de la tensión real (1 línea):** `identidad-criptografica-como-arnes` resuelve el problema de identidad **puertas adentro** — un operador que firma y audita a sus propios agentes, con incentivo compartido de responsabilidad; `sistemas-para-humanos-saturados-por-agentes` describe el problema **puertas afuera** — un operador verificando agentes de terceros cuyo interés es, justo al revés, no ser fácilmente bloqueables. La misma solución técnica falla al cruzar esa frontera de incentivos.

---

```yaml
---
titulo: "Firmar a tu propio agente no identifica al que toca la puerta"
tipo: correlacion
conceptos: [sistemas-para-humanos-saturados-por-agentes, identidad-criptografica-como-arnes]
fecha: 2026-09-30
tags: [agentes, identidad, gobernanza-ia, confianza]
estado: borrador
---
```

# Firmar a tu propio agente no identifica al que toca la puerta

## La tensión

`identidad-criptografica-como-arnes` describe el mecanismo de Buzz (Block, julio 2026): cada agente recibe una identidad criptográfica propia, separada de su dueño humano, sobre el protocolo Nostr. Funciona porque hay un incentivo alineado en ambos lados de la relación — la empresa que despliega el agente *quiere* poder revocarlo, auditarlo y demostrar quién autorizó qué. Es una solución de gobernanza interna: resuelve "¿quién es este agente que yo mismo desplegué?".

`sistemas-para-humanos-saturados-por-agentes` describe un problema distinto que ocurre en la frontera opuesta del mismo sistema: un operador (Resy, una API de reservas) recibiendo tráfico de agentes que *no despliega ni controla* — personal agents de usuarios externos, sondeando "cientos de veces por hora". El concepto nombra la identidad criptográfica (Web Bot Auth, RFC 9421) como "la única señal técnicamente verificable", pero advierte que "requiere que el operador la implemente y valide activamente" — sin decir qué pasa si el lado que llama no tiene ningún incentivo en identificarse.

Ahí está la tensión no resuelta por ninguno de los dos textos: el mecanismo de `identidad-criptografica-como-arnes` funciona porque el agente *quiere* ser identificable (le conviene: revocabilidad limpia, cumplimiento, confianza). El agente que sondea Resy cientos de veces por hora no tiene ese incentivo — identificarse con precisión es exactamente lo que le permitiría al operador rate-limitarlo o bloquearlo. La cuenta de Instinct AI en Resy no fue desactivada por *fallar* en identificarse: fue desactivada por un patrón de comportamiento que un sistema de identidad perfecto tampoco habría evitado, porque el problema no era saber quién era el agente, sino qué tan seguido tocaba la puerta.

## El insight no obvio

Leído solo, `identidad-criptografica-como-arnes` puede sonar como una respuesta general al "problema de identidad de agentes" — el propio texto lo llama el "problema más fundamental" del trabajo multi-agente. Leído solo, `sistemas-para-humanos-saturados-por-agentes` nombra la identidad criptográfica como la salida técnica más prometedora frente al tráfico agéntico no autorizado.

Juntos revelan que son dos problemas de identidad distintos que comparten el mismo vocabulario técnico (firmas, claves, protocolos verificables) pero no el mismo supuesto de incentivos. Uno asume cooperación (la empresa quiere trazabilidad de *sus* agentes); el otro asume fricción (el operador quiere trazabilidad de agentes *ajenos*, que preferirían no dejarse trazar). Una solución de identidad diseñada para el primer caso —Buzz, con adopción voluntaria y alineada— no se traslada automáticamente al segundo sin resolver antes un problema que ninguno de los dos conceptos nombra: cómo hacer *obligatoria*, no solo posible, la identificación de un agente que no tiene ningún interés en ser identificado.

## El límite

Esta correlación no dice que la identidad criptográfica sea inútil para el problema de saturación — dice que es insuficiente sin un mecanismo adicional de exigencia. Web Bot Auth, tal como lo describe `sistemas-para-humanos-saturados-por-agentes`, sigue siendo voluntario: un agente que decide no firmarse simplemente no se beneficia de un trato preferente, pero tampoco queda bloqueado por default (el mismo destino que ya tiene el 72% de los AI crawlers que ignoran robots.txt, otro mecanismo voluntario). Y del lado de `identidad-criptografica-como-arnes`: aunque existiera un estándar de identidad universal y obligatorio para agentes de terceros, seguiría sin resolver la pregunta que ese concepto ya deja abierta para el caso interno — que la identidad clarifica responsabilidad, no calidad de comportamiento. Un agente de reservas perfectamente identificado que sigue sondeando cientos de veces por hora sigue saturando el sistema; solo que ahora el operador sabe exactamente a quién bloquear.

---

## 2. La saturación es lo que pasa cuando no existe la puerta legible

**Par:** `sistemas-para-humanos-saturados-por-agentes` × `web-bifurcada`

**Señales:** misma familia (`agencia-ia`) + 2 tags compartidos (`agentes`, `sistemas`) + el concepto nuevo nombra literalmente a `web-bifurcada` en su sección "Por qué importa" ("Extiende el problema de `web-bifurcada` más allá del contenido").

**Justificación de la tensión real (1 línea):** el propio concepto nuevo *dice* que extiende a `web-bifurcada`, pero no completa el argumento causal: `web-bifurcada` enmarca construir una capa legible para agentes como ventaja competitiva (ahorro de costo, mejor experiencia agéntica), mientras que la ausencia de esa misma capa es, leído junto al caso Resy, lo que empuja a los agentes a abusar del canal humano a escala de máquina — la saturación no es una fuerza externa inevitable, es el síntoma de una capa que no se construyó.

---

```yaml
---
titulo: "La saturación es lo que pasa cuando no existe la puerta legible"
tipo: correlacion
conceptos: [sistemas-para-humanos-saturados-por-agentes, web-bifurcada]
fecha: 2026-09-30
tags: [agentes, sistemas, infraestructura, web]
estado: borrador
---
```

# La saturación es lo que pasa cuando no existe la puerta legible

## La tensión

`web-bifurcada` documenta que servir una capa Markdown/estructurada a agentes no es solo más barato (80% menos tokens en el caso de Cloudflare) — es una decisión de diseño de producto: "la pregunta nueva es si el producto existe y es operable en la capa de agentes". El texto lo enmarca como oportunidad: quien construye esa capa gana eficiencia y, por extensión, mejores resultados cuando un agente decide entre proveedores.

`sistemas-para-humanos-saturados-por-agentes` describe el caso de Resy: un agente (Instinct AI) "sondeando cientos de veces por hora buscando disponibilidad", tratado como abuso y bloqueado. El concepto lo nombra literalmente como extensión de `web-bifurcada` "más allá del contenido", pero no dice explícitamente *por qué* ese tráfico llega en esa forma agresiva. La razón está implícita si se leen los dos juntos: Resy no tenía —al momento del incidente CNN, semanas antes de lanzar su integración oficial con ChatGPT en agosto 2026— una capa legible y estructurada para agentes. Sin esa puerta, un agente que necesita disponibilidad en tiempo real no tiene más opción que *imitar a un humano* repetidamente contra la interfaz humana, a velocidad de máquina. Eso es indistinguible, para el sistema, de un ataque.

## El insight no obvio

Leído solo, `web-bifurcada` sugiere que construir la capa de agentes es una optimización de costos y experiencia — algo que se hace *si conviene*, con el riesgo real (que el propio concepto nombra) de sobreinvertir antes de que el tráfico agéntico sea significativo. Leído solo, `sistemas-para-humanos-saturados-por-agentes` sugiere que el tráfico agéntico saturante es un problema de gobernanza y verificación — a quién dejar entrar y bajo qué condiciones.

Juntos revelan una relación causal que ninguno nombra del todo: la ausencia de la capa legible de `web-bifurcada` no es neutral frente al problema de saturación — lo *produce*. Un agente que no tiene una API o un endpoint Markdown claro para consultar disponibilidad no desaparece: se reencauza hacia el único canal que existe, el humano, y lo satura porque ahí no hay fricción de diseño que lo limite (ninguna estructura, ningún rate-limit natural, solo lo que un scraper decide hacer). El "problema de agentes" que describe `sistemas-para-humanos-saturados-por-agentes` es, en parte, un problema de infraestructura faltante que `web-bifurcada` ya sabe cómo nombrar pero no conecta con sus consecuencias de saturación.

## El límite

Esto no implica que construir la capa legible resuelva el problema de saturación por sí sola — podría simplemente trasladarlo: una API limpia y barata de consultar es, para un agente sin fricción de por medio, más fácil de sondear cientos de veces por hora, no menos (más barata en tokens no significa más barata en carga del servidor). `web-bifurcada` no discute límites de tasa ni control de acceso; su argumento es de eficiencia de representación, no de gobernanza de tráfico. Y el caso Resy-en-ChatGPT que cita `sistemas-para-humanos-saturados-por-agentes` confirma el límite: la solución que terminó adoptando no fue construir una capa Markdown abierta (la ruta que sugeriría `web-bifurcada`), sino una integración oficial cerrada — exactamente la ruta que el propio concepto nuevo advierte que "transfiere el poder de intermediación" a la plataforma de IA. La capa legible resuelve el problema de fricción técnica; no resuelve, por sí sola, quién queda autorizado a usarla.

---

## 3. La legibilidad que atrae también es la que satura

**Par:** `sistemas-para-humanos-saturados-por-agentes` × `legibilidad-de-maquina`

**Señales:** misma familia (`agencia-ia`) + 2 tags compartidos (`agentes`, `sistemas`) + ambos abordan directamente cómo un servicio debe comportarse frente a agentes, desde ángulos opuestos (atraerlos vs. limitarlos).

**Justificación de la tensión real (1 línea):** `legibilidad-de-maquina` presenta ser fácil de operar para un agente como ventaja competitiva pura; `sistemas-para-humanos-saturados-por-agentes` muestra que esa misma facilidad es indiferenciable entre demanda legítima y sobrecarga — la legibilidad no se puede dirigir selectivamente a la demanda "buena".

---

```yaml
---
titulo: "La legibilidad que atrae también es la que satura"
tipo: correlacion
conceptos: [sistemas-para-humanos-saturados-por-agentes, legibilidad-de-maquina]
fecha: 2026-09-30
tags: [agentes, sistemas, estrategia, infraestructura]
estado: borrador
---
```

# La legibilidad que atrae también es la que satura

## La tensión

`legibilidad-de-maquina` argumenta que la competencia entre productos ya se decide también por qué tan fácil es operarlos para una máquina: "el agente del usuario elige al competidor... porque su sistema es más predecible para una máquina y comete menos errores". El texto presenta esto casi sin matices como ventaja a perseguir — más legibilidad, mejor posición competitiva.

`sistemas-para-humanos-saturados-por-agentes` describe el reverso exacto de esa misma propiedad: un sistema fácil de operar para una máquina es, por definición, fácil de sondear repetidamente a escala de máquina. El agente que revisa disponibilidad "cientos de veces por hora" en Resy no está explotando una falla de diseño — está usando exactamente la facilidad de operación que `legibilidad-de-maquina` recomienda maximizar. La misma propiedad que gana el favor del agente de un cliente legítimo es la que permite el patrón que un sistema de detección de abuso termina bloqueando.

## El insight no obvio

Leído solo, `legibilidad-de-maquina` ya contiene una tensión interna —con `lo-ilegible-como-senal`— sobre cuándo un negocio preferiría ser ilegible: para proteger "estrategia, precios, inventario". Es una razón de **secreto competitivo**. `sistemas-para-humanos-saturados-por-agentes` no discute legibilidad en absoluto — discute a quién dejar entrar y verificar.

Juntos exponen una segunda razón para preferir cierta ilegibilidad que ninguno de los dos nombra: no proteger información sensible, sino **protegerse de la carga**. La legibilidad de máquina no distingue entre el agente que consulta disponibilidad una vez para un cliente real y el que lo hace doscientas veces buscando el momento óptimo — ambos usan exactamente el mismo canal, con exactamente la misma facilidad. Esto significa que la ventaja competitiva que describe `legibilidad-de-maquina` no es gratuita: cada unidad de legibilidad agregada para atraer demanda legítima es, simultáneamente, una unidad de legibilidad disponible para quien quiera abusar de ella. No hay una perilla que suba una sin la otra.

## El límite

Esta correlación no implica que valga la pena sacrificar legibilidad para evitar saturación — `legibilidad-de-maquina` documenta que la pérdida de negocio por baja legibilidad es real y "silenciosa", mientras que el costo de la saturación (rate-limits, infraestructura adicional) suele ser más visible y más fácil de justificar resolver de otras formas (como, precisamente, la identidad verificable que discute `sistemas-para-humanos-saturados-por-agentes`). El límite es que esta tensión solo es aguda en servicios con lo que el concepto nuevo llama "alta fricción natural" —reservas, citas, inventario limitado—, donde consultar más rápido tiene valor real para quien sondea. Una API de solo lectura sobre datos no escasos (clima, tipo de cambio) puede maximizar legibilidad sin este problema, porque no hay nada que "ganar" sondeándola más seguido.

---

_Propuestas generadas por pedido explícito de Luigui ("dame 3 correlaciones a partir de este nuevo concepto"), no por la rutina automática "busca correlaciones". Requieren revisión y aprobación antes de escribir en `Correlaciones/`._
_Para aprobar: `Jarvis, revisa propuestas pendientes`_
