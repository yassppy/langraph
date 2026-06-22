## LangChain

### ¿Qué es?

Framework de código abierto creada por Harrison Chase, que conecta Modelos de Lenguaje (LLMs) con el mundo exterior: bases de datos, APIs, archivos locales, PDFs y herramientas de código.

> **Analogía:** Imagina que ChatGPT es un chef brillante encerrado en una cocina sin ventanas. LangChain le abre la puerta y le da acceso al supermercado (internet), al archivo de recetas (PDFs) y al inventario interno (base de datos de la empresa).

### ¿Por qué nació?

LangChain nació para simplificar la creación de aplicaciones con LLMs sin tener que construir todo desde cero, permitiendo combinarlos con otras herramientas y fuentes de datos.
Surgió como solución a tres problemas concretos:

- Conocimiento limitado: los modelos no tenían acceso a la base de datos interna de la empresa.
- Pérdida de contexto: las conversaciones no se almacenaban, por lo que el modelo "olvidaba" lo dicho anteriormente.
- Dependencia del proveedor: cambiar de un LLM a otro requería reescribir gran parte del código.

### ¿Para qué se usa?

- Chatbots avanzados
- Asistentes de consultas
- Sistema de preguntas y respuestas sobre documentos
- Automatización de tareas con IA

### Como funciona

LangChain organiza el modelo de leguaje en componentes reutilizables
- Modelos: OpenAI, Anthropic, Hugging Face, Gemini
- Prompts: Instruciones que le das al modelo
- chains: Secuencias de pasos que ejecuta LangChain (-> Preguntas -> procesar -> responder)
- Agentes: Sistemas que deciden que *acción tomar según la situación*
- Memoria: Permite recordar la información de la conversación para mantener el contexto

### ¿Qué es LCEL?

LCEL son las siglas de (LangChain Expression Language) es una forma de definir secuencias de pasos en LangChain de manera declarativa. Se utilizar el operador pipes *|* para encadenar componentes de forma declarativa.

### ¿Qué es Runnable?

Todos los componentes en LangChain son "runnables", lo que significa que pueden ser ejecutados como una secuencia de pasos.

### Limitación clave

LangChain **solo funciona en línea recta**: Paso 1 → Paso 2 → Paso 3. Si algo falla, no puede retroceder ni repetir. Esto lo llevó a crear LangGraph.

### Arquitectura

Se aplicará Layered Architecture junto con los siguientes principios de diseño:

- Single Responsibility Principle: cada archivo tiene una única responsabilidad, sin mezclar funcionalidades.
- Singleton Pattern: reutilizar una sola instancia del LLM en todo el proyecto.
- Strategy Pattern: permite intercambiar implementaciones (modelos, memorias, cadenas) sin cambiar el código que las usa.
- Módulos desacoplados: cada capa expone su funcionalidad de forma independiente.

````mermaid
src/
└── langchain_section/
    ├── config/      → CAPA DE CONFIGURACIÓN
    ├── core/        → CAPA NÚCLEO
    ├── memory/      → CAPA DE MEMORIA
    ├── chains/      → CAPA DE CADENAS
    ├── graphs/      → CAPA DE GRAFOS
    └── demos/       → CAPA DE DEMOS
````
