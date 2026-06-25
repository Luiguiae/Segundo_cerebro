# HTML Base — Sistema Visual para Presentaciones

Sistema de diseño compartido para todas las presentaciones HTML del vault.
Extraído de los documentos de referencia: `business-case-poblaciones-sinteticas.html` y `bc_landing_svg.html`.

---

## Paleta de colores (CSS custom properties)

```css
:root {
  /* Fondos */
  --ink:     #0F1923;   /* hero sections, nav, CTA dark */
  --canvas:  #F8F9FA;   /* body background, light sections */
  --white:   #FFFFFF;

  /* Marca */
  --teal:    #006B75;   /* acento primario — links, badges, eyebrows, bordes */
  --teal-lt: #E6F4F5;   /* fondo sutil teal para tarjetas de highlight */

  /* Estado */
  --green:   #16A34A;
  --amber:   #D97706;
  --red:     #DC2626;
  --blue:    #2563EB;

  /* Tipografía */
  --text-primary:   #0F1923;
  --text-secondary: #4B5563;
  --text-muted:     #9CA3AF;

  /* Bordes */
  --border: #E5E7EB;
  --border-teal: #006B75;
}
```

---

## Tipografía

```html
<!-- Google Fonts import (siempre el primero en <head>) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
/* Escala tipográfica */
body          { font-family: 'Inter', sans-serif; font-size: 16px; line-height: 1.6; }
h1, h2, h3   { font-family: 'DM Serif Display', serif; }
.mono, code  { font-family: 'JetBrains Mono', monospace; }

/* Display (hero) */
.hero-title  { font-size: clamp(2rem, 5vw, 4rem); line-height: 1.05; color: white; }

/* Section headers */
h2.section-title { font-size: clamp(1.8rem, 3vw, 2.5rem); color: var(--text-primary); }

/* Eyebrow (etiqueta sobre el título) */
.eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--teal);
  font-weight: 600;
}

/* Lead paragraph */
.lead { font-size: 1.15rem; line-height: 1.7; color: var(--text-secondary); max-width: 65ch; }

/* Stat número grande */
.stat-number {
  font-family: 'DM Serif Display', serif;
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 1;
  color: var(--teal);
}
```

---

## Estructura HTML base

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Título del documento]</title>
  <!-- Google Fonts -->
  <!-- <style> toda la CSS va aquí — documento autocontenido </style> -->
</head>
<body>
  <!-- 1. Nav fijo -->
  <nav class="nav">...</nav>

  <!-- 2. Hero (fondo --ink) -->
  <section class="hero" id="inicio">...</section>

  <!-- 3+ Secciones de contenido -->
  <!-- Alternar: fondo --canvas y fondo --ink según ritmo visual -->

  <!-- Final: CTA / Aprobación (fondo --ink) -->
  <section class="cta" id="aprobacion">...</section>

  <footer>...</footer>
</body>
</html>
```

---

## Componentes reutilizables

### Nav fijo

```html
<nav class="nav">
  <div class="nav-inner">
    <div class="nav-brand">
      <span class="mono" style="color: var(--teal)">▸</span>
      [Nombre del proyecto / empresa]
    </div>
    <div class="nav-links">
      <a href="#problema">Problema</a>
      <a href="#solucion">Solución</a>
      <a href="#roi">ROI</a>
      <a href="#aprobacion" class="nav-cta">Aprobar →</a>
    </div>
  </div>
</nav>
```

```css
.nav {
  position: fixed; top: 0; width: 100%; z-index: 100;
  background: rgba(15, 25, 35, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0,107,117,0.3);
  padding: 1rem 2rem;
}
.nav-inner { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
.nav-brand { color: white; font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; }
.nav-links { display: flex; align-items: center; gap: 2rem; }
.nav-links a { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 0.85rem; transition: color 0.2s; }
.nav-links a:hover { color: var(--teal); }
.nav-cta {
  background: var(--teal); color: white !important;
  padding: 0.4rem 1rem; border-radius: 4px;
  font-weight: 600; font-size: 0.8rem !important;
}
```

### Stat card

```html
<div class="stat-card">
  <div class="stat-number">[valor]</div>
  <div class="stat-label mono">[métrica]</div>
  <div class="stat-sub">[contexto]</div>
</div>
```

```css
.stat-card { text-align: center; padding: 1.5rem; }
.stat-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.5); margin-top: 0.5rem; }
.stat-sub { font-size: 0.8rem; color: rgba(255,255,255,0.4); margin-top: 0.25rem; }
```

### Tarjeta de contenido (fondo light)

```html
<div class="card">
  <div class="card-icon">[emoji o svg]</div>
  <h3>[título]</h3>
  <p>[descripción]</p>
</div>
```

```css
.card {
  background: white; border-radius: 12px;
  border: 1px solid var(--border);
  padding: 1.5rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.card-icon { font-size: 1.5rem; margin-bottom: 1rem; }
```

### Tarjeta de riesgo

```html
<div class="risk-card risk-[low|medium|high]">
  <div class="risk-header">
    <span class="risk-badge">[BAJO|MEDIO|ALTO]</span>
    <h4>[nombre del riesgo]</h4>
  </div>
  <p>[descripción]</p>
  <div class="risk-mit"><strong>Mitigación:</strong> [acción]</div>
</div>
```

```css
.risk-card { border-left: 4px solid; border-radius: 0 8px 8px 0; padding: 1.25rem; background: white; }
.risk-low    { border-color: var(--green); }
.risk-medium { border-color: var(--amber); }
.risk-high   { border-color: var(--red); }
.risk-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; font-weight: 700; padding: 0.2rem 0.5rem; border-radius: 3px; text-transform: uppercase; }
.risk-low    .risk-badge { background: #DCFCE7; color: var(--green); }
.risk-medium .risk-badge { background: #FEF3C7; color: var(--amber); }
.risk-high   .risk-badge { background: #FEE2E2; color: var(--red); }
```

### Tabla de comparación

```html
<table class="comparison-table">
  <thead>
    <tr>
      <th>Criterio</th>
      <th>[Opción A] ★</th>
      <th>[Opción B]</th>
      <th>[Opción C]</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[criterio]</td>
      <td class="good">✓ [valor]</td>
      <td class="neutral">~ [valor]</td>
      <td class="bad">✗ [valor]</td>
    </tr>
  </tbody>
</table>
```

### Fase del roadmap

```html
<div class="phase-card">
  <div class="phase-num mono">[Q1 2026]</div>
  <div class="phase-title">[Nombre fase]</div>
  <ul class="phase-items">
    <li>[entregable]</li>
  </ul>
  <div class="phase-kpi mono">[KPI: valor objetivo]</div>
</div>
```

---

## Convenciones de producción

- **Autocontenido:** todo CSS en `<style>` interno. Sin JS externo. Google Fonts como única dependencia externa.
- **Responsive:** usa `clamp()` para tipografía y `grid` con `auto-fill` o `minmax` para layouts. Mobile-first.
- **Sin `px` fijos en tipografía:** usa `rem` y `clamp()`.
- **Scroll suave:** `html { scroll-behavior: smooth; }` + `padding-top: 4rem` en cada `section` con id.
- **Filename:** `[slug-del-concepto]-[formato].html` guardado en `Documentos/Presentaciones/html/`
- **Lang:** siempre `<html lang="es">`.
- **Idioma:** todo el contenido generado en español.
