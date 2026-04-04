"""
Agente generador de conceptos atómicos.
Recibe el contexto de la temática (incluyendo tono_prompt) y el
contenido extraído por el buscador. Construye el system prompt
ajustado al dominio y genera el concepto atómico usando Groq como
motor principal y Gemini como respaldo automático.
"""

import os
import re
import json
from datetime import date

import yaml
import groq as groq_sdk
from google import genai
from google.genai import types as genai_types
from agentes.cruzador import inferir_relacionados

GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_MODELO    = "llama-3.3-70b-versatile"
GEMINI_MODELO  = "gemini-2.5-flash"

SECCIONES_REQUERIDAS = [
    "¿Qué es?",
    "¿Por qué importa?",
    "¿Cómo funciona?",
    "Ejemplos concretos",
    "Tensiones o limitaciones",
    "Se conecta con...",
    "Citas o fragmentos clave",
    "Mis notas",
]

PLANTILLA_EJEMPLO = """\
---
titulo: ""
alias: []
tags: []
tipo: concepto
fecha: YYYY-MM-DD
fuente:
  tipo: articulo
  referencia: ""
  autor: ""
relacionado: []
proyectos: []
estado: borrador
---
## ¿Qué es?

## ¿Por qué importa?

## ¿Cómo funciona?

## Ejemplos concretos

## Tensiones o limitaciones

## Se conecta con...

## Citas o fragmentos clave

## Mis notas
"""


class ErrorGeneracion(Exception):
    """Se lanza cuando Groq y Gemini fallan o el output no es válido."""
    pass


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

def _construir_system_prompt(contexto_tematica: dict) -> str:
    tono = contexto_tematica.get("tono_prompt", "").strip()
    nombre = contexto_tematica.get("nombre", "")
    return f"""\
Eres un asistente de investigación especializado en la temática "{nombre}".

IDIOMA: Responde SIEMPRE en español, sin excepción, sin importar el idioma del contenido fuente.

TONO Y VOZ: {tono}

TAREA: A partir del contenido que recibirás, genera UN único concepto atómico \
siguiendo exactamente la plantilla de abajo. No inventes datos, hechos ni citas \
que no estén presentes en el contenido recibido. Si una sección no tiene información \
suficiente, escribe "Sin información disponible." en esa sección.

PLANTILLA OBLIGATORIA (respeta exactamente este formato):

{PLANTILLA_EJEMPLO}

REGLAS DEL FRONTMATTER:
- titulo: título conciso en español (máx. 80 caracteres)
- alias: lista de términos alternativos o sinónimos en español
- tags: lista de 3-6 etiquetas temáticas en minúsculas
- tipo: siempre "concepto"
- fecha: la fecha de hoy en formato YYYY-MM-DD
- fuente.tipo: uno de [articulo, video, reunion, experimento, podcast]
- fuente.referencia: URL o título de la fuente principal
- fuente.autor: nombre del autor o publicación
- relacionado: dejar como lista vacía []
- proyectos: dejar como lista vacía []
- estado: siempre "borrador"

FORMATO DE SALIDA: devuelve ÚNICAMENTE el bloque markdown con el frontmatter \
y las 8 secciones. Sin texto adicional antes ni después.\
"""


# ---------------------------------------------------------------------------
# Construcción del prompt de usuario
# ---------------------------------------------------------------------------

def _construir_prompt_usuario(resultados: list[dict]) -> str:
    bloques = []
    for i, r in enumerate(resultados, 1):
        titulo   = r.get("titulo", "Sin título")
        url      = r.get("url", "")
        contenido = r.get("contenido_completo") or r.get("fragmento", "")
        # Truncar contenido largo para no exceder el contexto del modelo
        if len(contenido) > 3000:
            contenido = contenido[:3000] + "\n[...contenido truncado]"
        bloques.append(
            f"### Fuente {i}: {titulo}\nURL: {url}\n\n{contenido}"
        )
    return "CONTENIDO A PROCESAR:\n\n" + "\n\n---\n\n".join(bloques)


# ---------------------------------------------------------------------------
# Parseo y validación del output del LLM
# ---------------------------------------------------------------------------

def _extraer_seccion(texto: str, nombre_seccion: str) -> str:
    """Extrae el contenido de una sección ## del markdown."""
    patron = rf"##\s+{re.escape(nombre_seccion)}\s*\n(.*?)(?=\n##\s|\Z)"
    coincidencia = re.search(patron, texto, re.DOTALL)
    return coincidencia.group(1).strip() if coincidencia else ""


def _parsear_y_validar(texto: str) -> dict:
    """
    Parsea el markdown generado por el LLM y valida que tenga
    el frontmatter YAML correcto y las 8 secciones requeridas.
    Lanza ErrorGeneracion si la validación falla.
    """
    # Extraer frontmatter entre los primeros dos ---
    coincidencia_fm = re.search(r"^---\s*\n(.*?)\n---", texto, re.DOTALL)
    if not coincidencia_fm:
        raise ErrorGeneracion("El output no contiene frontmatter YAML válido.")

    try:
        fm = yaml.safe_load(coincidencia_fm.group(1))
    except yaml.YAMLError as e:
        raise ErrorGeneracion(f"El frontmatter YAML no es válido: {e}")

    if not isinstance(fm, dict) or not fm.get("titulo"):
        raise ErrorGeneracion("El frontmatter no contiene el campo 'titulo'.")

    # Verificar que las 8 secciones están presentes
    secciones_faltantes = [
        s for s in SECCIONES_REQUERIDAS
        if not re.search(rf"##\s+{re.escape(s)}", texto)
    ]
    if secciones_faltantes:
        raise ErrorGeneracion(
            f"Faltan secciones en el output: {secciones_faltantes}"
        )

    # Extraer fuente (puede venir como dict o como campos planos)
    fuente = fm.get("fuente") or {}
    if not isinstance(fuente, dict):
        fuente = {}

    return {
        "titulo":            str(fm.get("titulo", "")),
        "alias":             json.dumps(fm.get("alias") or [], ensure_ascii=False),
        "tags":              json.dumps(fm.get("tags") or [], ensure_ascii=False),
        "tipo":              str(fm.get("tipo", "concepto")),
        "fecha":             str(fm.get("fecha", date.today().isoformat())),
        "fuente_tipo":       str(fuente.get("tipo", "articulo")),
        "fuente_referencia": str(fuente.get("referencia", "")),
        "fuente_autor":      str(fuente.get("autor", "")),
        "relacionado":       json.dumps(fm.get("relacionado") or [], ensure_ascii=False),
        "proyectos":         json.dumps(fm.get("proyectos") or [], ensure_ascii=False),
        "estado":            "pendiente",  # siempre pendiente al crear
        # Secciones
        "que_es":            _extraer_seccion(texto, "¿Qué es?"),
        "por_que_importa":   _extraer_seccion(texto, "¿Por qué importa?"),
        "como_funciona":     _extraer_seccion(texto, "¿Cómo funciona?"),
        "ejemplos":          _extraer_seccion(texto, "Ejemplos concretos"),
        "tensiones":         _extraer_seccion(texto, "Tensiones o limitaciones"),
        "se_conecta_con":    _extraer_seccion(texto, "Se conecta con..."),
        "citas":             _extraer_seccion(texto, "Citas o fragmentos clave"),
        "mis_notas":         _extraer_seccion(texto, "Mis notas"),
        # Texto completo generado (útil para exportación directa)
        "_texto_completo":   texto,
    }


# ---------------------------------------------------------------------------
# Llamadas a los modelos
# ---------------------------------------------------------------------------

def _llamar_groq(system_prompt: str, user_prompt: str) -> str:
    cliente = groq_sdk.Groq(api_key=GROQ_API_KEY)
    respuesta = cliente.chat.completions.create(
        model=GROQ_MODELO,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=2048,
    )
    return respuesta.choices[0].message.content.strip()


def _llamar_gemini(system_prompt: str, user_prompt: str) -> str:
    cliente = genai.Client(api_key=GEMINI_API_KEY)
    respuesta = cliente.models.generate_content(
        model=GEMINI_MODELO,
        contents=user_prompt,
        config=genai_types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=2048,
        ),
    )
    return respuesta.text.strip()


# ---------------------------------------------------------------------------
# Función pública
# ---------------------------------------------------------------------------

def generar_concepto(contexto_tematica: dict, resultados: list[dict]) -> dict:
    """
    Genera un concepto atómico a partir del contexto de la temática y los
    resultados del buscador. Intenta con Groq primero; si falla, usa Gemini.

    Parámetros:
        contexto_tematica: dict con nombre, tono_prompt (y otros campos de Tematica)
        resultados: list[dict] devuelta por buscador.buscar()

    Retorna:
        dict con todos los campos del modelo Concepto listos para insertar en la BD.

    Lanza:
        ErrorGeneracion si ambos modelos fallan o el output no es válido.
    """
    system_prompt = _construir_system_prompt(contexto_tematica)
    user_prompt   = _construir_prompt_usuario(resultados)

    # --- Intento 1: Groq ---
    texto_generado = None
    error_groq = None
    try:
        texto_generado = _llamar_groq(system_prompt, user_prompt)
    except Exception as e:
        error_groq = str(e)

    # --- Intento 2: Gemini (solo si Groq falló) ---
    if texto_generado is None:
        error_gemini = None
        try:
            texto_generado = _llamar_gemini(system_prompt, user_prompt)
        except Exception as e:
            error_gemini = str(e)
            raise ErrorGeneracion(
                f"Ambos modelos fallaron.\n"
                f"  Groq:   {error_groq}\n"
                f"  Gemini: {error_gemini}"
            )

    # --- Parseo y validación ---
    concepto = _parsear_y_validar(texto_generado)
    concepto["tematica_id"] = contexto_tematica.get("id")

    # --- Cruce con INDEX.md del Segundo Cerebro ---
    tags_lista = json.loads(concepto.get("tags", "[]"))
    relacionados = inferir_relacionados(concepto["titulo"], tags_lista)
    concepto["relacionado"] = json.dumps(relacionados, ensure_ascii=False)

    return concepto
