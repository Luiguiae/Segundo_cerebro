"""
Mejora 009 — Operaciones vault-aware via filesystem + YAML directo.
"""

import re
import yaml
import os
from pathlib import Path

VAULT_PATH     = Path(os.path.expanduser("~/Documents/Segundo_cerebro"))
CONCEPTOS_PATH = VAULT_PATH / "Conocimiento" / "Conceptos"

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

# ── Operaciones de análisis del grafo ────────────────────────────────────────

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

