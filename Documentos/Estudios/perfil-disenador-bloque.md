---
titulo: "El perfil del diseñador en la era de la IA: de T-shape a bloque"
tipo: estudio
estado: borrador
autor: Luigui Avila
fecha: 2026-03-04
updated: 2026-03-04
tags: [diseño, perfil, contratacion, t-shape, generalist, ia, roles, skills]
fuentes:
  - autor: "Jenny Wen"
    titulo: "Lenny's Podcast — The future of design"
    url: "https://www.youtube.com/watch?v=eh8bcBIAAFo"
---

# El perfil del diseñador en la era de la IA: de T-shape a bloque

---

## 1. Contexto

El modelo T-shape — un área de profundidad, competencia amplia en todo lo demás — fue el ideal estándar del diseñador de producto durante la última década. El supuesto implícito: la especialización profunda en diseño visual, interacción o investigación era el diferenciador.

Ese supuesto está siendo reemplazado.

Con la IA comprimiendo los ciclos de producción, el valor diferencial ya no está en saber más de diseño que todos — está en poder operar en más dimensiones con suficiente profundidad como para no necesitar un intermediario.

---

## 2. Los tres arquetipos que emergen

Según Jenny Wen (Head of Design, Anthropic), hay tres perfiles que resultan especialmente valiosos en este contexto:

### Arquetipo 1: El generalist fuerte ("block-shaped")

No el generalist clásico que es mediocre en todo. El generalist que opera a nivel 80th percentile en múltiples skills — diseño visual, interacción, investigación, y capacidad de implementación técnica.

**El modelo conceptual:**
```
T-shape clásico:      Block-shape:
    ████                ████████
    ████                ████████
    ████                ████████
  ████████              ████████
  ████████              ████████
  ████████              ████████
```

La diferencia no es "más ancho" — es "más profundo en más dimensiones". Raro y difícil de contratar.

**Por qué es valioso ahora:** En un equipo donde los engineers pueden shipar features solos con IA, el diseñador generalist fuerte puede entrar en cualquier punto del proceso sin crear un cuello de botella. No necesita que otros lo "traduzcan" al código ni a la estrategia.

### Arquetipo 2 y 3

Jenny Wen los menciona pero la transcripción fue truncada antes de desarrollarlos. Hipótesis de lo que podría ser:
- El diseñador-investigador que traduce señales de usuarios en criterio de producto
- El diseñador-orquestador que no implementa sino que dirige agentes y engineers con criterio de diseño fuerte

*(Pendiente completar con fuentes adicionales)*

---

## 3. El cambio en la distribución del trabajo

Dato empírico de Jenny Wen (Head of Design, Anthropic, ex Director of Design Figma):

| Dimensión | Hace 2-3 años | Hoy |
|---|---|---|
| Mocking y prototyping | 60-70% | 30-40% |
| Pairing con engineers | ~20% | 30-40% |
| Implementación directa de código | ~0% | Slice significativo |
| Coordinación y reuniones | ~10% | Sin cambio visible |

**Implicación:** El diseñador que no puede pairing con engineers ni tocar código está operando en el 30-40% del rol. El resto del rol se está redistribuyendo hacia perfiles que sí pueden.

---

## 4. La rotación IC como requisito para managers

Jenny Wen volvió intencionalmente a IC después de haber sido directora en Figma (equipo de 12-15 personas + managers).

Argumento: Un manager de diseño que no hace el trabajo no puede empatizar con cómo cambió el proceso. En engineering, ya existe el precedente: los EMs hacen rotaciones técnicas de meses antes de gestionar.

> "If I had not worked in this environment, I don't know if I would've totally understood it or knew what to do or how to guide my teams."

**Implicación para management de diseño:**
- El "pure people management" (carrera, 1:1s, bienestar) pierde valor como función independiente
- El manager del futuro combina dirección del trabajo + creación de ambiente + capacidad de hacer el trabajo él mismo
- La rotación IC no es un retroceso de carrera — es una inversión en credibilidad y criterio

---

## 5. Figma como herramienta de exploración no-lineal

Una observación conceptualmente útil de Jenny Wen sobre por qué Figma sobrevive en este nuevo contexto:

El coding con IA es **lineal**: empezás en una dirección, iterás con el modelo, te quedás invertido en esa solución. No favorece la exploración radical.

Figma permite **exploración no-lineal**: 8-10 direcciones en paralelo, sin comprometerse. Detalles micro (tipografía, colores, espaciado) que sería tedioso cambiar en código.

**Distinción útil:**
- Código con IA → mejor para implementar una dirección con velocidad
- Figma → mejor para decidir qué dirección implementar

Esta distinción tiene implicancias para cuándo usar cada herramienta y en qué orden.

---

## 6. El residuo humano irreducible: accountability

Jenny Wen y Lenny Rachitsky convergen en el mismo punto que Gustavo Soto Miño:

> "At the end of the day, someone has to decide what is actually going to get built and what actually matters. Someone still needs to be accountable for the decision."

La IA mejorará en gusto y juicio estético. Lo que no delega: la responsabilidad de que la decisión fue tomada por alguien que puede responder por ella.

Analogía de Lenny: la radiología. La IA diagnostica igual o mejor. El humano firma el diagnóstico porque alguien debe ser liable si está mal. No es el mejor trabajo, pero es el trabajo que permanece.

---

## 7. Tensiones y limitaciones

- El modelo "block-shaped" es difícil de contratar y más difícil aún de desarrollar. Puede crear equipos de diseño más pequeños pero con perfiles más raros y más caros.
- La rotación IC no escala si el equipo necesita dirección constante. Hay momentos donde el manager debe elegir entre estar en el trabajo o estar en el equipo.
- Figma como herramienta de exploración vs. código como herramienta de implementación asume que el diseñador sabe en qué fase está. La confusión entre las dos fases es costosa.

---

## Se conecta con...

- `Documentos/Presentaciones/decks/2026-03-04-disenador-constructor-outline.md` → el perfil bloque y los datos de distribución de tiempo son evidencia directa para la charla
- `Documentos/Research/trust-through-speed.md` → el diseñador que puede implementar también es quien decide cuándo algo está listo para salir
- `Documentos/Research/decisiones-invisibles-y-gobernanza-ia.md` → el accountability como residuo humano es el mismo argumento en dos contextos distintos
