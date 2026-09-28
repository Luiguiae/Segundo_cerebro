# Correlaciones propuestas — 2026-09-28

Candidatos evaluados: 17 (reconstruido el conjunto de exclusión completo leyendo los 29 pares con archivo en `Correlaciones/`, los 4 `Inbox/*_correlaciones-propuestas.tmp.md` existentes —2026-08-25, 2026-08-31, 2026-09-07, 2026-09-21— y las 5 entradas de `JARVIS_LOG.md` tituladas "busca correlaciones", incluida la del 2026-09-14 que no dejó `.tmp.md` por 0 sobrevivientes: 114 pares únicos ya evaluados en total. Sobre ese conjunto de exclusión, se regeneró desde cero el pool de mención cruzada —grep de slugs entre backticks sobre los 99 conceptos `estado: activo`— y aparecieron 16 pares con mención cruzada nunca evaluados antes: el vault siguió madurando entre corridas y generó nuevas menciones que no existían en 2026-09-21. Se sumó 1 candidato más por familia+3 tags compartidos entre los 2 sub-conectados de siempre —`capas-de-profundidad-sistemica` e `interdependencia-sistemica`, que nunca se habían emparejado entre sí en ninguna corrida—, priorizado por instrucción explícita de dar preferencia a esa pareja. Total: 17, bajo el tope de 20; no fue necesario bajar a señales más débiles.)

Sobrevivientes autocrítica adversarial: 1
Descartados: 16 — mismo patrón dominante que las corridas del 2026-09-07, 2026-09-14 y 2026-09-21: en los 16 casos, el archivo que menciona al otro concepto ya contiene la síntesis completa de la relación en su propia sección "Tensiones y límites" o "Por qué importa" (12 de 16 bajo un subtítulo literal `**Tensión con `[concepto]`:**` o `Tensiona con`/`Tensiona también con`/`Relación con`), incluyendo su resolución. El pool de mención cruzada de este vault parece seguir un patrón estructural: cuando Jarvis escribe un concepto que menciona a otro por su slug, casi siempre resuelve la relación ahí mismo en el momento de escribirlo — la mención cruzada sin resolución ya es la excepción, no la norma.

---

## 1. La profundidad correcta no frena el efecto dominó

**Par:** `capas-de-profundidad-sistemica` × `interdependencia-sistemica`

**Señales:** misma familia (`epistemologia-practica`) + 3 tags compartidos (`sistemas`, `marco`, `patron`) + ambos son los 2 únicos sub-conectados del vault (0-1 en `relacionado`, ambos con solo `arquitectura-de-inteligencia`) + nunca emparejados entre sí en ninguna de las 5 corridas previas de este comando.

**Justificación de la tensión real (1 línea):** `capas-de-profundidad-sistemica` asume que localizar el "nudo" en una capa (material, sociotécnica o sociocultural) es condición suficiente para diseñar una intervención no cosmética — pero `interdependencia-sistemica` niega que exista contención posible: cualquier modificación, sin importar en qué capa se dirija, puede propagarse por relaciones que no respetan fronteras de capa, incluyendo saltos hacia una capa distinta de la que se intervino. Ninguno de los dos textos nombra esta combinación.

---

```yaml
---
titulo: "La profundidad correcta no frena el efecto dominó"
tipo: correlacion
conceptos: [capas-de-profundidad-sistemica, interdependencia-sistemica]
fecha: 2026-09-28
tags: [sistemas, marco, patron, tension]
estado: borrador
---
```

# La profundidad correcta no frena el efecto dominó

## La tensión

`capas-de-profundidad-sistemica` propone que todo sistema se lee en tres niveles —material, sociotécnico, sociocultural— y que "diagnosticar en qué capa reside el nudo es condición para diseñar una intervención que no sea cosmética". El marco es implícitamente vertical: una vez localizada la capa correcta, el trabajo de diseño consiste en actuar ahí con precisión.

`interdependencia-sistemica` describe un eje distinto, horizontal: "ningún componente de un sistema tiene impacto aislado... modificar una pieza activa una cadena de efectos en el resto de la red, muchos de ellos no anticipados desde el punto de intervención" — la metáfora de la torre de Jenga, donde remover una pieza periférica puede colapsar el conjunto.

Ninguno de los dos conceptos dice explícitamente lo que pasa cuando se combinan: una intervención correctamente diagnosticada en profundidad (capas) puede seguir fallando porque las relaciones de interdependencia no están contenidas dentro de esa capa — pueden saltar hacia otra. Localizar el nudo en la capa sociotécnica no garantiza que el efecto de la intervención se quede en esa capa: puede propagarse hacia la capa material (un cambio de proceso que rompe una herramienta) o hacia la sociocultural (un ajuste técnico que se lee como una señal de poder). El diagnóstico vertical correcto no compra inmunidad frente al efecto horizontal.

## El insight no obvio

Leído solo, `capas-de-profundidad-sistemica` sugiere que el riesgo de una intervención cosmética se resuelve con mejor diagnóstico: mira más profundo, encuentra la capa correcta, interviene ahí. Leído solo, `interdependencia-sistemica` sugiere que el riesgo de un colapso no anticipado se resuelve con mejor mapeo de dependencias: identifica qué piezas conectan con qué.

Juntos revelan que son dos preguntas independientes que hay que responder simultáneamente, no una seguida de la otra. Un diagnóstico de capas impecable (saber que el problema es sociotécnico, no material) no dice nada sobre el alcance horizontal de la intervención una vez que se ejecuta ahí. Y un mapeo de dependencias impecable, hecho sin el eje de profundidad, puede rastrear relaciones dentro de una capa sin detectar que la relación que realmente importa cruza a otra. El riesgo compuesto — y más peligroso que cualquiera de los dos por separado — es el efecto que salta de capa a través de una dependencia no mapeada: exactamente el punto ciego que ninguno de los dos marcos, usado solo, está diseñado para ver, porque cada uno mira en el eje del otro sin saberlo.

## El límite

Esta correlación no resuelve el problema que señala — lo hace más difícil de lo que cualquiera de los dos conceptos admite por separado. `capas-de-profundidad-sistemica` ya reconoce el riesgo de "parálisis analítica" al intervenir en capas profundas; `interdependencia-sistemica` ya reconoce que "modelar todas las dependencias de un sistema es computacionalmente y cognitivamente prohibitivo". Combinar ambos ejes —qué capa, más qué dependencias, más qué dependencias cruzan de capa— no es una síntesis accionable: es la confirmación de que el espacio de diagnóstico completo excede lo que cualquier proyecto de diseño real puede modelar antes de actuar. El valor práctico de la correlación no es un método nuevo, es una advertencia: un diagnóstico de capas que se siente completo puede no serlo, porque nunca fue diseñado para detectar fugas hacia otra capa.

---

_Propuestas generadas automáticamente por Jarvis. Requieren revisión y aprobación de Luigui antes de escribir en `Correlaciones/`._
_Para aprobar: `Jarvis, revisa propuestas pendientes`_

## Descartados y razón (16)

Patrón dominante (16 de 16): el archivo fuente que menciona al otro concepto ya contiene, en su propia sección "Tensiones y límites" o "Por qué importa" (con frecuencia bajo un subtítulo literal `**Tensión con...**` / `Tensiona con` / `Relación con` / `Conecta directamente con`), la síntesis completa de la relación, incluyendo su resolución.

- `agencia-humana-como-imperativo-ux` × `comprehension-debt` — ya resuelto en "Por qué importa" de `agencia-humana-como-imperativo-ux`: "esa opacidad... crea dependencia sin comprensión, que es precisamente lo que `comprehension-debt` describe en el contexto de desarrollo de software. La misma dinámica opera en el diseño de productos."
- `agente-como-carpeta` × `vibe-coding` — ya resuelto como analogía declarada, no tensión: "esto tiene el mismo efecto democratizador que ya documentaste en `vibe-coding` y `spec-driven-development`, pero aplicado específicamente a la construcción de agentes" (mismo patrón que el descarte previo de `agente-como-carpeta` × `spec-driven-development` en la corrida del 2026-09-21).
- `arquitectura-de-confianza` × `gobernanza-ia-performativa` — sección literal "Tensión con `gobernanza-ia-performativa`:" en `arquitectura-de-confianza`, ya resuelta por completo.
- `automatizar-mi-propio-trabajo` × `fundamentales-vs-flux` — "Este concepto vive en tensión con `fundamentales-vs-flux`" en `automatizar-mi-propio-trabajo`, con la resolución ya desarrollada en el mismo párrafo.
- `colonialismo-cultural-digital` × `poblaciones-sinteticas` — sección literal "**Tensión epistemológica con `colonialismo-cultural-digital`.**" en `poblaciones-sinteticas`, ya resuelta.
- `el-agente-que-no-para` × `impuesto-de-verificacion` — ya resuelto en "Por qué importa" de `el-agente-que-no-para`: "esto tiene una consecuencia directa sobre el `impuesto-de-verificacion`... el impuesto no desaparece — se concentra."
- `espectro-autonomia-agente` × `gobernanza-ia-performativa` — ya resuelto en "Por qué importa" de `espectro-autonomia-agente`: "exactamente el patrón que `gobernanza-ia-performativa` documenta a nivel organizacional."
- `espectro-autonomia-agente` × `quien-controla-el-prompt` — sección literal "Tensiona con `quien-controla-el-prompt`:" en `espectro-autonomia-agente`, ya resuelta.
- `fundamentales-vs-flux` × `pmf-perecedero` — sección literal "Tensiona con `fundamentales-vs-flux`:" en `pmf-perecedero`, con la respuesta ya dada ("la velocidad de ciclo de PMF es el fundamental").
- `gobernanza-ia-performativa` × `impuesto-de-alineacion` — ya resuelto en "Por qué importa" de `impuesto-de-alineacion`: "conecta directamente con `gobernanza-ia-performativa`: la capa visible del contrato existe; la capa que realmente opera puede ser distinta."
- `identidad-criptografica-como-arnes` × `llm-como-motor-de-plausibilidad` — ya resuelto (breve pero completo) en "Límite del concepto" de `identidad-criptografica-como-arnes`: "la identidad clarifica responsabilidad, no previene el error de origen (ver `llm-como-motor-de-plausibilidad`)."
- `ingenieria-agentica` × `juicio-como-trabajo-completo` — sección literal "Tensiona también con `juicio-como-trabajo-completo`:" en `ingenieria-agentica`, ya resuelta.
- `ingenieria-agentica` × `vibe-coding` — ya resuelto en "Por qué importa" de `ingenieria-agentica`: "esto tensiona directamente con `vibe-coding` como paradigma vigente", con el argumento completo desarrollado en el mismo párrafo.
- `legibilidad-de-maquina` × `lo-ilegible-como-senal` — sección literal "Tensión con `lo-ilegible-como-senal`:" en `legibilidad-de-maquina`, ya resuelta.
- `limite-de-la-escala-de-modelo` × `llm-como-motor-de-plausibilidad` — sección literal "**Relación con `llm-como-motor-de-plausibilidad`:**" en `limite-de-la-escala-de-modelo`, ya resuelta con el argumento técnico completo.
- `mvp-a-prototipo-en-produccion` × `pmf-perecedero` — sección literal "Tensiona con `mvp-a-prototipo-en-produccion`:" en `pmf-perecedero`, ya resuelta.

---
_Nota: siguen pendientes de revisión, sin tocar en esta corrida: `Inbox/2026-08-25_0811_correlaciones-propuestas.tmp.md` (3), `Inbox/2026-08-31_1122_correlaciones-propuestas.tmp.md` (2), `Inbox/2026-08-31_1122_borradores-graduados.tmp.md` (1), `Inbox/2026-09-07_1117_correlaciones-propuestas.tmp.md` (1), `Inbox/2026-09-21_1109_correlaciones-propuestas.tmp.md` (1)._
