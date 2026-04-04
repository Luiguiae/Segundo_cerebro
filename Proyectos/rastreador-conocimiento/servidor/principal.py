"""
Aplicación principal FastAPI del Rastreador de Conocimiento.
Punto de entrada del servidor: inicializa la base de datos, registra
los routers y expone todos los endpoints de la API.
"""

import asyncio
import io
import json
import logging
import re
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from modelos import Concepto, Tematica, inicializar_bd, motor
from configuracion import obtener_sesion, router_fuentes, router_tematicas
from agentes.orquestador import orquestar
from agentes.buscador import extraer_url
from agentes.redactor import generar_concepto, ErrorGeneracion

logger = logging.getLogger(__name__)


@asynccontextmanager
async def vida_util(app: FastAPI):
    inicializar_bd()
    yield


app = FastAPI(
    title="Rastreador de Conocimiento",
    description="API para gestionar agentes de búsqueda y conceptos atómicos.",
    version="0.1.0",
    lifespan=vida_util,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_tematicas)
app.include_router(router_fuentes)

# Servir estáticos del build de React (solo si existen)
_DIR_ESTATICOS = Path(__file__).parent / "estaticos"
if _DIR_ESTATICOS.exists():
    app.mount("/assets", StaticFiles(directory=_DIR_ESTATICOS / "assets"), name="assets")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SolicitudBusqueda(BaseModel):
    ids_tematicas: list[int]


class RespuestaBusqueda(BaseModel):
    ids_creados: list[int]
    total: int


class SolicitudExportar(BaseModel):
    ids: list[int]


class SolicitudProcesar(BaseModel):
    entrada: str
    tematica_id: int | None = None  # opcional: aplica contexto especializado


class ConceptoRespuesta(BaseModel):
    id: int
    titulo: str
    alias: str
    tags: str
    tipo: str
    fecha: str
    fuente_tipo: str
    fuente_referencia: str
    fuente_autor: str
    relacionado: str
    proyectos: str
    estado: str
    que_es: str
    por_que_importa: str
    como_funciona: str
    ejemplos: str
    tensiones: str
    se_conecta_con: str
    citas: str
    mis_notas: str
    tematica_id: int | None
    creado_en: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/salud", tags=["sistema"])
def salud():
    return {"estado": "ok"}


@app.post("/buscar", response_model=RespuestaBusqueda, tags=["flujo"])
async def buscar_conceptos(
    solicitud: SolicitudBusqueda,
    sesion: Session = Depends(obtener_sesion),
):
    """
    Lanza un par buscador+redactor por cada temática seleccionada en paralelo.
    Guarda los conceptos generados con estado 'pendiente' y devuelve sus IDs.
    """
    if not solicitud.ids_tematicas:
        raise HTTPException(status_code=422, detail="La lista de ids_tematicas no puede estar vacía.")

    conceptos_data = await orquestar(solicitud.ids_tematicas, sesion)

    if not conceptos_data:
        raise HTTPException(
            status_code=502,
            detail="El orquestador no generó ningún concepto. Revisa las claves de API y los logs.",
        )

    ids_creados = []
    for datos in conceptos_data:
        # Eliminar campos internos que no pertenecen al modelo
        datos.pop("_texto_completo", None)
        datos.pop("tono_usado", None)

        nuevo = Concepto(**datos)
        sesion.add(nuevo)
        sesion.flush()  # obtener el ID antes del commit
        ids_creados.append(nuevo.id)

    sesion.commit()
    logger.info("POST /buscar — %d conceptos guardados: %s", len(ids_creados), ids_creados)

    return RespuestaBusqueda(ids_creados=ids_creados, total=len(ids_creados))


@app.patch("/conceptos/{id}/aprobar", tags=["flujo"])
def aprobar_concepto(id: int, sesion: Session = Depends(obtener_sesion)):
    """Cambia el estado del concepto a 'aprobado'."""
    concepto = sesion.get(Concepto, id)
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado.")
    if concepto.estado == "aprobado":
        raise HTTPException(status_code=409, detail="El concepto ya está aprobado.")
    concepto.estado = "aprobado"
    sesion.commit()
    return {"id": id, "estado": concepto.estado}


@app.delete("/conceptos/{id}", status_code=204, tags=["flujo"])
def rechazar_concepto(id: int, sesion: Session = Depends(obtener_sesion)):
    """Elimina permanentemente un concepto (rechazado)."""
    concepto = sesion.get(Concepto, id)
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado.")
    sesion.delete(concepto)
    sesion.commit()


_PATRON_URL = re.compile(r"^https?://\S+", re.IGNORECASE)

# Contexto genérico para entradas manuales sin temática asignada
_CONTEXTO_MANUAL = {
    "id":                   None,
    "nombre":               "Entrada manual",
    "terminos_busqueda":    [],
    "terminos_busqueda_en": [],
    "fuentes_prioritarias": [],
    "tono_prompt":          "Neutral y preciso. Sintetiza fielmente el contenido recibido sin añadir interpretaciones propias.",
}


@app.post("/procesar", tags=["flujo"])
async def procesar_entrada(
    solicitud: SolicitudProcesar,
    sesion: Session = Depends(obtener_sesion),
):
    """
    Procesa una URL o texto libre. Si es URL extrae el contenido con Jina Reader,
    luego genera un concepto atómico y lo guarda con estado 'pendiente'.
    Acepta opcionalmente un tematica_id para aplicar contexto especializado.
    """
    entrada = solicitud.entrada.strip()
    if not entrada:
        raise HTTPException(status_code=422, detail="El campo 'entrada' no puede estar vacío.")

    es_url = bool(_PATRON_URL.match(entrada))

    if es_url:
        contenido = await asyncio.to_thread(extraer_url, entrada)
        if not contenido:
            raise HTTPException(
                status_code=422,
                detail="No se pudo extraer contenido de la URL. Puede ser un sitio con paywall o restricciones.",
            )
        resultado = {"titulo": entrada, "url": entrada, "fragmento": "", "contenido_completo": contenido}
    else:
        resultado = {"titulo": "Texto manual", "url": "", "fragmento": entrada, "contenido_completo": entrada}

    # Contexto: temática específica si se proporcionó, genérico si no
    if solicitud.tematica_id:
        tematica = sesion.get(Tematica, solicitud.tematica_id)
        if not tematica:
            raise HTTPException(status_code=404, detail="Temática no encontrada.")
        contexto = {
            "id":                   tematica.id,
            "nombre":               tematica.nombre,
            "terminos_busqueda":    json.loads(tematica.terminos_busqueda),
            "terminos_busqueda_en": json.loads(tematica.terminos_busqueda_en),
            "fuentes_prioritarias": json.loads(tematica.fuentes_prioritarias),
            "tono_prompt":          tematica.tono_prompt,
        }
    else:
        contexto = _CONTEXTO_MANUAL

    try:
        datos = await asyncio.to_thread(generar_concepto, contexto, [resultado])
    except ErrorGeneracion as e:
        raise HTTPException(status_code=502, detail=f"Error al generar el concepto: {e}")

    datos.pop("_texto_completo", None)
    datos.pop("tono_usado", None)

    nuevo = Concepto(**datos)
    sesion.add(nuevo)
    sesion.commit()
    sesion.refresh(nuevo)

    logger.info("POST /procesar — concepto id=%d creado desde %s", nuevo.id, "URL" if es_url else "texto")
    return {"id": nuevo.id, "titulo": nuevo.titulo, "estado": nuevo.estado}


def _concepto_a_markdown(c: Concepto) -> str:
    """Serializa un Concepto a texto markdown con frontmatter YAML + 8 secciones."""
    alias    = json.loads(c.alias    or "[]")
    tags     = json.loads(c.tags     or "[]")
    relacionado = json.loads(c.relacionado or "[]")
    proyectos   = json.loads(c.proyectos   or "[]")

    alias_yaml      = json.dumps(alias,      ensure_ascii=False)
    tags_yaml       = json.dumps(tags,       ensure_ascii=False)
    relacionado_yaml = json.dumps(relacionado, ensure_ascii=False)
    proyectos_yaml  = json.dumps(proyectos,  ensure_ascii=False)

    return f"""\
---
titulo: "{c.titulo}"
alias: {alias_yaml}
tags: {tags_yaml}
tipo: {c.tipo or "concepto"}
fecha: {c.fecha}
fuente:
  tipo: {c.fuente_tipo or "articulo"}
  referencia: "{c.fuente_referencia}"
  autor: "{c.fuente_autor}"
relacionado: {relacionado_yaml}
proyectos: {proyectos_yaml}
estado: borrador
---
## ¿Qué es?
{c.que_es}

## ¿Por qué importa?
{c.por_que_importa}

## ¿Cómo funciona?
{c.como_funciona}

## Ejemplos concretos
{c.ejemplos}

## Tensiones o limitaciones
{c.tensiones}

## Se conecta con...
{c.se_conecta_con}

## Citas o fragmentos clave
{c.citas}

## Mis notas
{c.mis_notas}
"""


def _nombre_archivo(c: Concepto) -> str:
    """Genera un nombre de archivo kebab-case sin caracteres especiales."""
    nombre = c.titulo.lower()
    nombre = re.sub(r"[áàäâ]", "a", nombre)
    nombre = re.sub(r"[éèëê]", "e", nombre)
    nombre = re.sub(r"[íìïî]", "i", nombre)
    nombre = re.sub(r"[óòöô]", "o", nombre)
    nombre = re.sub(r"[úùüû]", "u", nombre)
    nombre = re.sub(r"ñ", "n", nombre)
    nombre = re.sub(r"[^a-z0-9\s-]", "", nombre)
    nombre = re.sub(r"[\s]+", "-", nombre.strip())
    nombre = re.sub(r"-+", "-", nombre)
    return f"{nombre[:80]}.md"


@app.post("/exportar", tags=["flujo"])
def exportar_conceptos(
    solicitud: SolicitudExportar,
    sesion: Session = Depends(obtener_sesion),
):
    """
    Genera un .zip en memoria con un .md por cada concepto aprobado solicitado.
    Cada .md sigue exactamente la plantilla del Segundo Cerebro.
    """
    if not solicitud.ids:
        raise HTTPException(status_code=422, detail="La lista de ids no puede estar vacía.")

    conceptos = (
        sesion.query(Concepto)
        .filter(Concepto.id.in_(solicitud.ids), Concepto.estado == "aprobado")
        .all()
    )

    if not conceptos:
        raise HTTPException(
            status_code=404,
            detail="Ninguno de los IDs corresponde a un concepto aprobado.",
        )

    buffer = io.BytesIO()
    nombres_usados: dict[str, int] = {}

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for concepto in conceptos:
            nombre = _nombre_archivo(concepto)
            # Evitar colisiones de nombre dentro del zip
            if nombre in nombres_usados:
                nombres_usados[nombre] += 1
                nombre = nombre.replace(".md", f"-{nombres_usados[nombre]}.md")
            else:
                nombres_usados[nombre] = 1

            zf.writestr(nombre, _concepto_a_markdown(concepto).encode("utf-8"))

    buffer.seek(0)
    logger.info("POST /exportar — %d conceptos exportados", len(conceptos))

    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=conceptos.zip"},
    )


@app.get("/conceptos/aprobados", tags=["flujo"])
def listar_aprobados(sesion: Session = Depends(obtener_sesion)):
    """Devuelve todos los conceptos con estado 'aprobado', más recientes primero."""
    conceptos = (
        sesion.query(Concepto)
        .filter(Concepto.estado == "aprobado")
        .order_by(Concepto.creado_en.desc())
        .all()
    )
    return [
        {"id": c.id, "titulo": c.titulo, "tematica_id": c.tematica_id,
         "creado_en": c.creado_en.isoformat()}
        for c in conceptos
    ]


@app.get("/conceptos", tags=["flujo"])
def listar_conceptos(sesion: Session = Depends(obtener_sesion)):
    # IMPORTANTE: este endpoint debe declararse ANTES de la catch-all SPA
    """Devuelve todos los conceptos con estado 'pendiente', más recientes primero."""
    conceptos = (
        sesion.query(Concepto)
        .filter(Concepto.estado == "pendiente")
        .order_by(Concepto.creado_en.desc())
        .all()
    )
    return [
        {
            "id":               c.id,
            "titulo":           c.titulo,
            "alias":            c.alias,
            "tags":             c.tags,
            "tipo":             c.tipo,
            "fecha":            c.fecha,
            "fuente_tipo":      c.fuente_tipo,
            "fuente_referencia": c.fuente_referencia,
            "fuente_autor":     c.fuente_autor,
            "relacionado":      c.relacionado,
            "proyectos":        c.proyectos,
            "estado":           c.estado,
            "que_es":           c.que_es,
            "por_que_importa":  c.por_que_importa,
            "como_funciona":    c.como_funciona,
            "ejemplos":         c.ejemplos,
            "tensiones":        c.tensiones,
            "se_conecta_con":   c.se_conecta_con,
            "citas":            c.citas,
            "mis_notas":        c.mis_notas,
            "tematica_id":      c.tematica_id,
            "creado_en":        c.creado_en.isoformat(),
        }
        for c in conceptos
    ]


# ---------------------------------------------------------------------------
# SPA fallback — debe ir AL FINAL para no interceptar rutas de la API
# ---------------------------------------------------------------------------

@app.get("/{ruta_completa:path}", include_in_schema=False)
def servir_spa(ruta_completa: str):
    """Captura todas las rutas del frontend y devuelve index.html."""
    index = _DIR_ESTATICOS / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"error": "Interfaz no compilada. Ejecuta 'npm run build' en interfaz/"}
