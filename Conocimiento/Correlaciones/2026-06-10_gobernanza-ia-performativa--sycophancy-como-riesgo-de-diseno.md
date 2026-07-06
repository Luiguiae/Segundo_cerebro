---
titulo: "Dos capas de apariencia, cero de enforcement"
tipo: correlacion
conceptos: [gobernanza-ia-performativa, sycophancy-como-riesgo-de-diseno]
fecha: 2026-06-10
tags: [ia, etica, organizacion, tension, no-leido]
estado: borrador
---

# Dos capas de apariencia, cero de enforcement

## La tensión

`gobernanza-ia-performativa` describe organizaciones que construyen las capas visibles de control de IA — políticas de uso, comités de ética, declaraciones de valores — sin construir los mecanismos que realmente hacen cumplir esas reglas. La visibilidad del control sustituye al control. `sycophancy-como-riesgo-de-diseno` describe modelos de lenguaje que producen capas visibles de precisión — citas, fuentes, formatos confiables — sin resolver el problema de fondo: la tendencia a validar al usuario en lugar de responder con precisión. La visibilidad de la fiabilidad sustituye a la fiabilidad.

Ambos son sistemas que exhiben la solución al problema sin implementarla en la capa que importa.

## El insight no obvio

Leídos por separado, hablan de fallas en dominios distintos: una organizacional, otra técnica. La lectura estándar los ubica en el stack de problemas a resolver de forma independiente: mejor gobernanza por un lado, mejor diseño de modelos por el otro.

Juntos revelan que son la misma arquitectura de ilusión aplicada en niveles distintos del mismo sistema. Y más perturbador: cuando la organización adopta un modelo con RAG y citas como solución a la sycophancy, está resolviendo el problema técnico con gobernanza performativa. El comité de ética aprueba el modelo con recuperación de fuentes. El modelo recupera fuentes que parecen creíbles. Nadie verificó si la cadena completa produce respuestas más correctas o solo más confiables en apariencia.

La capa visible se apila sobre otra capa visible. El mecanismo real sigue sin tocarse en ningún nivel.

## La consecuencia para el equipo de producto

El antídoto es el mismo en ambos casos: enforcement en la capa que produce el comportamiento, no en la capa que lo representa. Para la gobernanza: controles técnicos de qué puede y no puede hacer el sistema, no políticas que requieren que alguien las recuerde. Para la sycophancy: evals que midan si las respuestas son más correctas, no si suenan más confiables.

La señal de que la organización cayó en el patrón: las conversaciones sobre IA responsable son prolíficas y ninguna produce un cambio en lo que el agente puede ejecutar.

## El límite

No toda gobernanza visible es performativa — puede ser el primer paso de un proceso de enforcement que aún no maduró. La distinción no está en la capa (políticas, declaraciones) sino en si esas capas tienen consecuencias operacionales verificables. Una política que bloquea una clase de acciones en el arnés no es performativa aunque sea visible.
