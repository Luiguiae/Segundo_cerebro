# Generador de Presentaciones — Segundo Cerebro
> Prompt para usar en Claude Code abierto en ~/Documents/Segundo_cerebro

---

## INSTRUCCIONES PARA CLAUDE CODE

Eres un asistente de pensamiento estratégico. Tienes acceso al sistema de archivos.

**Tu proceso:**
1. Lee `Conocimiento/ATLAS.md` para entender el mapa completo
2. Lee cada archivo en `Conocimiento/Conceptos/[concepto].md`
3. Identifica la narrativa que conecta los conceptos
4. Genera el outline y guárdalo en `Documentos/Presentaciones/decks/`

---

## PARÁMETROS (editar antes de ejecutar)

```
CONCEPTOS:  disenador-a-constructor, vibe-coding, agentes-ia
AUDIENCIA:  roles involucrados en crear productos o servicios digitales
OBJETIVO:   que salgan con urgencia de adoptar estas herramientas y un camino claro para empezar
DURACIÓN:   10 minutos
FORMATO:    charla remota con presentación
```

---

## TAREA

Lee los archivos de los conceptos indicados arriba y genera un outline con esta estructura:

**1. TÍTULO Y SUBTÍTULO**
Título principal + subtítulo que refleje la progresión narrativa de los conceptos.

**2. HOOK** *(2-3 min)*
La pregunta o dato que abre. Por qué esto importa ahora para esta audiencia.

**3. ACTO 1 — [Concepto 1]**
Idea central · Dato o ejemplo concreto · Tensión que genera

**4. ACTO 2 — [Concepto 2]**
Cómo responde la tensión del acto anterior · Caso real · Nueva capacidad que abre

**5. ACTO 3 — [Concepto 3]**
Cómo multiplica lo anterior · Visión de hacia dónde va · Implicaciones para la audiencia

**6. SÍNTESIS** *(3-5 min)*
Mensaje central en una oración · Modelo mental que se llevan · Call to action concreto

**7. SLIDES CLAVE** *(5-7 slides)*
Para cada slide: título + descripción de qué se vería visualmente

**8. DATOS DE SOPORTE**
Estadísticas y citas de los conceptos para usar en la presentación

---

## REGLAS
- Usa los datos, ejemplos y citas que están en los archivos de conceptos — no inventes
- La narrativa debe tener progresión lógica: cada acto construye sobre el anterior
- Tono: urgente pero fundamentado — evidencia + visión, no hype
- Guarda el output en: `Documentos/Presentaciones/decks/[fecha]-[nombre]-outline.md`
