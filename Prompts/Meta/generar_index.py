#!/usr/bin/env python3
"""
generar_index.py
Recorre Conocimiento/Conceptos/, extrae el frontmatter de cada nota atómica
y genera un INDEX.md con mapa de conceptos, tags y relaciones.

Uso:
    python generar_index.py
    python generar_index.py --base /ruta/a/Segundo_cerebro
"""

import argparse
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ── Configuración ──────────────────────────────────────────────────────────────
DEFAULT_BASE = Path.home() / "Documents" / "Segundo_cerebro"
CONCEPTOS_DIR = "Conocimiento/Conceptos"
OUTPUT_FILE   = "Conocimiento/INDEX.md"
# ───────────────────────────────────────────────────────────────────────────────


def parse_frontmatter(text: str) -> dict:
    """Extrae el bloque YAML entre --- y lo parsea manualmente (sin dependencias)."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    meta = {}
    block = match.group(1)

    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key   = key.strip()
        value = value.strip()

        # Listas inline: [a, b, c]
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            meta[key] = [v.strip().strip('"').strip("'")
                         for v in inner.split(",") if v.strip()]
        # Valor entre comillas
        elif value.startswith('"') and value.endswith('"'):
            meta[key] = value[1:-1]
        else:
            meta[key] = value

    return meta


def cargar_conceptos(directorio: Path) -> list[dict]:
    """Lee todos los .md en el directorio y devuelve lista de metadatos + nombre de archivo."""
    conceptos = []
    for archivo in sorted(directorio.glob("*.md")):
        texto = archivo.read_text(encoding="utf-8")
        meta  = parse_frontmatter(texto)
        if not meta:
            continue
        meta["_archivo"] = archivo.stem          # nombre sin extensión
        meta["_ruta"]    = str(archivo.relative_to(directorio.parent.parent))
        conceptos.append(meta)
    return conceptos


def construir_indice_tags(conceptos: list[dict]) -> dict[str, list[str]]:
    indice = defaultdict(list)
    for c in conceptos:
        for tag in c.get("tags", []):
            if tag:
                indice[tag].append(c["_archivo"])
    return dict(sorted(indice.items()))


def construir_grafo_relaciones(conceptos: list[dict]) -> dict[str, list[str]]:
    grafo = defaultdict(list)
    for c in conceptos:
        nombre = c["_archivo"]
        for rel in c.get("relacionado", []):
            rel_limpio = rel.strip("[]").strip()
            if rel_limpio:
                grafo[nombre].append(rel_limpio)
    return dict(grafo)


def generar_markdown(conceptos: list[dict],
                     indice_tags: dict,
                     grafo: dict,
                     fecha_gen: str) -> str:

    lineas = [
        "# 🧠 INDEX — Segundo Cerebro",
        f"\n> Generado automáticamente el {fecha_gen}  ",
        f"> Total de conceptos: **{len(conceptos)}**\n",
        "---\n",
    ]

    # ── 1. Tabla de conceptos ─────────────────────────────────────────────────
    lineas += [
        "## 📚 Todos los conceptos\n",
        "| Concepto | Tags | Estado | Fecha | Fuente |",
        "|----------|------|--------|-------|--------|",
    ]
    for c in conceptos:
        titulo  = c.get("titulo", c["_archivo"])
        tags    = ", ".join(f"`{t}`" for t in c.get("tags", []) if t) or "—"
        estado  = c.get("estado", "—")
        fecha   = c.get("fecha", "—")
        fuente  = c.get("fuente", {})
        if isinstance(fuente, dict):
            tipo_fuente = fuente.get("tipo", "—")
        else:
            tipo_fuente = str(fuente)
        archivo = c["_archivo"]
        lineas.append(f"| [[{archivo}\\|{titulo}]] | {tags} | {estado} | {fecha} | {tipo_fuente} |")

    lineas.append("")

    # ── 2. Índice por tags ────────────────────────────────────────────────────
    lineas += ["---\n", "## 🏷️ Índice por tags\n"]
    for tag, archivos in indice_tags.items():
        lineas.append(f"### `{tag}`")
        for a in archivos:
            lineas.append(f"- [[{a}]]")
        lineas.append("")

    # ── 3. Mapa de relaciones ─────────────────────────────────────────────────
    lineas += ["---\n", "## 🔗 Mapa de relaciones\n"]
    if grafo:
        for concepto, relaciones in sorted(grafo.items()):
            lineas.append(f"**[[{concepto}]]** →")
            for r in relaciones:
                lineas.append(f"  - [[{r}]]")
            lineas.append("")
    else:
        lineas.append("_Aún no hay relaciones definidas. "
                      "Agrega el campo `relacionado` en tus notas._\n")

    # ── 4. Conceptos sin relaciones ───────────────────────────────────────────
    huerfanos = [c["_archivo"] for c in conceptos
                 if not c.get("relacionado")]
    if huerfanos:
        lineas += ["---\n", "## ⚠️ Conceptos sin relaciones\n",
                   "_Estos conceptos aún no tienen conexiones definidas:_\n"]
        for h in huerfanos:
            lineas.append(f"- [[{h}]]")
        lineas.append("")

    # ── 5. Instrucciones rápidas ──────────────────────────────────────────────
    lineas += [
        "---\n",
        "## ⚡ Cómo usar este índice\n",
        "1. **Agregar un concepto**: crea un `.md` en `Conocimiento/Conceptos/` usando la plantilla.",
        "2. **Regenerar el índice**: ejecuta `python Prompts/Meta/generar_index.py`",
        "3. **Buscar correlaciones**: filtra por tags o busca en el mapa de relaciones.",
        "4. **Generar presentación**: pasa los nombres de los conceptos a Claude con el prompt en `Prompts/Presentaciones/`.",
        "",
    ]

    return "\n".join(lineas)


def main():
    parser = argparse.ArgumentParser(description="Genera INDEX.md del Segundo Cerebro")
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE,
                        help="Ruta raíz del Segundo Cerebro")
    args = parser.parse_args()

    base          = args.base
    dir_conceptos = base / CONCEPTOS_DIR
    ruta_output   = base / OUTPUT_FILE

    if not dir_conceptos.exists():
        print(f"❌ No encontré el directorio: {dir_conceptos}")
        print("   Crea primero la carpeta Conocimiento/Conceptos/ en tu Segundo Cerebro.")
        return

    conceptos = cargar_conceptos(dir_conceptos)

    if not conceptos:
        print(f"⚠️  No hay conceptos en {dir_conceptos}")
        print("   Agrega archivos .md usando la plantilla concepto-atomico.md")
        return

    indice_tags = construir_indice_tags(conceptos)
    grafo       = construir_grafo_relaciones(conceptos)
    fecha_gen   = datetime.now().strftime("%Y-%m-%d %H:%M")
    contenido   = generar_markdown(conceptos, indice_tags, grafo, fecha_gen)

    ruta_output.write_text(contenido, encoding="utf-8")

    print(f"✅ INDEX.md generado en: {ruta_output}")
    print(f"   Conceptos procesados : {len(conceptos)}")
    print(f"   Tags únicos          : {len(indice_tags)}")
    print(f"   Conceptos con links  : {len(grafo)}")


if __name__ == "__main__":
    main()
