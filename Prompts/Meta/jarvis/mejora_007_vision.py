#!/usr/local/bin/python3.11
"""
mejora_007_vision.py — Visión de pantalla: Jarvis lee lo que estás viendo (Mejora 007)

Dispatcher pattern — cada función de intent retorna str:
  ver_pantalla(params)           → texto para responder_con_groq()
  profundizar_pantalla(params)   → prompt para ejecutar_claude()
  capturar_como_concepto(params) → prompt para ejecutar_claude()
  relacionar_con_vault(params)   → texto para responder_con_groq()

Si hay error de permisos o falla, retorna mensaje legible que Jarvis habla directamente.
Usa es_error_vision(s) para distinguir errores de contenido real antes de despachar.

Dependencias opcionales:
  pip3.11 install pyobjc-framework-Cocoa pyobjc-framework-ApplicationServices Pillow anthropic
"""

import base64
import io
import os
import subprocess
import tempfile
from pathlib import Path

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"
ATLAS_PATH = CEREBRO_PATH / "Conocimiento" / "ATLAS.md"

_VISION_MODEL = os.environ.get("JARVIS_VISION_MODEL", "claude-sonnet-4-20250514")

_PERMISO_ACCESIBILIDAD = (
    "Necesito permisos de accesibilidad para leer tu pantalla. "
    "Ve a Configuración del Sistema, Privacidad y Seguridad, Accesibilidad, "
    "y agrega Terminal."
)
_PERMISO_PANTALLA = (
    "Necesito permiso de grabación de pantalla para capturar la pantalla. "
    "Ve a Configuración del Sistema, Privacidad y Seguridad, Grabación de pantalla, "
    "y agrega Terminal."
)
_SOLO_DASHBOARD = (
    "Solo veo el dashboard. ¿Puedes indicarme qué pestaña revisar?"
)
_ERROR_PREFIXES = ("Necesito permisos", "No pude", "Error al", "No tengo acceso", "Solo veo")


def es_error_vision(texto: str) -> bool:
    """True si el texto es un mensaje de error — hablar() directamente, no pasar a Groq/Claude."""
    return any(texto.startswith(p) for p in _ERROR_PREFIXES)


# ── Accessibility / AppleScript ────────────────────────────────────────────────

def _osascript(script: str, timeout: int = 8) -> str | None:
    """Ejecuta AppleScript y retorna stdout, mensaje de permiso, o None si falla."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
        stderr = result.stderr.lower()
        if any(k in stderr for k in ("not authorized", "privacy", "accessibility", "permission")):
            return _PERMISO_ACCESIBILIDAD
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


_CHROME_SCRIPT = """
try
    tell application "Google Chrome"
        set frontWin to front window
        set activeTab to active tab of frontWin
        set tabURL to URL of activeTab

        -- Si el tab activo es el dashboard de Jarvis, buscar el siguiente no-localhost
        if tabURL contains "localhost" or tabURL contains "127.0.0.1" then
            set foundTab to missing value
            repeat with t in every tab of frontWin
                set tURL to URL of t
                if tURL does not contain "localhost" and tURL does not contain "127.0.0.1" then
                    set foundTab to t
                    exit repeat
                end if
            end repeat
            if foundTab is missing value then
                return "__SOLO_DASHBOARD__"
            end if
            set activeTab to foundTab
            set tabURL to URL of foundTab
        end if

        set tabTitle to title of activeTab
        try
            set pageText to execute activeTab javascript "document.body.innerText.substring(0, 3000)"
        on error
            set pageText to ""
        end try
        if pageText is not "" then
            return "Título: " & tabTitle & return & "URL: " & tabURL & return & "Contenido:" & return & pageText
        else
            return "Título: " & tabTitle & return & "URL: " & tabURL
        end if
    end tell
on error
    return ""
end try
"""

_SAFARI_SCRIPT = """
try
    tell application "Safari"
        set tabTitle to name of front document
        set tabURL to URL of front document
        try
            set pageText to do JavaScript "document.body.innerText.substring(0, 3000)" in front document
        on error
            set pageText to ""
        end try
        if pageText is not "" then
            return "Título: " & tabTitle & return & "URL: " & tabURL & return & "Contenido:" & return & pageText
        else
            return "Título: " & tabTitle & return & "URL: " & tabURL
        end if
    end tell
on error
    return ""
end try
"""

_ARC_SCRIPT = """
try
    tell application "Arc"
        set tabTitle to title of active tab of front window
        set tabURL to URL of active tab of front window
        return "Título: " & tabTitle & return & "URL: " & tabURL
    end tell
on error
    return ""
end try
"""

_GENERIC_SCRIPT = """
try
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set appName to name of frontApp
        try
            set winTitle to title of front window of frontApp
            return "App: " & appName & return & "Ventana: " & winTitle
        on error
            return "App: " & appName
        end try
    end tell
on error
    return ""
end try
"""

_BROWSER_SCRIPTS: dict[str, str] = {
    "Google Chrome": _CHROME_SCRIPT,
    "Safari": _SAFARI_SCRIPT,
    "Arc": _ARC_SCRIPT,
}


def extraer_texto_accesibilidad() -> str | None:
    """
    Extrae el texto de la ventana activa via AppleScript (primario) y pyobjc AX API (secundario).
    Retorna texto, mensaje de permiso, o None si no hay contenido suficiente.
    """
    app_name_raw = _osascript(
        'tell application "System Events" to get name of first application process whose frontmost is true',
        timeout=5
    )
    if app_name_raw == _PERMISO_ACCESIBILIDAD:
        return _PERMISO_ACCESIBILIDAD
    app_name = app_name_raw or "Unknown"

    # Script específico para browsers (extrae URL + contenido de página)
    browser_script = _BROWSER_SCRIPTS.get(app_name)
    if browser_script:
        resultado = _osascript(browser_script)
        if resultado == _PERMISO_ACCESIBILIDAD:
            return _PERMISO_ACCESIBILIDAD
        if resultado == "__SOLO_DASHBOARD__":
            return _SOLO_DASHBOARD
        if resultado and len(resultado) > 30:
            return f"App activa: {app_name}\n{resultado}"

    # Script genérico (título de ventana)
    resultado = _osascript(_GENERIC_SCRIPT)
    if resultado == _PERMISO_ACCESIBILIDAD:
        return _PERMISO_ACCESIBILIDAD
    if resultado and len(resultado) > 10:
        return resultado

    # Fallback: pyobjc AX API para apps no scriptables
    return _extraer_via_pyobjc(app_name)


def _extraer_via_pyobjc(app_name: str) -> str | None:
    """Extrae texto del elemento enfocado vía pyobjc Accessibility API."""
    try:
        import AppKit
        ws = AppKit.NSWorkspace.sharedWorkspace()
        front_app = ws.frontmostApplication()
        pid = front_app.processIdentifier()

        from ApplicationServices import (  # type: ignore[import]
            AXUIElementCreateApplication,
            AXUIElementCopyAttributeValue,
            kAXErrorSuccess,
        )

        ax_app = AXUIElementCreateApplication(pid)
        texts = [f"App: {app_name}"]

        err, windows = AXUIElementCopyAttributeValue(ax_app, "AXWindows", None)
        if err == kAXErrorSuccess and windows:
            wins = list(windows) if hasattr(windows, "__iter__") else []
            for win in wins[:1]:
                err2, title = AXUIElementCopyAttributeValue(win, "AXTitle", None)
                if err2 == kAXErrorSuccess and title:
                    texts.append(f"Ventana: {title}")

        err, focused = AXUIElementCopyAttributeValue(ax_app, "AXFocusedUIElement", None)
        if err == kAXErrorSuccess and focused:
            err2, val = AXUIElementCopyAttributeValue(focused, "AXValue", None)
            if err2 == kAXErrorSuccess and isinstance(val, str) and len(val) > 20:
                texts.append(val[:5000])

        return "\n".join(texts) if len(texts) > 1 else None

    except ImportError:
        return None
    except Exception as e:
        if any(k in str(e).lower() for k in ("not authorized", "permission")):
            return _PERMISO_ACCESIBILIDAD
        return None


# ── Screenshot ─────────────────────────────────────────────────────────────────

def tomar_screenshot() -> str:
    """
    Captura la pantalla completa y retorna base64 PNG optimizado (max 1280px wide).
    Usa screencapture CLI (macOS built-in) con fallback a Pillow ImageGrab.
    """
    img_bytes: bytes | None = None

    # Método 1: screencapture (integrado en macOS, confiable en pantallas Retina)
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            tmp_path = f.name
        result = subprocess.run(
            ["screencapture", "-x", "-t", "png", tmp_path],
            capture_output=True, timeout=15
        )
        if result.returncode == 0 and Path(tmp_path).stat().st_size > 1000:
            with open(tmp_path, "rb") as f:
                img_bytes = f.read()
        os.unlink(tmp_path)
    except Exception:
        pass

    # Método 2: Pillow ImageGrab
    if img_bytes is None:
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
        except ImportError:
            raise RuntimeError(
                "No pude capturar la pantalla: instala Pillow con 'pip3.11 install Pillow'."
            )
        except Exception as e:
            raise RuntimeError(f"No pude capturar la pantalla: {e}") from e

    if img_bytes is None:
        raise RuntimeError("No pude capturar la pantalla.")

    # Redimensionar para reducir tokens (max 1280px de ancho)
    try:
        from PIL import Image
        buf_in = io.BytesIO(img_bytes)
        img = Image.open(buf_in)
        if img.width > 1280:
            ratio = 1280 / img.width
            img = img.resize((1280, int(img.height * ratio)), Image.LANCZOS)
            buf_out = io.BytesIO()
            img.save(buf_out, format="PNG", optimize=True)
            img_bytes = buf_out.getvalue()
    except ImportError:
        pass
    except Exception:
        pass

    return base64.standard_b64encode(img_bytes).decode()


# ── Claude Vision ──────────────────────────────────────────────────────────────

def analizar_con_vision(base64_image: str, instruccion: str = "") -> str:
    """
    Envía el screenshot a Claude Vision y retorna la descripción textual del contenido.
    Requiere ANTHROPIC_API_KEY en el entorno.
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "La librería 'anthropic' no está instalada. Ejecuta: pip3.11 install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no disponible en el entorno.")

    prompt = instruccion or (
        "Describe en detalle el contenido visible en esta pantalla. "
        "Si hay texto, transcríbelo. Si hay una página web, incluye el título, "
        "la URL si es visible, y el contenido principal del artículo o página. "
        "Responde en español."
    )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=_VISION_MODEL,
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image,
                    },
                },
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return response.content[0].text


# ── Wrapper principal ──────────────────────────────────────────────────────────

def _fallback_accesibilidad() -> str:
    """Extrae texto vía AppleScript cuando el screenshot no está disponible."""
    texto = extraer_texto_accesibilidad()
    if texto == _PERMISO_ACCESIBILIDAD:
        return _PERMISO_ACCESIBILIDAD
    if texto and len(texto.strip()) > 10:
        return texto
    return "No pude obtener el contenido de la pantalla."


def obtener_contexto_pantalla(instruccion_vision: str = "") -> str:
    """
    Retorna el texto de lo que el usuario está viendo.
    Prioridad: screenshot + Claude Vision (PRIMARIO) → AppleScript (SECUNDARIO).
    El screenshot captura cualquier app — no solo el navegador.
    Retorna mensaje legible si no tiene permisos.
    """
    # PRIMARIO: screenshot de pantalla completa + Claude Vision
    try:
        b64 = tomar_screenshot()
        print(f"[Vision007] Screenshot OK ({len(b64) // 1024}KB base64)", flush=True)
    except RuntimeError as e:
        msg = str(e)
        print(f"[Vision007] Screenshot falló: {msg} — fallback AppleScript", flush=True)
        if "pantalla" in msg.lower() or "capturar" in msg.lower():
            return _PERMISO_PANTALLA
        return _fallback_accesibilidad()
    except Exception as e:
        print(f"[Vision007] Screenshot error: {e} — fallback AppleScript", flush=True)
        return _fallback_accesibilidad()

    print("[Vision007] Llamando Claude API...", flush=True)
    try:
        resultado = analizar_con_vision(b64, instruccion_vision)
        print("[Vision007] Respuesta Claude:", repr(resultado[:200]), flush=True)
        return resultado
    except Exception as e:
        print("[Vision007] ERROR Claude Vision:", e, flush=True)
        import traceback
        traceback.print_exc()
        print("[Vision007] Fallback a AppleScript...", flush=True)
        fallback = _fallback_accesibilidad()
        if fallback and not fallback.startswith("No pude"):
            return fallback
        return f"Error al analizar la pantalla: {e}"


# ── Funciones de intent ────────────────────────────────────────────────────────

def ver_pantalla(params: dict) -> str:
    """
    Intent: ver_pantalla — "¿qué estoy viendo?", "de qué trata esto", "explícame esto"
    Retorna texto para pasar a responder_con_groq().
    Si es_error_vision() → hablar() directamente.
    """
    accion = params.get("accion", "describir")
    _instruccion_map = {
        "describir": (
            "Describe detalladamente qué está haciendo el usuario en esta pantalla. "
            "Qué app está usando, qué contenido está viendo. Responde en español."
        ),
        "resumir": (
            "Resume qué está haciendo el usuario en esta pantalla en 2-3 oraciones. "
            "Qué app usa, qué contenido ve. Responde en español."
        ),
        "opinar": (
            "Describe qué está viendo el usuario en esta pantalla y analiza críticamente "
            "el contenido. Qué app usa, qué está leyendo o trabajando. Responde en español."
        ),
    }
    instruccion_vision = _instruccion_map.get(accion, _instruccion_map["describir"])

    contexto = obtener_contexto_pantalla(instruccion_vision)
    if es_error_vision(contexto):
        return contexto

    _verbo = {"describir": "describe", "resumir": "resume", "opinar": "da tu opinión sobre"}.get(
        accion, "describe"
    )
    return (
        f"El usuario quiere que {_verbo} lo que está viendo en su pantalla. "
        f"Aquí está el contenido extraído:\n\n{contexto}\n\n"
        f"Responde en máximo 3 oraciones en español, sin bullets, apto para TTS. "
        f"No menciones que estás leyendo una pantalla — responde directamente sobre el contenido."
    )


def profundizar_pantalla(params: dict) -> str:
    """
    Intent: profundizar_pantalla — "profundiza sobre lo que estoy leyendo"
    Retorna prompt para pasar a ejecutar_claude().
    Si es_error_vision() → hablar() directamente.
    """
    foco = params.get("foco", "")
    instruccion_vision = (
        "Identifica el tema o contenido principal visible en esta pantalla para investigarlo. "
        "Si hay un autor, institución o fuente mencionados, inclúyelos. Responde en español."
    )

    contexto = obtener_contexto_pantalla(instruccion_vision)
    if es_error_vision(contexto):
        return contexto

    foco_extra = f"\n\nFoco específico solicitado por Luigui: {foco}" if foco else ""

    return (
        f"Jarvis, profundiza este concepto. Usa el siguiente texto extraído de la pantalla "
        f"como borrador de entrada para el skill profundizador-conceptos. "
        f"Sigue la plantilla canónica del vault. Genera el .md enriquecido con fuentes externas, "
        f"incluyendo estas secciones: frontmatter completo (titulo, tipo, familia, tags, relacionado, "
        f"fecha, estado: borrador, fuentes), ## El concepto, ## Por qué importa, "
        f"## Tensiones y límites, ## Datos y evidencia, ## Ejes investigados. "
        f"Mínimo 2 fuentes sólidas con autor identificable, cifra verificable, fecha de acceso. "
        f"NO guardes el archivo automáticamente — entrega el .md en el chat para que Luigui lo apruebe.\n\n"
        f"TEXTO EXTRAÍDO DE LA PANTALLA:\n{contexto[:4000]}"
        f"{foco_extra}"
    )


def capturar_como_concepto(params: dict) -> str:
    """
    Intent: capturar_como_concepto — "guarda esto como concepto", "crea un concepto de esto"
    Retorna prompt para pasar a ejecutar_claude().
    Si es_error_vision() → hablar() directamente.
    """
    titulo_candidato = params.get("titulo_candidato", "")
    instruccion_vision = (
        "Extrae el argumento o idea central visible en esta pantalla. "
        "Responde en español con el contenido más importante."
    )

    contexto = obtener_contexto_pantalla(instruccion_vision)
    if es_error_vision(contexto):
        return contexto

    titulo_hint = f"\nTítulo sugerido por Luigui: {titulo_candidato}" if titulo_candidato else ""

    return (
        f"Jarvis, genera un concepto atómico completo desde el siguiente texto extraído de pantalla. "
        f"Lee Plantillas/taxonomia.md y Plantillas/rubrica.md antes de crear el archivo. "
        f"El concepto debe tener: frontmatter con titulo (legible, con mayúscula), tipo: concepto, "
        f"familia (una de las 6 válidas), tags (máx 5 de la lista controlada en taxonomia.md), "
        f"relacionado (máx 3, solo slugs que existan en Conocimiento/Conceptos/ — verifica con find), "
        f"fecha de hoy, estado: borrador; y tres secciones obligatorias: "
        f"## El concepto, ## Por qué importa, ## Tensiones y límites. "
        f"Aplica Gate 0 (estructura) y rúbrica (Gate 1 + Gate 2) antes de confirmar. "
        f"NO instales el archivo — entrega el .md completo en el chat para que Luigui lo apruebe."
        f"{titulo_hint}\n\n"
        f"TEXTO EXTRAÍDO DE LA PANTALLA:\n{contexto[:4000]}"
    )


def relacionar_con_vault(params: dict) -> str:
    """
    Intent: relacionar_con_vault — "¿tengo algo sobre esto en el vault?"
    Retorna texto para pasar a responder_con_groq().
    Si es_error_vision() → hablar() directamente.
    """
    instruccion_vision = (
        "Describe el tema principal de esta pantalla en 2-3 palabras clave. "
        "Responde en español."
    )

    contexto = obtener_contexto_pantalla(instruccion_vision)
    if es_error_vision(contexto):
        return contexto

    atlas = ""
    if ATLAS_PATH.exists():
        atlas = ATLAS_PATH.read_text(encoding="utf-8")[:5000]

    return (
        f"El usuario está viendo el siguiente contenido en su pantalla:\n\n{contexto[:2000]}\n\n"
        f"---\n\nÍNDICE DEL VAULT DEL SEGUNDO CEREBRO:\n{atlas}\n\n"
        f"Identifica los 2-3 conceptos del vault más relacionados con el contenido de pantalla. "
        f"Responde en máximo 3 oraciones en español, sin bullets, apto para TTS. "
        f"Menciona los títulos exactos de los conceptos relacionados y explica brevemente la conexión."
    )
