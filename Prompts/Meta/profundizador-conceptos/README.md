# profundizador-conceptos

Enriquece un borrador de concepto con investigación web y lo devuelve como `.md` listo para el vault.

## Cómo usarlo

1. Pega el borrador en el chat (texto libre o ruta a `Conocimiento/Conceptos/nombre.md`)
2. Di: `"profundiza este concepto"` o `"busca fuentes para esto"`
3. Claude investiga 3 ejes clave y entrega el concepto enriquecido en formato atómico

## Qué hace internamente

- Extrae 3 ejes de investigación del borrador
- Lanza búsquedas web por eje (mínimo 2 fuentes sólidas cada uno)
- Construye el `.md` expandido con sección `## Datos y evidencia`

## Qué NO hace

- No guarda el archivo — tú decides el nombre y cuándo guardarlo
- No modifica el ATLAS (eso lo hace `generar_index.py`)
- No inventa datos: lo que no encuentra lo marca `[sin fuente verificada]`
