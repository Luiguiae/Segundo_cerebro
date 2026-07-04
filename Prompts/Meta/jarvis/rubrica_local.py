"""
rubrica_local.py — Evaluación local de rúbrica con Groq (mejora-006, Fase 5a).

Reimplementación ligera del pipeline de rúbrica del VPS (evaluador.py) para uso
directo desde el daemon de voz — sin Tavily/DeepSeek (eso es Fase 5b, vía HTTP
al VPS, no acá). El prompt de evaluación se arma desde Plantillas/rubrica.md y
Plantillas/taxonomia.md reales, no de una copia hardcodeada — evita repetir el
problema de divergencia que la auditoría del 2026-07-04 encontró entre
evaluador.py y jarvis_server.py en el VPS.

No usa responder_con_groq() de jarvis.py: esa función trunca a max_tokens=150,
insuficiente para una propuesta de cuerpo completo. Llamada HTTP propia, mismo
patrón que detectar_intent_groq (response_format json_object, sin max_tokens).
"""

import json
import os
from pathlib import Path

import requests

CEREBRO_PATH = Path.home() / "Documents" / "Segundo_cerebro"


def _construir_prompt_rubrica() -> str:
    """Arma el system prompt de evaluación a partir de los documentos normativos
    reales del vault — se re-lee en cada llamada para no quedar desactualizado
    si Luigui edita taxonomia.md/rubrica.md."""
    rubrica = (CEREBRO_PATH / "Plantillas" / "rubrica.md").read_text(encoding="utf-8")
    taxonomia = (CEREBRO_PATH / "Plantillas" / "taxonomia.md").read_text(encoding="utf-8")
    return (
        "Eres el evaluador de calidad del Segundo Cerebro de Luigui. Evalúa el concepto "
        "que te paso contra estos dos documentos normativos reales del vault — no inventes "
        "criterios ni campos fuera de lo que ellos definen.\n\n"
        f"=== TAXONOMÍA (estructura, campos, tags controlados) ===\n{taxonomia}\n\n"
        f"=== RÚBRICA (criterios de calidad, Gate 1 y Gate 2) ===\n{rubrica}\n\n"
        "Responde ÚNICAMENTE con JSON con esta forma exacta:\n"
        '{"pasa_gate1": bool, "pasa_gate2": bool, '
        '"hallazgos": ["hallazgo breve en español", "..."], '
        '"propuesta_frontmatter": {"tags": ["tag1", "tag2"]} o null, '
        '"propuesta_cuerpo": "cuerpo markdown COMPLETO actualizado (## El concepto, '
        '## Por qué importa, ## Tensiones y límites, y si aplica ## Datos y evidencia / '
        '## Ejes investigados) o null si no propones cambios al cuerpo"}\n\n'
        "Reglas: 'propuesta_frontmatter' SOLO puede tener 'tags' (máximo 5, de la lista "
        "controlada de la taxonomía) — no propongas cambios a titulo/familia/relacionado/"
        "estado/fuentes, esos los maneja Luigui aparte. 'propuesta_cuerpo', si la incluyes, "
        "debe ser el archivo completo desde el encabezado H1, no un fragmento ni un diff. "
        "Si el concepto ya cumple todo, pasa_gate1 y pasa_gate2 en true, hallazgos puede ser "
        "un elogio breve, y ambas propuestas null — no propongas cambios cosméticos innecesarios."
    )


def evaluar_concepto_con_groq(ruta: Path) -> dict:
    """Lee el .md en `ruta` y lo evalúa contra la rúbrica/taxonomía reales vía Groq.

    Retorna: {"pasa_gate1": bool, "pasa_gate2": bool, "hallazgos": list[str],
              "propuesta_frontmatter": dict | None, "propuesta_cuerpo": str | None}

    Lanza RuntimeError si GROQ_API_KEY no está disponible o la llamada falla —
    el caller debe capturarlo y degradar con un mensaje hablado."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY no disponible.")

    contenido = ruta.read_text(encoding="utf-8")
    system_prompt = _construir_prompt_rubrica()

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Concepto a evaluar (archivo: {ruta.name}):\n\n{contenido}"},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=45,
    )
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"]
    data = json.loads(raw)

    return {
        "pasa_gate1": bool(data.get("pasa_gate1", False)),
        "pasa_gate2": bool(data.get("pasa_gate2", False)),
        "hallazgos": data.get("hallazgos") or [],
        "propuesta_frontmatter": data.get("propuesta_frontmatter") or None,
        "propuesta_cuerpo": data.get("propuesta_cuerpo") or None,
    }
