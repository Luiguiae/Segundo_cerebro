# Skill: correlacion-conceptos
**Versión:** 0.1  
**Fecha:** 2026-04-03  
**Estado:** En revisión

---

## Resumen
Skill de Claude que analiza los conceptos del Segundo Cerebro, detecta correlaciones entre ellos y genera un archivo `.md` con narrativa lista para presentar, guardado en `Conocimiento/Correlaciones/`.

## Problema
Las conexiones entre conceptos son valiosas pero perecederas: aparecen en conversaciones, se pierden si no se capturan de inmediato, y reconstruirlas manualmente consume tiempo. El Segundo Cerebro tiene los conceptos atómicos, pero no tiene un mecanismo que materialice las correlaciones entre ellos de forma sistemática y con narrativa lista para usar.

## Usuario objetivo
Luigui — diseñador-constructor que usa el Segundo Cerebro como infraestructura de conocimiento. Trabaja en presentaciones, propuestas y charlas donde las correlaciones entre conceptos son el insumo principal. Necesita capturar esas conexiones rápido, con un formato que pueda llevar directo a una slide o a un argumento.

## Casos de uso principales

**P1 — Correlación bajo demanda entre dos conceptos**  
Como usuario del Segundo Cerebro, quiero indicarle a Claude dos conceptos y recibir un archivo `.md` con la correlación entre ellos, para tener una narrativa lista sin tener que construirla desde cero.

**P1 — Descubrimiento autónomo de correlaciones**  
Como usuario del Segundo Cerebro, quiero que Claude analice `Conocimiento/Conceptos/` y proponga las correlaciones más potentes que encuentre, para descubrir conexiones que yo no había visto.

**P2 — Correlación múltiple (3+ conceptos)**  
Como usuario, quiero correlacionar más de dos conceptos en una sola narrativa, para construir argumentos más complejos para presentaciones.

## Criterios de aceptación

### P1 — Correlación bajo demanda
- DADO que el usuario menciona dos conceptos que existen en `Conocimiento/Conceptos/`
- CUANDO activa la skill de correlación
- ENTONCES Claude lee ambos archivos de concepto, identifica la tensión o fricción entre ellos, construye una narrativa con estructura tensión → síntesis, y guarda el resultado en `Conocimiento/Correlaciones/YYYY-MM-DD_concepto-a--concepto-b.md`
- Y el archivo generado tiene YAML frontmatter con `conceptos`, `fecha`, `tags`, y `tipo: correlacion`

### P1 — Descubrimiento autónomo
- DADO que el usuario pide "encuentra correlaciones en mis conceptos"
- CUANDO la skill corre
- ENTONCES Claude lee todos los archivos en `Conocimiento/Conceptos/`, propone un listado de pares con mayor potencial de correlación (mínimo 3, máximo 5), y espera confirmación del usuario antes de generar los archivos
- Y el criterio de selección prioriza pares con tensión productiva (contradicción o fricción), no solo similitud

## Estructura del archivo de output

```markdown
---
tipo: correlacion
conceptos: [concepto-a, concepto-b]
fecha: YYYY-MM-DD
tags: [tag1, tag2]
---

# [Título que captura la tensión entre los conceptos]

## La tensión
[Párrafo que describe la contradicción o fricción entre ambos conceptos.
Por qué no son lo mismo. Por qué conviven con dificultad.]

## La síntesis
[Párrafo que resuelve o eleva la tensión. El insight que emerge de ponerlos juntos.
Listo para usarse como argumento en una presentación.]

## Aplicaciones
- [Contexto concreto donde esta correlación es útil]
- [Otro contexto]

## Conceptos relacionados
- [[concepto-c]] — [por qué aparece aquí]
```

## Fuera de alcance — v1
- No genera slides ni exporta a Reveal.js (eso lo hace un proceso separado)
- No actualiza el `ATLAS.md` automáticamente (lo hace `generar_index.py` aparte)
- No correlaciona conceptos que no existan como archivos en `Conocimiento/Conceptos/`
- No hace correlaciones de más de 3 conceptos en esta versión
- No tiene interfaz gráfica — se activa desde chat con Claude

## Stack / restricciones técnicas
- **Entorno:** Claude.ai chat (skill cargada como `.skill`)
- **Filesystem objetivo:** `~/Documents/Segundo_cerebro/`
- **Formato de conceptos fuente:** `.md` con YAML frontmatter
- **Herramienta de escritura:** Claude Code (cuando se quiera automatizar la escritura al disco)
- **Convención de nombres:** `YYYY-MM-DD_concepto-a--concepto-b.md`
- **Sin dependencias externas:** el output es Markdown puro

## Métricas de éxito
- El archivo generado puede usarse sin edición como insumo de una slide o argumento
- La narrativa pasa el test: ¿genera una reacción de "no había pensado en eso" al leerla?
- El flujo completo (activar skill → tener archivo guardado) toma menos de 2 minutos

## Preguntas abiertas
- [ ] ¿La skill debe proponer el título o el usuario lo confirma antes de guardar? → Decidir en prueba
- [ ] ¿Cuántos tags máximo en el frontmatter? → Propuesta: máx. 5

## Decisiones registradas
- **Convención de nombres:** `YYYY-MM-DD_concepto-a--concepto-b.md` — permite orden cronológico y lectura clara del par correlacionado
- **Sesgo narrativo:** tensión productiva (contradicción → síntesis) — más útil para presentaciones que inventario de similitudes
