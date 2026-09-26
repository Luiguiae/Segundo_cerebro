#!/usr/bin/env python3
"""
poda-por-uso.py — Mejora E del paquete de mejoras 2026-09-26 (poda de conceptos por uso).

Escanea Conocimiento/Conceptos/, cuenta las referencias ENTRANTES de cada concepto y
lista los que llevan más de 90 días sin que nadie los cite. Solo REPORTE: escribe
Conocimiento/Mantenimiento/poda-candidatos.md y nada más. No borra, mueve ni modifica
ningún concepto ni correlación (tampoco su frontmatter): "archivar" es decisión de
Luigui, y marcar el frontmatter de un concepto es una decisión de schema aparte.

Señal de uso (v1) — un concepto cuenta como referenciado si aparece en:
  - el campo `relacionado` de OTRO concepto (una auto-referencia no cuenta), o
  - el campo `conceptos` de alguna correlación en Conocimiento/Correlaciones/.
NO cuenta (fuera de v1): `edges` tipados, wikilinks del cuerpo, consultas de Jarvis. Los
`edges` se muestran solo como dato informativo para quien revisa el reporte.

Antigüedad = hoy − campo `fecha` del frontmatter (fecha de creación según taxonomia.md).
No se usa la fecha de modificación del archivo: cada auditoría o checkout la resetea.
Si `fecha` falta o no se puede leer, el concepto NO se evalúa (queda en "No evaluables"):
no se adivina.

Uso:
    python3 Prompts/Meta/poda-por-uso.py --dry-run     # imprime el reporte, no escribe
    python3 Prompts/Meta/poda-por-uso.py               # escribe poda-candidatos.md
    python3 Prompts/Meta/poda-por-uso.py --dias 60 --hoy 2026-09-26 --base /ruta/al/vault

Ejecutar a mano y revisar el output antes de programarlo como rutina periódica.
"""

import argparse
import os
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

# Mismo parser de frontmatter que usa el ATLAS: así las referencias se cuentan
# exactamente como las lee el resto del sistema (listas inline y de bloque).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generar_index import parse_frontmatter  # noqa: E402

DEFAULT_BASE      = Path.home() / "Documents" / "Segundo_cerebro"
CONCEPTOS_REL     = "Conocimiento/Conceptos"
CORRELACIONES_REL = "Conocimiento/Correlaciones"
SALIDA_REL        = "Conocimiento/Mantenimiento/poda-candidatos.md"
UMBRAL_DIAS       = 90


def normalizar_slug(valor) -> str:
    """'[[slug|Alias]]', '"slug"', 'slug.md' → 'slug'."""
    s = str(valor).strip().strip('"').strip("'")
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2].split("|")[0]
    if s.endswith(".md"):
        s = s[:-3]
    return s.strip()


def como_lista(valor) -> list:
    """El parser devuelve lista si el YAML era lista, str si era escalar."""
    if valor is None:
        return []
    if isinstance(valor, list):
        return valor
    return [valor]


def parsear_fecha(valor) -> date | None:
    try:
        return datetime.strptime(str(valor).strip().strip('"').strip("'"), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def leer_meta(ruta: Path, advertencias: list) -> dict | None:
    try:
        meta, _ = parse_frontmatter(ruta.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as e:
        advertencias.append(f"`{ruta.name}`: no se pudo leer ({e.__class__.__name__})")
        return None
    return meta


def analizar(base: Path, hoy: date, umbral: int) -> dict:
    advertencias: list[str] = []
    conceptos: dict[str, dict] = {}
    entrantes: dict[str, set] = defaultdict(set)   # slug → fuentes que lo citan
    edges_in:  dict[str, set] = defaultdict(set)   # informativo, NO cuenta como uso

    # 1) Conceptos: metadatos + referencias salientes (relacionado)
    directorio = base / CONCEPTOS_REL
    for archivo in sorted(directorio.rglob("*.md")):
        slug = archivo.stem
        meta = leer_meta(archivo, advertencias)
        if meta is None:
            continue
        if slug in conceptos:
            advertencias.append(
                f"slug duplicado `{slug}` ({conceptos[slug]['carpeta']}/ y {archivo.parent.name}/) — "
                "se analiza solo el primero"
            )
            continue
        salientes = {normalizar_slug(r) for r in como_lista(meta.get("relacionado"))} - {"", slug}
        for destino in salientes:
            entrantes[destino].add(f"relacionado:{slug}")
        for edge in como_lista(meta.get("edges")):
            if isinstance(edge, dict) and edge.get("target"):
                objetivo = normalizar_slug(edge["target"])
                if objetivo and objetivo != slug:
                    edges_in[objetivo].add(slug)
        conceptos[slug] = {
            "slug": slug,
            "titulo": str(meta.get("titulo") or slug),
            "carpeta": archivo.parent.name,
            "estado": str(meta.get("estado") or "?"),
            "fecha_txt": meta.get("fecha"),
            "fecha": parsear_fecha(meta.get("fecha")),
            "salientes": salientes,
        }

    # 2) Correlaciones: cada concepto listado en `conceptos` recibe una referencia
    for archivo in sorted((base / CORRELACIONES_REL).glob("*.md")):
        meta = leer_meta(archivo, advertencias)
        if meta is None:
            continue
        for c in como_lista(meta.get("conceptos")):
            slug = normalizar_slug(c)
            if slug:
                entrantes[slug].add(f"correlacion:{archivo.stem}")

    # 3) Clasificación
    candidatos, con_refs, jovenes, archivados, no_evaluables = [], [], [], [], []
    for c in conceptos.values():
        # solo cuentan relaciones hacia conceptos que existen (un slug colgante no es una relación)
        c["n_salientes"] = len(c["salientes"] & conceptos.keys())
        c["edges_in"] = len(edges_in.get(c["slug"], ()))
        if c["estado"] == "archivado":
            archivados.append(c)
        elif c["fecha"] is None:
            no_evaluables.append(c)
        else:
            c["dias"] = (hoy - c["fecha"]).days
            if c["dias"] <= umbral:
                jovenes.append(c)
            elif entrantes.get(c["slug"]):
                con_refs.append(c)
            else:
                candidatos.append(c)
    candidatos.sort(key=lambda c: (-c["dias"], c["slug"]))

    return {
        "total": len(conceptos), "candidatos": candidatos, "con_refs": con_refs,
        "jovenes": jovenes, "archivados": archivados, "no_evaluables": no_evaluables,
        "advertencias": advertencias,
    }


def esc(texto: str) -> str:
    return str(texto).replace("|", "\\|")


def renderizar(r: dict, hoy: date, umbral: int, ahora: datetime) -> str:
    n = len(r["candidatos"])
    # Slugs en `código`, NO wikilinks: este reporte no debe "citar" lo que señala
    # (en el grafo de Obsidian un wikilink cuenta como uso y anularía el propósito).
    L = [
        "# Poda por uso — candidatos a revisión",
        "",
        f"> Generado automáticamente el {ahora:%Y-%m-%d %H:%M} por `Prompts/Meta/poda-por-uso.py`  ",
        "> **Solo reporte:** no se modificó ningún concepto ni correlación. La decisión de archivar es tuya.  ",
        f"> Criterio: más de {umbral} días de antigüedad (campo `fecha`, referencia: {hoy}) y **0 referencias entrantes**.  ",
        "> Señal de uso (v1): aparecer en el `relacionado` de otro concepto o en el `conceptos` de una correlación. "
        "No cuentan los `edges`, los wikilinks del cuerpo ni las consultas de Jarvis.",
        "",
        "## Resumen",
        "",
        f"- Conceptos analizados: {r['total']}",
        f"- **Candidatos: {n}**",
        f"- Con al menos una referencia: {len(r['con_refs'])}",
        f"- Excluidos por antigüedad ≤ {umbral} días: {len(r['jovenes'])}",
        f"- Archivados (omitidos): {len(r['archivados'])}",
        f"- No evaluables (sin `fecha` válida): {len(r['no_evaluables'])}",
        "",
        f"## Candidatos ({n})",
        "",
    ]
    if n == 0:
        L.append("Ningún concepto cumple el criterio.")
    else:
        L += [
            "| concepto | título | carpeta | estado | fecha | días | relaciona a | edges† |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for c in r["candidatos"]:
            L.append(
                f"| `{c['slug']}` | {esc(c['titulo'])} | {c['carpeta']} | {c['estado']} | "
                f"{c['fecha']} | {c['dias']} | {c['n_salientes']} | {c['edges_in']} |"
            )
        L += [
            "",
            "**relaciona a:** cuántos conceptos cita este en su propio `relacionado` (0 = aislado; "
            "más de 0 = huérfano de entrada pero conectado hacia afuera).  ",
            "**edges†:** cuántos conceptos lo apuntan con un `edge` tipado. **No cuenta como uso en v1**, "
            "pero conviene mirarlo antes de archivar: un candidato con edges† > 0 sí forma parte del grafo tipado.",
        ]
    if r["no_evaluables"]:
        L += ["", "## No evaluables", ""]
        for c in sorted(r["no_evaluables"], key=lambda c: c["slug"]):
            L.append(f"- `{c['slug']}` — `fecha` ausente o inválida ({c['fecha_txt']!r})")
    if r["advertencias"]:
        L += ["", "## Advertencias", ""] + [f"- {a}" for a in r["advertencias"]]
    return "\n".join(L) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Reporte de conceptos sin referencias entrantes (solo lectura).")
    p.add_argument("--base", type=Path, default=DEFAULT_BASE, help="raíz del vault")
    p.add_argument("--dias", type=int, default=UMBRAL_DIAS, help=f"antigüedad mínima (default {UMBRAL_DIAS})")
    p.add_argument("--hoy", type=str, default=None, help="fecha de referencia YYYY-MM-DD (default: hoy; útil para pruebas)")
    p.add_argument("--dry-run", action="store_true", help="imprime el reporte y NO escribe el archivo")
    a = p.parse_args()

    hoy = parsear_fecha(a.hoy) if a.hoy else date.today()
    if hoy is None:
        print("--hoy debe ser YYYY-MM-DD", file=sys.stderr)
        return 2
    if not (a.base / CONCEPTOS_REL).is_dir():
        print(f"No existe {a.base / CONCEPTOS_REL}", file=sys.stderr)
        return 2

    resultado = analizar(a.base, hoy, a.dias)
    reporte = renderizar(resultado, hoy, a.dias, datetime.now())

    if a.dry_run:
        sys.stdout.write(reporte)
        print(f"\n[dry-run] no se escribió nada · candidatos: {len(resultado['candidatos'])} "
              f"de {resultado['total']} conceptos", file=sys.stderr)
        return 0

    salida = a.base / SALIDA_REL
    salida.parent.mkdir(parents=True, exist_ok=True)
    tmp = salida.with_suffix(".md.tmp")
    tmp.write_text(reporte, encoding="utf-8")
    os.replace(tmp, salida)   # escritura atómica: nunca queda un reporte a medias
    print(f"Escrito {salida.relative_to(a.base)} · candidatos: {len(resultado['candidatos'])} "
          f"de {resultado['total']} conceptos analizados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
