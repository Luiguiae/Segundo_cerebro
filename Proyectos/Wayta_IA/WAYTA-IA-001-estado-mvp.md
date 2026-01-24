---
id: WAYTA-IA-001
titulo: "Wayta IA — Estado del MVP (motor determinista + UI + narrador mock)"
estado: activo
autor: Luigui Avila
updated: 2026-01-24
tags: [wayta-ia, mvp, nextjs, motor-simbolico, floreria, ritual, producto]
---

# Resumen ejecutivo (1 minuto)
Wayta IA es una florería virtual con inspiración ancestral andina (Perú precolombino) que traduce intenciones del usuario a arreglos florales con coherencia simbólica. El MVP ya tiene un ciclo funcional completo: **UI → API → Motor simbólico determinista → Narración (mock)**.

El valor clave del enfoque es separar:
- **decisión (reglas explícitas, auditables)**
- **narración (capa de lenguaje, intercambiable por IA real luego)**

---

# Alcance del MVP (qué hace hoy)
## Experiencia
- Formulario web (desktop/mobile) con 4 inputs:
  - nivelMistico (1–4)
  - intencion (6 opciones)
  - inspiracionAncestral (profunda/sutil/neutral)
  - direccionRegalo (para_mi/para_otro/acompanamiento)
- Botón “Iniciar ritual”
- Render de:
  - título narrativo
  - narrativa breve (2–3 párrafos, mock)
  - cierre
  - panel “debug” con justificación en bullets
  - payload enviado

## Backend
- Endpoint Next.js:
  - `POST /api/recomendar`
- Respuesta:
  - `recomendado` (salida estructurada del motor)
  - `narracion` (mock)

---

# Decisiones clave (no negociables por ahora)
1. **El motor decide. La IA no decide.**
   - El sistema primero recomienda de forma determinista.
   - La narración es capa secundaria.

2. **Determinismo por arquetipo**
   - Tipo de arreglo fijo según arquetipo (con fallback controlado).

3. **Guardrails culturales**
   - No se prometen efectos reales (sanación/curación).
   - Inspiración ancestral: evocación respetuosa, sin dogma.

4. **Mock narrador antes que OpenAI**
   - Costo = 0
   - Control total del output
   - Cambio a OpenAI futuro será swap de implementación sin tocar el motor

---

# Arquitectura (visión simple)
## Capas
1) UI (page.tsx)
2) API (route.ts)
3) Motor simbólico (tipos.ts + reglas.ts + motor.ts)
4) Narración (narrador-mock.ts)

## Principio rector
- `tipos.ts` define el “lenguaje del dominio”
- `reglas.ts` define decisiones estables (mapeos)
- `motor.ts` orquesta y produce una salida estructurada + justificación

---

# Motor simbólico (cómo piensa)
## Inputs
- nivelMistico
- intencion
- inspiracionAncestral
- direccionRegalo
(opcional futuro: 16 tipos personalidad como matiz, no como motor)

## Outputs
- arquetipoDominante
- paleta
- tonoRitual
- profundidadSimbolica
- tipoArreglo
- justificacionBullets (3–5)

---

# Evidencia de funcionamiento (prueba mínima)
Se probó el endpoint con curl y retornó recomendación consistente.
Ejemplo (protección + tierra + flores_cuarzos) con justificación en bullets.

---

# Backlog inmediato (próximas iteraciones)
1) Contenido simbólico curado (carpeta `/contenido/`)
- flores.md
- cuarzos.md
- aromas.md
- cosmovision-andina.md

2) Narrador IA (OpenAI) con “modo on-demand”
- Botón “Revelar significado”
- Cache por combinación simbólica (para controlar costo)

3) Catálogo / precios / disponibilidad
- Mapeo de `tipoArreglo` a productos reales y rangos

4) Compra y contacto
- WhatsApp / checkout simple / delivery scheduling

---

# Riesgos
- Sobre-cargar el simbolismo demasiado pronto (scope).
- Caer en apropiación cultural superficial si el contenido no se cura con cuidado.
- Convertir MBTI en motor principal (explosión combinatoria).

Mitigación:
- mantener motor pequeño
- separar contenido de reglas
- hacer de MBTI un “matiz” opcional posterior

---

# Links / ubicaciones (en el repo de Wayta IA)
- Motor: `mvp/app/src/lib/motor/`
- API: `mvp/app/src/app/api/recomendar/route.ts`
- UI: `mvp/app/src/app/page.tsx`
- Narrador mock: `mvp/app/src/lib/ia/narrador-mock.ts`

---

# Nota personal (criterio)
Este MVP prueba que puedo construir y disponibilizar un producto funcional
yo solo, usando IA como acelerador y no como “cerebro decisor”.
El objetivo no es “hacerlo místico”, sino hacerlo coherente, explicable y vendible.
