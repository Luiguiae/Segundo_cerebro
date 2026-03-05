---
titulo: "Ciclo de Gobierno de Decisiones con IA"
tipo: proceso
estado: borrador
autor: Luigui Avila
fecha: 2026-03-04
updated: 2026-03-04
tags: [gobernanza, decisiones, ia, proceso, cadencia, delegacion]
fuentes:
  - autor: "Gustavo Soto Miño"
    titulo: "La urgencia de decidir"
    url: "https://laurgencia.digital/"
---

# Ciclo de Gobierno de Decisiones con IA

Proceso operativo para hacer explícito lo que el sistema decide implícitamente.
Adaptado de "La urgencia de decidir" (Gustavo Soto Miño).

---

## Propósito

Gobernar las decisiones que un sistema con IA ejecuta no significa documentar todo, aprobar todo ni ralentizar el sistema. Significa hacer explícito **lo que necesita serlo** para que el sistema pueda aprender y corregir.

Este proceso responde a una pregunta concreta: ¿cómo convierte un equipo lo implícito en explícito sin agregar burocracia?

---

## Herramienta 1: Espectro de Delegación

Antes de delegar una tarea o decisión a un agente de IA, aplicar las tres preguntas de test:

### Preguntas de test

**¿Qué pasa si el agente falla?**
Si la consecuencia es irreversible — una decisión sobre una persona, un contrato, una operación crítica — la decisión no puede delegarse sin supervisión humana activa. El agente ejecuta. Una persona responde.

**¿El criterio está completamente explícito?**
Si no puedes escribirlo de una forma que no admita interpretación, el agente lo va a interpretar de todas formas. Solo que sin avisarte. Eso no es automatización: es ambigüedad a escala.

**¿Quién responde si esto sale mal?**
Si la respuesta es "el modelo lo decidió" — no hubo gobernanza. Hubo abdicación. La responsabilidad no se delega con la tarea: se asigna antes de que la tarea empiece.

### Espectro de delegación

```
CRITERIO HUMANO IRRENUNCIABLE          DELEGABLE A AGENTES
←——————————————————————————————————————————————————————→

Valores en conflicto                   Ejecución de flujos
(sin respuesta técnicamente            (el agente ejecuta mejor
correcta; requiere juicio humano)      si el proceso está definido)

                  Validación de hipótesis
                  (el agente procesa —
                  el criterio lo pone la persona)

                  Síntesis de información
                  (el agente puede decidir
                  si el criterio está escrito)
```

**Regla:** No se puede delegar lo que aún no está definido.

---

## Herramienta 2: Ciclo de Gobierno

Cuatro momentos que cualquier equipo puede instalar. El objetivo no es decidir todo — es asegurarse de que lo que importa tenga dueño, criterio y revisión.

```
         DECISIÓN
         EXPLÍCITA
        ↗         ↖
   REVISAR       NOMBRAR
      ↑               ↓
   EJECUTAR ← ASIGNAR
```

### Los cuatro momentos

**01 NOMBRAR**
Hacer visible lo que el sistema preferiría mantener implícito. Llamar decisión a lo que es una decisión — *antes* de ejecutarla.
- Si no tiene nombre, no tiene dueño.
- Señal de alerta: "siempre fue así", "eso nunca quedó del todo definido", "el modelo lo decidió".

**02 ASIGNAR**
Un responsable real. No el área. No el proceso. Una persona que pueda explicar por qué el sistema hizo lo que hizo y que responda si el criterio estaba mal.

**03 EJECUTAR**
Con trazabilidad mínima. El registro no necesita ser perfecto — necesita existir. Si nadie puede reconstruir por qué se decidió algo, el sistema no puede aprender.

**04 REVISAR**
El mecanismo por el cual el sistema construye memoria organizacional. Sin revisión, la organización repite los mismos errores con mayor velocidad y mayor consistencia cada ciclo.

---

## Herramienta 3: Cadencia Semanal

El ciclo de gobierno no es un proyecto con inicio y fin. Es una práctica semanal de cinco días.

### Lunes — Nombrar (15 min)
- ¿Qué decisiones vamos a tomar esta semana?
- ¿Cuáles ya están tomadas implícitamente y nadie las declaró?
- Nombrar lo que el sistema está a punto de hacer antes de que lo haga.

### Martes a Jueves — Ejecutar
- Con el criterio visible.
- Con responsable asignado.
- Con un registro mínimo del razonamiento detrás de cada decisión que importe.

### Viernes — Revisar (15 min)
- ¿Qué decidió el sistema esta semana que nadie declaró?
- ¿Qué consecuencias produjo que nadie diseñó?
- ¿Qué criterio necesita actualizarse antes de que vuelva a ejecutarse?

### Siguiente Lunes — Actualizar
- El criterio que sobrevivió a la semana se consolida.
- El que no funcionó se corrige antes de escalar.
- El sistema aprende en ciclos de cinco días, no en sprints de seis meses.

---

## Aplicación en este repositorio

### Wayta IA
El motor simbólico determinista de Wayta IA es la implementación concreta del Espectro de Delegación:
- **Criterio humano explícito:** las reglas del motor (qué flor, en qué combinación, por qué)
- **Delegado al agente:** la narración (cómo se cuenta la decisión del motor)
- **Responsable:** Luigui Avila — puede explicar por qué el motor produce cada recomendación

Antes de cada iteración del motor, aplicar:
1. ¿El criterio nuevo está escrito de forma que no admita interpretación?
2. ¿Quién responde si la recomendación es incorrecta?

### Usuarios sintéticos (ADR-001)
Las simulaciones son decisiones automatizadas. Aplicar el ciclo:
- **NOMBRAR:** ¿Qué hipótesis estamos probando con esta simulación?
- **ASIGNAR:** ¿Quién valida que el criterio del prompt refleja la hipótesis?
- **EJECUTAR:** Registrar prompt, muestra, condiciones (ya en SIM-001)
- **REVISAR:** ¿Qué decidió el agente que nadie declaró? ¿Hay sesgos en la respuesta no contemplados en el diseño?

### Synthetic Reconstruction (ADR-005)
Antes de usar un estimado SR en una decisión estratégica:
- ¿El índice de certeza está explícito?
- ¿Los supuestos están declarados?
- ¿Quién responde si el estimado estaba mal?

---

## Señales de que el ciclo no está operando

- "El modelo lo decidió" como respuesta a una consecuencia no esperada
- Nadie puede reconstruir por qué el sistema hace lo que hace
- Las mismas discusiones ocurren sprint tras sprint sin resolución
- El criterio existe en la cabeza de una persona, no en un documento
- Los errores se corrigen en producción, no en el criterio

---

## Relación con ADRs

El Ciclo de Gobierno es la versión operativa semanal de lo que los ADRs hacen a nivel arquitectónico:

| ADR | Ciclo de Gobierno |
|---|---|
| Decisión explícita, con alternativas y consecuencias | Nombrar: declarar qué se decide antes de ejecutar |
| Responsable y fecha | Asignar: persona real, no área |
| Registro permanente | Ejecutar: trazabilidad mínima |
| Revisable si el contexto cambia | Revisar: actualizar criterio cada semana |

La diferencia: los ADRs operan en escala de meses o trimestres. La cadencia semanal opera en escala de días. Ambos son necesarios — ninguno reemplaza al otro.
