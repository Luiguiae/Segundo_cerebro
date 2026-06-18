"""
Mejora 009 — Operaciones vault-aware via MCP de Obsidian.
Corre SOLO cuando Obsidian está abierto (el plugin expone el WebSocket).
Para operaciones simples, usar filesystem directo (más rápido).
"""

import json
import requests
import os
from pathlib import Path

VAULT_PATH = Path(os.path.expanduser("~/Documents/Segundo_cerebro"))
MCP_BASE   = "http://localhost:22360"

# ── Healthcheck ────────────────────────────────────────────────────────────────

def mcp_disponible() -> bool:
    """Retorna True si el plugin MCP está corriendo (Obsidian abierto)."""
    try:
        r = requests.get(f"{MCP_BASE}/sse", timeout=2, stream=True)
        return r.status_code in (200, 400, 405)
    except Exception:
        return False

# ── Operaciones de lectura ─────────────────────────────────────────────────────

def listar_backlinks(slug: str) -> list[dict]:
    """
    Retorna lista de conceptos que apuntan al slug dado.
    Requiere que el slug sea el nombre del archivo sin extensión.
    """
    resp = requests.post(
        f"{MCP_BASE}/tools/get_backlinks",
        json={"notePath": f"Conocimiento/Conceptos/{slug}.md"},
        timeout=10
    )
    resp.raise_for_status()
    return resp.json().get("backlinks", [])

def detectar_huerfanos() -> list[str]:
    """
    Retorna lista de slugs en Conocimiento/Conceptos/** que no tienen
    ningún backlink apuntando hacia ellos.
    """
    resp = requests.post(
        f"{MCP_BASE}/tools/find_orphans",
        json={"folder": "Conocimiento/Conceptos/"},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json().get("orphans", [])

def buscar_por_tag(tag: str) -> list[str]:
    """
    Retorna lista de rutas relativas de conceptos que tienen el tag dado.
    """
    resp = requests.post(
        f"{MCP_BASE}/tools/search",
        json={"query": f"tag:{tag}"},
        timeout=10
    )
    resp.raise_for_status()
    return [r["path"] for r in resp.json().get("results", [])]

# ── Operaciones de escritura ───────────────────────────────────────────────────

def patch_frontmatter(ruta_relativa: str, campos: dict) -> bool:
    """
    Actualiza solo los campos indicados en el frontmatter de un archivo.
    No toca el body del concepto.
    ruta_relativa: ej. "Conocimiento/Conceptos/ia/agentes-ia.md"
    campos: dict con los campos a actualizar, ej. {"tags": ["ia", "nuevo-tag"]}
    """
    resp = requests.post(
        f"{MCP_BASE}/tools/update_frontmatter",
        json={"path": ruta_relativa, "frontmatter": campos},
        timeout=10
    )
    resp.raise_for_status()
    return resp.json().get("success", False)

def renombrar_nota(ruta_actual: str, nuevo_nombre: str) -> bool:
    """
    Renombra un archivo y actualiza automáticamente todos los backlinks
    que apuntan a él. Nuevo nombre sin extensión.
    """
    resp = requests.post(
        f"{MCP_BASE}/tools/rename_file",
        json={"oldPath": ruta_actual, "newName": nuevo_nombre},
        timeout=10
    )
    resp.raise_for_status()
    return resp.json().get("success", False)

def patch_seccion(ruta_relativa: str, heading: str, nuevo_contenido: str) -> bool:
    """
    Reemplaza el contenido de una sección específica (por heading H2)
    sin tocar el resto del archivo.
    """
    resp = requests.post(
        f"{MCP_BASE}/tools/patch_section",
        json={
            "path": ruta_relativa,
            "heading": heading,
            "content": nuevo_contenido
        },
        timeout=10
    )
    resp.raise_for_status()
    return resp.json().get("success", False)
