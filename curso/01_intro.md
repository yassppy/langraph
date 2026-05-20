# LangChain y LangGraph

---

## LangChain

### ¿Qué es?

Framework de código abierto que conecta Modelos de Lenguaje (LLMs) con el mundo exterior: bases de datos, APIs, archivos locales, PDFs y herramientas de código.

> **Analogía:** Imagina que ChatGPT es un chef brillante encerrado en una cocina sin ventanas. LangChain le abre la puerta y le da acceso al supermercado (internet), al archivo de recetas (PDFs) y al inventario interno (base de datos de la empresa).

### ¿Por qué nació?

Los LLMs tenían dos problemas graves:

- **No accedían a datos privados** — solo conocen lo que aprendieron durante su entrenamiento, no los datos internos de una empresa.
- **Olvidaban el contexto** — cada conversación empieza desde cero.

LangChain nació para resolver ambos.

### ¿Para qué se usa?

| Caso de uso | Qué hace |
|---|---|
| **RAG** | Busca en tus documentos y genera respuestas basadas en ellos, no en suposiciones. |
| **Pipelines de extracción** | Convierte miles de correos o facturas en tablas JSON limpias para guardar en bases de datos. |
| **Q&A sobre código** | Responde preguntas específicas sobre un repositorio de código. |

### Limitación clave

LangChain **solo funciona en línea recta**: Paso 1 → Paso 2 → Paso 3. Si algo falla, no puede retroceder ni repetir. Esto lo llevó a crear LangGraph.

---

## LangGraph

### ¿Qué es?

Una extensión de LangChain que organiza los componentes en forma de **grafo** (nodos y conexiones), lo que permite crear bucles, ramificaciones y puntos de pausa.

> **Analogía:** Si LangChain es una línea de ensamblaje en fábrica, LangGraph es un laberinto inteligente: el agente puede dar marcha atrás si se equivoca, pedir ayuda en ciertos puntos, o repetir pasos hasta acertar.

### ¿Por qué nació?

Porque en el mundo real los procesos no son lineales. Un agente que escribe código necesita:

```
escribir → probar → fallar → corregirse → volver a intentar
```

Eso es un ciclo, y LangChain no podía hacerlo. LangGraph también permite **pausar y pedir aprobación humana** antes de ejecutar acciones críticas.

### Conceptos clave

- **Nodo** — cada paso o tarea del proceso (escribir código, leer error, corregir).
- **Conexión** — la decisión de a dónde ir después (¿continuar o reintentar?).
- **Ciclo** — la capacidad de volver a un nodo anterior si algo falla.

### ¿Para qué se usa?

| Caso de uso | Qué hace |
|---|---|
| **Agente autocorrectivo** | Escribe código, lo prueba, lee el error en consola, se corrige y repite hasta que funcione. |
| **Aprobación humana** | Se pausa en pasos críticos (transferencias bancarias, reclamos de seguros) para que un supervisor valide antes de continuar. |
| **Sistemas multi-agente** | Varios agentes especializados (soporte técnico, facturación) colaboran y se pasan el control según el problema. |

---

## La diferencia en una sola frase

**LangChain** conecta un LLM con herramientas externas en pasos lineales. **LangGraph** añade bucles, retrocesos y pausas — convirtiendo un pipeline en un agente verdaderamente autónomo.

---

## Preguntas de repaso

Respóndelas en voz alta sin mirar los apuntes:

1. ¿Qué problema concreto resuelve LangChain que ChatGPT solo no puede hacer?
2. ¿Por qué un agente que corrige código necesita LangGraph y no puede usar solo LangChain?
3. Explica la diferencia entre nodo y conexión en LangGraph con un ejemplo de tu vida cotidiana.
4. ¿En qué situación real querrías que un agente se pause y espere aprobación humana?