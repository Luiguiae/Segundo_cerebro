"""
Esquemas SQLAlchemy para SQLite.
Define las tablas Concepto, Tematica y Fuente, y la función
inicializar_bd() que crea las tablas y siembra los datos iniciales.
"""

import json
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rastreador.db")
motor = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class Tematica(Base):
    __tablename__ = "tematicas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, unique=True)
    # JSON serializado: términos de búsqueda en español
    terminos_busqueda = Column(Text, nullable=False, default="[]")
    # JSON serializado: términos de búsqueda equivalentes en inglés
    terminos_busqueda_en = Column(Text, nullable=False, default="[]")
    # JSON serializado: lista de URLs que se anteponen al pool global de fuentes
    fuentes_prioritarias = Column(Text, nullable=False, default="[]")
    # Texto libre que ajusta el estilo del system prompt del redactor
    tono_prompt = Column(Text, nullable=False, default="")
    activa = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)

    def terminos(self) -> list[str]:
        return json.loads(self.terminos_busqueda)

    def terminos_en(self) -> list[str]:
        return json.loads(self.terminos_busqueda_en)

    def fuentes_extra(self) -> list[str]:
        return json.loads(self.fuentes_prioritarias)


class Fuente(Base):
    __tablename__ = "fuentes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False, unique=True)
    descripcion = Column(String(300), nullable=False, default="")
    activa = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)


class Concepto(Base):
    __tablename__ = "conceptos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Campos del encabezado YAML
    titulo = Column(String(500), nullable=False)
    alias = Column(Text, nullable=False, default="[]")       # JSON: lista de strings
    tags = Column(Text, nullable=False, default="[]")        # JSON: lista de strings
    tipo = Column(String(50), nullable=False, default="concepto")
    fecha = Column(String(10), nullable=False)               # YYYY-MM-DD
    fuente_tipo = Column(String(50), nullable=False, default="")
    fuente_referencia = Column(Text, nullable=False, default="")
    fuente_autor = Column(String(300), nullable=False, default="")
    relacionado = Column(Text, nullable=False, default="[]") # JSON: lista de títulos
    proyectos = Column(Text, nullable=False, default="[]")   # JSON: lista de strings
    estado = Column(String(20), nullable=False, default="pendiente")
    # Secciones del cuerpo
    que_es = Column(Text, nullable=False, default="")
    por_que_importa = Column(Text, nullable=False, default="")
    como_funciona = Column(Text, nullable=False, default="")
    ejemplos = Column(Text, nullable=False, default="")
    tensiones = Column(Text, nullable=False, default="")
    se_conecta_con = Column(Text, nullable=False, default="")
    citas = Column(Text, nullable=False, default="")
    mis_notas = Column(Text, nullable=False, default="")
    # Metadatos internos
    tematica_id = Column(Integer, nullable=True)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Datos semilla
# ---------------------------------------------------------------------------

TEMATICAS_INICIALES = [
    {
        "nombre": "Vibe Coding",
        "terminos_busqueda": json.dumps(["vibe coding", "programación con IA", "cursor ide", "copilot programación"]),
        "terminos_busqueda_en": json.dumps(["vibe coding", "AI-assisted programming", "cursor ide workflow", "copilot coding"]),
        "fuentes_prioritarias": json.dumps(["blog.cursor.sh", "ycombinator.com/blog"]),
        "tono_prompt": "Entusiasta y práctico. Enfocado en flujos de trabajo reales con herramientas de IA para desarrollo de software.",
    },
    {
        "nombre": "Agentes IA",
        "terminos_busqueda": json.dumps(["agentes autónomos IA", "sistemas multi-agente", "agentes LLM", "orquestación agentes"]),
        "terminos_busqueda_en": json.dumps(["AI agents", "autonomous LLM agents", "multi-agent systems", "agent orchestration"]),
        "fuentes_prioritarias": json.dumps(["arxiv.org", "ycombinator.com/blog"]),
        "tono_prompt": "Técnico y riguroso. Prioriza conceptos de arquitectura, coordinación y evaluación de agentes.",
    },
    {
        "nombre": "Diseñador a Constructor",
        "terminos_busqueda": json.dumps(["diseñador que construye", "diseño e ingeniería", "constructor no-code", "diseñador full-stack"]),
        "terminos_busqueda_en": json.dumps(["designer who codes", "design engineering", "no-code builder", "designer as maker"]),
        "fuentes_prioritarias": json.dumps(["adplist.org", "medium.com"]),
        "tono_prompt": "Reflexivo y orientado a práctica. Conecta habilidades de diseño con capacidades de construcción digital.",
    },
    {
        "nombre": "Usuarios Sintéticos",
        "terminos_busqueda": json.dumps(["usuarios sintéticos", "personas simuladas IA", "investigación usuarios IA", "síntesis datos cualitativos"]),
        "terminos_busqueda_en": json.dumps(["synthetic users", "AI-simulated personas", "AI user research", "qualitative data synthesis AI"]),
        "fuentes_prioritarias": json.dumps(["newsletter.uxuniversity.io", "researchbookmark.substack.com"]),
        "tono_prompt": "Analítico y crítico. Evalúa validez metodológica y casos de uso reales de usuarios sintéticos en investigación.",
    },
    {
        "nombre": "Equipos Pequeños de Alto Impacto",
        "terminos_busqueda": json.dumps(["equipos pequeños productividad", "startups lean", "indie hacker", "equipos alto impacto"]),
        "terminos_busqueda_en": json.dumps(["small high-performance teams", "lean startup teams", "indie hacker productivity", "high-impact small teams"]),
        "fuentes_prioritarias": json.dumps(["ycombinator.com/blog", "iterativethinking.substack.com"]),
        "tono_prompt": "Pragmático y orientado a resultados. Destaca estructuras organizativas, dinámicas de equipo y casos concretos.",
    },
    {
        "nombre": "Referentes en IA",
        "terminos_busqueda": json.dumps(["Felix Lee IA diseño", "Ryo Lu producto IA", "líderes pensamiento IA diseño", "referentes diseño producto IA"]),
        "terminos_busqueda_en": json.dumps(["Felix Lee AI design", "Ryo Lu product AI", "Jenny Wen product design", "AI design thought leaders"]),
        "fuentes_prioritarias": json.dumps(["adplist.org", "medium.com"]),
        "tono_prompt": "Narrativo y biográfico. Extrae ideas clave, perspectivas únicas y contribuciones concretas de cada referente.",
    },
    {
        "nombre": "Decolonización",
        "terminos_busqueda": json.dumps(["decolonización digital", "IA decolonial", "conocimiento indígena tecnología", "epistemologías del sur"]),
        "terminos_busqueda_en": json.dumps(["digital decolonization", "decolonial AI", "indigenous knowledge technology", "epistemologies of the south"]),
        "fuentes_prioritarias": json.dumps(["medium.com", "arxiv.org"]),
        "tono_prompt": "Crítico y decolonial. Cuestiona supuestos eurocéntricos y visibiliza perspectivas no dominantes en tecnología.",
    },
    {
        "nombre": "Pensamiento Sistémico",
        "terminos_busqueda": json.dumps(["pensamiento sistémico", "bucles de retroalimentación", "sistemas complejos adaptativos", "dinámica de sistemas"]),
        "terminos_busqueda_en": json.dumps(["systems thinking", "feedback loops", "complex adaptive systems", "system dynamics"]),
        "fuentes_prioritarias": json.dumps(["medium.com", "arxiv.org"]),
        "tono_prompt": "Estructurado y conceptual. Identifica bucles de retroalimentación, emergencia y propiedades sistémicas.",
    },
    {
        "nombre": "Pensamiento Crítico",
        "terminos_busqueda": json.dumps(["pensamiento crítico", "sesgos cognitivos", "epistemología práctica", "razonamiento bajo incertidumbre"]),
        "terminos_busqueda_en": json.dumps(["critical thinking", "cognitive biases", "practical epistemology", "reasoning under uncertainty"]),
        "fuentes_prioritarias": json.dumps(["medium.com"]),
        "tono_prompt": "Riguroso y socrático. Expone supuestos, evalúa argumentos y distingue evidencia de opinión.",
    },
    {
        "nombre": "Filosofía de la IA",
        "terminos_busqueda": json.dumps(["filosofía inteligencia artificial", "consciencia IA", "ética IA", "filosofía mente máquina"]),
        "terminos_busqueda_en": json.dumps(["AI philosophy", "machine consciousness", "AI ethics philosophy", "philosophy of mind AI"]),
        "fuentes_prioritarias": json.dumps(["arxiv.org", "medium.com"]),
        "tono_prompt": "Filosófico y especulativo pero anclado. Conecta preguntas fundamentales con implicaciones prácticas actuales.",
    },
    {
        "nombre": "Robótica e IA",
        "terminos_busqueda": json.dumps(["robótica e inteligencia artificial", "inteligencia encarnada", "robots IA 2025", "IA física"]),
        "terminos_busqueda_en": json.dumps(["robotics AI", "embodied intelligence", "physical AI robots", "humanoid robots 2025"]),
        "fuentes_prioritarias": json.dumps(["arxiv.org", "ycombinator.com/blog"]),
        "tono_prompt": "Técnico y orientado a avances recientes. Diferencia entre promesas y capacidades reales demostradas.",
    },
    {
        "nombre": "Podredumbre Mental",
        "terminos_busqueda": json.dumps(["podredumbre cerebral", "atención fragmentada digital", "economía dopamina", "distracción tecnológica"]),
        "terminos_busqueda_en": json.dumps(["brain rot", "digital attention fragmentation", "dopamine economy", "technology distraction cognition"]),
        "fuentes_prioritarias": json.dumps(["medium.com", "iterativethinking.substack.com"]),
        "tono_prompt": "Directo y sin eufemismos. Nombra los mecanismos de degradación cognitiva y sus consecuencias reales.",
    },
    {
        "nombre": "Vibe Design",
        "terminos_busqueda": json.dumps(["vibe design", "diseño estético primero", "diseño sensorial digital", "UI orientada a estado de ánimo"]),
        "terminos_busqueda_en": json.dumps(["vibe design", "aesthetic-first design", "mood-driven UI", "sensory digital design"]),
        "fuentes_prioritarias": json.dumps(["adplist.org", "medium.com"]),
        "tono_prompt": "Sensorial y evocador. Prioriza la experiencia emocional y estética por encima de la funcionalidad pura.",
    },
]

FUENTES_INICIALES = [
    {"url": "adplist.org", "descripcion": "Substack de Felix Lee — diseño y carrera"},
    {"url": "iterativethinking.substack.com", "descripcion": "Ulises Arvizu — pensamiento iterativo"},
    {"url": "researchbookmark.substack.com", "descripcion": "UX University — investigación de usuarios"},
    {"url": "medium.com", "descripcion": "Medium — artículos generales"},
    {"url": "newsletter.uxuniversity.io", "descripcion": "UX University newsletter"},
    {"url": "blog.cursor.sh", "descripcion": "Blog oficial de Cursor IDE"},
    {"url": "ycombinator.com/blog", "descripcion": "Blog de Y Combinator"},
    {"url": "arxiv.org",    "descripcion": "Repositorio de papers científicos"},
    {"url": "linkedin.com", "descripcion": "LinkedIn — artículos y publicaciones profesionales"},
]


def inicializar_bd() -> None:
    """Crea las tablas y siembra datos iniciales si las tablas están vacías."""
    Base.metadata.create_all(motor)

    with Session(motor) as sesion:
        if sesion.query(Tematica).count() == 0:
            for datos in TEMATICAS_INICIALES:
                sesion.add(Tematica(**datos))

        if sesion.query(Fuente).count() == 0:
            for datos in FUENTES_INICIALES:
                sesion.add(Fuente(**datos))

        sesion.commit()


if __name__ == "__main__":
    inicializar_bd()
    print("Base de datos inicializada correctamente.")
