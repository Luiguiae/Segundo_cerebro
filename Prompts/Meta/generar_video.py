#!/usr/bin/env python3
"""
generar_video.py — Bridge entre el vault del Segundo Cerebro y Remotion.

Uso:
  python3 generar_video.py concepto <slug-o-ruta>
  python3 generar_video.py presentacion <titulo> <slug1> [slug2 ...]

Salida: Videos/<nombre>.mp4
"""

import sys
import os
import re
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

VAULT = Path(__file__).parent.parent.parent
REMOTION_DIR = VAULT / "remotion"
VIDEOS_DIR = VAULT / "Videos"
CONCEPTOS_DIR = VAULT / "Conocimiento" / "Conceptos"


# ── Markdown parsing ──────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extracts YAML frontmatter and body from a markdown string."""
    if not text.startswith("---"):
        return {}, text
    try:
        end = text.index("\n---", 3)
    except ValueError:
        return {}, text
    yaml_block = text[4:end]
    body = text[end + 4:].strip()
    return parse_yaml_simple(yaml_block), body


def parse_yaml_simple(yaml: str) -> dict:
    """Minimal YAML parser for vault frontmatter (no external deps)."""
    result: dict = {}
    lines = yaml.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        if ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest.startswith("["):
                # Inline list
                items = re.findall(r"[\w\-\.]+", rest[1:rest.index("]")])
                result[key] = items
            elif rest == "" or rest == "|":
                # Block list follows
                items = []
                i += 1
                while i < len(lines) and lines[i].startswith(" "):
                    stripped = lines[i].strip()
                    if stripped.startswith("- "):
                        items.append(stripped[2:].strip())
                    i += 1
                result[key] = items
                continue
            else:
                result[key] = rest.strip('"').strip("'")
        i += 1
    return result


def extract_section(body: str, heading: str) -> str:
    """Extracts the text of a markdown ## section."""
    pattern = rf"## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, body, re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def resolve_md_path(ref: str) -> Path:
    """
    Resolves a .md reference to an absolute path.
    Accepts: absolute path, path relative to vault root, or slug (searches Conceptos/).
    """
    p = Path(ref)

    # Absolute path or relative path that exists
    if p.is_absolute() and p.exists():
        return p
    if not p.is_absolute():
        # Try relative to vault root
        vault_relative = VAULT / ref
        if vault_relative.exists():
            return vault_relative
        # Try relative to current working directory
        cwd_relative = Path.cwd() / ref
        if cwd_relative.exists():
            return cwd_relative

    # Slug search in Conceptos/ (add .md if missing)
    slug = p.stem if p.suffix == ".md" else p.name
    for path in CONCEPTOS_DIR.rglob(f"{slug}.md"):
        return path

    sys.exit(f"ERROR: No se encontró el archivo '{ref}'. "
             f"Verificá la ruta o que el slug exista en Conceptos/")


# ── Props builders ────────────────────────────────────────────────────────────

def first_paragraph(section: str, max_chars: int = 600) -> str:
    paras = [p.strip() for p in section.split("\n\n") if p.strip()]
    return paras[0][:max_chars] if paras else ""


def extract_title_from_body(body: str) -> str:
    """Falls back to H1 heading in the body if frontmatter has no title."""
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else "Sin título"


def build_concepto_props(ref: str) -> dict:
    path = resolve_md_path(ref)
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    slug = path.stem
    titulo_raw = fm.get("titulo", "")
    titulo = titulo_raw.strip('"').strip("'") if titulo_raw else extract_title_from_body(body)

    el_concepto = first_paragraph(extract_section(body, "El concepto"))
    por_que_importa = first_paragraph(extract_section(body, "Por qué importa"))
    tensiones = first_paragraph(extract_section(body, "Tensiones y límites"), 500)

    # Fallback: if vault sections are missing, use first 3 paragraphs of body as content
    if not el_concepto and not por_que_importa:
        paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("#")]
        el_concepto = paras[0][:600] if len(paras) > 0 else ""
        por_que_importa = paras[1][:600] if len(paras) > 1 else ""
        tensiones = paras[2][:500] if len(paras) > 2 else ""

    relacionado = fm.get("relacionado", [])
    if isinstance(relacionado, str):
        relacionado = [relacionado]

    return {
        "titulo": titulo or slug,
        "familia": fm.get("familia", "epistemologia-practica"),
        "tags": fm.get("tags", []),
        "relacionado": relacionado,
        "elConcepto": el_concepto,
        "porQueImporta": por_que_importa,
        "tensiones": tensiones,
    }


def build_presentacion_props(titulo: str, refs: list[str]) -> dict:
    slides = []
    for ref in refs:
        try:
            path = resolve_md_path(ref)
        except SystemExit:
            print(f"AVISO: '{ref}' no encontrado, omitiendo.", file=sys.stderr)
            continue

        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        concepto_text = extract_section(body, "El concepto")
        paras = [p.strip() for p in concepto_text.split("\n\n") if p.strip()]
        insight = paras[0][:400] if paras else first_paragraph(body, 400)

        importa_text = extract_section(body, "Por qué importa")
        importa_paras = [p.strip() for p in importa_text.split("\n\n") if p.strip()]
        detalle = importa_paras[0][:300] if importa_paras else None

        titulo_slide = fm.get("titulo", "")
        titulo_slide = titulo_slide.strip('"').strip("'") if titulo_slide else extract_title_from_body(body) or path.stem

        slides.append({
            "titulo": titulo_slide,
            "familia": fm.get("familia", "epistemologia-practica"),
            "insight": insight,
            **({"detalle": detalle} if detalle else {}),
        })

    return {
        "tituloGeneral": titulo,
        "slides": slides,
    }


# ── Render ────────────────────────────────────────────────────────────────────

def _verificar_remotion_disponible() -> None:
    """Falla temprano y con mensaje claro si el proyecto remotion/ no está armado,
    en vez de dejar que `npx remotion render` truene con un error críptico."""
    entry = REMOTION_DIR / "src" / "index.ts"
    package_json = REMOTION_DIR / "package.json"
    if not entry.exists() or not package_json.exists():
        sys.exit(
            "ERROR: el proyecto remotion/ no está completo "
            f"(falta {'src/index.ts' if not entry.exists() else 'package.json'}).\n"
            "Los comandos 'Jarvis, genera video' y 'genera presentacion' no pueden "
            "funcionar hasta restaurar remotion/src y remotion/package.json."
        )


def render(composition_id: str, props: dict, output_name: str) -> Path:
    _verificar_remotion_disponible()
    VIDEOS_DIR.mkdir(exist_ok=True)
    output_path = VIDEOS_DIR / f"{output_name}.mp4"

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(props, f, ensure_ascii=False, indent=2)
        props_file = f.name

    try:
        cmd = [
            "npx", "--yes", "remotion", "render",
            "src/index.ts",
            composition_id,
            str(output_path),
            f"--props={props_file}",
        ]
        print(f"\n→ Renderizando {composition_id}...")
        print(f"  Output: {output_path}\n")
        result = subprocess.run(cmd, cwd=str(REMOTION_DIR), check=True, timeout=600)
    finally:
        os.unlink(props_file)

    return output_path


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "concepto":
        ref = sys.argv[2]
        props = build_concepto_props(ref)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_slug = re.sub(r"[^a-z0-9]+", "-", props["titulo"].lower()).strip("-")[:60]
        output = render("ConceptoVideo", props, f"{timestamp}_{output_slug}")
        print(f"\n✓ Video generado: {output}")

    elif mode == "presentacion":
        if len(sys.argv) < 4:
            sys.exit("ERROR: 'presentacion' requiere: <titulo> <slug1> [slug2 ...]")
        titulo = sys.argv[2]
        slugs = sys.argv[3:]
        props = build_presentacion_props(titulo, slugs)
        if not props["slides"]:
            sys.exit("ERROR: Ningún concepto encontrado. Verifica los slugs.")
        timestamp = datetime.now().strftime("%Y-%m-%d")
        titulo_slug = re.sub(r"[^a-z0-9]+", "-", titulo.lower()).strip("-")
        output = render("PresentacionVideo", props, f"{timestamp}_{titulo_slug}")
        print(f"\n✓ Video generado: {output}")

    else:
        sys.exit(f"ERROR: Modo desconocido '{mode}'. Usa 'concepto' o 'presentacion'.")


if __name__ == "__main__":
    main()
