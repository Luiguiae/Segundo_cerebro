---
title: "Usuarios Sintéticos: Capacidad de Investigación"
owner: "Luigui Avila"
status: draft
updated: "2026-01-XX"
tags: ["investigación", "usuarios-sintéticos", "IA", "research", "capacidad"]
fuentes:
  - Documentos/Estudios/usuarios-sinteticos.md
  - Documentos/Decisiones/ADRs/ADR-001-usuarios-sinteticos.md
  - Documentos/00-start-here/README.md
---

# Contexto

El repositorio Segundo Cerebro documenta pensamiento, decisiones y diseño para trabajar con LLMs (Cursor), según `Documentos/00-start-here/README.md`. La investigación con usuarios reales presenta limitaciones estructurales documentadas en `Documentos/Estudios/usuarios-sinteticos.md`:

- **Costo temporal:** Reclutamiento, coordinación y ejecución de sesiones consumen horas significativas
- **Escalabilidad limitada:** No es viable simular múltiples escenarios o variaciones de comportamiento con usuarios reales
- **Sesgos de muestreo:** La distribución de participantes rara vez refleja la distribución real de usuarios en producción
- **Fricción en la iteración:** Cada cambio en hipótesis o prototipos requiere nueva ronda de reclutamiento y sesiones

La investigación tradicional con usuarios reales es necesaria pero insuficiente para explorar rápidamente espacios de diseño y validar hipótesis en etapas tempranas.

El `ADR-001` (`Documentos/Decisiones/ADRs/ADR-001-usuarios-sinteticos.md`) establece la decisión arquitectónica de adoptar usuarios sintéticos como método complementario de investigación. Este PRD define cómo operar, gobernar y evolucionar esta capacidad reutilizable en el Segundo Cerebro.

# Objetivo

Establecer usuarios sintéticos como capacidad reutilizable del Segundo Cerebro que permita:

1. **Operar:** Definir flujos, criterios y reglas de uso para investigación con usuarios sintéticos
2. **Gobernar:** Establecer criterios de validez, documentación obligatoria y trazabilidad
3. **Evolucionar:** Permitir mejora continua de la capacidad basada en aprendizaje y uso

**Medición de éxito:**
- Uso consistente de usuarios sintéticos según reglas definidas
- Documentación explícita de uso en todos los casos
- Trazabilidad entre exploración sintética y validación con usuarios reales
- Reducción de horas-hombre en fases exploratorias sin comprometer calidad de validación final

# Alcance

## Incluye

- Definición operativa de usuarios sintéticos como capacidad reutilizable
- Flujos de uso para exploración temprana, iteración rápida y distribución de comportamientos
- Reglas de gobernanza: cuándo usar, cuándo no usar, cómo documentar
- Criterios de validez y calidad para uso de usuarios sintéticos
- Integración con estructura del repositorio (`Documentos/Research/`, `Documentos/Estudios/`, `Documentos/PRDS/`)
- Reglas de interacción humano-LLM para uso por agentes

## NO incluye

- Implementación técnica de herramientas o plataformas
- Definición de modelos de IA específicos
- Reemplazo de investigación con usuarios reales
- Validación final de decisiones de producto
- Predicción de métricas de negocio

# Usuario / Segmento

## Usuarios primarios

**Investigadores y diseñadores de producto:**
- Contexto: Fases exploratorias de investigación donde velocidad y exploración son prioritarias
- Necesidad: Explorar múltiples hipótesis, escenarios y variaciones sin costo de reclutamiento
- Uso: Generar hipótesis, identificar fricciones potenciales, refinar preguntas de investigación

**Equipos de diseño:**
- Contexto: Iteración rápida de prototipos y variaciones de diseño
- Necesidad: Validar cambios sin esperar nueva ronda de usuarios reales
- Uso: Comparar variaciones de diseño, explorar casos edge, validar múltiples contextos de uso

**Agentes LLMs (Cursor):**
- Contexto: Trabajo asistido por IA en el repositorio Segundo Cerebro
- Necesidad: Reglas operativas claras para usar usuarios sintéticos correctamente
- Uso: Simular interacciones, generar perfiles, explorar escenarios según reglas definidas

## Segmentación por caso de uso

Según `Documentos/Estudios/usuarios-sinteticos.md`, los casos de uso válidos son:

1. **Exploración temprana:** Generar hipótesis, explorar escenarios antes de prototipar, identificar fricciones
2. **Iteración rápida:** Validar cambios en prototipos, comparar variaciones, refinar preguntas
3. **Distribución de comportamientos:** Simular distribución amplia de perfiles, explorar casos edge
4. **Reducción de horas-hombre:** Reducir tiempo en exploración para enfocar validación crítica con usuarios reales

# Supuestos y restricciones

## Supuestos

1. Los usuarios sintéticos son simulaciones de comportamiento generadas mediante IA (LLMs), según `Documentos/Estudios/usuarios-sinteticos.md`
2. Los usuarios sintéticos complementan pero no reemplazan investigación con usuarios reales (`ADR-001`)
3. La validación final de decisiones de producto requiere usuarios reales
4. Los LLMs tienen sesgos que se reflejan en usuarios sintéticos generados
5. El repositorio Segundo Cerebro seguirá la estructura documentada en `Documentos/00-start-here/README.md`

## Restricciones

### Restricciones de uso (casos inválidos)

Según `Documentos/Estudios/usuarios-sinteticos.md`, NO usar usuarios sintéticos para:

- **Validación final:** No validar decisiones de producto que afectan usuarios reales
- **Justificación de decisiones:** No usar como única evidencia para decisiones de negocio
- **Predicción de métricas:** No predecir conversión, retención o métricas de negocio
- **Casos críticos:** No validar accesibilidad, seguridad o aspectos regulatorios
- **Grupos vulnerables:** No usar para decisiones que afectan grupos vulnerables sin validación real

### Restricciones epistemológicas

- **Sesgo de simulación:** Los usuarios sintéticos reflejan sesgos del modelo de IA usado
- **Falsa confianza:** Pueden generar sensación de validación sin evidencia real
- **Distribución artificial:** La "realista" distribución puede no corresponder a distribución real
- **No descubren problemas inesperados:** No pueden descubrir problemas que solo emergen en uso real

### Restricciones de documentación

Según `ADR-001`, es obligatorio:
- Documentar explícitamente cuando se usan usuarios sintéticos vs. usuarios reales
- Validar hallazgos con usuarios reales antes de decisiones finales
- Mantener trazabilidad entre exploración sintética y validación real

# Flujo propuesto

## Flujo general: Exploración → Validación

```
1. Exploración con usuarios sintéticos
   ├─ Generar hipótesis
   ├─ Explorar escenarios
   ├─ Identificar fricciones potenciales
   └─ Documentar en Documentos/Research/ como hipótesis

2. Refinamiento
   ├─ Iterar preguntas de investigación
   ├─ Comparar variaciones de diseño
   └─ Refinar prototipos

3. Validación con usuarios reales (obligatorio)
   ├─ Validar hallazgos de usuarios sintéticos
   ├─ Descubrir problemas inesperados
   └─ Tomar decisiones finales de producto

4. Documentación y trazabilidad
   ├─ Documentar en Documentos/Research/ o Documentos/Estudios/
   ├─ Referenciar desde PRDs en secciones Usuario/Segmento y Supuestos
   └─ Mantener trazabilidad entre exploración sintética y validación real
```

## Flujo operativo por caso de uso

### Caso 1: Exploración temprana

1. Definir perfil de usuario sintético (necesidades, contexto, comportamiento)
2. Generar hipótesis sobre necesidades de usuario
3. Explorar múltiples escenarios de uso
4. Identificar fricciones potenciales en flujos propuestos
5. Documentar hallazgos en `Documentos/Research/` como hipótesis
6. Refinar preguntas para sesiones con usuarios reales

### Caso 2: Iteración rápida

1. Definir variaciones de diseño a comparar
2. Simular interacciones con múltiples perfiles
3. Comparar resultados entre variaciones
4. Identificar fricciones antes de prototipar
5. Documentar hallazgos en `Documentos/Research/`
6. Validar cambios con usuarios reales antes de implementar

### Caso 3: Distribución de comportamientos

1. Definir distribución de perfiles a simular
2. Simular interacciones con distribución amplia
3. Explorar casos edge difíciles de reclutar
4. Validar que diseño funciona para múltiples contextos
5. Documentar hallazgos en `Documentos/Estudios/`
6. Validar casos críticos con usuarios reales

## Reglas de interacción humano-LLM

Para agentes LLMs que usen usuarios sintéticos:

1. **Prompting para simulación:**
   - Especificar perfil de usuario sintético (necesidades, contexto, comportamiento)
   - Solicitar distribución realista de comportamientos
   - Reconocer sesgos del modelo y documentarlos

2. **Validación de outputs:**
   - No confiar ciegamente en outputs de usuarios sintéticos
   - Validar hallazgos con usuarios reales
   - Documentar limitaciones de simulación

3. **Reutilización en Segundo Cerebro:**
   - Documentar usuarios sintéticos usados en `Documentos/Research/`
   - Referenciar desde PRDs y decisiones (ADRs)
   - Mantener trazabilidad entre exploración sintética y validación real

# Riesgos

## Riesgos técnicos

- **Sesgo de simulación:** Los usuarios sintéticos reflejan sesgos del modelo de IA usado (`Documentos/Estudios/usuarios-sinteticos.md`)
- **Distribución artificial:** La "realista" distribución puede no corresponder a distribución real
- **Limitaciones del modelo:** Los LLMs pueden generar comportamientos no realistas o inconsistentes

## Riesgos de negocio

- **Falsa confianza:** Pueden generar sensación de validación sin evidencia real
- **Mal uso:** Sin límites claros, pueden usarse para validación final o justificación sin evidencia
- **Costo de documentación:** Requiere documentar explícitamente uso y mantener trazabilidad

## Riesgos de UX

- **No descubren problemas inesperados:** Los usuarios sintéticos no pueden descubrir problemas que solo emergen en uso real
- **Falta de contexto emocional:** No tienen experiencias vividas ni contexto emocional auténtico
- **Validación incompleta:** No validan decisiones finales de producto sin usuarios reales

## Mitigación de riesgos

1. **Límites explícitos:** Documentar casos de uso inválidos y restricciones
2. **Documentación obligatoria:** Requerir documentación explícita de uso y trazabilidad
3. **Validación obligatoria:** Validar hallazgos con usuarios reales antes de decisiones finales
4. **Gobernanza:** Establecer criterios de validez y calidad para uso de usuarios sintéticos

# Pendientes

## Preguntas abiertas

1. ¿Qué criterios específicos definen calidad de un perfil de usuario sintético?
2. ¿Cómo medir efectividad de usuarios sintéticos vs. usuarios reales en exploración temprana?
3. ¿Qué herramientas o plataformas facilitarían uso sistemático de usuarios sintéticos?
4. ¿Cómo evolucionar la capacidad basada en aprendizaje y uso?

## Decisiones por tomar

1. Establecer plantilla o formato estándar para documentar uso de usuarios sintéticos
2. Definir métricas de éxito para uso de usuarios sintéticos
3. Establecer proceso de revisión y mejora continua de la capacidad
4. Definir criterios de validez específicos para diferentes casos de uso

## Próximos pasos

1. Validar flujos propuestos con uso real
2. Documentar casos de uso exitosos en `Documentos/Research/`
3. Iterar sobre criterios de validez y calidad
4. Establecer gobernanza operativa de la capacidad

---

**Referencias:**
- `Documentos/Estudios/usuarios-sinteticos.md` - Marco conceptual base
- `Documentos/Decisiones/ADRs/ADR-001-usuarios-sinteticos.md` - Decisión arquitectónica
- `Documentos/00-start-here/README.md` - Estructura del repositorio
- `Plantillas/PRD_plantilla.md` - Plantilla para PRDs
