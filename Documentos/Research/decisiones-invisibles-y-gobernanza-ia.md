---
titulo: "Decisiones invisibles y gobernanza IA"
tipo: research
estado: borrador
autor: Luigui Avila
fecha: 2026-03-04
updated: 2026-03-04
tags: [gobernanza, decisiones, ia, organizaciones, fragilidad, delegacion]
fuentes:
  - autor: "Gustavo Soto Miño"
    titulo: "La urgencia de decidir"
    url: "https://laurgencia.digital/"
---

# Decisiones invisibles y gobernanza IA

Hipótesis exploratoria a partir de "La urgencia de decidir" (Gustavo Soto Miño).

---

## Hipótesis central

La inteligencia artificial no crea el problema decisional en las organizaciones — lo **hereda y lo amplifica**. El verdadero problema era preexistente: las organizaciones ejecutan decisiones que nadie declaró como decisiones. Cuando la IA entra al sistema, esas decisiones escalan con consistencia industrial, sin fricción humana que frene el daño.

> "No hay ninguna versión futura de la IA que elimine la necesidad de criterio humano explícito sobre qué debe hacer el sistema, por qué y con qué límites."

---

## Preguntas abiertas

- ¿Cuántas decisiones en un flujo de producto existen como "norma heredada" sin que nadie las haya validado explícitamente?
- ¿Cómo se distingue, en la práctica, una decisión tomada intencionalmente de una que simplemente *ocurrió*?
- ¿Qué parte del backlog de un producto es en realidad deuda decisional, no deuda técnica?
- ¿Puede el Espectro de Delegación aplicarse a nivel de prompt engineering, no solo de arquitectura organizacional?

---

## Marco: Los 4 tipos de decisiones invisibles

Soto Miño propone una taxonomía para nombrar lo que el sistema decide cuando nadie está mirando:

| Tipo | Señal | Riesgo | Frecuencia |
|---|---|---|---|
| **Heredadas** | "siempre fue así" | Bajo | Alta |
| **Diferidas** | "eso nunca quedó del todo definido" | Medio | Silenciosa |
| **Fragmentadas** | "cada equipo hizo lo suyo" | Medio | Difícil de trazar |
| **Automatizadas** | "el modelo lo decidió" | Alto | Las más urgentes |

Las **automatizadas** son las más críticas porque son las únicas que escalan sin fricción humana.

---

## Contexto: El margen que desapareció

Las organizaciones funcionaban con tres tipos de colchón que absorbían malas decisiones:

1. **Margen de tiempo** — para corregir lo que se construyó mal
2. **Margen de presupuesto** — para compensar decisiones no del todo pensadas
3. **Margen de paciencia** — de usuarios, mercado y organización

Tres fuerzas comprimieron ese margen simultáneamente:
- **Usuarios** formados por los mejores productos digitales del mundo que aplican ese estándar en todas partes
- **Capital** que dejó de financiar ambigüedad estratégica
- **IA** que comprimió ciclos completos (definición → diseño → construcción → validación → despliegue en paralelo)

Las tres fuerzas no llegan en secuencia: se superponen y amplifican entre sí.

---

## Conexión con fragilidad (Taleb)

Soto Miño cita a Taleb sin desarrollarlo. La hipótesis implícita: los sistemas organizacionales que acumulan decisiones invisibles son **frágiles** en el sentido técnico del término — bajo presión, no solo fallan sino que fallan *más de lo esperado*.

La IA convierte una mala decisión local en una instrucción que el sistema sigue con fidelidad implacable. La fragilidad se vuelve sistémica.

**Pregunta sin responder:** ¿Existe el equivalente a la "antifragilidad" decisional? ¿Qué haría que un sistema organizacional *mejore* bajo la presión de la IA?

---

## Tensiones y limitaciones del marco

- Nombrar el problema no lo resuelve. El propio autor reconoce haber visto organizaciones que nombran bien sus disfunciones y las reproducen con consistencia.
- El marco es diagnóstico más que prescriptivo. Las tres herramientas propuestas (Espectro, Ciclo, Cadencia) son operativas pero no abordan la resistencia política a hacer explícito lo implícito.
- No queda claro cómo escalar el Ciclo de Gobierno en organizaciones donde "nombrar" una decisión implica visibilizar errores de quienes tienen poder.

---

## Se conecta con...

- **Wayta IA** → El principio *el motor decide, la IA narra* es la implementación concreta del Espectro de Delegación. Las reglas deterministas del motor son criterio humano explícito antes de delegar.
- **Usuarios sintéticos (ADR-001)** → Las decisiones automatizadas son el riesgo exacto que el marco de gobernanza de usuarios sintéticos intenta prevenir. El Ciclo de Gobierno podría formalizar la revisión de simulaciones.
- **Synthetic Reconstruction (ADR-005)** → El concepto de fragilidad aplica directamente al riesgo de leer estimados SR como certezas. Sin incertidumbre explícita, el sistema es frágil.
- **Diseñador Constructor** → La charla en proceso asume que ganar velocidad técnica es suficiente. Este marco agrega la tensión faltante: velocidad sin gobernanza decisional amplifica errores a escala.
- `Documentos/Procesos/ciclo-gobierno-decisiones-ia.md` → operacionalización del Ciclo de Gobierno

---

## Mis notas

El argumento más potente del texto no es la taxonomía sino la tesis del margen: durante años las malas decisiones *funcionaban* no porque fueran correctas sino porque el sistema tenía colchones para absorber sus consecuencias. La IA no crea fragilidad — **revela la fragilidad que ya existía**.

Esto tiene implicaciones directas para cómo se presenta el valor de la gobernanza: no como overhead burocrático sino como lo que permite que la velocidad sea sostenible.

Pendiente explorar: si el Ciclo de Gobierno (Nombrar → Asignar → Ejecutar → Revisar) se puede mapear como un ADR en movimiento — es decir, si la cadencia semanal es la versión operativa de lo que los ADRs hacen a nivel arquitectónico.
