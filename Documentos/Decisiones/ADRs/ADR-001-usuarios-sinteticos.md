---
# ADR-001: Adoptar usuarios sintéticos como método complementario de investigación

Fecha: 2026-01-XX
Estado: Propuesto
Decisor(es): Luigui Avila
Contexto relacionado:
- Documentos/Estudios/usuarios-sinteticos.md
- Documentos/00-start-here/README.md
- Plantillas/Adr_plantilla.md

## Contexto

El repositorio Segundo Cerebro documenta pensamiento, decisiones y diseño para trabajar con LLMs (Cursor). La investigación con usuarios reales presenta limitaciones estructurales documentadas en `Documentos/Estudios/usuarios-sinteticos.md`:

- **Costo temporal:** Reclutamiento, coordinación y ejecución de sesiones consumen horas significativas
- **Escalabilidad limitada:** No es viable simular múltiples escenarios o variaciones de comportamiento con usuarios reales
- **Sesgos de muestreo:** La distribución de participantes rara vez refleja la distribución real de usuarios en producción
- **Fricción en la iteración:** Cada cambio en hipótesis o prototipos requiere nueva ronda de reclutamiento y sesiones

La investigación tradicional con usuarios reales es necesaria pero insuficiente para explorar rápidamente espacios de diseño y validar hipótesis en etapas tempranas del Segundo Cerebro.

El repositorio requiere métodos que permitan iteración rápida y exploración de múltiples escenarios sin comprometer recursos de investigación en hipótesis que no funcionan.

## Decisión

Adoptar **usuarios sintéticos** como método complementario de investigación en el Segundo Cerebro, con las siguientes condiciones:

1. **Definición:** Usuarios sintéticos son simulaciones de comportamiento de usuario generadas mediante IA (LLMs) que permiten simular interacciones, explorar variaciones de comportamiento, reducir horas-hombre en fases exploratorias y distribuir comportamientos de manera más realista que muestras pequeñas.

2. **Uso complementario:** Los usuarios sintéticos no reemplazan usuarios reales; complementan la investigación en fases donde la velocidad y la exploración son prioritarias.

3. **Casos de uso válidos:**
   - Exploración temprana: generar hipótesis, explorar escenarios antes de prototipar, identificar fricciones potenciales
   - Iteración rápida: validar cambios en prototipos, comparar variaciones de diseño, refinar preguntas de investigación
   - Distribución de comportamientos: simular distribución más amplia de perfiles, explorar casos edge
   - Reducción de horas-hombre: reducir tiempo en fases exploratorias para enfocar tiempo con usuarios reales en validación crítica

4. **Límites explícitos:** No usar para validación final, justificación de decisiones, predicción de métricas ni casos críticos (accesibilidad, seguridad, regulatorios).

5. **Documentación obligatoria:** Documentar explícitamente cuando se usan usuarios sintéticos vs. usuarios reales, y validar hallazgos con usuarios reales antes de decisiones finales.

## Alternativas consideradas

**1. Solo investigación con usuarios reales**
- **Descartada porque:** Presenta limitaciones estructurales de costo temporal, escalabilidad limitada y fricción en iteración documentadas en `Documentos/Estudios/usuarios-sinteticos.md`. No permite explorar rápidamente espacios de diseño.

**2. Reemplazar usuarios reales con usuarios sintéticos**
- **Descartada porque:** Los usuarios sintéticos no tienen experiencias vividas, no pueden descubrir problemas inesperados que solo emergen en uso real, y no validan decisiones finales de producto según `Documentos/Estudios/usuarios-sinteticos.md`.

**3. Usar usuarios sintéticos sin límites ni documentación**
- **Descartada porque:** Presenta riesgos epistemológicos (sesgo de simulación, falsa confianza, distribución artificial) y puede generar sensación de validación sin evidencia real según `Documentos/Estudios/usuarios-sinteticos.md`.

**4. Adoptar usuarios sintéticos como método complementario con límites y documentación explícita**
- **Seleccionada porque:** Permite exploración rápida y reducción de horas-hombre en fases exploratorias, mientras mantiene validación con usuarios reales para decisiones finales. Los límites y documentación explícita mitigan riesgos epistemológicos.

## Consecuencias

### Positivas

- **Reducción de horas-hombre:** Acelerar ciclos de exploración-validación y reducir tiempo en hipótesis que no funcionan, permitiendo enfocar recursos de investigación en validación crítica
- **Exploración ampliada:** Permitir explorar más hipótesis en menos tiempo, múltiples escenarios de uso y casos edge sin límites de reclutamiento
- **Iteración rápida:** Validar cambios en prototipos y comparar variaciones de diseño sin esperar nueva ronda de usuarios reales
- **Distribución realista:** Simular distribución más amplia de perfiles que muestra pequeña de usuarios reales
- **Refinamiento de preguntas:** Iterar preguntas de investigación antes de sesiones con usuarios reales

### Negativas / Riesgos

- **Sesgo de simulación:** Los usuarios sintéticos reflejan sesgos del modelo de IA usado, según `Documentos/Estudios/usuarios-sinteticos.md`
- **Falsa confianza:** Pueden generar sensación de validación sin evidencia real
- **Distribución artificial:** La "realista" distribución puede no corresponder a distribución real
- **Costo de documentación:** Requiere documentar explícitamente cuando se usan usuarios sintéticos vs. reales, y mantener trazabilidad entre exploración sintética y validación real
- **Riesgo de mal uso:** Sin límites claros, pueden usarse para validación final o justificación de decisiones sin evidencia real
- **No descubren problemas inesperados:** Los usuarios sintéticos no pueden descubrir problemas que solo emergen en uso real

## Notas

- Este ADR se basa en el marco conceptual documentado en `Documentos/Estudios/usuarios-sinteticos.md`
- Los usuarios sintéticos deben referenciarse desde PRDs en secciones de Usuario/Segmento y Supuestos y restricciones
- Los hallazgos de usuarios sintéticos deben documentarse en `Documentos/Research/` como hipótesis, no como evidencia final
- La validación con usuarios reales es obligatoria antes de decisiones finales de producto
- Este ADR establece el patrón arquitectónico para uso de usuarios sintéticos en el Segundo Cerebro, pero no especifica implementación técnica

---

**Referencias:**
- `Documentos/Estudios/usuarios-sinteticos.md` - Marco conceptual base
- `Documentos/00-start-here/README.md` - Estructura del repositorio
- `Plantillas/Adr_plantilla.md` - Plantilla para ADRs
