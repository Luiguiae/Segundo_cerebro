"""
Orquestador de agentes por temática.
Recibe una lista de IDs de temáticas, recupera su contexto completo
desde la base de datos y lanza en paralelo un par buscador+redactor
por cada temática usando asyncio.gather.
"""

import asyncio
import json
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from modelos import Fuente, Tematica
from agentes.buscador import buscar
from agentes.redactor import generar_concepto, ErrorGeneracion

logger = logging.getLogger(__name__)


def _tematica_a_contexto(t: Tematica) -> dict:
    """Convierte un objeto Tematica en el dict de contexto que esperan buscador y redactor."""
    return {
        "id":                    t.id,
        "nombre":                t.nombre,
        "terminos_busqueda":     json.loads(t.terminos_busqueda),
        "terminos_busqueda_en":  json.loads(t.terminos_busqueda_en),
        "fuentes_prioritarias":  json.loads(t.fuentes_prioritarias),
        "tono_prompt":           t.tono_prompt,
    }


async def _procesar_tematica(
    contexto: dict,
    fuentes_globales: list[str],
) -> list[dict]:
    """
    Par buscador + redactor para una sola temática.
    Corre en su propio hilo para no bloquear el event loop.
    Devuelve lista de conceptos generados (puede ser vacía si falla).
    """
    nombre = contexto["nombre"]
    inicio = datetime.now()
    logger.info("[%s] inicio búsqueda — %s", nombre, inicio.isoformat())

    # --- Búsqueda (sync en hilo separado) ---
    try:
        resultados = await asyncio.to_thread(buscar, contexto, fuentes_globales)
    except Exception as e:
        logger.error("[%s] buscador falló: %s", nombre, e)
        return []

    if not resultados:
        logger.warning("[%s] buscador no devolvió resultados", nombre)
        return []

    logger.info("[%s] buscador devolvió %d resultados", nombre, len(resultados))

    # --- Generación del concepto (sync en hilo separado) ---
    try:
        concepto = await asyncio.to_thread(generar_concepto, contexto, resultados)
    except ErrorGeneracion as e:
        logger.error("[%s] redactor falló: %s", nombre, e)
        return []

    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    logger.info("[%s] concepto generado en %.1fs — título: %s", nombre, duracion, concepto.get("titulo"))

    return [concepto]


async def orquestar(ids_tematicas: list[int], db: Session) -> list[dict]:
    """
    Lanza en paralelo un par buscador+redactor por cada temática seleccionada.

    Parámetros:
        ids_tematicas: lista de IDs de Tematica a procesar
        db: sesión SQLAlchemy activa

    Retorna:
        Lista plana de dicts de concepto listos para insertar en la BD.
        Los errores por temática se loguean y se omiten sin detener el batch.
    """
    if not ids_tematicas:
        return []

    # Recuperar contextos desde la BD
    tematicas = (
        db.query(Tematica)
        .filter(Tematica.id.in_(ids_tematicas), Tematica.activa == True)
        .all()
    )
    if not tematicas:
        logger.warning("Ninguna temática activa encontrada para IDs: %s", ids_tematicas)
        return []

    # Pool global de fuentes activas
    fuentes_globales = [
        f.url for f in db.query(Fuente).filter(Fuente.activa == True).all()
    ]

    contextos = [_tematica_a_contexto(t) for t in tematicas]

    inicio_total = datetime.now()
    logger.info(
        "Orquestando %d temáticas en paralelo: %s",
        len(contextos),
        [c["nombre"] for c in contextos],
    )

    # Lanzar todos los pares buscador+redactor en paralelo
    resultados_por_tematica = await asyncio.gather(
        *[_procesar_tematica(ctx, fuentes_globales) for ctx in contextos],
        return_exceptions=False,
    )

    fin_total = datetime.now()
    duracion_total = (fin_total - inicio_total).total_seconds()

    # Aplanar la lista de listas
    conceptos = [c for lista in resultados_por_tematica for c in lista]

    logger.info(
        "Orquestación completa: %d conceptos generados en %.1fs total",
        len(conceptos),
        duracion_total,
    )

    return conceptos
