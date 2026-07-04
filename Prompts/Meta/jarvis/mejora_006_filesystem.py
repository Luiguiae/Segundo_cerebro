#!/usr/local/bin/python3.11
"""
mejora_006_filesystem.py — Acceso al filesystem completo vía voz (Mejora 006)

Dispatcher: operacion_archivo(params) → str (resultado legible por TTS)
"""

import os
import re
import shutil
from pathlib import Path

RUTAS_CONOCIDAS: dict[str, str] = {
    "vault":        "~/Documents/Segundo_cerebro",
    "wayta":        "~/Documents/Wayta_IA",
    "downloads":    "~/Downloads",
    "descargas":    "~/Downloads",
    "descarga":     "~/Downloads",
    "desktop":      "~/Desktop",
    "escritorio":   "~/Desktop",
    "documentos":   "~/Documents",
    "documents":    "~/Documents",
    "projects":     "~/Documents",
    "proyectos":    "~/Documents",
    "películas":    "~/Movies",
    "peliculas":    "~/Movies",
    "música":       "~/Music",
    "musica":       "~/Music",
    "imágenes":     "~/Pictures",
    "imagenes":     "~/Pictures",
    "home":         "~",
}

_MAX_LEER = 10_000   # caracteres máximo en leer_archivo
_MAX_BUSCAR = 20     # archivos máximos que buscar_en_archivos recorre
_RE_FECHA = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')  # YYYY | YYYY-MM | YYYY-MM-DD


def _raices_permitidas() -> tuple[Path, ...]:
    """Raíces absolutas derivadas de RUTAS_CONOCIDAS — únicos directorios donde
    las operaciones de filesystem están autorizadas a operar."""
    vistas: list[Path] = []
    for base in RUTAS_CONOCIDAS.values():
        p = Path(base).expanduser().resolve()
        if p not in vistas:
            vistas.append(p)
    return tuple(vistas)


_RAICES_PERMITIDAS = _raices_permitidas()


def _ruta_confinada(p: Path) -> bool:
    """True si `p` (ya resuelto) está contenido dentro de alguna raíz permitida.
    Bloquea path traversal (alias + '..') hacia fuera de RUTAS_CONOCIDAS."""
    try:
        resuelto = p.resolve()
    except Exception:
        return False
    return any(resuelto == raiz or resuelto.is_relative_to(raiz) for raiz in _RAICES_PERMITIDAS)


def _rechazo_fuera_de_alcance(p: Path) -> str:
    return f"Acceso denegado: '{p}' está fuera de los directorios permitidos."


def resolver_ruta(ruta_str: str) -> Path:
    """Convierte alias o ruta relativa/absoluta a Path absoluto dentro de ~/."""
    if not ruta_str:
        return Path.home()
    normalizado = ruta_str.strip().lower()
    # alias exacto
    if normalizado in RUTAS_CONOCIDAS:
        return Path(RUTAS_CONOCIDAS[normalizado]).expanduser().resolve()
    # alias como prefijo ("wayta ia", "downloads old")
    for alias, base in RUTAS_CONOCIDAS.items():
        if normalizado.startswith(alias):
            sufijo = normalizado[len(alias):].strip().strip("/")
            raiz = Path(base).expanduser()
            return (raiz / sufijo).resolve() if sufijo else raiz.resolve()
    # path literal
    p = Path(ruta_str).expanduser()
    if p.is_absolute():
        return p.resolve()
    # relativo al home
    return (Path.home() / ruta_str).resolve()


def _guardar_en_ruta(origen: Path, destino: Path) -> Path:
    """Devuelve la ruta final donde se moverá el archivo a destino."""
    if destino.is_dir():
        return destino / origen.name
    return destino


def listar_archivos(ruta: str, extension: str | None = None) -> str:
    """Lista archivos de una carpeta. extension puede ser 'md', 'py', etc."""
    p = resolver_ruta(ruta)
    if not _ruta_confinada(p):
        return _rechazo_fuera_de_alcance(p)
    if not p.exists():
        return f"La ruta '{p}' no existe."
    if not p.is_dir():
        return f"'{p}' no es una carpeta."

    archivos = sorted(p.iterdir())
    if extension:
        ext = extension.lstrip(".")
        archivos = [a for a in archivos if a.suffix.lstrip(".") == ext]

    if not archivos:
        return f"La carpeta '{p.name}' está vacía."

    dirs  = [a.name + "/" for a in archivos if a.is_dir()]
    files = [a.name for a in archivos if a.is_file()]
    partes = []
    if dirs:
        partes.append("Carpetas: " + ", ".join(dirs))
    if files:
        partes.append("Archivos: " + ", ".join(files))
    return f"En '{p.name}': " + " | ".join(partes)


def leer_archivo(ruta: str) -> str:
    """Lee el contenido de un archivo de texto (max _MAX_LEER chars)."""
    p = resolver_ruta(ruta)
    if not _ruta_confinada(p):
        return _rechazo_fuera_de_alcance(p)
    if not p.exists():
        return f"El archivo '{p}' no existe."
    if p.is_dir():
        return f"'{p}' es una carpeta, no un archivo."

    EXTENSIONES_TEXTO = {
        ".txt", ".md", ".py", ".js", ".ts", ".json", ".yaml", ".yml",
        ".toml", ".sh", ".zsh", ".cfg", ".ini", ".csv",
    }
    if p.suffix.lower() not in EXTENSIONES_TEXTO:
        return f"No puedo leer '{p.name}' — solo archivos de texto plano."

    try:
        contenido = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error al leer '{p.name}': {e}"

    if len(contenido) > _MAX_LEER:
        return contenido[:_MAX_LEER] + f"\n\n[Archivo truncado — {len(contenido)} chars totales, mostrando primeros {_MAX_LEER}]"
    return contenido


def crear_carpeta(ruta: str) -> str:
    """Crea una carpeta (y sus padres) si no existe."""
    p = resolver_ruta(ruta)
    if not _ruta_confinada(p):
        return _rechazo_fuera_de_alcance(p)
    if p.exists():
        return f"La carpeta '{p.name}' ya existe en '{p.parent}'."
    try:
        p.mkdir(parents=True, exist_ok=True)
        return f"Carpeta '{p.name}' creada en '{p.parent}'."
    except Exception as e:
        return f"Error al crear '{p}': {e}"


def mover_archivo(origen: str, destino: str) -> str:
    """Mueve un archivo de origen a destino."""
    p_origen  = resolver_ruta(origen)
    p_destino = resolver_ruta(destino)

    if not _ruta_confinada(p_origen):
        return _rechazo_fuera_de_alcance(p_origen)
    if not _ruta_confinada(p_destino):
        return _rechazo_fuera_de_alcance(p_destino)

    if not p_origen.exists():
        return f"El origen '{p_origen}' no existe."

    ruta_final = _guardar_en_ruta(p_origen, p_destino)
    if ruta_final.exists():
        return f"Ya existe un archivo '{ruta_final.name}' en el destino. No se movió."

    try:
        p_destino.mkdir(parents=True, exist_ok=True) if p_destino.is_dir() or not p_destino.suffix else None
        shutil.move(str(p_origen), str(ruta_final))
        return f"'{p_origen.name}' movido a '{ruta_final.parent.name}'."
    except Exception as e:
        return f"Error al mover '{p_origen.name}': {e}"


def eliminar_archivo(ruta: str) -> str:
    """Mueve el archivo a ~/.Trash/ — nunca rm permanente."""
    p = resolver_ruta(ruta)
    if not _ruta_confinada(p):
        return _rechazo_fuera_de_alcance(p)
    if not p.exists():
        return f"El archivo '{p}' no existe."

    trash = Path.home() / ".Trash"
    trash.mkdir(exist_ok=True)

    # Evitar colisión de nombres en Trash
    destino = trash / p.name
    if destino.exists():
        stem = p.stem
        sufijo = p.suffix
        import time
        ts = int(time.time())
        destino = trash / f"{stem}_{ts}{sufijo}"

    try:
        shutil.move(str(p), str(destino))
        return f"'{p.name}' movido a la Papelera."
    except Exception as e:
        return f"Error al eliminar '{p.name}': {e}"


def _frontmatter_campo(ruta: Path, campo: str) -> str | None:
    """Lee el frontmatter YAML de un .md y retorna el valor del campo dado."""
    try:
        lineas = ruta.read_text(encoding="utf-8", errors="replace").splitlines()
        en_fm = False
        for linea in lineas[:25]:
            if linea.strip() == "---":
                if not en_fm:
                    en_fm = True
                    continue
                break  # cierre del frontmatter
            if en_fm and linea.lower().startswith(f"{campo}:"):
                return linea.split(":", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return None


def _buscar_por_fecha(p: Path, fecha: str) -> str:
    """Busca .md cuyo frontmatter campo fecha: contenga la fecha dada."""
    matches: list[str] = []
    for archivo in sorted(p.rglob("*.md")):
        valor = _frontmatter_campo(archivo, "fecha")
        if valor and fecha in valor:
            titulo = _frontmatter_campo(archivo, "titulo") or archivo.stem
            matches.append(f"- {titulo}  [{archivo.stem}]")
    if not matches:
        return f"No encontré archivos con fecha '{fecha}' en '{p.name}'."
    return f"Archivos con fecha '{fecha}' en '{p.name}' ({len(matches)}):\n" + "\n".join(matches)


def buscar_en_archivos(ruta: str, query: str) -> str:
    """Busca 'query' en archivos de texto dentro de la carpeta (recursivo, max _MAX_BUSCAR).
    Si query tiene formato YYYY-MM-DD (o YYYY-MM, YYYY), busca en el campo fecha: del frontmatter."""
    p = resolver_ruta(ruta)
    if not _ruta_confinada(p):
        return _rechazo_fuera_de_alcance(p)
    if not p.exists():
        return f"La ruta '{p}' no existe."
    if not p.is_dir():
        return f"'{p}' no es una carpeta."
    if not query:
        return "No especificaste qué buscar."

    # Búsqueda por fecha en frontmatter
    if _RE_FECHA.match(query.strip()):
        return _buscar_por_fecha(p, query.strip())

    query_lower = query.lower()
    matches: list[str] = []
    revisados = 0

    EXTENSIONES_TEXTO = {".txt", ".md", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".sh", ".csv"}

    for archivo in sorted(p.rglob("*")):
        if revisados >= _MAX_BUSCAR:
            break
        if not archivo.is_file():
            continue
        if archivo.suffix.lower() not in EXTENSIONES_TEXTO:
            continue
        revisados += 1
        try:
            contenido = archivo.read_text(encoding="utf-8", errors="replace")
            for i, linea in enumerate(contenido.splitlines(), 1):
                if query_lower in linea.lower():
                    ruta_rel = archivo.relative_to(p)
                    matches.append(f"{ruta_rel}:{i}: {linea.strip()[:100]}")
                    break  # una coincidencia por archivo
        except Exception:
            continue

    if not matches:
        return f"No encontré '{query}' en '{p.name}' (revisé {revisados} archivos)."
    return f"'{query}' encontrado en {len(matches)} archivo(s):\n" + "\n".join(matches)


def operacion_archivo(params: dict) -> str:
    """
    Dispatcher principal. params debe tener:
      operacion: listar | leer | crear_carpeta | mover | eliminar | buscar
      ruta: str
      archivo: str (opcional — se concatena a ruta si está presente)
      destino: str (para mover)
      query: str (para buscar)
      extension: str (para listar con filtro)
    """
    operacion = params.get("operacion", "").strip().lower()
    ruta      = params.get("ruta", "").strip()
    archivo   = params.get("archivo", "").strip()
    destino   = params.get("destino", "").strip()
    query     = params.get("query", "").strip()
    extension = params.get("extension", "").strip()

    # Si hay 'archivo', lo concatena a 'ruta' para formar la ruta completa
    ruta_completa = str(Path(ruta) / archivo) if ruta and archivo else (ruta or archivo)

    if operacion in ("listar", "list", "qué hay", "que hay"):
        return listar_archivos(ruta_completa or ruta, extension or None)

    if operacion in ("leer", "lee", "read", "mostrar", "abre"):
        return leer_archivo(ruta_completa)

    if operacion in ("crear_carpeta", "crear carpeta", "mkdir"):
        return crear_carpeta(ruta_completa)

    if operacion in ("mover", "move", "mueve"):
        if not destino:
            return "Indica el destino para mover el archivo."
        return mover_archivo(ruta_completa, destino)

    if operacion in ("eliminar", "borrar", "delete", "remove"):
        return eliminar_archivo(ruta_completa)

    if operacion in ("buscar", "search", "grep"):
        if not query:
            return "Indica el texto que quieres buscar."
        return buscar_en_archivos(ruta or ruta_completa, query)

    return f"Operación '{operacion}' no reconocida. Operaciones disponibles: listar, leer, crear_carpeta, mover, eliminar, buscar."
