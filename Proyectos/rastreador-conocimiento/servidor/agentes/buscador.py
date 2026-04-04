"""
Agente de búsqueda web especializado por temática.
Usa Tavily API para buscar contenido relevante a partir del contexto
de la temática (términos de búsqueda y fuentes prioritarias), y Jina
Reader para extraer el texto limpio de cada URL encontrada.
"""

import os
import httpx
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
JINA_API_KEY = os.getenv("JINA_API_KEY", "")
MAX_RESULTADOS = 5
TIMEOUT_JINA = 15  # segundos


def _construir_query(terminos: list[str]) -> str:
    """Une los términos con OR para ampliar el alcance en Tavily."""
    return " OR ".join(f'"{t}"' for t in terminos[:3])


def _buscar_tavily(query: str, dominios: list[str]) -> list[dict]:
    """
    Llama a Tavily con la query y restringe por dominios cuando se proporcionan.
    Devuelve lista de {titulo, url, fragmento}.
    """
    cliente = TavilyClient(api_key=TAVILY_API_KEY)
    kwargs = {
        "query": query,
        "search_depth": "basic",
        "max_results": MAX_RESULTADOS,
    }
    if dominios:
        kwargs["include_domains"] = dominios

    respuesta = cliente.search(**kwargs)
    return [
        {
            "titulo": r.get("title", ""),
            "url": r.get("url", ""),
            "fragmento": r.get("content", ""),
        }
        for r in respuesta.get("results", [])
        if r.get("url")
    ]


def extraer_url(url: str) -> str:
    """
    Extrae el texto limpio de una URL usando Jina Reader (r.jina.ai).
    Devuelve cadena vacía si falla (paywall, timeout, error HTTP).
    """
    cabeceras = {"Accept": "text/plain"}
    if JINA_API_KEY:
        cabeceras["Authorization"] = f"Bearer {JINA_API_KEY}"

    try:
        respuesta = httpx.get(
            f"https://r.jina.ai/{url}",
            headers=cabeceras,
            timeout=TIMEOUT_JINA,
            follow_redirects=True,
        )
        respuesta.raise_for_status()
        return respuesta.text.strip()
    except Exception:
        return ""


def buscar(contexto_tematica: dict, fuentes_globales: list[str]) -> list[dict]:
    """
    Busca contenido relevante para la temática en dos idiomas y devuelve
    hasta MAX_RESULTADOS resultados con el texto completo extraído.

    Parámetros:
        contexto_tematica: dict con claves
            - nombre (str)
            - terminos_busqueda (list[str])     — en español
            - terminos_busqueda_en (list[str])  — en inglés
            - fuentes_prioritarias (list[str])
            - tono_prompt (str)
        fuentes_globales: list[str] — pool compartido de fuentes (URLs/dominios)

    Retorna:
        list[dict] con claves: titulo, url, fragmento, contenido_completo
    """
    terminos_es = contexto_tematica.get("terminos_busqueda", [])
    terminos_en = contexto_tematica.get("terminos_busqueda_en", [])
    fuentes_prioritarias = contexto_tematica.get("fuentes_prioritarias", [])

    resultados_vistos: dict[str, dict] = {}  # url → resultado (deduplicación)

    # --- Ronda 1: búsqueda en fuentes prioritarias (ES + EN) ---
    if fuentes_prioritarias:
        for terminos, idioma in [(terminos_es, "es"), (terminos_en, "en")]:
            if not terminos:
                continue
            query = _construir_query(terminos)
            for r in _buscar_tavily(query, fuentes_prioritarias):
                if r["url"] not in resultados_vistos:
                    r["idioma_busqueda"] = idioma
                    resultados_vistos[r["url"]] = r
            if len(resultados_vistos) >= MAX_RESULTADOS:
                break

    # --- Ronda 2: búsqueda en pool global si no alcanzamos el máximo ---
    if len(resultados_vistos) < MAX_RESULTADOS and fuentes_globales:
        for terminos, idioma in [(terminos_es, "es"), (terminos_en, "en")]:
            if not terminos or len(resultados_vistos) >= MAX_RESULTADOS:
                break
            query = _construir_query(terminos)
            for r in _buscar_tavily(query, fuentes_globales):
                if r["url"] not in resultados_vistos:
                    r["idioma_busqueda"] = idioma
                    resultados_vistos[r["url"]] = r
                if len(resultados_vistos) >= MAX_RESULTADOS:
                    break

    # --- Ronda 3: búsqueda sin restricción de dominio si aún faltan resultados ---
    if len(resultados_vistos) < MAX_RESULTADOS:
        for terminos, idioma in [(terminos_es, "es"), (terminos_en, "en")]:
            if not terminos or len(resultados_vistos) >= MAX_RESULTADOS:
                break
            query = _construir_query(terminos)
            for r in _buscar_tavily(query, []):
                if r["url"] not in resultados_vistos:
                    r["idioma_busqueda"] = idioma
                    resultados_vistos[r["url"]] = r
                if len(resultados_vistos) >= MAX_RESULTADOS:
                    break

    # --- Extracción de contenido completo con Jina ---
    resultados_finales = list(resultados_vistos.values())[:MAX_RESULTADOS]
    for resultado in resultados_finales:
        texto_completo = extraer_url(resultado["url"])
        # Si Jina no devuelve nada, el fragmento de Tavily sirve como respaldo
        resultado["contenido_completo"] = texto_completo or resultado["fragmento"]

    return resultados_finales
