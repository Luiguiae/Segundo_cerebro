"""
Mejora 009 — Operaciones vault-aware via filesystem + parser manual de frontmatter.

No depende de PyYAML: el intérprete que ejecuta el daemon (/usr/local/bin/python3.11)
no tiene pyyaml instalado, y un `import yaml` a nivel de módulo sin protección
tumbaba el daemon completo al usar auditar_huerfanos/buscar_por_tag. El parser
manual de abajo cubre el subconjunto de YAML que usa la plantilla canónica del
vault (escalares, listas inline `[a, b]` y listas en bloque `- item`).
"""

import re
import os
from pathlib import Path

VAULT_PATH     = Path(os.path.expanduser("~/Documents/Segundo_cerebro"))
CONCEPTOS_PATH = VAULT_PATH / "Conocimiento" / "Conceptos"

# ── Helpers internos ───────────────────────────────────────────────────────────

_CAMPO_RE = re.compile(r'^([A-Za-z0-9_]+):\s*(.*)$')


def _parse_frontmatter(contenido: str) -> tuple[dict, str]:
    """Devuelve (campos, body_sin_frontmatter). Parser manual — sin PyYAML.
    Soporta escalares (`campo: valor`), listas inline (`campo: [a, b, c]`)
    y listas en bloque (`campo:` seguido de líneas `  - item`)."""
    if not contenido.startswith("---"):
        return {}, contenido
    partes = contenido.split("---", 2)
    if len(partes) < 3:
        return {}, contenido

    campos: dict = {}
    lineas = partes[1].splitlines()
    i, n = 0, len(lineas)
    while i < n:
        linea = lineas[i]
        if not linea.strip() or linea.strip().startswith("#"):
            i += 1
            continue
        m = _CAMPO_RE.match(linea)
        if not m:
            i += 1
            continue
        clave, resto = m.group(1), m.group(2).strip()

        if resto.startswith("[") and resto.endswith("]"):
            # lista inline: [a, b, c]
            items = [x.strip().strip('"').strip("'") for x in resto[1:-1].split(",") if x.strip()]
            campos[clave] = items
            i += 1
        elif resto == "":
            # posible lista en bloque (o mapa anidado, ej. fuentes:) — recolecta líneas indentadas
            items: list = []
            es_lista_simple = True
            j = i + 1
            while j < n and (lineas[j].startswith("  ") or not lineas[j].strip()):
                sub = lineas[j].strip()
                if sub.startswith("- "):
                    valor = sub[2:].strip().strip('"').strip("'")
                    if ":" in valor:
                        es_lista_simple = False  # item de mapa anidado (ej. "- titulo: ...")
                    else:
                        items.append(valor)
                elif sub:
                    es_lista_simple = False
                j += 1
            if es_lista_simple and items:
                campos[clave] = items
            i = j
        else:
            campos[clave] = resto.strip('"').strip("'")
            i += 1

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
        texto = archivo.read_text(encoding="utf-8", errors="replace")
        campos, body = _parse_frontmatter(texto)
        for slug in (campos.get("relacionado") or []):
            con_backlink.add(slug)
        for match in re.findall(r'\[\[([^\]|]+)', body):
            con_backlink.add(match.strip())
    return sorted(todos - con_backlink)

def buscar_por_tag(tag: str) -> list[str]:
    """Retorna slugs (stem del archivo, apto para TTS) de conceptos con el tag dado."""
    resultado = []
    for archivo in _todos_los_conceptos():
        texto = archivo.read_text(encoding="utf-8", errors="replace")
        campos, _ = _parse_frontmatter(texto)
        tags = campos.get("tags") or []
        if tag in tags:
            resultado.append(archivo.stem)
    return resultado
