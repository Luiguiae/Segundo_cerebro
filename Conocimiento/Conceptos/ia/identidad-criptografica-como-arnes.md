---
titulo: Identidad criptográfica como arnés
tipo: concepto
fecha: 2026-07-27
familia: agencia-ia
estado: activo
tags: [ia, agentes, identidad, arnes, seguridad]
relacionado: [representacion-agente, arnes-del-agente, workforce-de-agentes]
fuentes:
  - titulo: "Block Launches Buzz: Open-Source Workspace Where AI Agents Sign Their Own Work — Tech Times"
    url: "https://www.techtimes.com/articles/321242/20260722/block-launches-buzz-open-source-workspace-where-ai-agents-sign-their-own-work.htm"
    fecha_acceso: 2026-07-27
  - titulo: "Jack Dorsey's Block Launches Buzz, an Open Source Workspace — Coin Edition"
    url: "https://coinedition.com/jack-dorseys-block-launches-buzz-an-open-source-workspace/"
    fecha_acceso: 2026-07-27
  - titulo: "Dorsey's Block Turns AI Agents Into Real Employees — PYMNTS"
    url: "https://www.pymnts.com/news/artificial-intelligence/2026/dorseys-block-turns-ai-agents-into-real-employees/"
    fecha_acceso: 2026-07-27
    nota: "Lanzamiento de Buzz, Block, 21 de julio de 2026"
---

# Identidad criptográfica como arnés

## El concepto

La práctica más común para desplegar agentes de IA en un flujo de trabajo real es entregarles las credenciales de un humano: la cuenta de Slack de alguien, el login de GitHub de alguien, la API key de alguien. Un ingeniero de Block que trabajó en el lanzamiento de Buzz lo describió sin rodeos como una práctica "rara" y "peligrosa" — el agente actúa bajo el nombre de una persona, y cuando algo sale mal, no hay forma limpia de distinguir qué hizo el humano de qué hizo la máquina.

Buzz, el workspace de agentes lanzado por Block (la empresa de Jack Dorsey) en julio de 2026, propone una solución estructural distinta: cada agente recibe su propia **identidad criptográfica**, separada de la de su dueño humano. El dueño firma una autorización de alcance limitado — "este agente puede hacer X, en este canal, con estos permisos" — y a partir de ahí, el agente firma su propio trabajo bajo su propia identidad. Cada mensaje, cada commit, cada acción queda registrado con la firma del agente, no con la del humano que lo desplegó.

El mecanismo técnico corre sobre Nostr, un protocolo descentralizado donde cada participante —humano o agente— posee un par de claves que le pertenece a él, no a la plataforma. Block identificó esto como el "problema más fundamental" del trabajo multi-agente: no es la capacidad de los agentes, es la identidad. Sin una respuesta clara a "quién es este agente y quién lo autorizó", ninguna otra pregunta sobre gobernanza, permisos o responsabilidad tiene una base sólida sobre la cual construirse.

La identidad criptográfica funciona aquí como una forma de arnés — no un conjunto de reglas de comportamiento, sino la infraestructura de identidad y autorización que hace posible aplicar reglas de comportamiento de manera verificable y auditable.

## Por qué importa

El diseño resuelve un problema práctico con una consecuencia de gobernanza importante: la **revocabilidad granular**. Si la clave de un agente se ve comprometida, el equipo puede revocar exclusivamente ese agente sin tener que reemplazar la identidad humana completa detrás de él. Esto es estructuralmente distinto de revocar el acceso de un empleado, cuya identidad y credenciales suelen estar entrelazadas con docenas de sistemas y permisos heredados.

El otro efecto es sobre la trazabilidad. Cuando un agente actúa bajo identidad propia, cada acción queda vinculada de forma verificable a quién lo autorizó y en qué momento — sin necesidad de reconstruir logs dispersos o adivinar quién copió y pegó qué en qué chat. En un contexto donde el 95% de ejecutivos encuestados dice que la IA está cambiando roles y estructuras de equipo, y donde la ley de responsabilidad de agentes de IA todavía se está formando, la capacidad de responder con precisión "qué humano autorizó a este agente a hacer esto, y cuándo" deja de ser un diferencial de producto y empieza a convertirse en requisito de cumplimiento.

## Datos y evidencia

- **Buzz (Block, julio 2026):** cada agente recibe una identidad criptográfica separada de su dueño humano, construida sobre el protocolo descentralizado Nostr. La identidad, el historial y la reputación del agente pueden viajar a través de cualquier sistema compatible con Nostr — no están capturadas dentro de una sola plataforma propietaria.
- **Diseño de autorización de alcance limitado:** el dueño humano firma una autorización específica y acotada; el agente firma su propio trabajo bajo su propia identidad. Esto separa estructuralmente "quién autorizó" de "quién ejecutó", preservando ambos en un registro verificable.
- **Contexto regulatorio:** Writer (mayo 2026) encuestó ejecutivos y encontró que el 95% reporta que la IA está cambiando roles y estructuras de equipo en sus organizaciones — evidencia del contexto de urgencia en el que emergen soluciones de identidad como esta.
- **Modelo y arnés agnósticos:** Buzz soporta agentes construidos sobre cualquier modelo o arnés — incluyendo Claude Code, Codex, y goose (el framework de agentes open source de Block) — lo que sugiere que la identidad criptográfica se está posicionando como capa de infraestructura independiente de qué modelo específico impulsa al agente.

## Tensiones y límites

**Tensión con `arnes-del-agente`:** ese concepto define el arnés como el sistema de reglas, herramientas, permisos y guardrails que constituye el artefacto central de diseño cuando el producto es un agente. Este concepto propone que, antes de poder diseñar ese arnés de forma verificable, se necesita una capa de identidad que permita saber con certeza quién es el agente y quién lo autorizó. La identidad criptográfica no reemplaza al arnés de comportamiento — es la infraestructura que hace posible auditar si el arnés se respetó.

**Tensión con `representacion-agente`:** ese concepto plantea el problema general de identidad y autorización cuando un agente actúa en nombre de una persona ante otros agentes. Este concepto es la primera instancia de producción de una solución técnica específica a ese problema — pero resuelve solo la capa de identidad y autorización, no resuelve automáticamente la capa de confianza: que un agente tenga una firma verificable no garantiza que su comportamiento sea correcto o seguro, solo que sus acciones son trazables.

**Límite del concepto:** el mecanismo resuelve trazabilidad y revocabilidad, no calidad de las decisiones del agente. Un agente con identidad criptográfica impecable puede seguir tomando decisiones equivocadas dentro del alcance que se le autorizó — la identidad clarifica responsabilidad, no previene el error de origen (ver `llm-como-motor-de-plausibilidad`).

## Ejes investigados

- Mecanismo técnico: identidad criptográfica sobre protocolo descentralizado Nostr como respuesta al problema de "credenciales prestadas" (Block, Buzz, julio 2026)
- Distinción entre autorización de alcance limitado (firmada por el humano) y ejecución firmada (por el agente) como separación estructural de responsabilidad
- Revocabilidad granular como propiedad emergente de la identidad separada: revocar un agente sin afectar la identidad humana subyacente
- Contexto regulatorio emergente: la trazabilidad de autorización como futuro requisito de cumplimiento, no solo buena práctica de diseño
- Relación con el diseño de arneses de comportamiento: identidad como precondición de auditabilidad, no como sustituto de reglas de comportamiento
