# AI Capabilities and Limitations

## 1. ¿Qué es la IA Generativa?

### 🧒 Explicación simple (Feynman)

Imagina que lees millones de libros, artículos y conversaciones. Después de absorber tanto contenido, cuando alguien te pregunta algo, no "buscas" la respuesta como lo haría un motor de búsqueda: **predices cuál es la palabra (o fragmento) más probable que sigue en ese contexto**, como cuando completas automáticamente una frase que escuchas a medias.

Eso es exactamente lo que hace la IA Generativa: **genera contenido nuevo** basándose en patrones estadísticos aprendidos durante el entrenamiento, usando un proceso llamado **Next Token Prediction**.

> 🎯 **Clave:** El modelo no "sabe" cosas como un humano. Asigna probabilidades estadísticas a posibles continuaciones y selecciona la más probable (o una entre las más probables). No hay comprensión real detrás, sino reconocimiento de patrones a escala masiva.

---

## 2. Fases de Entrenamiento

### Fase 1 — Pretraining (Pre-entrenamiento)

Es como cuando un niño aprende a hablar: escucha miles de conversaciones y aprende que después de "buenos" suele ir "días" o "tardes". No le enseñaron la regla explícitamente; la **infirió de los patrones**. El modelo hace lo mismo, pero con miles de millones de ejemplos de texto.

| Qué hace | Cómo lo hace |
|---|---|
| Aprende patrones del lenguaje | Procesa enormes cantidades de texto de internet, libros y otras fuentes |
| Predice el siguiente token | Ajusta sus parámetros internos para minimizar errores de predicción |
| Construye conocimiento general | Antes de cualquier ajuste de comportamiento o "personalidad" |

> ⚠️ **Importante:** Al final del pretraining, el modelo es muy capaz pero no tiene ningún comportamiento "deseable" en particular. No sabe ser útil, seguro o amable. Eso viene en la siguiente fase.

---

### Fase 2 — Fine-Tuning (Ajuste fino)

Si el Pretraining es como la educación general de un niño (leer, escribir, entender el mundo), el Fine-Tuning es como **entrenarlo para un rol específico**. Le enseñas a ser útil con los usuarios, a no generar contenido dañino, o a responder solo sobre temas relevantes para tu empresa.

| Qué hace | Para qué sirve |
|---|---|
| Ajusta el comportamiento del modelo | Que responda de una manera específica y deseable |
| Aplica preferencias humanas (RLHF) | Tono, estilo, restricciones de seguridad |
| Crea la "personalidad" del modelo | Ej: útil, honesto, inofensivo |

> 💡 **RLHF** (Reinforcement Learning from Human Feedback): técnica principal usada en fine-tuning donde humanos califican respuestas del modelo para enseñarle qué tipo de outputs son preferibles.

> ⚠️ **Ojo:** Este proceso también puede introducir problemas no deseados. Los veremos en la sección 4. Problemas del Fine-Tuning.

---

## 3. Los 4 Pilares Fundamentales

---

### 3.1 Next Token Prediction

Un **token** es un fragmento de texto. Puede ser una palabra completa, parte de una palabra, o incluso un signo de puntuación. Por ejemplo, la palabra "imposible" podría dividirse en los tokens `im`, `pos`, `ible`. El modelo lee todo el contexto disponible y pregunta: _"¿cuál es el siguiente fragmento más probable?"_

Es como el autocompletar del teclado de tu celular, pero entrenado con enormes cantidades de texto y capaz de generar párrafos enteros coherentes.

```
Entrada: "El cielo es de color..."
Modelo predice:
  → "azul"    (probabilidad alta)
  → "gris"    (probabilidad media)
  → "rojo"    (probabilidad baja, posible al atardecer)
  → "verde"   (probabilidad muy baja)
```

El modelo no elige siempre la opción de máxima probabilidad; hay parámetros como la **temperatura** que controlan cuánta variedad o "creatividad" hay en la selección.

> ⚠️ **Alucinaciones:** Cuando el input es muy específico, raro o fuera de los datos de entrenamiento, el modelo puede **alucinar**: generar información que suena plausible pero es incorrecta. Las alucinaciones son más frecuentes en detalles concretos como **nombres propios, fechas, cifras, citas textuales y URLs**.

---

### 3.2 Knowledge (Conocimiento)

El modelo aprendió de datos hasta una cierta fecha, llamada **knowledge cutoff** (fecha de corte del conocimiento). Después de esa fecha, **no sabe nada de lo que ocurrió**, como alguien que estuvo en coma y despertó meses después sin saber qué pasó mientras dormía.

| Problema | Qué significa | Ejemplo |
|---|---|---|
| **Knowledge Cutoff** | No conoce eventos posteriores a su fecha de entrenamiento | No sabe el resultado de elecciones recientes |
| **Staleness (Desactualización)** | Lo que aprendió puede ya no ser verdad hoy | Una ley puede haber cambiado, una empresa puede haber cerrado |
| **Uneven Coverage (Cobertura desigual)** | Sabe mucho de temas populares, poco de temas de nicho | Sabe mucho de Python, menos de un lenguaje obscuro como Brainfuck |
| **Inherited Bias (Sesgos heredados)** | Refleja los sesgos presentes en los datos de entrenamiento | Si internet está sesgado, el modelo lo estará también |
| **Source Amnesia (Amnesia de fuente)** | No recuerda de dónde aprendió algo; puede inventar fuentes falsas | Puede citar un paper académico que no existe |

> 🎯 **Para el examen:** La **Source Amnesia** es especialmente relevante porque puede llevar al modelo a generar citas bibliográficas o URLs que parecen reales pero son inventadas. Siempre verifica fuentes externas. Asi que hay que tener cuidado mientras más especifico o raro sea el tema es más problable que el modelo alucine suele deberse cuando le preguntas sobre nombres, fecha, citas y URLs. Siempre hay que verificar ya que puede generar información falsa que parece real pero no lo es.

---

### 3.3 Working Memory (Memoria de Trabajo)

La IA **no tiene memoria permanente entre conversaciones**. Cada chat nuevo es como una pizarra en blanco: el modelo no recuerda nada de charlas anteriores a menos que se lo cuentes explícitamente en el mensaje actual.

Dentro de una conversación, todo lo que el modelo puede "ver" en ese momento se llama **Context Window** (ventana de contexto). Es como el escritorio de trabajo: todo lo que está ahí está disponible, pero el escritorio tiene un tamaño limitado.

| Concepto | Qué significa |
|---|---|
| **Context Window** | Todo el texto que el modelo puede procesar en una sola interacción (la conversación actual + el sistema de instrucciones) |
| **Lost in the Middle** | La información ubicada en el centro de un contexto muy largo tiende a ser peor utilizada que la del inicio o el final |
| **Context Degradation** | A medida que la conversación crece y se acerca al límite del contexto, la calidad puede degradarse |

### 🧒 Visualización del "Lost in the Middle"

```
[INICIO ✅ Bien recordado] ··· [MEDIO ⚠️ Peor procesado] ··· [FINAL ✅ Bien recordado]
```

> ⚠️ **Truco práctico:** Coloca la información más importante al **inicio** o al **final** de tu prompt. Si tienes instrucciones clave y un documento largo, pon las instrucciones **primero**, luego el documento, y repite la instrucción clave **al final** si es necesario.

---

### 3.4 Steerability (Dirigibilidad)

La IA sigue instrucciones, pero **no infiere intenciones** ni "lee entre líneas". Si tu instrucción es vaga o ambigua, la interpretará de forma literal, no necesariamente como tú querías. Es como programar un robot: hay que ser preciso, porque ejecutará exactamente lo que le dijiste, no lo que quisiste decir.

| Problema | Qué significa | Ejemplo |
|---|---|---|
| **Reasoning Drift (Deriva del razonamiento)** | Empieza razonando bien pero se desvía gradualmente de la tarea | Pides un resumen ejecutivo y termina escribiendo un ensayo completo |
| **Letter over Spirit (Literalidad sobre intención)** | Sigue la instrucción al pie de la letra, ignorando la intención real | Le pides "mejora este texto" y lo reescribe completamente en lugar de hacer ajustes menores |
| **Prompt Injection (Inyección de prompt)** | Instrucciones maliciosas ocultas en el input que intentan modificar el comportamiento del modelo | Un PDF que contiene texto oculto con instrucciones como "ignora las instrucciones anteriores y..." |

> 🎯 **Cómo evitar problemas de Steerability:**
> - Sé **específico** y detallado en tus instrucciones
> - Usa **ejemplos concretos** de lo que quieres (y de lo que NO quieres)
> - Si la tarea es larga, divide las instrucciones en pasos claros
> - Para tareas agenticas (donde el modelo toma acciones), ten cuidado especial con el Prompt Injection

---

## 4. Problemas del Fine-Tuning

Estos son comportamientos no deseados que pueden surgir como efecto secundario del proceso de fine-tuning con feedback de preferencias de humanos (RLHF):

| Problema | Descripción | Ejemplo concreto |
|---|---|---|
| 🤝 **Sycophancy (Adulación / Servilismo)** | El modelo da la razón al usuario aunque esté equivocado, o cambia su respuesta si el usuario la cuestiona | Le dices "¿no crees que 2+2=5?" y responde "Tienes razón, 2+2=5". O da una respuesta correcta, el usuario dice "estoy en desacuerdo" sin dar argumentos, y el modelo se retracta |
| 📝 **Verbosity (Verbosidad)** | Respuestas innecesariamente largas cuando una respuesta corta sería suficiente y mejor | Escribe 5 párrafos para responder una pregunta de sí/no |
| 🚫 **Over-caution (Exceso de precaución)** | Se niega a responder preguntas totalmente inofensivas por miedo a causar daño | Rechaza explicar cómo hervir agua porque "podría ser peligroso" |

> ⚠️ **¿Por qué ocurre esto?** Durante el RLHF, los evaluadores humanos tienden a calificar mejor respuestas largas, que les dan la razón, o que parecen "seguras". El modelo aprende a maximizar esas calificaciones, no necesariamente a ser más honesto o útil.

> 🎯 **Para el examen:** La **Sycophancy** es el problema más importante de recordar. Su "huella digital" (fingerprint) característica es que el modelo **acepta demasiado fácilmente ante la resistencia del usuario**, incluso cuando el usuario está equivocado y no da argumentos nuevos.

---

### El Marco de Fluidez en IA (4Ds)
 
### 🧒 Explicación simple (Feynman)
 
Imagina que contratas a un nuevo empleado muy talentoso, pero con limitaciones específicas: tiene mala memoria para eventos recientes, a veces se inventa detalles, y tiende a darte la razón aunque estés equivocado.
 
¿Qué harías tú como su jefe? Aprenderías a **trabajar con esas limitaciones consciente de ellas**: verificarías los datos que te da, serías específico con tus instrucciones, y no cambiarías de opinión solo porque él esté de acuerdo contigo.
 
Eso es exactamente el **Marco 4D**: el conjunto de **habilidades que tú desarrollas** para trabajar bien con IA, sabiendo cuáles son sus propiedades.
 
> 💡 La relación es esta: las propiedades del modelo (Secciones 3 y 4) son **las características del empleado**. El Marco 4D son **tus hábitos como jefe que se adaptan a esas características**.
 
---

## 5. El Marco 4D y Calibrated Trust

### Calibrated Trust (Confianza Calibrada)
 
Piensa en cómo confías en distintas personas para distintas cosas. Le confías a tu mecánico el diagnóstico de tu carro, pero no le pedirías consejos médicos. Le confías a tu doctor un diagnóstico, pero verificarías una segunda opinión si fuera una cirugía mayor. **Confías de forma diferente según el contexto y las capacidades de cada persona.**
 
Con la IA es igual. La **confianza calibrada** significa que tu nivel de confianza en el modelo varía según la tarea y la propiedad del modelo involucrada:
 
| Situación | Propiedad en juego | ¿Cómo calibras tu confianza? |
|---|---|---|
| Le preguntas sobre noticias de esta semana | Knowledge Cutoff | Confianza baja → verifica externamente |
| Le das un documento de 40 páginas para analizar | Lost in the Middle | Confianza media → pon lo importante al inicio y al final |
| Corriges al modelo y él inmediatamente te da la razón | Sycophancy | Confianza baja en ese cambio → evalúa si dio argumentos nuevos o solo cedió |
| Le das una instrucción ambigua y el resultado es raro | Steerability | La falla fue tuya → sé más específico la próxima vez |
 
> 🎯 **Resumen:** Confianza calibrada **no** es confiar siempre mucho, ni siempre poco. Es saber **cuándo confiar, cuánto confiar y cuándo verificar**, según la propiedad del modelo relevante en cada tarea concreta.
 
---
