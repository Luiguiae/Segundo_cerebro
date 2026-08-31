# Borradores revisados — 2026-08-31

Primera corrida real de "gradúa los borradores" (comando implementado 2026-08-24, nunca ejecutado antes — confirmado por ausencia de entradas "graduador" en `JARVIS_LOG.md`). Ningún borrador tenía intento de graduación en los últimos 14 días, así que se revisaron los 4 existentes: 2 conceptos, 2 correlaciones.

Revisados: 4 · Graduados: 1 · Sin graduar: 3

---

## Graduados

### `Conceptos/organizaciones/rutina-trabajo-enfocada.md`

**Diagnóstico previo** (`JARVIS_LOG.md`, auditoría 2026-08-24): Gate 2 2/4 — "no agrega interpretación propia (solo describe) y la 'tensión' es boilerplate genérico sin mecanismo".

**Eje investigado (1, acotado al hueco diagnosticado):** mecanismo cognitivo detrás del costo de interrumpir el foco — por qué una rutina de trabajo enfocada es una necesidad funcional medible y no una preferencia de estilo, y cuál tensión específica genera con la coordinación de un equipo pequeño. 2 fuentes sólidas, ambas con autoría e institución verificables:
- Sophie Leroy (2009), *Organizational Behavior and Human Decision Processes*, 109(2) — "attention residue": el residuo de atención de una tarea inconclusa degrada medible el desempeño en la siguiente tarea.
- Gloria Mark, Daniela Gudith, Ulrich Klocke — University of California Irvine, CHI 2008 — 23 minutos y 15 segundos promedio para retomar por completo una tarea tras una interrupción.

**Qué cambió:**
- `## El concepto`: ahora ancla la definición en el mecanismo de attention residue (Leroy) en vez de describir la rutina enfocada en abstracto.
- `## Por qué importa`: agrega el costo cuantificado (23min15s de reingreso, Mark et al.) y lo conecta con la razón de ser de un equipo pequeño (juicio de criterio, no solo ejecución).
- `## Tensiones y límites`: reemplaza la tensión genérica ("difícil en entornos con distracciones... rigidez puede ser perjudicial") por una tensión específica con mecanismo: la disponibilidad para desbloquear a otros en `equipos-pequenos-alto-impacto` compite directamente con el foco protegido, porque cada interrupción cuesta ~23min de reingreso a quien la recibe — no hay resolución limpia, solo el límite práctico de que debe ser acuerdo explícito del equipo, no disciplina individual.
- Nuevas secciones `## Datos y evidencia` y `## Ejes investigados` (estructura Gen-4).
- `fuentes:` agregado al frontmatter con las 2 fuentes.
- `estado: borrador → activo` (propuesto).
- Sin cambios en `tags`, `relacionado`, `familia` — ya eran válidos contra `taxonomia.md`.

**Contenido completo propuesto:**

```markdown
---
titulo: "Rutina de trabajo enfocada"
tipo: concepto
familia: equipos-impacto
tags:
  - trabajo
  - productividad
relacionado:
  - disenador-a-constructor
  - equipos-pequenos-alto-impacto
fecha: 2026-06-25
estado: activo
fuentes:
  - titulo: "Why is it so hard to do my work? The challenge of attention residue when switching between work tasks"
    autor: "Sophie Leroy — Organizational Behavior and Human Decision Processes, 109(2)"
    url: "https://www.sciencedirect.com/science/article/abs/pii/S0749597809000399"
    fecha_acceso: 2026-08-31
  - titulo: "The Cost of Interrupted Work: More Speed and Stress"
    autor: "Gloria Mark, Daniela Gudith, Ulrich Klocke — University of California, Irvine (CHI 2008)"
    url: "https://ics.uci.edu/~gmark/chi08-mark.pdf"
    fecha_acceso: 2026-08-31
---

## El concepto
La rutina de trabajo enfocada es la práctica de proteger bloques de tiempo ininterrumpido para una sola tarea, en vez de tratar el foco como un recurso que se recupera instantáneamente al volver a una tarea interrumpida. No es una preferencia de estilo personal: responde a un mecanismo cognitivo específico. Leroy (2009) documenta el "attention residue" — cuando alguien cambia de la Tarea A a la Tarea B sin haber cerrado A, una porción de la atención permanece fija en la tarea inconclusa, y ese residuo degrada medible el desempeño en B. El efecto es más fuerte cuando la tarea abandonada estaba bajo presión de tiempo, inconclusa, o cargada emocionalmente — que es exactamente el perfil de la mayoría de interrupciones de trabajo real (un mensaje urgente, una reunión que corta a mitad de una tarea compleja). La rutina de trabajo enfocada, entendida así, no es "trabajar sin distraerse" en abstracto: es el diseño deliberado de cierres de tarea completos antes de cada cambio de contexto, precisamente para evitar generar el residuo que Leroy mide.

## Por qué importa
El costo de no proteger estos bloques no es difuso, es cuantificable. Mark, Gudith y Klocke (2008), observando trabajadores de oficina en tiempo real, midieron que después de una interrupción se necesitan en promedio 23 minutos y 15 segundos para retomar por completo la tarea original — y que en ese intervalo la persona típicamente pasa por dos tareas intermedias antes de volver a la original, no un regreso directo. Eso significa que una rutina de trabajo con interrupciones frecuentes no reduce el tiempo disponible en la proporción de las interrupciones mismas — lo reduce en la proporción de las interrupciones más el tiempo de reingreso a cada tarea que quedó abierta. Para equipos pequeños que dependen de que cada persona produzca trabajo de criterio (no solo ejecución), ese costo de reingreso compite directamente con la razón por la que el equipo es pequeño: si el valor del equipo está en el juicio individual aplicado con profundidad, fragmentar ese juicio en bloques de atención residual lo devalúa antes de que llegue a producir algo.

## Tensiones y límites
La tensión no es "distracción vs. disciplina" en abstracto — es un conflicto de mecanismo específico entre dos necesidades reales de un equipo pequeño. La coordinación rápida que `equipos-pequenos-alto-impacto` requiere (una pregunta resuelta en el chat, una decisión desbloqueada en minutos) depende de que las personas estén disponibles para interrumpirse mutuamente. Pero cada interrupción, según Mark et al. (2008), impone ~23 minutos de reingreso a quien la recibe. Un equipo que optimiza agresivamente por disponibilidad instantánea genera, por diseño, el mismo residuo de atención que degrada el trabajo de criterio que se supone que ese equipo debe producir. No hay una resolución limpia: proteger bloques de foco reduce la disponibilidad para desbloquear a otros; maximizar disponibilidad fragmenta el foco de quien está disponible. El límite práctico es que la rutina de trabajo enfocada solo funciona si el equipo la trata como acuerdo explícito y mutuo (ventanas conocidas de no-interrupción), no como disciplina individual — porque una sola persona protegiendo su foco en un equipo que no coordina alrededor de eso solo desplaza el costo de interrupción a quien sí está disponible.

## Datos y evidencia
- El "attention residue" mide una caída de desempeño en la tarea siguiente cuando la tarea previa quedó inconclusa al momento del cambio; el efecto es mayor cuanto más inconclusa, urgente o emocionalmente cargada estaba la tarea abandonada — Sophie Leroy, *Organizational Behavior and Human Decision Processes*, 109(2), 2009 [sin cifra porcentual única reportada por la fuente consultada; el hallazgo es la existencia y dirección del efecto, medido en múltiples experimentos de laboratorio].
- Tiempo promedio para retomar por completo una tarea después de una interrupción: 23 minutos y 15 segundos, con dos tareas intermedias de por medio antes de volver a la tarea original — Gloria Mark, Daniela Gudith y Ulrich Klocke, University of California Irvine, *CHI 2008* ("The Cost of Interrupted Work: More Speed and Stress").

## Ejes investigados
- **Eje 1 — mecanismo cognitivo del costo de interrumpir el foco:** por qué una rutina de trabajo enfocada es una necesidad funcional y no una preferencia de estilo, y cuál es el costo medido de no protegerla. 2 fuentes sólidas encontradas (Leroy 2009; Mark, Gudith & Klocke 2008), ambas con autoría y afiliación institucional verificables.
- Ejes no investigados en esta pasada (fuera del hueco diagnosticado): comparación entre técnicas de bloqueo de tiempo (Pomodoro, timeboxing) y su efectividad relativa; efecto de la rutina de trabajo enfocada en roles no cognitivos.
```

**Evaluación Gate 2 nueva (concepto, necesita ≥3/4):**
1. No es un resumen (agrega interpretación) — **PASA**: ancla el argumento en un mecanismo específico (attention residue) y lo conecta con la tensión concreta de equipos pequeños, no solo describe.
2. Tiene tensión interna real — **PASA**: la tensión ahora tiene mecanismo cuantificado (disponibilidad vs. costo de reingreso de 23min), no es boilerplate.
3. Relacionable — **PASA**: `equipos-pequenos-alto-impacto` y `disenador-a-constructor` existen y ambos activos.
4. Transferible — **PASA**: autocontenido, no asume contexto de sesión.

**4/4 — supera el mínimo de 3/4.**

---

## Sin graduar

### `Conceptos/ia/gestion-del-tiempo.md`

**Diagnóstico previo:** falla Gate 1 criterio "Propio" — "contenido genérico tipo listicle, sin fuente ni mecanismo específico, sin conexión temática a IA pese a vivir en `Conceptos/ia/`".

**Qué se intentó:** ninguna profundización dirigida — se evaluó primero si el hueco era del tipo que "profundización acotada a 1-2 ejes" puede cerrar, y no lo es. El fallo diagnosticado es de identidad del archivo completo, no un hueco de evidencia puntual: el cuerpo entero (las tres secciones) es una definición genérica de gestión del tiempo sin ningún mecanismo específico, sin voz propia, y sin ninguna conexión a IA — el tema por el que vive en la carpeta `ia/`. Cerrar ese hueco requeriría reemplazar el argumento central completo (reescribir el concepto desde otro ángulo, o mudarlo de carpeta/tema), que el procedimiento de graduación prohíbe explícitamente ("no una reescritura genérica... no reemplaza el argumento central").

**Qué sigue faltando:** el concepto necesita, o (a) una reescritura completa con un mecanismo propio y conexión real a IA (ej. cómo la gestión del tiempo cambia específicamente cuando el trabajo se comparte con agentes — que es un tema real del vault, ver `capital-de-contexto`, `pit-stop-cognitivo`), o (b) reubicación fuera de `ia/` si el argumento se mantiene genérico. Ambas opciones son decisión de contenido de Luigui, no de graduación automática.

---

### `Correlaciones/2026-06-25_agentes-ia--capital-de-contexto.md`

**Diagnóstico previo:** "la 'tensión' es una relación de dependencia, no una contradicción real (título equivalente a '[A] and [B]'); la síntesis es un truismo genérico".

**Qué se intentó:** ninguna profundización — el hueco diagnosticado es estructural (Gate 2 correlación, criterio 1: "tensión real, no co-ocurrencia"), no una falta de datos o fuentes. Ninguna cantidad de evidencia adicional convierte una relación de dependencia genuina en una contradicción; eso requiere re-concebir la relación completa entre los dos conceptos, que es "profundizar concepto" aplicado a una correlación — fuera del motor que este comando usa (el motor es para conceptos, no para correlaciones, y el propio procedimiento solo autoriza profundización "acotada a 1-2 ejes" sobre huecos de evidencia, no sobre la validez del argumento central).

**Qué sigue faltando:** una tensión real entre `agentes-ia` y `capital-de-contexto` (si existe) requiere lectura y redacción manual — mismo motor que "Correlacionar conceptos", no "graduar borradores". Nota adicional: el patrón se repite en 4 correlaciones más de este mismo vault contra `capital-de-contexto` (auditoría 2026-07-06 y 2026-08-24), todas rechazadas por el mismo motivo — sugiere que `capital-de-contexto` combina mal con pares generados por señal automática de tags/familia, y probablemente necesita correlaciones redactadas manualmente en vez de propuestas por el buscador automático.

---

### `Correlaciones/2026-06-25_gestion-del-tiempo--capital-de-contexto.md`

**Diagnóstico previo:** "mismo patrón: tensión superficial, aplicaciones genéricas sin especificidad del vault, síntesis obvia".

**Qué se intentó:** ninguna profundización — mismo motivo estructural que la correlación anterior (Gate 2 criterio 1), agravado porque uno de los dos conceptos (`gestion-del-tiempo`) tampoco graduó en esta misma corrida por las razones de arriba. Enriquecer una correlación que depende de un concepto sin voz propia ni mecanismo no resuelve el problema — hereda la debilidad del concepto base.

**Qué sigue faltando:** depende primero de que `gestion-del-tiempo.md` se resuelva (reescritura o reubicación). Recomendación: si `gestion-del-tiempo.md` se reescribe con un ángulo específico de IA, esta correlación puede reintentarse como "Correlacionar conceptos" manual; si se reubica o archiva, esta correlación pierde sentido y debería archivarse con ella.

---

_Generado automáticamente por Jarvis. Requiere revisión y aprobación de Luigui antes de sobrescribir el archivo original en `Conocimiento/` con el contenido graduado._
_Para aprobar: `Jarvis, revisa propuestas pendientes`_
