"""
Mejora 009 — Operaciones vault-aware.

Las funciones de análisis (backlinks, huérfanos, tag search, patch) usan filesystem
directo + YAML — no dependen de que Obsidian esté abierto y son más rápidas que
el protocolo MCP.

mcp_disponible() sigue chequeando el plugin MCP como señal de que Obsidian está
abierto (útil para operaciones que SÍ requieren Obsidian, como renombrar con
backlinks actualizados).
"""

import re
import yaml
import requests
import os
from pathlib import Path

VAULT_PATH     = Path(os.path.expanduser("~/Documents/Segundo_cerebro"))
CONCEPTOS_PATH = VAULT_PATH / "Conocimiento" / "Conceptos"
MCP_BASE       = "http://localhost:22360"

# ── Healthcheck ────────────────────────────────────────────────────────────────

def mcp_disponible() -> bool:
    """Retorna True si Obsidian está abierto (plugin MCP activo en puerto 22360).
    GET /sse sin Accept:text/event-stream retorna 406 — servidor vivo pero rechaza el header.
    """
    try:
        r = requests.get(f"{MCP_BASE}/sse", timeout=2)
        return r.status_code in (200, 406)
    except Exception:
        return False

# ── Helpers internos ───────────────────────────────────────────────────────────

def _parse_frontmatter(contenido: str) -> tuple[dict, str]:
    """Devuelve (campos_yaml, body_sin_frontmatter)."""
    if not contenido.startswith("---"):
        return {}, contenido
    partes = contenido.split("---", 2)
    if len(partes) < 3:
        return {}, contenido
    try:
        campos = yaml.safe_load(partes[1]) or {}
    except Exception:
        campos = {}
    return campos, partes[2]

def _todos_los_conceptos() -> list[Path]:
    """Lista todos los .md en Conocimiento/Conceptos/**"""
    return list(CONCEPTOS_PATH.rglob("*.md"))

# ── Operaciones de lectura del grafo ──────────────────────────────────────────

def listar_backlinks(slug: str) -> list[str]:
    """Retorna slugs de conceptos que apuntan al slug dado.
    Detecta tanto el campo `relacionado:` del frontmatter como [[wikilinks]] en el body.
    """
    patron_wiki = re.compile(rf'\[\[{re.escape(slug)}\]\]')
    resultado = []
    for archivo in _todos_los_conceptos():
        if archivo.stem == slug:
            continue
        texto = archivo.read_text(encoding="utf-8")
        campos, body = _parse_frontmatter(texto)
        relacionado = campos.get("relacionado") or []
        if slug in relacionado or patron_wiki.search(texto):
            resultado.append(archivo.stem)
    return resultado

def detectar_huerfanos() -> list[str]:
    """Retorna slugs de conceptos a los que ningún otro concepto apunta."""
    todos = {f.stem for f in _todos_los_conceptos()}
    con_backlink: set[str] = set()
    for archivo in _todos_los_conceptos():
        texto = archivo.read_text(encoding="utf-8")
        campos, body = _parse_frontmatter(texto)
        for slug in (campos.get("relacionado") or []):
            con_backlink.add(slug)
        for match in re.findall(r'\[\[([^\]|]+)', body):
            con_backlink.add(match.strip())
    return sorted(todos - con_backlink)

def buscar_por_tag(tag: str) -> list[str]:
    """Retorna rutas relativas (desde la raíz del vault) de conceptos con el tag dado."""
    resultado = []
    for archivo in _todos_los_conceptos():
        texto = archivo.read_text(encoding="utf-8")
        campos, _ = _parse_frontmatter(texto)
        tags = campos.get("tags") or []
        if tag in tags:
            resultado.append(str(archivo.relative_to(VAULT_PATH)))
    return resultado

# ── Escritura quirúrgica ───────────────────────────────────────────────────────

def patch_frontmatter(ruta_relativa: str, campos_nuevos: dict) -> bool:
    """Actualiza solo los campos indicados en el frontmatter. No toca el body."""
    archivo = VAULT_PATH / ruta_relativa
    if not archivo.exists():
        return False
    contenido = archivo.read_text(encoding="utf-8")
    campos, body = _parse_frontmatter(contenido)
    campos.update(campos_nuevos)
    nuevo = "---\n" + yaml.dump(campos, allow_unicode=True, sort_keys=False) + "---" + body
    archivo.write_text(nuevo, encoding="utf-8")
    return True

def renombrar_nota(ruta_actual: str, nuevo_nombre: str) -> bool:
    """Renombra el archivo físico. No actualiza backlinks — usar desde Obsidian para eso."""
    archivo = VAULT_PATH / ruta_actual
    if not archivo.exists():
        return False
    destino = archivo.parent / f"{nuevo_nombre}.md"
    archivo.rename(destino)
    return True

def patch_seccion(ruta_relativa: str, heading: str, nuevo_contenido: str) -> bool:
    """Reemplaza el contenido de una sección H2 sin tocar el resto del archivo."""
    archivo = VAULT_PATH / ruta_relativa
    if not archivo.exists():
        return False
    contenido = archivo.read_text(encoding="utf-8")
    patron = re.compile(
        rf'(## {re.escape(heading)}\n)(.*?)(?=\n## |\Z)',
        re.DOTALL
    )
    if not patron.search(contenido):
        return False
    nuevo = patron.sub(rf'\g<1>{nuevo_contenido}\n', contenido)
    archivo.write_text(nuevo, encoding="utf-8")
    return True
