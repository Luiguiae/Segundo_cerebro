---
titulo: El agente como carpeta
tipo: concepto
fecha: 2026-08-17
familia: agencia-ia
estado: activo
tags: [ia, agentes, arquitectura, diseño, arnes]
relacionado: [arnes-del-agente, spec-driven-development, espectro-autonomia-agente]
fuentes:
  - titulo: "Un agente es una carpeta — Josemaría Lucas (Co-Founder, Tuio)"
    url: "https://www.linkedin.com/in/josemarialucas"
    fecha_acceso: 2026-08-17
    nota: "Post de LinkedIn ilustrado con el framework Managed Deep Agents (concepto 'Your agent is a folder')"
---

# El agente como carpeta

## El concepto

Durante los primeros dos años de agentes de IA en producción, la pregunta de diseño dominante era conductual: qué puede hacer el agente, qué reglas sigue, cuándo debe pedir confirmación. Esa es la capa que ya cubre el arnés del agente. Pero hay una pregunta anterior, más fundamental, que rara vez se hace explícita: **¿de qué está hecho un agente, literalmente, como artefacto de software?**

La respuesta que propone el framework "Managed Deep Agents" —y que Josemaría Lucas resume con precisión quirúrgica— es incómodamente simple: **un agente es una carpeta.** No una metáfora. Una estructura de archivos real:

```
support-agent/
  agent.py
  instructions.md
  tools/query_db.py
  middleware/audit.py
  schedules/daily_check_in.py
  skills/research/SKILL.md
  sandbox/setup.sh
```

Instrucciones, herramientas, skills, middleware, schedules, memoria, identidad, canales, sandboxes, evals — todo son archivos dentro de un directorio. El agente no "vive" en ningún sitio. No es un proceso. No es un servicio. Es una **definición estática de comportamiento**, tan inerte como cualquier código fuente sin compilar.

Lo que le da vida es el **harness**: el runtime que recorre esa carpeta y la ejecuta. El harness planifica, invoca herramientas, gestiona el filesystem, delega en subagentes, y mantiene checkpoints de estado. Sin harness, la carpeta es solo texto. Con harness, es un agente capaz de correr durante horas o días, fallar, recuperarse, y continuar donde se quedó.

El cambio conceptual es sutil pero profundo: pasamos de *"un agente es un programa que razona"* a *"un agente es una carpeta de configuración que un runtime interpreta."*

## Por qué importa

Esta separación arquitectónica —carpeta declarativa vs. runtime con estado— tiene consecuencias de diseño que no son obvias hasta que se nombran:

**Un agente se vuelve versionable como código.** Si el agente es una carpeta, se puede hacer `git diff` sobre su comportamiento. Un cambio en `instructions.md` es una línea modificada, revisable en un pull request, con historial de quién cambió qué y cuándo. Esto es cualitativamente distinto de auditar cambios en un flujo conversacional o en una configuración oculta dentro de una UI de producto.

**La pregunta de diseño se bifurca en dos preguntas independientes.** "¿Qué debe saber y poder hacer este agente?" (la carpeta: instrucciones, tools, skills, memoria) es una decisión distinta de "¿qué motor lo ejecuta y con qué garantías de runtime?" (el harness: planificación, checkpointing, gestión de subagentes). La misma carpeta puede, en principio, correr sobre distintos harnesses — lo que separa la propiedad intelectual del comportamiento de la infraestructura que lo ejecuta.

**Baja la barrera de quién puede construir un agente.** Estructurar una carpeta con markdown y archivos de configuración es una habilidad más accesible que diseñar arquitecturas de prompting o cadenas de razonamiento. Esto tiene el mismo efecto democratizador que ya documentaste en `vibe-coding` y `spec-driven-development`, pero aplicado específicamente a la construcción de agentes.

## Datos y evidencia

- **Managed Deep Agents (framework citado):** propone una composición explícita del agente en diez categorías de archivo — Instructions, Tools, Skills, Memory, Middleware, MCP connectors, Sandboxes, Identity, Channels, Schedules, Evals — cada una controlando una dimensión distinta: contexto, capacidades, invocación y verificación.
- **Flujo de construcción documentado:** el framework reduce la creación de un agente a cuatro pasos estandarizados — `mda init` (inicializar), elegir qué archivos necesita, `mda dev` (correr localmente), `mda deploy` (desplegar) — un flujo que espeja directamente el ciclo de desarrollo de software convencional, no un proceso de diseño conversacional.
- **Separación runtime/definición:** el hosted runtime, la persistencia backend y el despliegue son responsabilidad explícita de la infraestructura ("Managed for you"), mientras que la definición de comportamiento vive enteramente en archivos que el equipo de producto controla y versiona.

## Tensiones y límites

**Relación de complementariedad con `arnes-del-agente`:** ese concepto opera en la capa de comportamiento —qué puede hacer el agente, cuándo debe confirmar, qué nunca puede hacer. Este concepto opera en una capa anterior: de qué está hecho el agente como artefacto. No son el mismo concepto con nombres distintos: el arnés es el contenido de ciertos archivos dentro de la carpeta (por ejemplo, `middleware/` y las reglas que codifica); la carpeta es la arquitectura completa que aloja ese arnés junto con memoria, identidad, herramientas y programación. Diseñar bien el arnés no garantiza una buena arquitectura de carpeta, y viceversa.

**Tensión con la ilusión de simplicidad:** decir "un agente es una carpeta" suena a que construir agentes es tan simple como crear archivos de texto. La complejidad real no desaparece — se desplaza al harness, que debe resolver problemas genuinamente difíciles de sistemas distribuidos: checkpointing confiable, recuperación ante fallos, coordinación de subagentes, gestión de memoria a largo plazo. La carpeta hace visible y editable la superficie de comportamiento; no simplifica la ingeniería de ejecución subyacente.

**Límite del concepto:** esta arquitectura asume un ecosistema donde existe un runtime capaz de interpretar la carpeta de forma confiable —hoy, eso significa depender de un proveedor de harness específico (propio o de terceros). La portabilidad real de "la misma carpeta corriendo sobre distintos harnesses" es todavía más promesa que práctica extendida, comparable a la fragmentación temprana de estándares en cualquier ecosistema de infraestructura nuevo.

## Ejes investigados

- Distinción arquitectónica entre la carpeta (definición estática, declarativa) y el harness (runtime con estado) como las dos mitades constitutivas de un agente moderno
- Composición explícita en diez categorías de archivo, cada una controlando una dimensión distinta del agente: contexto, capacidades, invocación, verificación (framework Managed Deep Agents)
- Consecuencias de versionar comportamiento de agente como código: auditabilidad, revisión por pares, historial de cambios
- Relación de complementariedad, no sustitución, con el concepto de arnés del agente como capa de reglas de comportamiento
- Democratización de la construcción de agentes: de arquitectura de prompting a estructuración de archivos y carpetas
