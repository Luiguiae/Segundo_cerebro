"""
Cruzador con el ATLAS.md del Segundo Cerebro.
Lee los conceptos existentes y cruza tags y términos del título
contra el concepto nuevo para inferir el campo 'relacionado'.
Si el ATLAS.md no existe o falla, devuelve lista vacía sin bloquear.
"""

import os
import re
import logging
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

# Ruta por defecto: desde agentes/ subir 5 niveles → raíz del Segundo Cerebro
# agentes/ → servidor/ → rastreador-conocimiento/ → Proyectos/ → Segundo_cerebro/
_RUTA_DEFAULT = Path(__file__).parent.parent.parent.parent.parent / "Conocimiento" / "ATLAS.md"
MAX_RELACIONADOS = 5


def _ruta_index() -> Path:
    env = os.getenv("RUTA_INDEX_MD", "")
    return Path(env).expanduser() if env else _RUTA_DEFAULT


# ---------------------------------------------------------------------------
# Parseo del ATLAS.md
# ---------------------------------------------------------------------------

# Línea de tabla: | [[slug|Nombre]] | `tag1`, `tag2`, ... | ...
_RE_FILA = re.compile(
    r"\|\s*\[\[(?P<slug>[^\]|]+)(?:\|(?P<nombre>[^\]]+))?\]\]"
    r"\s*\|\s*(?P<tags>[^|]*)\|",
    re.IGNORECASE,
)
_RE_TAG = re.compile(r"`([^`]+)`")


def _parsear_index(texto: str) -> list[dict]:
    """
    Extrae lista de {nombre, slug, tags} de la tabla del ATLAS.md.
    nombre: texto para mostrar (o slug si no hay alias).
    tags:   set de strings en minúsculas.
    """
    conceptos = []
    for m in _RE_FILA.finditer(texto):
        slug   = m.group("slug").strip()
        nombre = (m.group("nombre") or slug).strip()
        tags   = {t.lower() for t in _RE_TAG.findall(m.group("tags"))}
        conceptos.append({"nombre": nombre, "slug": slug, "tags": tags})
    return conceptos


@lru_cache(maxsize=1)
def _cargar_conceptos_index() -> list[dict]:
    """Carga y parsea el ATLAS.md una sola vez (cached en memoria)."""
    ruta = _ruta_index()
    if not ruta.exists():
        logger.warning("ATLAS.md no encontrado en %s — campo 'relacionado' quedará vacío.", ruta)
        return []
    try:
        texto = ruta.read_text(encoding="utf-8")
        conceptos = _parsear_index(texto)
        logger.info("ATLAS.md cargado: %d conceptos existentes.", len(conceptos))
        return conceptos
    except Exception as e:
        logger.error("Error al leer ATLAS.md: %s", e)
        return []


def invalidar_cache() -> None:
    """Fuerza recarga del ATLAS.md en la próxima llamada (útil en tests)."""
    _cargar_conceptos_index.cache_clear()


# ---------------------------------------------------------------------------
# Lógica de cruce
# ---------------------------------------------------------------------------

def _normalizar(texto: str) -> set[str]:
    """Convierte un texto a un conjunto de tokens en minúsculas (≥ 3 chars)."""
    tokens = re.findall(r"[a-záéíóúüñ]+", texto.lower())
    return {t for t in tokens if len(t) >= 3}


def inferir_relacionados(titulo: str, tags: list[str]) -> list[str]:
    """
    Cruza el título y tags del concepto nuevo contra el ATLAS.md.
    Devuelve los nombres de los conceptos relacionados (máx. MAX_RELACIONADOS).
    Nunca lanza excepción.
    """
    try:
        conceptos_existentes = _cargar_conceptos_index()
        if not conceptos_existentes:
            return []

        tags_nuevo   = {t.lower() for t in tags}
        tokens_titulo = _normalizar(titulo)
        puntuaciones: list[tuple[int, str]] = []

        for c in conceptos_existentes:
            puntos = 0

            # Coincidencia exacta de tags (peso alto)
            coincidencias_tags = tags_nuevo & c["tags"]
            puntos += len(coincidencias_tags) * 3

            # Coincidencia de tokens del título contra tags del existente
            coincidencias_titulo_vs_tags = tokens_titulo & c["tags"]
            puntos += len(coincidencias_titulo_vs_tags) * 2

            # Coincidencia de tokens entre títulos
            tokens_existente = _normalizar(c["nombre"])
            coincidencias_titulos = tokens_titulo & tokens_existente
            puntos += len(coincidencias_titulos) * 1

            if puntos > 0:
                puntuaciones.append((puntos, c["nombre"]))

        # Ordenar por puntuación descendente y devolver los mejores
        puntuaciones.sort(key=lambda x: x[0], reverse=True)
        return [nombre for _, nombre in puntuaciones[:MAX_RELACIONADOS]]

    except Exception as e:
        logger.error("Error en inferir_relacionados: %s", e)
        return []
