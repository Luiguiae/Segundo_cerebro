# Candidatos — Transcript Taller 2026-09-01 16:05

> Archivo temporal. No instalar en Conocimiento/Conceptos/ hasta revisión explícita.
> Transcript: voz con OCR ruidoso — las citas reflejan el texto crudo aunque esté fragmentado.

---

## Cuello de botella que migra aguas arriba

Cuando se acelera una etapa del ciclo de desarrollo (p. ej., con agentes de IA), las etapas previas —discovery, diseño, refinamiento de backlog— se convierten en el nuevo cuello de botella. La aceleración no desaparece: se desplaza hacia arriba en el flujo.

> "generar cuellos de botella aguas arriba... cómo en la medida que yo acelere un poco pues todos los ciclos de desarrollo... de repente pues se me acumulan las historias o puede ser que discovery o diseño porque de repente necesito más backlog porque el equipo de desarrollo pues tiene capacidad" — 16:08:17 / 16:08:33

---

## Contrato de API como habilitador de desarrollo en paralelo

Publicar los contratos de API en un repositorio centralizado permite que un equipo de desarrollo inicie su trabajo sin esperar a que el equipo propietario de la API esté disponible para integrarse. El contrato desacopla la dependencia temporal entre equipos.

> "yo puedo ir avanzando... a partir del contrato... los contratos de las apis están publicadas en una web que el [banco] maneja... centralizadas todas las apis del ecosistema... yo necesito consumir el api... me descargo el contrato... comenzar mi desarrollo ahora" — 16:28:34 / 16:29:10

---

## Usuarios sintéticos como desbloqueador de research

La dificultad de reclutar usuarios reales para entrevistas de diseño (por acceso, seguridad o volumen) actúa como stopper recurrente en múltiples cronogramas. Los usuarios sintéticos se nombran como estrategia para desbloquear ese cuello de botella sin depender del acceso a la población real.

> "sobre usuarios sintéticos porque uno de los stoppers que siempre tenemos son como las entrevistas con usuarios... también tenemos como una brecha para poder contactar usuarios, no es súper complejo poder contactar usuarios del [segmento] mayorista" — 16:34:06 / 16:34:26

---

## Contexto persistente del agente entre sesiones

Un agente que retiene el contexto de sesiones anteriores —sobre la arquitectura, el estilo de código, las convenciones del equipo— elimina el costo de re-explicar en cada sesión y hace que su utilidad sea acumulativa en vez de reiniciarse. Se nombra explícitamente como diferenciador frente a herramientas como GitHub Copilot.

> "de una sesión a otra el [contexto] que no se pierde... que no necesariamente [depende de] los temas de adopción... la lógica es poder... que sean reutilizables entre todos" — 16:19:31 / 16:19:42

---

## Piloto de un microservicio como prueba de transferibilidad

La estrategia de validar un agente en un solo equipo reducido (3 personas, un microservicio o un front) antes de escalar al resto del squad. La lógica: si funciona en un contexto acotado, el patrón es transferible sin rediseño. El piloto actúa como prueba de concepto estructural, no solo de funcionalidad.

> "solo tres personas se dedican a afinar al agente; si llega a funcionar para un microservicio o un front, va a funcionar para el resto" — 16:59:26

---

## Discovery cerrado como condición de aceleración

Para que los agentes de IA aceleren el desarrollo, el discovery debe estar cerrado. Si el "qué construir" todavía está abierto, la aceleración pierde su ancla y puede reabrir etapas ya resueltas. El principio nombrado explícitamente: los agentes optimizan el "cómo", no el "qué".

> "no necesitamos hacer nada de discovery, es enfocar mucho ahí en desarrollo" — 16:47:06
> "siento que en esta iniciativa en particular esos temas ya están resueltos y más bien en lo que tendríamos que dar foco es en cómo desarrollamos" — 16:37:26
