# Rastreador de Conocimiento — Sistema de Agentes de Investigación

## Resumen
Sistema web de agentes IA especializados que buscan contenido nuevo sobre 13 temáticas definidas, generan conceptos atómicos listos para revisión, y permiten al usuario aprobarlos o rechazarlos para exportarlos al Segundo Cerebro.

## Problema
Luigui genera conocimiento valioso pero de forma reactiva — solo cuando lo encuentra manualmente. El sistema debe hacer la búsqueda de forma proactiva y continua, entregando contenido ya procesado (concepto atómico completo) para que el único trabajo humano sea decidir si entra o no al Segundo Cerebro.

## Usuarios objetivo
Un solo usuario (Luigui) que revisa el tablero periódicamente, aprueba o rechaza conceptos, y exporta los aprobados a su Segundo Cerebro local.

## Casos de uso principales

1. **Como usuario, quiero lanzar una búsqueda bajo demanda por temática** para obtener conceptos atómicos nuevos listos para revisar.

2. **Como usuario, quiero aprobar o rechazar cada concepto generado** para controlar qué entra a mi Segundo Cerebro.

3. **Como usuario, quiero pegar una URL o texto de un artículo/email** para que el sistema lo procese, profundice en la web y genere un concepto atómico.

4. **Como usuario, quiero gestionar mis fuentes y temáticas desde el tablero** para agregar, editar o eliminar sin tocar código.

5. **Como usuario, quiero exportar los conceptos aprobados como archivos .md** para copiarlos manualmente a mi Segundo Cerebro.

## Criterios de aceptación

### CU1 — Búsqueda bajo demanda
- DADO que estoy en el tablero
- CUANDO selecciono una o más temáticas y presiono "Buscar"
- ENTONCES el sistema lanza un agente por cada temática seleccionada, busca en las fuentes configuradas, y genera un concepto atómico por cada resultado relevante
- Y los conceptos aparecen en la cola de revisión con estado "pendiente"

### CU2 — Aprobar / Rechazar
- DADO que hay conceptos en la cola de revisión
- CUANDO presiono "Aprobar" en un concepto
- ENTONCES el concepto pasa a estado "aprobado" y queda disponible para exportar
- CUANDO presiono "Rechazar"
- ENTONCES el concepto desaparece de la cola sin guardarse

### CU3 — Entrada manual (URL o texto)
- DADO que pego una URL o texto en la entrada manual
- CUANDO presiono "Procesar"
- ENTONCES el agente lee el contenido, busca contexto adicional en la web, y genera un concepto atómico
- Y el concepto aparece en la cola de revisión

### CU4 — Gestión de fuentes y temáticas
- DADO que estoy en la sección de configuración
- CUANDO agrego una nueva fuente (URL) o temática (texto)
- ENTONCES queda disponible para las próximas búsquedas sin reiniciar el sistema

### CU5 — Exportación
- DADO que hay conceptos aprobados
- CUANDO presiono "Exportar seleccionados"
- ENTONCES el sistema genera un archivo .zip con los .md de cada concepto aprobado
- Y cada .md sigue exactamente la plantilla del Segundo Cerebro (encabezado YAML + 8 secciones)

## Fuera de alcance (v1)
- Sincronización automática con el Segundo Cerebro local (se hace manual vía exportación)
- Búsqueda programada automática (se activa bajo demanda, puede evolucionar a diaria)
- Autenticación / multi-usuario
- Edición del concepto atómico antes de aprobar (solo aprobar o rechazar en v1)
- Integración con transcripciones de YouTube (ya existe herramienta separada)

## Pila técnica / restricciones

### Servidor
- **Python 3.11+** con FastAPI
- **Tavily API** para búsqueda web (nivel gratuito: 1000 búsquedas/mes)
- **Jina Reader API** para extracción de contenido de URLs (nivel gratuito)
- **Motor de generación con fallback automático**:
  - Principal: Groq (llama-3.3-70b) — nivel gratuito, muy rápido
  - Respaldo: Gemini (gemini-2.5-flash) — nivel gratuito
  - Lógica: intenta Groq → si falla usa Gemini → si ambos fallan muestra error claro
- Base de datos: **SQLite** (simple, sin dependencias externas, suficiente para 1 usuario)
- La plantilla de concepto atómico debe respetar el encabezado YAML del Segundo Cerebro

### Interfaz
- **React** (página única, sin marco pesado)
- **Tailwind CSS** para estilos
- Tres vistas: Cola de revisión / Configuración / Exportación

### Despliegue
- **Render** nivel gratuito para comenzar
- Variables de entorno para claves de API (nunca escritas en el código)

### Estructura de archivos
```
rastreador-conocimiento/
├── documentos/
│   ├── ESPECIFICACION.md     ← fuente de verdad (mantenida por humano)
│   ├── plan.md               ← generado por Claude Code
│   └── tareas.md             ← generado por Claude Code
├── servidor/
│   ├── principal.py          ← aplicación FastAPI
│   ├── agentes/
│   │   ├── orquestador.py    ← lanza agentes por temática
│   │   ├── buscador.py       ← busca en web + fuentes
│   │   └── redactor.py       ← genera concepto atómico
│   ├── modelos.py            ← esquemas SQLite
│   └── configuracion.py     ← temas y fuentes configurables
├── interfaz/
│   ├── src/
│   │   ├── Aplicacion.jsx
│   │   ├── vistas/
│   │   │   ├── Cola.jsx          ← cola de revisión
│   │   │   ├── Configuracion.jsx ← gestión de temas y fuentes
│   │   │   └── Exportacion.jsx   ← exportación
│   │   └── componentes/
│   │       └── TarjetaConcepto.jsx
└── AGENTES.md               ← restricciones globales para Claude Code
```

### Plantilla de concepto atómico (respetar exactamente)
```yaml
---
titulo: ""
alias: []
tags: []
tipo: concepto
fecha: YYYY-MM-DD
fuente:
  tipo: articulo | video | reunion | experimento | podcast
  referencia: ""
  autor: ""
relacionado: []
proyectos: []
estado: borrador
---
## ¿Qué es?
## ¿Por qué importa?
## ¿Cómo funciona?
## Ejemplos concretos
## Tensiones o limitaciones
## Se conecta con...
## Citas o fragmentos clave
## Mis notas
```

## Temáticas iniciales (13 agentes)
1. Vibe Coding
2. Agentes IA
3. Diseñador a Constructor
4. Usuarios Sintéticos
5. Equipos Pequeños de Alto Impacto
6. Referentes en IA (Felix Lee, Ryo Lu, Jenny Wen)
7. Decolonización
8. Pensamiento Sistémico
9. Pensamiento Crítico
10. Filosofía de la IA
11. Robótica e IA
12. Podredumbre Mental
13. Vibe Design

## Fuentes iniciales (pool compartido)
- adplist@substack.com / Substack de Felix Lee
- iterativethinking@substack.com / Ulises Arvizu
- researchbookmark@substack.com / UX University
- medium.com
- newsletter.uxuniversity.io
- blog.cursor.sh
- ycombinator.com/blog
- arxiv.org

## Métricas de éxito
- El usuario puede lanzar una búsqueda y recibir al menos 3 conceptos atómicos por temática en menos de 2 minutos
- Los conceptos generados siguen exactamente la plantilla del Segundo Cerebro
- El archivo exportado se puede copiar directamente a Conocimiento/Conceptos/ sin editar
- El usuario puede agregar una fuente o temática nueva en menos de 30 segundos

## Decisiones cerradas
- Máximo 5 conceptos por agente por búsqueda
- Conceptos rechazados se eliminan permanentemente
- El campo `relacionado` se cruza automáticamente contra el ATLAS.md del Segundo Cerebro
