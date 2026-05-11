#!/usr/bin/env python3
"""
generar_index.py  v3
Recorre Conocimiento/Conceptos/, extrae frontmatter y primer párrafo de cada
nota atómica, y genera un ATLAS.md con mapa de conceptos, tags, relaciones y
grafo tipado de edges (mejora-006).

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
DEFAULT_BASE  = Path.home() / "Documents" / "Segundo_cerebro"
CONCEPTOS_DIR = "Conocimiento/Conceptos"
OUTPUT_FILE   = "Conocimiento/ATLAS.md"
RESUMEN_MAX   = 120

TIPOS_RELACION = [
    "contradicts",
    "requires",
    "enables",
    "refines",
    "extends",
    "exemplifies",
    "same_mechanism_as",
    "analogous_to",
    "precedes",
]
# ───────────────────────────────────────────────────────────────────────────────


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extrae el bloque YAML entre --- y lo parsea manualmente (sin dependencias).
    Soporta: listas inline [a, b], valores en comillas, y secuencias de objetos
    (campo edges: con lista de dicts indentados).
    Devuelve (meta, cuerpo) donde cuerpo es el texto después del frontmatter."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    meta   = {}
    block  = match.group(1)
    cuerpo = match.group(2)
    lines  = block.splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip indented lines — handled inside block-sequence branches
        if line.startswith(" ") or line.startswith("\t"):
            i += 1
            continue
        if not line.strip() or ":" not in line:
            i += 1
            continue

        key, _, value = line.partition(":")
        key   = key.strip()
        value = value.strip()

        # Block sequence: key with empty value followed by indented "- " items
        if value == "":
            j = i + 1
            block_lines = []
            while j < len(lines) and (
                lines[j].startswith("  ") or lines[j].startswith("\t")
            ):
                block_lines.append(lines[j])
                j += 1

            if block_lines and block_lines[0].strip().startswith("- "):
                items        = []
                current_item = None
                for bl in block_lines:
                    stripped = bl.strip()
                    if stripped.startswith("- "):
                        content = stripped[2:]
                        if ":" in content:
                            # Dict item (e.g. edges: - target: foo)
                            current_item = {}
                            items.append(current_item)
                            ik, _, iv = content.partition(":")
                            current_item[ik.strip()] = iv.strip().strip('"').strip("'")
                        else:
                            # Scalar item (e.g. relacionado: - pit-stop-cognitivo)
                            items.append(content.strip().strip('"').strip("'"))
                            current_item = None
                    elif stripped and current_item is not None and ":" in stripped:
                        ik, _, iv = stripped.partition(":")
                        current_item[ik.strip()] = iv.strip().strip('"').strip("'")
                meta[key] = items
                i = j
                continue
            # else: empty-value scalar
            meta[key] = value

        elif value.startswith("[") and value.endswith("]"):
            inner    = value[1:-1]
            meta[key] = [
                v.strip().strip('"').strip("'")
                for v in inner.split(",")
                if v.strip()
            ]
        elif value.startswith('"') and value.endswith('"'):
            meta[key] = value[1:-1]
        else:
            meta[key] = value

        i += 1

    return meta, cuerpo


def extract_resumen(cuerpo: str) -> str:
    """Extrae el primer párrafo con contenido del cuerpo de un concepto."""
    for line in cuerpo.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if re.match(r"^[-*_>|`]+$", line):
            continue
        if len(line) > RESUMEN_MAX:
            return line[:RESUMEN_MAX - 1] + "…"
        return line
    return "—"


def cargar_conceptos(directorio: Path) -> list[dict]:
    """Lee todos los .md en el directorio y devuelve lista de metadatos."""
    conceptos = []
    for archivo in sorted(directorio.rglob("*.md")):
        texto        = archivo.read_text(encoding="utf-8")
        meta, cuerpo = parse_frontmatter(texto)
        if not meta:
            continue
        meta["_archivo"] = archivo.stem
        meta["_ruta"]    = str(archivo.relative_to(directorio.parent.parent))
        meta["_resumen"] = extract_resumen(cuerpo)
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


def construir_grafo_tipado(conceptos: list[dict]) -> dict[str, list[dict]]:
    """Lee el campo edges: de cada concepto y construye grafo tipado."""
    grafo = {}
    for c in conceptos:
        edges = c.get("edges", [])
        if edges and isinstance(edges, list):
            grafo[c["_archivo"]] = edges
    return grafo


def agrupar_por_familia(conceptos: list[dict]) -> dict[str, list[dict]]:
    grupos = defaultdict(list)
    for c in conceptos:
        familia = c.get("familia", "sin-familia") or "sin-familia"
        grupos[familia].append(c)
    return dict(sorted(grupos.items()))


def generar_markdown(
    conceptos:    list[dict],
    indice_tags:  dict,
    grafo:        dict,
    grafo_tipado: dict,
    fecha_gen:    str,
) -> tuple[str, int]:

    con_resumen = sum(1 for c in conceptos if c["_resumen"] != "—")

    lineas = [
        "# ATLAS — Segundo Cerebro",
        "",
        f"> Generado automáticamente el {fecha_gen}  ",
        f"> Total de conceptos: **{len(conceptos)}**  ",
        "> **Context Layer**: Jarvis lee este archivo al inicio de cada sesión para operar sin abrir los conceptos individuales.",
        "> Contiene la tabla completa de conceptos, sus resúmenes, tags, relaciones y grafo tipado de edges.",
        "",
        "---",
        "",
    ]

    # ── 1. Tabla de conceptos ─────────────────────────────────────────────────
    lineas += [
        "## Todos los conceptos",
        "",
        "| Concepto | Resumen | Tags | Estado | Fecha |",
        "|----------|---------|------|--------|-------|",
    ]
    for c in conceptos:
        titulo  = c.get("titulo", c["_archivo"])
        resumen = c["_resumen"]
        tags    = ", ".join(f"`{t}`" for t in c.get("tags", []) if t) or "—"
        estado  = c.get("estado", "—")
        fecha   = c.get("fecha", "—")
        archivo = c["_archivo"]
        lineas.append(
            f"| [[{archivo}\\|{titulo}]] | {resumen} | {tags} | {estado} | {fecha} |"
        )
    lineas.append("")

    # ── 2. Conceptos por familia ──────────────────────────────────────────────
    lineas += ["---", "", "## Conceptos por familia", ""]
    grupos = agrupar_por_familia(conceptos)
    for familia, miembros in grupos.items():
        lineas.append(f"### `{familia}`")
        lineas.append("")
        for c in miembros:
            titulo  = c.get("titulo", c["_archivo"])
            archivo = c["_archivo"]
            resumen = c["_resumen"]
            lineas.append(f"- [[{archivo}\\|{titulo}]]")
            lineas.append(f"  → {resumen}")
        lineas.append("")

    # ── 3. Índice por tags ────────────────────────────────────────────────────
    lineas += ["---", "", "## Índice por tags", ""]
    for tag, archivos in indice_tags.items():
        lineas.append(f"### `{tag}`")
        for a in archivos:
            lineas.append(f"- [[{a}]]")
        lineas.append("")

    # ── 4. Mapa de relaciones (relacionado:) ──────────────────────────────────
    lineas += ["---", "", "## Mapa de relaciones", ""]
    if grafo:
        for concepto, relaciones in sorted(grafo.items()):
            lineas.append(f"**[[{concepto}]]** →")
            for r in relaciones:
                lineas.append(f"  - [[{r}]]")
            lineas.append("")
    else:
        lineas.append(
            "_Aún no hay relaciones definidas. "
            "Agrega el campo `relacionado` en tus notas._"
        )
        lineas.append("")

    # ── 5. Grafo tipado de edges ──────────────────────────────────────────────
    lineas += ["---", "", "## Grafo tipado de relaciones", ""]
    if grafo_tipado:
        # Agrupar por tipo de relación
        por_tipo: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for concepto, edges in sorted(grafo_tipado.items()):
            for edge in edges:
                tipo   = edge.get("tipo", "sin-tipo")
                target = edge.get("target", "?")
                por_tipo[tipo].append((concepto, target))

        total_edges = sum(len(v) for v in por_tipo.values())
        lineas.append(f"> {len(grafo_tipado)} conceptos con edges · {total_edges} edges en total")
        lineas.append("")

        # Tipos predefinidos primero, en orden canónico
        tipos_presentes = set(por_tipo.keys())
        for tipo in TIPOS_RELACION:
            if tipo not in por_tipo:
                continue
            lineas.append(f"### `{tipo}`")
            for origen, destino in sorted(por_tipo[tipo]):
                lineas.append(f"- [[{origen}]] → [[{destino}]]")
            lineas.append("")

        # Tipos no previstos al final
        for tipo in sorted(tipos_presentes - set(TIPOS_RELACION)):
            lineas.append(f"### `{tipo}` _(tipo no estándar)_")
            for origen, destino in sorted(por_tipo[tipo]):
                lineas.append(f"- [[{origen}]] → [[{destino}]]")
            lineas.append("")

        # Conceptos sin edges todavía
        sin_edges = [
            c["_archivo"] for c in conceptos
            if c["_archivo"] not in grafo_tipado
        ]
        if sin_edges:
            lineas += [
                "---",
                "",
                "### Conceptos sin edges tipados",
                "",
                "_Estos conceptos aún no tienen `edges:` definidos:_",
                "",
            ]
            for h in sin_edges:
                lineas.append(f"- [[{h}]]")
            lineas.append("")
    else:
        lineas.append("_No hay edges tipados definidos todavía. Agrega el campo `edges:` en tus notas._")
        lineas.append("")

    # ── 6. Conceptos sin relaciones (relacionado:) ────────────────────────────
    huerfanos = [c["_archivo"] for c in conceptos if not c.get("relacionado")]
    if huerfanos:
        lineas += ["---", "", "## Conceptos sin relaciones", "",
                   "_Estos conceptos aún no tienen conexiones definidas:_", ""]
        for h in huerfanos:
            lineas.append(f"- [[{h}]]")
        lineas.append("")

    # ── 7. Instrucciones rápidas ──────────────────────────────────────────────
    lineas += [
        "---",
        "",
        "## Cómo usar este índice",
        "",
        "1. **Agregar un concepto**: crea un `.md` en `Conocimiento/Conceptos/` usando la plantilla.",
        "2. **Regenerar el índice**: ejecuta `python3 Prompts/Meta/generar_index.py`",
        "3. **Buscar correlaciones**: filtra por tags o busca en el mapa de relaciones.",
        "4. **Navegar el grafo**: usa la sección 'Grafo tipado de relaciones' para seguir edges por tipo.",
        "5. **Generar entregables**: usa los prompts en `Prompts/JARVIS/prompts-jarvis.md`.",
        "",
    ]

    return "\n".join(lineas), con_resumen


def main():
    parser = argparse.ArgumentParser(description="Genera ATLAS.md del Segundo Cerebro")
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

    indice_tags  = construir_indice_tags(conceptos)
    grafo        = construir_grafo_relaciones(conceptos)
    grafo_tipado = construir_grafo_tipado(conceptos)
    fecha_gen    = datetime.now().strftime("%Y-%m-%d %H:%M")
    contenido, con_resumen = generar_markdown(
        conceptos, indice_tags, grafo, grafo_tipado, fecha_gen
    )

    ruta_output.write_text(contenido, encoding="utf-8")

    sin_resumen = [c["_archivo"] for c in conceptos if c["_resumen"] == "—"]
    con_edges   = len(grafo_tipado)
    total_edges = sum(len(v) for v in grafo_tipado.values())

    print(f"✅ ATLAS.md generado en: {ruta_output}")
    print(f"   Conceptos procesados : {len(conceptos)}")
    print(f"   Con resumen extraído : {con_resumen}")
    print(f"   Sin resumen (—)      : {len(sin_resumen)}")
    print(f"   Tags únicos          : {len(indice_tags)}")
    print(f"   Conceptos con links  : {len(grafo)}")
    print(f"   Conceptos con edges  : {con_edges}")
    print(f"   Total edges tipados  : {total_edges}")
    if sin_resumen:
        print(f"   ⚠️  Sin resumen       : {', '.join(sin_resumen)}")


if __name__ == "__main__":
    main()
