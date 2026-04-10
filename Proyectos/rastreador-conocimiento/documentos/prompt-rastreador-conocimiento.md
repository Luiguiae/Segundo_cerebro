# Prompt para Claude Code — Rastreador de Conocimiento

Lee el archivo `documentos/ESPECIFICACION.md` y luego:

1. Genera `documentos/plan.md`:
   - Resumen del objetivo
   - Fases de implementación en orden
   - Dependencias y riesgos identificados
   - NO escribas código todavía

2. Genera `documentos/tareas.md`:
   - Lista ordenada de tareas atómicas
   - Cada tarea: descripción, archivos afectados, criterio de completado
   - Las tareas deben poder ejecutarse de forma independiente

3. Una vez aprobados plan.md y tareas.md:
   - Ejecuta las tareas en orden
   - Por cada tarea: implementa → describe cambios → espera revisión antes de la siguiente

Pila técnica obligatoria:
- Servidor: Python 3.11+ con FastAPI
- Base de datos: SQLite
- Interfaz: React + Tailwind CSS
- APIs externas: Tavily (búsqueda), Jina Reader (extracción de URLs), Groq como principal y Gemini como respaldo para generación
- Despliegue: Render nivel gratuito

Restricciones críticas:
- Todo en español: nombres de carpetas, archivos, variables, funciones y comentarios
- Nunca escribir claves de API en el código — usar variables de entorno
- La plantilla de concepto atómico debe respetarse exactamente (ver sección Pila técnica en ESPECIFICACION.md)
- El campo `relacionado` debe inferirse automáticamente cruzando contra los conceptos existentes en el ATLAS.md del Segundo Cerebro cuando esté disponible
- SQLite como única base de datos — sin PostgreSQL ni dependencias externas en v1
