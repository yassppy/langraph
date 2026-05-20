# Grafos

---

## ¿Qué es un grafo?

Una estructura de datos que representa **relaciones entre entidades**. Tiene dos componentes:

- **Nodo** — una entidad, paso o decisión (una ciudad, una tarea, un agente).
- **Arista** — la relación o conexión entre dos nodos (una ruta, una transición, una dependencia).

> **Analogía:** Imagina un mapa de metro. Cada estación es un nodo. Cada vía que las une es una arista. El grafo es el mapa completo que muestra cómo llegar de un lugar a otro.

---

## Estado en un grafo (Stateful Graph)

A medida que el proceso avanza de nodo en nodo, se va acumulando información. Esa información acumulada se llama **estado**.

En un **stateful graph**:

- El estado empieza con ciertos datos iniciales.
- Cada nodo puede **leer** el estado actual y **modificarlo**.
- El estado modificado se pasa al siguiente nodo.
- Al final, el estado contiene el resultado completo del proceso.

> **Analogía:** Imagina una hoja de papel que viaja por una línea de ensamblaje. Cada operario (nodo) lee lo que dice la hoja, añade o corrige algo, y la pasa al siguiente. Al llegar al final, la hoja tiene todo el trabajo acumulado.

### Ejemplo concreto

Un agente que procesa un pedido online:

```
[Recibir pedido] → estado: { producto: "laptop", cantidad: 1 }
       ↓
[Verificar stock] → estado: { ..., stock: true }
       ↓
[Calcular precio] → estado: { ..., total: 1200 }
       ↓
[Confirmar orden] → estado: { ..., confirmado: true }
```

Cada nodo hereda el estado anterior y le suma nueva información.

---

## Tipos de grafos (lo que verás en LangGraph)

| Tipo | Descripción | Cuándo usarlo |
|---|---|---|
| **Lineal** | Los nodos se conectan en secuencia, uno tras otro. | Procesos simples sin errores posibles. |
| **Con ciclos** | Un nodo puede apuntar hacia atrás, creando un bucle. | Cuando necesitas reintentar o corregir. |
| **Con bifurcaciones** | Desde un nodo puedes ir a dos caminos distintos según una condición. | Lógica condicional (si X entonces A, si no entonces B). |

---

## Conexión con LangGraph

LangGraph usa exactamente esta estructura:

- Cada **paso del agente** es un nodo.
- El **estado compartido** viaja entre nodos y se va actualizando.
- Los **ciclos** permiten que el agente se corrija a sí mismo.
- Las **bifurcaciones** permiten decidir si continuar, reintentar o pedir aprobación humana.

---

## Preguntas de repaso

1. Explica la diferencia entre nodo y arista con un ejemplo de tu vida cotidiana (no de software).
2. ¿Qué significa que un grafo sea "stateful"? ¿Qué pasaría si no guardara estado?
3. ¿Por qué un grafo con ciclos es más útil que uno lineal para un agente de IA?
4. Dibuja en papel un grafo simple de 4 nodos que represente cómo preparas el desayuno.