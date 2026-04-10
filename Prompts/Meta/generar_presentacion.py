#!/usr/bin/env python3
"""
generar_presentacion.py
Lee conceptos del Segundo Cerebro y genera un outline de presentación
llamando a la API de Claude con el contenido de los archivos como contexto.

Uso:
    python3 generar_presentacion.py --conceptos vibe-coding agentes-ia disenador-a-constructor
    python3 generar_presentacion.py --conceptos vibe-coding agentes-ia --audiencia "diseñadores de producto" --duracion "45 min"
    python3 generar_presentacion.py --listar   # ver conceptos disponibles
"""

import argparse
import json
import re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ── Configuración ──────────────────────────────────────────────────────────────
DEFAULT_BASE   = Path.home() / "Documents" / "Segundo_cerebro"
CONCEPTOS_DIR  = "Conocimiento/Conceptos"
INDEX_FILE     = "Conocimiento/ATLAS.md"
OUTPUT_DIR     = "Documentos/Presentaciones/decks"
MODEL          = "claude-sonnet-4-20250514"
MAX_TOKENS     = 4000
# ───────────────────────────────────────────────────────────────────────────────


def leer_archivo(ruta: Path) -> str:
    if ruta.exists():
        return ruta.read_text(encoding="utf-8")
    return ""


def listar_conceptos(base: Path):
    directorio = base / CONCEPTOS_DIR
    archivos = sorted(directorio.glob("*.md"))
    if not archivos:
        print("⚠️  No hay conceptos en el Segundo Cerebro todavía.")
        return
    print(f"\n📚 Conceptos disponibles ({len(archivos)}):\n")
    for f in archivos:
        print(f"  → {f.stem}")
    print()


def construir_prompt(conceptos_contenido: dict, index_contenido: str,
                     audiencia: str, objetivo: str,
                     duracion: str, formato: str) -> str:

    nombres = list(conceptos_contenido.keys())
    bloques_conceptos = ""
    for nombre, contenido in conceptos_contenido.items():
        bloques_conceptos += f"\n\n### Concepto: {nombre}\n{contenido}"

    return f"""Eres un asistente de pensamiento estratégico especializado en presentaciones de producto y tecnología.

Tu tarea: leer los siguientes conceptos del Segundo Cerebro de Luigui y generar el outline completo de una presentación que los cruce de forma coherente, narrativa y accionable.

---

## ÍNDICE DEL SEGUNDO CEREBRO
{index_contenido}

---

## CONCEPTOS A CRUZAR
{bloques_conceptos}

---

## PARÁMETROS DE LA PRESENTACIÓN
- Conceptos centrales: {", ".join(nombres)}
- Audiencia: {audiencia}
- Objetivo: {objetivo}
- Duración estimada: {duracion}
- Formato: {formato}

---

## OUTPUT ESPERADO

Genera el outline completo en markdown con esta estructura:

1. **TÍTULO Y SUBTÍTULO** — título principal + subtítulo que refleje la narrativa evolutiva
2. **HOOK** — pregunta o dato que abre, por qué importa ahora
3. **ACTO 1** — primer concepto: idea central, dato concreto, tensión que genera
4. **ACTO 2** — segundo concepto: cómo responde la tensión, caso real, nueva capacidad
5. **ACTO 3** — tercer concepto (si aplica): cómo multiplica lo anterior, visión, implicaciones
6. **SÍNTESIS** — mensaje central en una oración, modelo mental, call to action
7. **SLIDES CLAVE SUGERIDOS** — 5-7 slides con descripción visual de lo que mostrarías
8. **DATOS DE SOPORTE** — estadísticas y referencias de los conceptos para usar en la presentación

Sé específico. Usa los datos, ejemplos y citas que están en los conceptos. 
La narrativa debe tener una progresión lógica donde cada acto construye sobre el anterior.
El tono debe ser urgente pero fundamentado — no hype, sino evidencia + visión."""


def llamar_claude_api(prompt: str) -> str:
    """Llama a la API de Claude y retorna el texto de respuesta."""
    url = "https://api.anthropic.com/v1/messages"

    payload = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}]
    }

    headers = {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
        # La API key se inyecta automáticamente en Claude Code
    }

    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"Error API ({e.code}): {error_body}")


def guardar_outline(contenido: str, conceptos: list[str], base: Path) -> Path:
    output_dir = base / OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    nombre = "-".join(conceptos[:3]) + "-outline"
    fecha  = datetime.now().strftime("%Y%m%d")
    ruta   = output_dir / f"{fecha}-{nombre}.md"

    encabezado = f"""---
generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}
conceptos: {conceptos}
script: generar_presentacion.py
---

"""
    ruta.write_text(encabezado + contenido, encoding="utf-8")
    return ruta


def main():
    parser = argparse.ArgumentParser(
        description="Genera outline de presentación desde conceptos del Segundo Cerebro"
    )
    parser.add_argument("--conceptos", nargs="+",
                        help="Nombres de conceptos a cruzar (sin .md)")
    parser.add_argument("--audiencia", default="diseñadores y equipos de producto",
                        help="Audiencia de la presentación")
    parser.add_argument("--objetivo", default="que adopten estas herramientas y tengan un camino claro para empezar",
                        help="Objetivo de la presentación")
    parser.add_argument("--duracion", default="45 minutos",
                        help="Duración estimada")
    parser.add_argument("--formato", default="charla con demo",
                        help="Formato: charla, workshop, deck ejecutivo")
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE,
                        help="Ruta raíz del Segundo Cerebro")
    parser.add_argument("--listar", action="store_true",
                        help="Listar conceptos disponibles")
    args = parser.parse_args()

    base = args.base

    if args.listar:
        listar_conceptos(base)
        return

    if not args.conceptos:
        print("❌ Debes especificar al menos un concepto. Usa --listar para ver los disponibles.")
        return

    # Leer INDEX
    index_contenido = leer_archivo(base / INDEX_FILE)
    if not index_contenido:
        print("⚠️  No encontré ATLAS.md. Ejecuta primero generar_index.py")

    # Leer conceptos
    conceptos_contenido = {}
    dir_conceptos = base / CONCEPTOS_DIR

    for nombre in args.conceptos:
        ruta = dir_conceptos / f"{nombre}.md"
        if not ruta.exists():
            print(f"⚠️  Concepto no encontrado: {nombre}.md — lo omito")
            continue
        conceptos_contenido[nombre] = leer_archivo(ruta)
        print(f"✓ Cargado: {nombre}")

    if not conceptos_contenido:
        print("❌ No se encontró ningún concepto válido.")
        return

    # Construir prompt y llamar a Claude
    print(f"\n🧠 Generando outline con Claude ({MODEL})...")
    prompt   = construir_prompt(
        conceptos_contenido, index_contenido,
        args.audiencia, args.objetivo, args.duracion, args.formato
    )
    outline  = llamar_claude_api(prompt)

    # Guardar
    ruta_output = guardar_outline(outline, list(conceptos_contenido.keys()), base)

    print(f"\n✅ Outline generado en: {ruta_output}")
    print("\n--- PREVIEW (primeras 20 líneas) ---")
    lineas = outline.split("\n")[:20]
    print("\n".join(lineas))
    print("...\n")


if __name__ == "__main__":
    main()
