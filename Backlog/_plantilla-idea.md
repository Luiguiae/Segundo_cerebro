---
id: slug-de-la-idea
titulo: Nombre del proyecto
fecha_captura: YYYY-MM-DD
estado: borrador
raiz_proyecto: ~/Projects/nombre-del-proyecto
tags: []
---

## 1. Problema
Una oración: qué dolor resuelve y para quién.

## 2. Usuario objetivo
Perfil concreto con contexto de uso real.

## 3. Casos de uso principales
Como [usuario], quiero [acción] para [beneficio]. (máx. 5)

## 4. Criterios de aceptación
DADO / CUANDO / ENTONCES por cada caso de uso.

## 5. Fuera de alcance
Lo que explícitamente NO entra en esta iteración.

## 6. Stack / arquitectura
- Tecnologías propuestas
- Dependencias externas (APIs, DBs, servicios)
- Estructura de carpetas del nuevo proyecto
- Integraciones con sistemas existentes

## 7. Métricas de éxito
¿Cómo sabremos que funcionó?

## 8. Preguntas abiertas
Decisiones pendientes antes de construir.

---

## SPEC.md

[Copiar aquí el contenido completo del SPEC.md generado en Claude.ai]

---

## Prompt para Jarvis

```
Lee el archivo docs/SPEC.md y luego:

1. Genera docs/plan.md:
   - Overview del objetivo
   - Fases de implementación en orden
   - Dependencias y riesgos identificados
   - NO escribas código todavía

2. Genera docs/tasks.md:
   - Lista ordenada de tareas atómicas
   - Cada tarea: descripción, archivos afectados, criterio de done
   - Tareas ejecutables de forma independiente

3. Una vez aprobados plan.md y tasks.md:
   - Ejecuta las tareas en orden
   - Por cada tarea: implementa → describe cambios → espera revisión

Stack: [pegar de la sección 6]
Restricciones: [pegar lo que no puede hacer]
```
