---
name: correlacion-conceptos
description: >
  Analiza conceptos del Segundo Cerebro, detecta correlaciones entre ellos y genera
  archivos .md con narrativa lista para presentar en Conocimiento/Correlaciones/.
  Úsala cuando el usuario diga "correlaciona X y Y", "¿cómo se relacionan X e Y?",
  "encuentra correlaciones en mis conceptos", o cualquier variante de esas frases.
---

# Skill: correlacion-conceptos
**Versión:** 0.1
**Entorno:** Claude.ai chat
**Filesystem objetivo:** `~/Documents/Segundo_cerebro/`

---

## Descripción

Esta skill analiza conceptos del Segundo Cerebro, detecta correlaciones entre ellos con sesgo de tensión productiva (contradicción → síntesis), y escribe el resultado como archivo `.md` en `Conocimiento/Correlaciones/`.

El output está listo para usarse como argumento en una presentación, sin edición adicional.

---

## Activación

Esta skill se activa con frases como:

- "Correlaciona [concepto-a] y [concepto-b]"
- "¿Cómo se relacionan [concepto-a] y [concepto-b]?"
- "Encuentra correlaciones en mis conceptos"
- "¿Qué conexiones hay entre mis conceptos?"
- "Descubre correlaciones"

---

## Herramientas

Esta skill usa **Claude Code** para todas las operaciones de lectura y escritura de archivos en disco.

- **Leer conceptos fuente:** Claude Code lee los archivos `.md` en `~/Documents/Segundo_cerebro/Conocimiento/Conceptos/`
- **Escribir correlaciones:** Claude Code escribe el archivo generado en `~/Documents/Segundo_cerebro/Conocimiento/Correlaciones/`

Sin Claude Code activo, la skill genera el contenido del archivo pero no puede escribirlo al disco — en ese caso, entrega el contenido en chat para que el usuario lo guarde manualmente.

---

## Modo A — Correlación bajo demanda

Se activa cuando el usuario especifica dos conceptos explícitamente.

### Pasos

**1. Localizar los archivos**

Usa Claude Code para buscar los archivos correspondientes en `~/Documents/Segundo_cerebro/Conocimiento/Conceptos/`. El nombre del archivo puede no coincidir exactamente con lo que el usuario escribió — busca por similitud de nombre o por el campo `titulo` en el frontmatter YAML.

Si uno de los conceptos no existe como archivo en esa carpeta: informa al usuario con el nombre exacto que no encontraste, y detente. No generes la correlación con datos inventados.

**2. Extraer información relevante**

Lee el contenido completo de ambos archivos. Presta especial atención a:
- `titulo`, `tags`, y cualquier campo de frontmatter que describa el concepto
- El primer párrafo o definición del cuerpo
- Cualquier tensión interna que el propio archivo mencione

**3. Identificar la tensión**

Busca la fricción entre los dos conceptos — el punto donde se contradicen, se excluyen, o compiten por el mismo espacio. No busques similitudes ni complementariedad superficial. La pregunta es: ¿por qué estos dos conceptos no pueden coexistir fácilmente? ¿Qué asume uno que el otro niega?

Si la tensión no es evidente, formula una pregunta que los enfrente y respóndela.

**4. Construir la narrativa**

Escribe siguiendo la estructura tensión → síntesis:
- **La tensión:** describe la contradicción o fricción con precisión. Evita lenguaje vago. El lector debe sentir que el conflicto es real.
- **La síntesis:** resuelve o eleva la tensión. El insight debe ser no obvio — algo que no se obtiene leyendo cada concepto por separado.
- **Aplicaciones:** dos o tres contextos concretos donde esta correlación es accionable.
- **Conceptos relacionados:** uno o dos conceptos del Segundo Cerebro que orbitan esta correlación, con una línea de por qué.

**5. Proponer el título**

El título debe capturar la tensión, no los nombres de los conceptos. Fórmula válida: una contradicción aparente, una paradoja, o una pregunta que los enfrente. Ejemplos de estructura:
- "Lo que X no ve de Y"
- "Cuando X necesita ser Y para funcionar"
- "La trampa de hacer X sin entender Y"

Propón el título automáticamente. No preguntes al usuario si lo aprueba — escríbelo directamente en el archivo.

**6. Guardar el archivo**

Usa Claude Code para escribir el archivo en:
```
~/Documents/Segundo_cerebro/Conocimiento/Correlaciones/YYYY-MM-DD_concepto-a--concepto-b.md
```

- `YYYY-MM-DD`: fecha actual
- `concepto-a` y `concepto-b`: nombres de los archivos fuente en kebab-case, sin acentos, sin mayúsculas, separados por `--`

Confirma al usuario que el archivo fue escrito, con la ruta exacta.

---

## Modo B — Descubrimiento autónomo

Se activa cuando el usuario pide que Claude encuentre correlaciones sin especificar conceptos.

### Pasos

**1. Leer el inventario de conceptos**

Usa Claude Code para listar todos los archivos `.md` en `~/Documents/Segundo_cerebro/Conocimiento/Conceptos/`. Para cada archivo, lee **solo el frontmatter YAML** (campos `titulo` y `tags`). No leas el cuerpo completo en este paso — es para preservar contexto.

**2. Identificar pares con tensión productiva**

Analiza los pares posibles y selecciona entre 3 y 5 con mayor potencial de tensión productiva. El criterio de selección es:

- **Prioriza:** pares que se contradicen, compiten por el mismo espacio conceptual, o asumen mundos distintos
- **Evita:** pares que son simplemente similares, complementarios, o del mismo dominio temático sin fricción

Para cada par seleccionado, formula internamente una frase que capture la tensión antes de presentarla al usuario.

**3. Presentar la propuesta al usuario**

Muestra la lista de pares con este formato:

```
Encontré [N] correlaciones con potencial de tensión:

1. **[Concepto A]** × **[Concepto B]**
   → [Una frase que describe la fricción específica entre ellos]

2. ...
```

Cierra con: "¿Cuáles quieres que desarrolle? Puedo hacerlas todas o las que elijas."

**4. Esperar confirmación**

No generes ningún archivo hasta que el usuario confirme qué pares desarrollar. Si el usuario dice "todas", procesa cada par siguiendo el Modo A desde el paso 3.

---

## Plantilla de output

Cada archivo de correlación generado debe seguir exactamente esta estructura:

```markdown
---
tipo: correlacion
conceptos: [nombre-concepto-a, nombre-concepto-b]
fecha: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---

# [Título que captura la tensión — no los nombres de los conceptos]

## La tensión
[Un párrafo. Describe la contradicción o fricción con precisión.
Por qué estos conceptos no conviven fácilmente. Qué asume uno que el otro niega.
Evita lenguaje vago. El lector debe sentir que el conflicto es real.]

## La síntesis
[Un párrafo. Resuelve o eleva la tensión.
El insight que emerge de ponerlos juntos — algo que no se obtiene leyendo cada concepto por separado.
Listo para usarse como argumento central en una presentación.]

## Aplicaciones
- [Contexto concreto donde esta correlación es útil — específico, no genérico]
- [Otro contexto concreto]

## Conceptos relacionados
- [[nombre-concepto-c]] — [una línea: por qué aparece aquí, qué agrega]
```

### Reglas de la plantilla

- **`conceptos`:** nombres de los archivos fuente en kebab-case, sin extensión
- **`fecha`:** fecha en que se genera el archivo, formato `YYYY-MM-DD`
- **`tags`:** máximo 5. Derivar de los tags de los conceptos fuente más uno o dos que describan la correlación específica
- **Título:** obligatoriamente expresa tensión. No puede ser "[Concepto A] y [Concepto B]" ni variantes de eso
- **La tensión:** mínimo 3 oraciones, máximo un párrafo corto
- **La síntesis:** mínimo 3 oraciones, máximo un párrafo corto. Debe contener un insight no obvio
- **Aplicaciones:** mínimo 2, máximo 4. Cada una comienza con un contexto específico, no con un verbo genérico
- **Conceptos relacionados:** mínimo 1, máximo 3. Solo conceptos que existan como archivos en `Conocimiento/Conceptos/`

---

## Restricciones — v1

### Lo que esta skill NO hace

- **No correlaciona más de 3 conceptos simultáneos.** Si el usuario pide correlacionar 4 o más conceptos en una sola narrativa, responde: "En v1 el límite es 3 conceptos por correlación. ¿Quieres que haga pares o una correlación triple con los más relevantes?"
- **No modifica ni menciona `INDEX.md`.** La actualización del índice la hace `generar_index.py` por separado. No toques ese archivo bajo ninguna circunstancia.
- **No genera slides ni exporta a otros formatos.** El output es siempre Markdown puro. Si el usuario pide una slide, responde: "Eso lo hace el proceso de exportación separado. Aquí genero el archivo `.md` con la correlación."
- **No inventa conceptos.** Si un concepto mencionado por el usuario no existe como archivo en `Conocimiento/Conceptos/`, no lo construyas desde cero. Informa al usuario y detente.
- **No pregunta si el título está bien.** El título se propone automáticamente y se escribe directamente en el archivo. Si al usuario no le gusta, puede pedirte que lo cambies después.

### Comportamiento ante casos límite

| Situación | Respuesta |
|-----------|-----------|
| Concepto no encontrado como archivo | Informa el nombre exacto que no existe. Ofrece buscar por nombre similar si hay coincidencias parciales. No genera nada. |
| El usuario pide correlacionar un concepto consigo mismo | "Un concepto no puede correlacionarse con sí mismo. ¿Quieres combinarlo con otro?" |
| El usuario pide más de 5 pares en Modo B | Muestra los 5 con mayor tensión. No presentes más. |
| Ya existe un archivo con el mismo nombre en `Correlaciones/` | Informa al usuario y pregunta: "¿Sobreescribo o genero una versión nueva?" |
| El usuario no tiene ningún archivo en `Conceptos/` | "No encontré conceptos en `Conocimiento/Conceptos/`. Crea al menos un archivo ahí para usar esta skill." |

---

## Ejemplo de correlación bien formada

El siguiente ejemplo muestra el output esperado para una correlación entre `prototipo` y `argumento`. Úsalo como referencia de tono, profundidad y estructura — no como plantilla literal.

---

```markdown
---
tipo: correlacion
conceptos: [prototipo, argumento]
fecha: 2026-04-03
tags: [diseño, persuasion, comunicacion, presentaciones, epistemologia]
---

# El prototipo que no viaja solo

## La tensión
Un prototipo muestra. Un argumento explica. El problema es que mostrar y explicar
no son lo mismo: un prototipo convence en la sala donde está, con quien lo sostiene
en la mano, en el momento exacto en que se lo toca. Fuera de ese contexto, se
convierte en una imagen que necesita al autor para funcionar. El argumento, en
cambio, viaja sin ti — puede ser citado, reenviado, malinterpretado, pero sobrevive
la ausencia. La tensión real es esta: quien confía en el prototipo para convencer
está construyendo una dependencia invisible. Cada vez que el prototipo avanza en
la conversación, el argumento retrocede.

## La síntesis
Los prototipos más poderosos no muestran — argumentan. Tienen el razonamiento
incorporado en la forma: cada decisión de diseño es una proposición, cada flujo
es una hipótesis visible. Cuando un prototipo está construido así, no necesita al
autor para defenderse — la forma ya habla. La pregunta que separa un prototipo
débil de uno que viaja solo no es "¿se ve bien?" sino "¿alguien que no estuvo en
la sala puede entender por qué está hecho así?". Construir con esa pregunta activa
cambia qué decisiones se documentan, qué se hace explícito, y qué se deja implícito.

## Aplicaciones
- En una propuesta de diseño: si el cliente necesita presentarla internamente sin ti,
  el prototipo no alcanza — necesita un argumento embebido o un documento que lo traduzca
- En una charla o workshop: un prototipo que se muestra sin andamiaje argumental
  produce admiración pero no convicción; el público sale diciendo "qué bueno" en lugar
  de "entiendo por qué"

## Conceptos relacionados
- [[legibilidad]] — un prototipo legible es aquel cuyo argumento puede leerse sin
  que el autor esté presente; la legibilidad es la condición que permite el viaje
```

---
