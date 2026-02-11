---
titulo: "ADR-005: Adoptar Synthetic Reconstruction (SR) como método de estimación agregada"
tipo: adr
estado: aceptado
autor: Luigui Avila
fecha: 2026-01-16
updated: 2026-02-10
tags: [synthetic-reconstruction, estimacion, metodologia, poblaciones-sinteticas]
fuentes:
  - Documentos/Estudios/poblaciones-sinteticas-sr.md
  - Documentos/Decisiones/ADRs/ADR-001-usuarios-sinteticos.md
  - Documentos/00-start-here/README.md
  - Plantillas/adr-plantilla.md
---

# ADR-005: Adoptar Synthetic Reconstruction (SR) como método de estimación agregada

## Contexto

En múltiples contextos organizacionales —especialmente en banca, servicios financieros y plataformas digitales— resulta inviable observar, experimentar o medir directamente el comportamiento de individuos reales antes de implementar una decisión de diseño, producto o servicio. Las razones incluyen restricciones regulatorias, costos, tiempos, riesgos reputacionales, sesgos de muestra y la imposibilidad de experimentar a escala sin impacto real, según `Documentos/Estudios/poblaciones-sinteticas-sr.md`.

Frente a este escenario, surge la necesidad de estimar impactos a nivel poblacional de forma anticipada, trazable y responsable, sin depender de observación individual directa ni de predicciones determinísticas.

El repositorio Segundo Cerebro requiere métodos que permitan tomar decisiones estratégicas bajo incertidumbre cuando no es posible contar con datos individuales completos o experimentación real. Los métodos tradicionales presentan limitaciones como la necesidad de grandes volúmenes de datos históricos, la dependencia de labels individuales o la imposibilidad de explicar supuestos y márgenes de error en modelos predictivos cerrados.

**Nota:** Este ADR complementa `ADR-001` sobre usuarios sintéticos. Mientras usuarios sintéticos operan a nivel micro o narrativo para explorar comportamientos cualitativos, SR opera a nivel agregado y estructural para estimar impactos poblacionales.

## Decisión

Adoptar **Synthetic Reconstruction (SR)** como método de estimación agregada en el Segundo Cerebro para decisiones estratégicas bajo incertidumbre, con las siguientes condiciones:

1. **Definición metodológica:** SR es un enfoque metodológico para estimar comportamientos e impactos agregados de una población cuando solo se dispone de información parcial, agregada o estructural. En lugar de predecir individuos, SR reconstruye un espacio de poblaciones plausibles que cumplen con distribuciones conocidas, restricciones estructurales y reglas explícitas de coherencia. El objetivo no es replicar la realidad exacta, sino generar estimaciones condicionadas y comparables que permitan analizar escenarios.

2. **Diferencia con otros métodos:** A diferencia de la predicción individual o de simulaciones narrativas simples, SR no optimiza exactitud individual ni realismo superficial, sino consistencia estructural y utilidad decisional.

3. **Casos de uso válidos:**
   - Evaluación de impacto de rediseños de canales digitales
   - Priorización de segmentos para pilotos
   - Estimación de riesgos de adopción o abandono
   - Análisis comparativo entre escenarios de despliegue
   - Estimación de impactos económicos agregados antes de la implementación
   - Etapas tempranas de diseño, planificación estratégica y evaluación ex ante

4. **Supuestos del método (declarados explícitamente):**
   - Es posible conocer o estimar distribuciones marginales relevantes
   - Se conocen tamaños poblacionales
   - Existen relaciones estructurales entre variables clave que pueden identificarse
   - Los comportamientos pueden representarse mediante propensiones relativas ajustadas por reglas explícitas
   - No se asume conocimiento completo del individuo ni estabilidad absoluta del comportamiento
   - Todo supuesto inferido debe declararse explícitamente y reflejarse en un índice de certeza

5. **Gobernanza y certeza:** Un componente central es la declaración explícita de incertidumbre mediante un índice de certeza que refleja la proporción de variables observadas frente a inferidas, la complejidad del escenario y la dependencia de heurísticas. La certeza no busca validar verdad empírica, sino comunicar confiabilidad relativa y condiciones de uso del resultado.

6. **Límites explícitos:** SR no es un modelo de predicción individual, no es un sistema de scoring, no es un motor de decisiones automáticas ni un reemplazo de la medición empírica real. No debe confundirse con generación de datos sintéticos para entrenamiento de modelos, ni con simulaciones narrativas de usuarios ficticios. Usar SR para inferir comportamientos individuales, tomar decisiones obligatorias o prometer resultados exactos constituye un uso incorrecto del método.

## Alternativas consideradas

**1. Usar solo métodos tradicionales de predicción individual**
- **Descartada porque:** Presenta limitaciones documentadas en `Documentos/Estudios/poblaciones-sinteticas-sr.md`: necesidad de grandes volúmenes de datos históricos, dependencia de labels individuales, imposibilidad de explicar supuestos y márgenes de error en modelos predictivos cerrados. No permite estimar impactos poblacionales cuando no hay datos individuales completos.

**2. Usar solo simulaciones narrativas o usuarios sintéticos**
- **Descartada porque:** Los usuarios sintéticos (según `ADR-001`) operan a nivel micro o narrativo para entender el "por qué" cualitativo, mientras que SR opera a nivel agregado para estimar el "cuánto" y el "a quién" a nivel poblacional. Son complementarios pero no sustituyen la estimación agregada estructurada que proporciona SR.

**3. Usar SR sin índice de certeza ni declaración de supuestos**
- **Descartada porque:** El principal riesgo metodológico es la sobredependencia de heurísticas no validadas. Sin índice de certeza y declaración explícita de supuestos, existe riesgo de leer estimaciones como predicciones o certezas, y de usar el output como sustituto de medición real según `Documentos/Estudios/poblaciones-sinteticas-sr.md`.

**4. Usar SR sin guardrails explícitos ni uso responsable**
- **Descartada porque:** A nivel organizacional, el mayor riesgo es el uso del output del modelo como sustituto de medición real o como justificación automática de decisiones ya tomadas. Estos riesgos deben mitigarse mediante guardrails explícitos, supuestos declarados y uso responsable del índice de certeza.

**5. Adoptar SR como método de estimación agregada con gobernanza explícita**
- **Seleccionada porque:** Permite tomar decisiones estratégicas bajo incertidumbre cuando no hay datos individuales completos, habilita comparación de escenarios y anticipación de impactos diferenciales por segmento, prioriza intervenciones antes de implementación, y la gobernanza explícita mitiga riesgos metodológicos y organizacionales.

## Consecuencias

### Positivas

- **Decisiones estratégicas bajo incertidumbre:** Permite tomar decisiones cuando no es posible contar con datos individuales completos o experimentación real, según `Documentos/Estudios/poblaciones-sinteticas-sr.md`
- **Comparación de escenarios:** Habilita comparar escenarios, anticipar impactos diferenciales por segmento y priorizar intervenciones antes de su implementación
- **Estimación agregada estructurada:** Proporciona estimaciones condicionadas y comparables a nivel poblacional, complementando métodos narrativos como usuarios sintéticos
- **Transparencia metodológica:** Requiere declaración explícita de supuestos y índice de certeza, permitiendo explicar márgenes de error y condiciones de uso
- **Anticipación de impactos:** Permite evaluar impactos poblacionales antes de implementar soluciones, anticipar efectos no intencionales y traducir decisiones de experiencia en impactos cuantificables
- **Enfoque sistémico:** Desplaza el foco desde optimización local hacia coherencia sistémica y toma de decisiones informada bajo incertidumbre

### Negativas / Riesgos

- **Sobredependencia de heurísticas no validadas:** El principal riesgo metodológico según `Documentos/Estudios/poblaciones-sinteticas-sr.md` es depender de heurísticas que no han sido validadas empíricamente
- **Interpretación incorrecta:** Riesgo de leer estimaciones como predicciones o certezas, confundiendo estimaciones condicionadas con verdades empíricas
- **Uso organizacional incorrecto:** Mayor riesgo a nivel organizacional: usar el output del modelo como sustituto de medición real o como justificación automática de decisiones ya tomadas
- **Complejidad metodológica:** Requiere conocimiento o estimación de distribuciones marginales, tamaños poblacionales y relaciones estructurales entre variables clave, lo que puede no estar disponible en todos los contextos
- **Costo de gobernanza:** Requiere declaración explícita de supuestos, índice de certeza y guardrails, lo que añade complejidad y tiempo al proceso
- **Validación post-implementación:** Requiere validación direccional post-implementación de decisiones informadas por SR, lo que añade responsabilidad de seguimiento
- **Limitación en certeza:** El índice de certeza no valida verdad empírica, solo comunica confiabilidad relativa, lo que puede generar expectativas incorrectas si no se comunica adecuadamente

## Notas

- Este ADR se basa en el estudio metodológico documentado en `Documentos/Estudios/poblaciones-sinteticas-sr.md`
- SR complementa pero no reemplaza métodos como usuarios sintéticos (`ADR-001`): usuarios sintéticos operan a nivel micro cualitativo, SR a nivel agregado estructural
- El índice de certeza es componente central: debe reflejar proporción de variables observadas vs. inferidas, complejidad del escenario y dependencia de heurísticas
- Los próximos pasos según el estudio incluyen: incorporación progresiva de variables observadas, validación direccional post-implementación, integración sistemática con datos reales una vez disponibles, y documentación de casos de uso exitosos y fallidos
- Este ADR establece la decisión metodológica de adoptar SR, pero no especifica implementación técnica ni herramientas específicas
- **Declaración explícita:** El estudio no proporciona ejemplos concretos de aplicación ni métricas de validación específicas; estos aspectos deberán desarrollarse en implementación y documentarse en `Documentos/Research/` o `Documentos/Estudios/`

---

**Referencias:**
- `Documentos/Estudios/poblaciones-sinteticas-sr.md` - Estudio metodológico base
- `Documentos/Decisiones/ADRs/ADR-001-usuarios-sinteticos.md` - Método complementario a nivel micro
- `Documentos/00-start-here/README.md` - Estructura del repositorio
- `Plantillas/adr-plantilla.md` - Plantilla para ADRs
