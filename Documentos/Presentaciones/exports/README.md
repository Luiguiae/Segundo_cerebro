# exports — Repositorio de presentaciones en PDF / PPT

Carpeta de salida para versiones exportadas de presentaciones.
Cada archivo aquí es una versión lista para compartir.

---

## Convención de nombres

```
[slug-presentacion]-[version].[ext]
```

Ejemplos:
- `disenador-constructor-v4.pdf`
- `disenador-constructor-v5.pdf`
- `ia-y-equipos-v1.pptx`

---

## Cómo exportar a PDF desde HTML (Reveal.js)

El script de exportación está en `/tmp/pdf-export/export.js`.
Para re-exportar o exportar una nueva presentación:

1. Editar `export.js`: cambiar `BASE_DIR` y `OUT_PDF`
2. Ejecutar:
   ```bash
   cd /tmp/pdf-export && node export.js
   ```

Requiere Node.js y puppeteer (`npm install puppeteer` en `/tmp/pdf-export`).

### Notas técnicas

- El script inyecta CSS de corrección post-render (`PRINT_FIX_CSS` en export.js) para evitar
  que contenido interactivo (márgenes de hover, animaciones) desborde los slides en papel.
- Si en el futuro un slide tiene overflow, agregar una regla específica en `PRINT_FIX_CSS`.
- Tamaño de página: 1280×720px (16:9). Cambiar en `page.pdf()` si se necesita otro formato.

---

## Archivos

| archivo | fuente | fecha | notas |
|---------|--------|-------|-------|
| `disenador-constructor-v4.pdf` | `html/disenador-constructor/index-v4.html` | 2026-04-17 | 1280×720px, fondo completo, overflow corregido slides 6–8 |
