# Tareas atómicas — Rastreador de Conocimiento

> Cada tarea es independiente dentro de su fase. Ejecutar en el orden indicado.
> Criterio de completado: el punto de aceptación es verificable sin ambigüedad.

---

## Fase 0 — Scaffolding

### T-01 — Crear estructura de carpetas del proyecto
**Descripción**: Crear todos los directorios según la especificación (`servidor/agentes/`, `interfaz/src/vistas/`, `interfaz/src/componentes/`).
**Archivos afectados**: directorios nuevos dentro de `rastreador-conocimiento/`
**Criterio**: `ls -R` muestra exactamente la estructura de la especificación.

### T-02 — Crear archivos base vacíos con comentario de propósito
**Descripción**: Crear `servidor/principal.py`, `servidor/modelos.py`, `servidor/configuracion.py`, `servidor/agentes/orquestador.py`, `servidor/agentes/buscador.py`, `servidor/agentes/redactor.py` con un docstring en español que describa su propósito.
**Archivos afectados**: los 6 archivos `.py` listados.
**Criterio**: cada archivo existe y tiene su docstring.

### T-03 — Crear `requirements.txt`
**Descripción**: Listar dependencias Python: `fastapi`, `uvicorn`, `sqlalchemy`, `tavily-python`, `groq`, `google-generativeai`, `httpx`, `python-dotenv`.
**Archivos afectados**: `servidor/requirements.txt`
**Criterio**: `pip install -r requirements.txt` sin errores en Python 3.11.

### T-04 — Inicializar proyecto React con Vite + Tailwind
**Descripción**: Correr `npm create vite@latest interfaz -- --template react` y configurar Tailwind CSS. Eliminar boilerplate innecesario.
**Archivos afectados**: `interfaz/` (package.json, vite.config.js, tailwind.config.js, index.css)
**Criterio**: `npm run dev` levanta en localhost sin errores; Tailwind aplica clases.

### T-05 — Crear `.env.example` con todas las variables requeridas
**Descripción**: Documentar las variables de entorno necesarias: `TAVILY_API_KEY`, `JINA_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY`, `DATABASE_URL`.
**Archivos afectados**: `servidor/.env.example`
**Criterio**: el archivo existe y tiene las 5 variables con valor de ejemplo vacío.

---

## Fase 1 — Modelo de datos

### T-06 — Definir modelo `Concepto` en SQLAlchemy
**Descripción**: Tabla con campos: `id`, `titulo`, `alias`, `tags`, `tipo`, `fecha`, `fuente_tipo`, `fuente_referencia`, `fuente_autor`, `relacionado`, `proyectos`, `estado`, `que_es`, `por_que_importa`, `como_funciona`, `ejemplos`, `tensiones`, `se_conecta_con`, `citas`, `mis_notas`, `tematica_id`, `creado_en`.
**Archivos afectados**: `servidor/modelos.py`
**Criterio**: `from modelos import Concepto` sin errores; `Base.metadata.create_all()` crea la tabla en SQLite.

### T-07 — Definir modelo `Tematica` en SQLAlchemy
**Descripción**: Tabla con campos: `id`, `nombre`, `terminos_busqueda` (lista JSON de palabras clave para Tavily), `fuentes_prioritarias` (lista JSON de URLs que se anteponen al pool general), `tono_prompt` (texto libre que ajusta el estilo del redactor, ej. "técnico y riguroso" o "crítico y decolonial"), `activa`, `creado_en`. Pre-poblar con las 13 temáticas iniciales en la función de inicialización; cada una con sus `terminos_busqueda` y `tono_prompt` predefinidos.
**Archivos afectados**: `servidor/modelos.py`
**Criterio**: la función de inicialización inserta las 13 temáticas si la tabla está vacía; cada fila tiene valores no nulos en `terminos_busqueda` y `tono_prompt`.

### T-08 — Definir modelo `Fuente` en SQLAlchemy
**Descripción**: Tabla con campos: `id`, `url`, `descripcion`, `activa`, `creado_en`. Pre-poblar con las 8 fuentes iniciales.
**Archivos afectados**: `servidor/modelos.py`
**Criterio**: la función de inicialización inserta las 8 fuentes si la tabla está vacía.

### T-09 — Crear función `inicializar_bd()`
**Descripción**: Función que crea las tablas y siembra datos iniciales (temáticas y fuentes). Se llama una sola vez al arrancar el servidor.
**Archivos afectados**: `servidor/modelos.py`
**Criterio**: al ejecutar `python modelos.py` se crea `rastreador.db` con las 3 tablas y los datos semilla.

---

## Fase 2 — Servidor base

### T-10 — Levantar aplicación FastAPI mínima
**Descripción**: Instanciar `FastAPI()` en `principal.py`, conectar SQLite con SQLAlchemy, llamar `inicializar_bd()` en el startup. Agregar endpoint `GET /salud` que devuelve `{"estado": "ok"}`.
**Archivos afectados**: `servidor/principal.py`
**Criterio**: `uvicorn principal:app` arranca sin errores; `GET /salud` devuelve 200.

### T-11 — Endpoints CRUD de temáticas
**Descripción**: `GET /tematicas`, `POST /tematicas`, `PATCH /tematicas/{id}`, `DELETE /tematicas/{id}`.
**Archivos afectados**: `servidor/principal.py`, `servidor/configuracion.py`
**Criterio**: se puede crear, listar, editar y eliminar una temática vía Swagger UI.

### T-12 — Endpoints CRUD de fuentes
**Descripción**: `GET /fuentes`, `POST /fuentes`, `PATCH /fuentes/{id}`, `DELETE /fuentes/{id}`.
**Archivos afectados**: `servidor/principal.py`, `servidor/configuracion.py`
**Criterio**: se puede crear, listar, editar y eliminar una fuente vía Swagger UI.

---

## Fase 3 — Agentes

### T-13 — Implementar `buscador.py` con Tavily
**Descripción**: Función `buscar(contexto_tematica: dict, fuentes_globales: list[str]) -> list[dict]` donde `contexto_tematica` contiene `nombre`, `terminos_busqueda` y `fuentes_prioritarias`. La consulta a Tavily se construye combinando `terminos_busqueda`; el dominio de búsqueda prioriza `fuentes_prioritarias` y luego el pool global. Devuelve hasta 5 resultados con `titulo`, `url`, `fragmento`.
**Archivos afectados**: `servidor/agentes/buscador.py`
**Criterio**: llamar la función con contextos de dos temáticas distintas produce consultas Tavily diferentes; los resultados reflejan las fuentes prioritarias de cada una.

### T-14 — Implementar extracción de URL con Jina Reader en `buscador.py`
**Descripción**: Función `extraer_url(url: str) -> str` que llama a Jina Reader (`r.jina.ai/{url}`) y devuelve el texto limpio. Maneja errores (paywall, timeout) devolviendo cadena vacía.
**Archivos afectados**: `servidor/agentes/buscador.py`
**Criterio**: `extraer_url("https://example.com")` devuelve texto no vacío; una URL inválida devuelve `""` sin lanzar excepción.

### T-15 — Implementar `redactor.py` con Groq + fallback Gemini
**Descripción**: Función `generar_concepto(contexto_tematica: dict, contenido: str, fuente: dict) -> dict` donde `contexto_tematica` incluye `nombre` y `tono_prompt`. El system prompt del LLM se construye interpolando `tono_prompt` para ajustar el estilo de redacción al dominio (ej. las temáticas de Decolonización y Filosofía usan un tono distinto al de Vibe Coding). Si Groq falla (error HTTP o timeout), reintenta con Gemini. Si ambos fallan, lanza `ErrorGeneracion` con mensaje claro. El concepto devuelto respeta exactamente la plantilla YAML + 8 secciones.
**Archivos afectados**: `servidor/agentes/redactor.py`
**Criterio**: el mismo contenido procesado con dos `tono_prompt` distintos produce system prompts diferentes y salidas visiblemente distintas en estilo; el fallback se activa correctamente cuando se simula un fallo de Groq.

### T-16 — Implementar `orquestador.py`
**Descripción**: Función asíncrona `orquestar(ids_tematicas: list[int], db) -> list[dict]` que, para cada temática seleccionada, recupera su `contexto_tematica` completo (nombre, terminos_busqueda, fuentes_prioritarias, tono_prompt) desde la BD y lanza en paralelo un par independiente `buscador → redactor`. Cada par opera con su propio contexto: el buscador recibe `contexto_tematica` + fuentes globales; el redactor recibe `contexto_tematica` + los resultados del buscador. El paralelismo se implementa con `asyncio.gather`.
**Archivos afectados**: `servidor/agentes/orquestador.py`
**Criterio**: llamar con 2 temáticas devuelve al menos 2 conceptos con estilos y términos acordes a cada dominio; el tiempo total es menor que la suma de tiempos individuales (paralelismo real verificable con logs de timestamps).

---

## Fase 4 — Endpoints de flujo principal

### T-17 — Endpoint `POST /buscar`
**Descripción**: Recibe `{"tematicas": ["Agentes IA", "Vibe Coding"]}`. Llama al orquestador, guarda los conceptos generados en SQLite con estado `pendiente`, devuelve la lista de IDs creados.
**Archivos afectados**: `servidor/principal.py`
**Criterio**: la solicitud devuelve 200 con lista de IDs; los conceptos aparecen en la BD con estado `pendiente`.

### T-18 — Endpoint `GET /conceptos`
**Descripción**: Devuelve todos los conceptos con estado `pendiente`, ordenados por `creado_en` descendente.
**Archivos afectados**: `servidor/principal.py`
**Criterio**: después de `/buscar`, `/conceptos` devuelve los conceptos creados.

### T-19 — Endpoint `PATCH /conceptos/{id}/aprobar`
**Descripción**: Cambia el estado del concepto a `aprobado`.
**Archivos afectados**: `servidor/principal.py`
**Criterio**: el concepto deja de aparecer en la cola de pendientes; aparece en la lista de aprobados.

### T-20 — Endpoint `DELETE /conceptos/{id}`
**Descripción**: Elimina permanentemente el concepto (rechazado).
**Archivos afectados**: `servidor/principal.py`
**Criterio**: el concepto ya no existe en la BD tras la llamada.

### T-21 — Endpoint `POST /procesar` (entrada manual)
**Descripción**: Recibe `{"entrada": "<URL o texto>"}`. Si es URL, extrae con Jina Reader. Pasa el contenido al redactor. Guarda el concepto con estado `pendiente`.
**Archivos afectados**: `servidor/principal.py`
**Criterio**: pegar una URL real devuelve un concepto en la cola de revisión.

---

## Fase 5 — Exportación

### T-22 — Endpoint `POST /exportar`
**Descripción**: Recibe `{"ids": [1, 3, 5]}`. Para cada ID aprobado, genera el texto `.md` usando la plantilla exacta (YAML + 8 secciones). Empaqueta en un `.zip` en memoria. Devuelve el archivo como `application/zip`.
**Archivos afectados**: `servidor/principal.py`
**Criterio**: el `.zip` descargado contiene tantos `.md` como IDs enviados; cada `.md` pasa validación de estructura (encabezado YAML válido + 8 secciones presentes).

---

## Fase 6 — Interfaz React

### T-23 — Crear `Aplicacion.jsx` con enrutamiento entre vistas
**Descripción**: Componente raíz con navegación entre `Cola`, `Configuracion` y `Exportacion`. Usar estado local o React Router (ligero).
**Archivos afectados**: `interfaz/src/Aplicacion.jsx`
**Criterio**: las tres vistas son navegables sin recargar la página.

### T-24 — Crear `TarjetaConcepto.jsx`
**Descripción**: Componente que muestra `titulo`, `tematica`, `que_es` (primeras 200 caracteres) y botones Aprobar / Rechazar. Recibe callbacks como props.
**Archivos afectados**: `interfaz/src/componentes/TarjetaConcepto.jsx`
**Criterio**: el componente se renderiza con datos de prueba; los botones llaman a sus callbacks.

### T-25 — Crear vista `Cola.jsx`
**Descripción**: Carga `GET /conceptos`, muestra `TarjetaConcepto` por cada pendiente. Al aprobar llama `PATCH /conceptos/{id}/aprobar`; al rechazar llama `DELETE /conceptos/{id}`. Botón "Buscar" con selector de temáticas que llama `POST /buscar`.
**Archivos afectados**: `interfaz/src/vistas/Cola.jsx`
**Criterio**: el flujo completo (buscar → ver tarjetas → aprobar/rechazar) funciona sin errores en el navegador.

### T-26 — Crear vista `Configuracion.jsx`
**Descripción**: Lista y formularios para agregar/editar/eliminar temáticas y fuentes, usando los endpoints CRUD.
**Archivos afectados**: `interfaz/src/vistas/Configuracion.jsx`
**Criterio**: se puede agregar una temática nueva y aparece inmediatamente en la lista sin recargar.

### T-27 — Crear vista `Exportacion.jsx`
**Descripción**: Lista conceptos aprobados con checkboxes. Botón "Exportar seleccionados" llama `POST /exportar` y descarga el `.zip`.
**Archivos afectados**: `interfaz/src/vistas/Exportacion.jsx`
**Criterio**: seleccionar 2 conceptos aprobados y exportar descarga un `.zip` con 2 archivos `.md`.

---

## Fase 7 — Cruce con ATLAS.md

### T-28 — Implementar inferencia del campo `relacionado`
**Descripción**: En `redactor.py`, si existe la variable de entorno `SEGUNDO_CEREBRO_INDEX` con la ruta al `ATLAS.md`, leer el archivo, extraer los títulos de conceptos existentes, y hacer una comparación semántica simple (palabras clave en común) entre el concepto nuevo y los existentes. Poblar `relacionado` con los títulos más cercanos (máximo 5). Si la variable no existe, dejar `relacionado: []`.
**Archivos afectados**: `servidor/agentes/redactor.py`
**Criterio**: con un `ATLAS.md` de prueba, el campo `relacionado` del concepto generado contiene al menos 1 título relevante.

---

## Fase 8 — Despliegue

### T-29 — Configurar `build` de React para servirse desde FastAPI
**Descripción**: `vite.config.js` genera los estáticos en `servidor/estaticos/`. FastAPI sirve `index.html` en la ruta raíz y los archivos estáticos en `/assets/`.
**Archivos afectados**: `interfaz/vite.config.js`, `servidor/principal.py`
**Criterio**: `npm run build` seguido de `uvicorn principal:app` sirve la aplicación completa en `localhost:8000`.

### T-30 — Crear `render.yaml` y `AGENTES.md`
**Descripción**: `render.yaml` define el servicio web (comando de arranque, variables de entorno requeridas). `AGENTES.md` documenta las restricciones globales del proyecto para Claude Code.
**Archivos afectados**: `rastreador-conocimiento/render.yaml`, `rastreador-conocimiento/AGENTES.md`
**Criterio**: `render.yaml` es válido según la especificación de Render; `AGENTES.md` lista todas las restricciones críticas del proyecto.
