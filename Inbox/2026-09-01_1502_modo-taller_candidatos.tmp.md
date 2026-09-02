# Candidatos a concepto atómico — Taller 2026-09-01 15:02

Fuente: `Inbox/2026-09-01_1502_modo-taller_transcript.tmp.md`
Identificados: 7 candidatos

---

## Conocimiento tácito como cuello de botella técnico

El conocimiento crítico para resolver un problema técnico reside en la cabeza de un especialista, no en la documentación formal. Cuando ese especialista no está disponible, el equipo queda bloqueado o pierde tiempo buscando en fuentes dispersas que no tienen la respuesta.

> "ese tipo o ese dato puntual a veces estás en la cabeza de algún especialista que no los documenta a ningún lado, te topaste con él y te ayudó, pues él dio con la respuesta con la solución" — 15:36:24

---

## El funcionario como proxy de acceso al usuario final

En contextos B2B bancarios, el equipo de producto no puede contactar directamente al cliente empresarial. El funcionario de cuenta actúa como intermediario obligatorio para reclutar usuarios, agendar entrevistas y conseguir información. Esto introduce una capa de fricción y dependencia en todo el proceso de investigación.

> "no es tan fácil acceder a los clientes finales generando esa confianza no entonces lo mejor es hacerlo a través de los funcionarios" — 15:29:04

> "lo que hacemos es bastante por decirlo de alguna manera manual de contactar a sus funcionarios y preguntarle e insistirle ya sean seguimiento de que se ha averiguado" — 15:24:09

---

## Documentación dispersa como riesgo epistémico

Cuando la documentación técnica de un sistema vive en múltiples fuentes sin estructura unificada (doc oficial, SharePoint, Confluence, foros internos), el costo de encontrar la respuesta correcta supera frecuentemente el costo de resolver el problema mismo. La dispersión convierte el conocimiento en un bien inasequible aunque exista.

> "si hablamos de tecnologías asociadas a kubernetes tenemos su documentación oficial, por Confluence que están en SharePoint, tenemos documentación que está [...] entonces es muy dispersa esa documentación y a veces [...] ese dato puntual a veces estás en la cabeza de algún especialista" — 15:35:59

---

## Lecciones aprendidas atrapadas en foros

Las lecciones aprendidas de mayor valor práctico (soluciones a errores reales, workarounds de migración, decisiones técnicas) se depositan en foros conversacionales y no en documentación estructurada. El conocimiento existe, es accesible en el momento, pero no se preserva ni se hace buscable. Se trata de una forma de pérdida de conocimiento organizacional sistemática.

> "lecciones aprendidas que muchos roles o especialistas lo tienen en su cabeza o se quedan en foros [...] en foros alguien tiene un problema, pone el error que tiene y alguien le da la solución [...] y esa información muy valiosa que finalmente siento yo que se debería explotar en algún lado, tiene que estar guardado" — 15:39:36 / 15:40:05

---

## Tensión entre piloto incremental y exigencia de diseño completo

La arquitectura empresarial exige ver el diseño completo y final antes de aprobar cualquier implementación, aunque se trate de un piloto o fase inicial. Esto bloquea la lógica iterativa: el equipo quiere aprender construyendo por partes, pero el gate arquitectónico requiere la foto final desde el inicio. El resultado es que los tiempos se dilatan y la capacidad de pilotar hipótesis se anula.

> "siempre ellos quieren llegar a un rubí entonces por más que nosotros queramos implementar por ejemplo un piloto o una fase inicial siempre me van a decir quiero tener la foto" — 15:57:17

> "aquí es donde los tiempos se dilatan porque nosotros queremos hacer una epoc [...] nosotros no tenemos toda esa visibilidad, el modelo te dice tú me tienes que traer todo" — 15:57:41 / 15:58:14

---

## Orquestación y validación humana como nuevo modelo de trabajo con IA

El cambio de modelo propuesto no es que los humanos dejen de trabajar, sino que el tipo de trabajo cambia: de ejecución manual a orquestación y validación de agentes. Los humanos pasan a ser supervisores del output de sistemas automatizados en lugar de productores directos. Se nombra explícitamente como uno de los tres "cambios de modelo" del piloto.

> "de la gente de nosotros haciendo más la orquestación y validación de los robots que [trabajo] manuales" — 15:07:21

---

## Perfilamiento de cliente como construcción hipotética a validar

La definición del segmento objetivo para una iniciativa de producto se construye inicialmente como un conjunto de hipótesis basadas en variables internas (transacciones, tipo de producto, volumen) que pueden estar incompletas o ser incorrectas. El equipo de producto opera con una "foto probable" del cliente que debe refinarse con data externa que muchas veces no existe o no es accesible. El error en el perfil inicial se descubre tarde, en el reclutamiento o en las entrevistas.

> "ahí nosotros como productos definimos variables que tal vez no son al 100% correctas, no nos apoyamos mucho de la data [...] perdemos mucho tiempo en esa definición y en sincerar ese tipo de perfiles que finalmente [cambian]" — 15:25:17

> "lo difícil de conseguir es conocer a nuestro cliente, actualmente no tenemos una base consolidada de cómo son nuestros clientes" — 15:20:59
