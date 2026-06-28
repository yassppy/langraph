# LangGraph

## ¿Qué es?

Una extensión de LangChain que organiza los componentes en forma de **grafo** (nodos y conexiones), lo que permite crear sistemas de IA con flujos cíclicos, decisiones condicionales y estado compartido. Permitiendo a nuestro LLM tomar diferentes caminos según el contexto. El sistema se puede corregir a sí mismo como si fuera un humano.

> **Analogía:** Si LangChain es un script que ejecutas de arriba a abajo, LangGraph es un pipeline con while loops y if/else: el agente puede reintentar un paso fallido, bifurcarse según el resultado de una herramienta, o volver a un nodo anterior sin reiniciar todo el proceso.

## ¿Por qué nació?

Porque en el mundo real los procesos no son lineales. Un agente que escribe código necesita:

```
escribir → probar → fallar → corregirse → volver a intentar
```

Eso es un ciclo, y LangChain no podía hacerlo. LangGraph también permite **pausar y pedir aprobación humana** antes de ejecutar acciones críticas.

## Conceptos clave

### State (Estado):

Es un diccionario tipado que viaja por todos los nodos del grafo. Cada nodo puede leer y escribir solamente los campos que le corresponden. Nadie borra lo que creó el otro, simplemente lee.

### Node (Nodo):

Un nodo es una función que recibe el estado completo y devuelve un diccionario con los campos actualizados.

### Edge (Arista):

Es la conexión entre nodos, que define cómo se transfiere el estado entre ellos.

- **Edge Normal:** Siempre va del nodo A al B sin condiciones.
- **Edge Conditional:** Una función decide a dónde ir basándose en el estado actual.

### StateGraph (Grafo de Estado):

El constructor de grafos: le dices qué estado usa, agregas nodos y aristas, y luego lo compilas con `.compile()` para obtener un objeto ejecutable.

## Notas finales sobre LangGraph

- No es un reemplazo de LangChain, es una extensión de él.
- No siempre es necesario.
- No es solo para agentes; es útil para cualquier flujo con lógica condicional, procesos de aprobación o sistemas de documentos.
- Si necesitas un flujo lineal, sigue con LangChain.
