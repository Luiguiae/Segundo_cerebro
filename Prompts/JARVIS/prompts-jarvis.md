# Prompts para Jarvis

Pega cualquiera de estos prompts directamente en Claude Code (VSCode).
Reemplaza los valores entre `[corchetes]` antes de ejecutar.

---

## 0 · Arranque estándar

Incluye este bloque al inicio de **cualquier** prompt si es la primera vez que abres
la sesión de Claude Code. En sesiones que ya tienen contexto, puedes omitirlo.

```
Lee los siguientes archivos para tener contexto completo antes de actuar:
- CLAUDE.md
- Plantillas/taxonomia.md
- Plantillas/rubrica.md
- JARVIS_LOG.md
- ATLAS.md

Confirma que los leíste y cuántos conceptos hay en el vault actualmente.
```

---

## 1 · Gestión del vault

### 1.1 Auditar el vault completo

```
Lee CLAUDE.md, Plantillas/taxonomia.md, Plantillas/rubrica.md y JARVIS_LOG.md.

Jarvis, audita el vault:
1. Lee todos los archivos en Conocimiento/Conceptos/ y Conocimiento/Correlaciones/
2. Evalúa cada uno contra Gate 1 y Gate 2 de la rúbrica
3. Actualiza el campo estado en el frontmatter de cada archivo
4. Registra resultados en JARVIS_LOG.md
5. Ejecuta: python3 Prompts/Meta/generar_index.py
6. Reporta: cuántos activo, borrador, rechazado
```

### 1.2 Agregar un concepto nuevo desde texto

```
Lee CLAUDE.md, Plantillas/taxonomia.md, Plantillas/rubrica.md y JARVIS_LOG.md.

Jarvis, crea un concepto atómico con esta información:

Título: [nombre del concepto]
Idea central: [explica la idea en 2-3 oraciones]
¿Por qué importa?: [contexto o aplicación]
Fuente: [de dónde viene — conversación, artículo, podcast, reunión]
Relacionado con: [otros conceptos que podrían conectar — opcional]

Aplica la taxonomía, evalúa con la rúbrica, y escríbelo en Conocimiento/Conceptos/
si aprueba. Regenera el ATLAS después.
```

### 1.3 Procesar una fuente externa (artículo / video / podcast)

```
Lee CLAUDE.md, Plantillas/taxonomia.md, Plantillas/rubrica.md y JARVIS_LOG.md.

Jarvis, procesa esta fuente:

URL o referencia: [pega el URL o el título]
Contenido: [pega el texto, transcripción, o resumen de la fuente]

1. Crea el archivo de fuente en Conocimiento/Fuentes/ con la taxonomía correcta
2. Identifica entre 2 y 4 candidatos a concepto atómico
3. Genera cada concepto candidato
4. Evalúa cada uno con la rúbrica
5. Escribe los que aprueban en Conocimiento/Conceptos/
6. Registra todo en JARVIS_LOG.md y regenera el ATLAS
```

### 1.4 Actualizar solo el ATLAS

```
Lee CLAUDE.md.

Jarvis, actualiza el ATLAS:
Ejecuta python3 Prompts/Meta/generar_index.py y reporta cuántos conceptos fueron procesados.
```

### 1.6 Profundizar concepto

```
Lee CLAUDE.md, Plantillas/taxonomia.md y Plantillas/rubrica.md.

Jarvis, profundiza este concepto:
[pega aquí el texto del borrador o escribe la ruta al archivo .md]
```

---

### 1.5 Limpiar referencias rotas

```
Lee CLAUDE.md, Plantillas/taxonomia.md y JARVIS_LOG.md.

Jarvis, limpia el vault:
1. Encuentra todos los campos relacionado que apuntan a archivos que no existen en Conocimiento/Conceptos/
2. Para cada referencia rota: elimínala del frontmatter
3. Registra cada cambio en JARVIS_LOG.md
4. Regenera el ATLAS
```

---

## 2 · Correlaciones

### 2.1 Correlacionar dos conceptos específicos

```
Lee CLAUDE.md, Plantillas/taxonomia.md, Plantillas/rubrica.md y JARVIS_LOG.md.

Jarvis, correlaciona [nombre-concepto-a] y [nombre-concepto-b]:
1. Verifica que ambos archivos existen en Conocimiento/Conceptos/
2. Lee su contenido completo
3. Identifica la tensión productiva entre ellos (no similitudes — la fricción)
4. Evalúa con Gate 2 de correlación de la rúbrica
5. Si aprueba: escribe el archivo en Conocimiento/Correlaciones/ con el formato del skill
6. Regenera el ATLAS y registra en JARVIS_LOG.md
```

### 2.2 Descubrir correlaciones de alto potencial

```
Lee CLAUDE.md, Plantillas/taxonomia.md, Plantillas/rubrica.md, JARVIS_LOG.md e ATLAS.md.

Jarvis, descubre correlaciones:
1. Lee el frontmatter de todos los conceptos en Conocimiento/Conceptos/
2. Identifica entre 3 y 5 pares con mayor potencial de tensión productiva
3. Preséntame los pares con una frase que describa la fricción de cada uno
4. Espera mi confirmación antes de generar los archivos
```

### 2.3 Correlacionar tres conceptos

```
Lee CLAUDE.md, Plantillas/taxonomia.md, Plantillas/rubrica.md y JARVIS_LOG.md.

Jarvis, correlaciona estos tres conceptos: [concepto-a], [concepto-b] y [concepto-c]
1. Verifica que los tres archivos existen
2. Busca la tensión que emerge solo cuando los tres están juntos (no pares)
3. Evalúa con la rúbrica
4. Si aprueba: escribe en Conocimiento/Correlaciones/
5. Regenera ATLAS y registra en log
```

---

## 3 · Entregables

### 3.1 Presentación HTML (Reveal.js)

```
Lee CLAUDE.md, ATLAS.md y los siguientes conceptos de Conocimiento/Conceptos/:
[lista los archivos relevantes, ej: disenador-a-constructor.md, vibe-coding.md]

Lee también Prompts/Presentaciones/prompt-generar-presentacion.md para seguir
el formato correcto.

Genera una presentación con estas instrucciones:

Tema central: [de qué trata la presentación]
Audiencia: [a quién va dirigida]
Duración estimada: [ej: 20 minutos, 10 slides]
Tono: [técnico / ejecutivo / inspiracional / taller]
Objetivo: [qué debe lograr en la audiencia — convencer, enseñar, inspirar]

Entrega el outline primero. Espera mi aprobación antes de generar el HTML.
```

### 3.2 Post de LinkedIn

```
Lee CLAUDE.md, ATLAS.md y los siguientes conceptos:
[lista los archivos relevantes]

Genera un post de LinkedIn con estas instrucciones:

Concepto o tensión central: [qué idea quieres comunicar]
Ángulo: [ej: ventaja competitiva / transformación personal / framework técnico]
Audiencia: [diseñadores / builders / líderes de producto / audiencia mixta]
Formato: [narrativo / framework directo / lista de principios]
Longitud: [corto ~150 palabras / estándar ~300 palabras / largo ~500 palabras]

Genera 2 versiones con enfoques distintos para que elija.
```

### 3.3 Artículo largo

```
Lee CLAUDE.md, ATLAS.md y los siguientes conceptos:
[lista los archivos relevantes]

Genera un artículo con estas instrucciones:

Título tentativo: [o describe el tema si no tienes título]
Tesis central: [la idea que el artículo defiende]
Audiencia: [quién lo va a leer y en qué contexto]
Extensión: [ej: 800 palabras / 1500 palabras / sin límite]
Plataforma: [Medium / newsletter / blog interno / LinkedIn Pulse]
Tono: [analítico / narrativo / provocador / técnico]

Entrega la estructura (H2s + idea de cada sección) primero.
Espera mi aprobación antes de desarrollar el cuerpo completo.
```

### 3.4 Taller (workshop)

```
Lee CLAUDE.md, ATLAS.md y los siguientes conceptos:
[lista los archivos relevantes]

Diseña un taller con estas instrucciones:

Tema: [de qué trata el taller]
Audiencia: [perfil de los participantes]
Duración: [ej: 2 horas / medio día / 1 día]
Modalidad: [presencial / remoto / híbrido]
Objetivo de aprendizaje: [qué deben poder hacer al terminar]
Número de participantes: [ej: 10-20 personas]

Entrega:
1. Estructura del taller (bloques de tiempo + actividad)
2. Materiales necesarios
3. Instrucciones del facilitador por bloque
4. Criterio de éxito del taller
```

### 3.5 Diagrama de arquitectura o proceso

```
Lee CLAUDE.md, ATLAS.md y los siguientes conceptos:
[lista los archivos relevantes]

Genera un diagrama con estas instrucciones:

Qué quieres mostrar: [ej: el flujo del Segundo Cerebro / la arquitectura de un sistema / un proceso de decisión]
Tipo de diagrama: [flowchart / estructural / proceso / comparación]
Audiencia: [técnica / ejecutiva / diseñadores]
Formato de entrega: [SVG / Mermaid / descripción para Figma]
Nivel de detalle: [overview / detallado]
```

### 3.6 Concepto atómico desde una conversación

```
Lee CLAUDE.md, Plantillas/taxonomia.md, Plantillas/rubrica.md y JARVIS_LOG.md.

Jarvis, extrae conceptos de esta conversación:

[pega el texto de la conversación aquí]

1. Identifica entre 1 y 3 ideas que merezcan ser conceptos atómicos independientes
2. Para cada una: genera el archivo .md completo con frontmatter y cuerpo
3. Evalúa cada uno con la rúbrica
4. Escribe los que aprueban en Conocimiento/Conceptos/
5. Regenera ATLAS y registra en JARVIS_LOG.md
```

### 3.7 Resumen ejecutivo / one-pager

```
Lee CLAUDE.md, ATLAS.md y los siguientes conceptos:
[lista los archivos relevantes]

Genera un one-pager ejecutivo con estas instrucciones:

Tema: [qué explica o propone el documento]
Audiencia: [a quién va — gerente / cliente / equipo / directorio]
Objetivo: [convencer / informar / solicitar aprobación / presentar resultados]
Formato: [markdown para imprimir / HTML / estructura de email]
Extensión máxima: [1 página / 500 palabras]
Tono: [formal / directo / consultivo]
```

---

## 4 · Mantenimiento avanzado

### 4.1 Proponer nuevos tags para la taxonomía

```
Lee CLAUDE.md, Plantillas/taxonomia.md y JARVIS_LOG.md.

Jarvis, revisa los tags del vault:
1. Lista todos los tags que están en uso en Conocimiento/Conceptos/ pero no en la lista controlada de taxonomia.md
2. Para cada tag no controlado: sugiere si debe agregarse a la taxonomía (con categoría) o reemplazarse por un tag existente
3. NO modifiques taxonomia.md — solo presenta las propuestas
4. Registra las propuestas en JARVIS_LOG.md como [PROPUESTA]
```

### 4.2 Detectar conceptos duplicados o solapados

```
Lee CLAUDE.md, ATLAS.md y todos los archivos en Conocimiento/Conceptos/.

Jarvis, detecta duplicados:
1. Lee el título y el primer párrafo de cada concepto
2. Identifica pares que cubran la misma idea desde ángulos muy similares
3. Para cada par: explica la diferencia real entre ellos o confirma que son duplicados
4. Propón si deben fusionarse, mantenerse separados, o si uno debe referenciar al otro
5. NO modifiques nada — solo presenta el análisis
```

### 4.3 Generar reporte del estado del vault

```
Lee CLAUDE.md, ATLAS.md, JARVIS_LOG.md y todos los archivos en Conocimiento/.

Jarvis, genera un reporte del estado del vault:
1. Cuántos conceptos hay por familia
2. Cuántos por estado (activo / borrador / archivado)
3. Qué familias tienen menos de 2 conceptos (gaps temáticos)
4. Qué conceptos no tienen ningún relacionado (nodos huérfanos)
5. Las 3 correlaciones con más conexiones en el ATLAS
6. Última fecha de actividad en el vault

Presenta el reporte en formato de tabla donde aplique.
```

---

## 5 · Gestión de sesiones

### 5.1 Cerrar sesión

```
Lee CLAUDE.md.
Jarvis, cierra la sesión.
```

### 5.2 Revisar pendientes

```
Lee CLAUDE.md.
Jarvis, ¿qué quedó pendiente de la última sesión?
```

---

## Referencia rápida

| Necesito... | Sección |
|-------------|---------|
| Revisar que todo esté bien | 1.1 Auditar |
| Agregar una idea nueva | 1.2 Agregar concepto |
| Procesar un artículo o video | 1.3 Procesar fuente |
| Conectar dos ideas | 2.1 Correlacionar |
| Descubrir conexiones nuevas | 2.2 Descubrir correlaciones |
| Hacer una presentación | 3.1 Presentación HTML |
| Escribir un post | 3.2 Post LinkedIn |
| Escribir un artículo | 3.3 Artículo largo |
| Diseñar un taller | 3.4 Taller |
| Hacer un diagrama | 3.5 Diagrama |
| Bajar una conversación al vault | 3.6 Extraer de conversación |
| Hacer un one-pager | 3.7 One-pager |
| Profundizar un concepto con fuentes | 1.6 Profundizar concepto |
| Cerrar y guardar sesión | 5.1 Cerrar sesión |
| Ver qué quedó pendiente | 5.2 Revisar pendientes |
