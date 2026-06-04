# Técnicas de Prompting

## ¿Qué es un LLMs?

Imagina una biblioteca con millones de libros. Un LLM los estudió durante su entrenamiento y aprendió cómo se relacionan las palabras y las ideas.

Cuando escribes un prompt, no busca información en internet ni abre libros; predice cuál es la siguiente palabra más probable basándose en todo lo que aprendió.

Un LLM está construido usando Transformers y Deep Learning para resolver tareas de NLP (Procesamiento del Lenguaje Natural). Gracias a ello puede comprender y generar texto de forma similar a una persona.

![llm](../assets/llm.png)

## Token

El LLM necesita cortar tu texto en pedazos manejables a eso se le llama tokenización.

## Context Window

Es la cantidad de tokens que el modelo puede procesar o recordar a la vez.
Esto tiene un problema si se alcanza el límite: si la conversación es muy larga y se llena, el modelo empieza a olvidar lo que dijiste al inicio y puede alucinar.

## Prompts

Un prompt es una instrucción o pregunta que le das al modelo para que responda. Para eso hay tecnicas de prompting que puedes usar para obtener mejores resultados.

- Hay que ser más especifico no significa que mientras más largo el prompt mejor.

## Estructura del prompt

1. ROL (system: es la personalidad como el modelo se comportará, user: lo que envia el ser humano, assistant: lo que ya ha respondido el modelo)
2. TAREA
3. CONTEXTO
4. RESTRICCIONES
5. FORMATO DE SALIDA

## Zero-Shot:

Es una técnica de prompting donde no se proporciona un ejemplo, no sabe el contexto, solo la instrucción o pregunta y se confia en el conocimiento del modelo.

Se utiliza en tareas simples como traducirme el contenido, escribirme el texto de la imagen, entre otros. Esto es menos costoso que Few-shot.

## Few-shot:

Esta técnica consiste en darle al modelo unos pocos ejemplos (generalmente de 2 a 5) de parejas de "pregunta y respuesta" o "entrada y salida" antes de presentarle la tarea real ayudando a la IA a entender el formato esperado aprendiendo esos patrones.

Se utiliza cuando quieres un formato en especifico, clasificación, tranformar datos entre otros. Esto es menos costoso que Chain-of-Thought.

## Chain-of-Thought:
Es una técnica diseñada para problemas que requieren lógica o varios pasos para resolverse. En lugar de pedirle a la IA solo la respuesta final, se le instruye para que muestre su razonamiento paso a paso para reducir errores en situaciones de lógica donde se requiere descomponer el problema en pasos más simples.

Se utiliza en decisiones, lógica, debugging, entre otros. Esto es más costoso.

## Prompt Templating:

Es cuando se crean plantillas reutilizables para tus prompts. Son prompts dinámicos que permiten personalizar la entrada sin modificar el prompt original.

Se utiliza en APIs, automatizaciones como en N8N, productos con IA.

## Function calling:

Es cuando se llama a una función específica en lugar de pedirle a la IA que responda directamente. Permite que la IA realice tareas específicas y devuelva resultados estructurados.
