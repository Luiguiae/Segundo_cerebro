# Plan de Implementación — Rastreador de Conocimiento

## Objetivo
Sistema web de agentes IA que buscan contenido nuevo sobre 13 temáticas, generan conceptos atómicos en el formato del Segundo Cerebro, y permiten al único usuario (Luigui) aprobar, rechazar y exportar los resultados como archivos `.md`.

---

## Fases de implementación

### Fase 0 — Scaffolding del proyecto
Crear la estructura de carpetas y archivos base según la especificación. Configurar entornos de desarrollo para el servidor (Python/FastAPI) y la interfaz (React/Tailwind). No incluye lógica de negocio.

### Fase 1 — Modelo de datos (SQLite)
Definir los esquemas de las tablas: `conceptos`, `tematicas`, `fuentes`. Incluye scripts de migración/inicialización. Esta fase no requiere FastAPI activo.

### Fase 2 — Servidor base (FastAPI + configuración)
Levantar la aplicación FastAPI con los endpoints CRUD para temáticas y fuentes. El servidor puede arrancar, leer y escribir en SQLite, y exponer la API de configuración.

### Fase 3 — Agentes de búsqueda y generación
Implementar los tres agentes:
- **buscador.py**: llama a Tavily y a Jina Reader para recuperar contenido.
- **redactor.py**: genera el concepto atómico con Groq (fallback a Gemini), respetando la plantilla exacta.
- **orquestador.py**: recibe una lista de temáticas, lanza buscadores en paralelo y entrega resultados al redactor.

Dependencias externas: Tavily API, Jina Reader API, Groq API, Gemini API (todas vía variables de entorno).

### Fase 4 — Endpoints de flujo principal
Endpoints para:
- `POST /buscar` — lanza búsqueda bajo demanda por temática(s).
- `GET /conceptos` — devuelve cola de revisión (estado `pendiente`).
- `PATCH /conceptos/{id}/aprobar` — cambia estado a `aprobado`.
- `DELETE /conceptos/{id}` — elimina concepto rechazado.
- `POST /procesar` — entrada manual (URL o texto).

### Fase 5 — Endpoint de exportación
`POST /exportar` que recibe lista de IDs aprobados y devuelve un `.zip` con los `.md` de cada concepto usando la plantilla exacta del Segundo Cerebro.

### Fase 6 — Interfaz React
Construir la SPA con tres vistas:
- **Cola.jsx**: muestra conceptos pendientes con botones Aprobar / Rechazar.
- **Configuracion.jsx**: gestión de temáticas y fuentes.
- **Exportacion.jsx**: muestra aprobados, permite seleccionar y descargar `.zip`.

Componente compartido: **TarjetaConcepto.jsx**.

### Fase 7 — Cruce con INDEX.md del Segundo Cerebro
Lógica para inferir el campo `relacionado` cruzando el título y tags del concepto generado contra los conceptos existentes en el `INDEX.md` del Segundo Cerebro (cuando esté disponible en la sesión o como archivo subido).

### Fase 8 — Preparación para despliegue en Render
`render.yaml` o instrucciones de despliegue. Variables de entorno documentadas. Script de arranque único que sirve la API y los estáticos de React.

---

## Dependencias entre fases

```
Fase 0 → Fase 1 → Fase 2 → Fase 3 → Fase 4 → Fase 5
                                  ↓
                             Fase 6 (puede avanzar en paralelo desde Fase 2)
                                  ↓
                             Fase 7 (requiere Fase 4 completa)
                                  ↓
                             Fase 8 (requiere Fases 5 y 6 completas)
```

---

## Riesgos identificados

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| Groq y Gemini con rate limits en nivel gratuito | Media | Fallback ya diseñado; limitar a 5 conceptos por agente |
| Tavily devuelve resultados irrelevantes | Media | El redactor evalúa relevancia antes de generar el concepto |
| Jina Reader falla en sitios con paywall | Alta | El buscador marca el error y continúa con otros resultados |
| Plantilla de concepto atómico mal aplicada | Baja | Test unitario que valida la estructura YAML + 8 secciones |
| INDEX.md no disponible | Media | El campo `relacionado` queda vacío `[]` sin bloquear el flujo |
| Render nivel gratuito con cold start lento | Alta | Aceptado en v1; documentado en README |
