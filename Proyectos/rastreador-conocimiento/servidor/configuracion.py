"""
Routers FastAPI para la gestión de temáticas y fuentes.
Expone los endpoints CRUD de /tematicas y /fuentes, permitiendo
agregar, editar y eliminar sin reiniciar el servidor.
"""

import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from modelos import Fuente, Tematica, motor


def obtener_sesion():
    with Session(motor) as sesion:
        yield sesion


# ---------------------------------------------------------------------------
# Schemas Pydantic
# ---------------------------------------------------------------------------

class TematicaCrear(BaseModel):
    nombre: str
    terminos_busqueda: list[str] = []
    terminos_busqueda_en: list[str] = []
    fuentes_prioritarias: list[str] = []
    tono_prompt: str = ""
    activa: bool = True


class TematicaActualizar(BaseModel):
    nombre: Optional[str] = None
    terminos_busqueda: Optional[list[str]] = None
    terminos_busqueda_en: Optional[list[str]] = None
    fuentes_prioritarias: Optional[list[str]] = None
    tono_prompt: Optional[str] = None
    activa: Optional[bool] = None


class TematicaRespuesta(BaseModel):
    id: int
    nombre: str
    terminos_busqueda: list[str]
    terminos_busqueda_en: list[str]
    fuentes_prioritarias: list[str]
    tono_prompt: str
    activa: bool

    model_config = {"from_attributes": True}


class FuenteCrear(BaseModel):
    url: str
    descripcion: str = ""
    activa: bool = True


class FuenteActualizar(BaseModel):
    url: Optional[str] = None
    descripcion: Optional[str] = None
    activa: Optional[bool] = None


class FuenteRespuesta(BaseModel):
    id: int
    url: str
    descripcion: str
    activa: bool

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Helpers de serialización
# ---------------------------------------------------------------------------

def _tematica_a_respuesta(t: Tematica) -> dict:
    return {
        "id": t.id,
        "nombre": t.nombre,
        "terminos_busqueda": json.loads(t.terminos_busqueda),
        "terminos_busqueda_en": json.loads(t.terminos_busqueda_en),
        "fuentes_prioritarias": json.loads(t.fuentes_prioritarias),
        "tono_prompt": t.tono_prompt,
        "activa": t.activa,
    }


# ---------------------------------------------------------------------------
# Router de temáticas
# ---------------------------------------------------------------------------

router_tematicas = APIRouter(prefix="/tematicas", tags=["tematicas"])


@router_tematicas.get("/", response_model=list[TematicaRespuesta])
def listar_tematicas(sesion: Session = Depends(obtener_sesion)):
    tematicas = sesion.query(Tematica).order_by(Tematica.id).all()
    return [_tematica_a_respuesta(t) for t in tematicas]


@router_tematicas.post("/", response_model=TematicaRespuesta, status_code=201)
def crear_tematica(datos: TematicaCrear, sesion: Session = Depends(obtener_sesion)):
    if sesion.query(Tematica).filter_by(nombre=datos.nombre).first():
        raise HTTPException(status_code=409, detail="Ya existe una temática con ese nombre.")
    nueva = Tematica(
        nombre=datos.nombre,
        terminos_busqueda=json.dumps(datos.terminos_busqueda),
        terminos_busqueda_en=json.dumps(datos.terminos_busqueda_en),
        fuentes_prioritarias=json.dumps(datos.fuentes_prioritarias),
        tono_prompt=datos.tono_prompt,
        activa=datos.activa,
    )
    sesion.add(nueva)
    sesion.commit()
    sesion.refresh(nueva)
    return _tematica_a_respuesta(nueva)


@router_tematicas.patch("/{id}", response_model=TematicaRespuesta)
def actualizar_tematica(id: int, datos: TematicaActualizar, sesion: Session = Depends(obtener_sesion)):
    tematica = sesion.get(Tematica, id)
    if not tematica:
        raise HTTPException(status_code=404, detail="Temática no encontrada.")
    if datos.nombre is not None:
        tematica.nombre = datos.nombre
    if datos.terminos_busqueda is not None:
        tematica.terminos_busqueda = json.dumps(datos.terminos_busqueda)
    if datos.terminos_busqueda_en is not None:
        tematica.terminos_busqueda_en = json.dumps(datos.terminos_busqueda_en)
    if datos.fuentes_prioritarias is not None:
        tematica.fuentes_prioritarias = json.dumps(datos.fuentes_prioritarias)
    if datos.tono_prompt is not None:
        tematica.tono_prompt = datos.tono_prompt
    if datos.activa is not None:
        tematica.activa = datos.activa
    sesion.commit()
    sesion.refresh(tematica)
    return _tematica_a_respuesta(tematica)


@router_tematicas.delete("/{id}", status_code=204)
def eliminar_tematica(id: int, sesion: Session = Depends(obtener_sesion)):
    tematica = sesion.get(Tematica, id)
    if not tematica:
        raise HTTPException(status_code=404, detail="Temática no encontrada.")
    sesion.delete(tematica)
    sesion.commit()


# ---------------------------------------------------------------------------
# Router de fuentes
# ---------------------------------------------------------------------------

router_fuentes = APIRouter(prefix="/fuentes", tags=["fuentes"])


@router_fuentes.get("/", response_model=list[FuenteRespuesta])
def listar_fuentes(sesion: Session = Depends(obtener_sesion)):
    return sesion.query(Fuente).order_by(Fuente.id).all()


@router_fuentes.post("/", response_model=FuenteRespuesta, status_code=201)
def crear_fuente(datos: FuenteCrear, sesion: Session = Depends(obtener_sesion)):
    if sesion.query(Fuente).filter_by(url=datos.url).first():
        raise HTTPException(status_code=409, detail="Ya existe una fuente con esa URL.")
    nueva = Fuente(url=datos.url, descripcion=datos.descripcion, activa=datos.activa)
    sesion.add(nueva)
    sesion.commit()
    sesion.refresh(nueva)
    return nueva


@router_fuentes.patch("/{id}", response_model=FuenteRespuesta)
def actualizar_fuente(id: int, datos: FuenteActualizar, sesion: Session = Depends(obtener_sesion)):
    fuente = sesion.get(Fuente, id)
    if not fuente:
        raise HTTPException(status_code=404, detail="Fuente no encontrada.")
    if datos.url is not None:
        fuente.url = datos.url
    if datos.descripcion is not None:
        fuente.descripcion = datos.descripcion
    if datos.activa is not None:
        fuente.activa = datos.activa
    sesion.commit()
    sesion.refresh(fuente)
    return fuente


@router_fuentes.delete("/{id}", status_code=204)
def eliminar_fuente(id: int, sesion: Session = Depends(obtener_sesion)):
    fuente = sesion.get(Fuente, id)
    if not fuente:
        raise HTTPException(status_code=404, detail="Fuente no encontrada.")
    sesion.delete(fuente)
    sesion.commit()
