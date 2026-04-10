# AGENTES.md — Restricciones globales para Claude Code

Este archivo define las reglas que Claude Code debe respetar en todo momento
al trabajar en el proyecto Rastreador de Conocimiento.

---

## Idioma

- Todo el código fuente debe estar en español: nombres de carpetas, archivos,
  variables, funciones, clases, columnas de BD y comentarios.
- La única excepción son las palabras clave del lenguaje (Python, JavaScript)
  y los nombres de librerías externas.

## Seguridad

- Nunca escribir claves de API en el código fuente.
- Todas las claves se leen exclusivamente desde variables de entorno.
- El archivo `.env` nunca debe commitearse — está en `.gitignore`.
- El archivo de referencia es `.env.example` (sin valores reales).

## Base de datos

- SQLite es la única base de datos permitida en v1.
- No introducir PostgreSQL, MySQL ni ninguna dependencia externa de BD.
- El archivo `rastreador.db` no se commitea — está en `.gitignore`.

## Plantilla de concepto atómico

La plantilla del Segundo Cerebro debe respetarse exactamente en todo momento:

```
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

- El campo `estado` en los archivos exportados siempre es `borrador`.
- El campo `relacionado` se infiere automáticamente via `cruzador.py`.

## Pila técnica — no modificar sin justificación

| Capa       | Tecnología                          |
|------------|-------------------------------------|
| Servidor   | Python 3.11+, FastAPI, SQLAlchemy   |
| BD         | SQLite                              |
| Interfaz   | React + Vite + Tailwind CSS         |
| Búsqueda   | Tavily API                          |
| Extracción | Jina Reader API                     |
| Generación | Groq (llama-3.3-70b) → Gemini (gemini-2.5-flash) |
| Despliegue | Render nivel gratuito               |

## Límites de operación

- Máximo 5 conceptos generados por agente por búsqueda.
- Conceptos rechazados se eliminan permanentemente (sin papelera).
- El campo `relacionado` cruza contra el ATLAS.md del Segundo Cerebro;
  si el archivo no existe, queda `[]` sin bloquear el flujo.

## Estructura de archivos — no renombrar sin actualizar este documento

```
rastreador-conocimiento/
├── documentos/          ← especificación, plan, tareas
├── servidor/
│   ├── principal.py
│   ├── modelos.py
│   ├── configuracion.py
│   ├── agentes/
│   │   ├── orquestador.py
│   │   ├── buscador.py
│   │   ├── redactor.py
│   │   └── cruzador.py
│   ├── estaticos/       ← generado por npm run build (no commitear)
│   └── requirements.txt
├── interfaz/
│   └── src/
│       ├── Aplicacion.jsx
│       ├── vistas/
│       │   ├── Cola.jsx
│       │   ├── Configuracion.jsx
│       │   └── Exportacion.jsx
│       └── componentes/
│           └── TarjetaConcepto.jsx
├── render.yaml
└── AGENTES.md
```
