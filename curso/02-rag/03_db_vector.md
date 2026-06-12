# Base de datos vectorial

## La idea central (analogía)

Imagina dos formas de organizar una biblioteca:

- **Base de datos tradicional**: organiza los libros por título, autor o código exacto. Si buscas "Manuel", encuentra solo libros que contengan literalmente esa palabra.
- **Base de datos vectorial**: organiza los libros por **tema y significado**. Si buscas "libros sobre soledad", te trae libros que hablan de ese tema aunque nunca usen la palabra "soledad".

## Diferencia clave

| | Base de datos tradicional | Base de datos vectorial |
|---|---|---|
| **Guarda** | Datos en estructura tabular (filas y columnas) | El *significado* de los datos como coordenadas numéricas (embeddings) en un espacio multidimensional |
| **Busca por** | Coincidencia exacta de palabras clave | Similitud semántica (significado parecido) |
| **Ejemplo de búsqueda** | "Busca todos los usuarios con la palabra Manuel" | "Dame la frase cuyo significado es más parecido a esta pregunta" |

## Bases de datos vectoriales populares

- Pinecone
- Chroma
- pgvector
- Milvus
- Weaviate

## ChromaDB

ChromaDB es una base de datos vectorial diseñada para **almacenar, organizar y buscar embeddings** junto con el texto original (documento) y sus metadatos.

Está pensada para responder preguntas semánticas complejas ("¿qué documentos hablan de algo parecido a esto?"), mientras que las bases de datos tradicionales responden preguntas más directas ("¿qué fila tiene exactamente este valor?").

> **Importante**: ChromaDB **no genera embeddings por sí sola** (tú debes crearlos, por ejemplo con un modelo de embeddings). Su trabajo es **almacenarlos** y **buscar por similitud semántica**, guardando todo de forma persistente en disco.

### Algoritmo HNSW

HNSW (Hierarchical Navigable Small World) es el algoritmo que usa ChromaDB para organizar los vectores.

Piensa en HNSW como un **mapa de atajos**: en lugar de comparar tu vector de búsqueda contra *todos* los vectores guardados (lo cual sería muy lento), organiza los vectores en una estructura de grafo jerárquico (como capas de un mapa, de lo general a lo específico) que permite saltar directo a las zonas más prometedoras y encontrar los vectores más similares de forma rápida y eficiente.

### Conceptos clave de ChromaDB

| Concepto | Qué es | Analogía con SQL |
|---|---|---|
| **Collection** | Unidad principal donde se agrupan los datos | Una tabla |
| **Documents** | El texto original del chunk (fragmento de texto) | El contenido de una celda |
| **Embeddings** | Los vectores numéricos que representan el significado de cada documento | Un índice "invisible" basado en significado |
| **Metadata** | Información adicional sobre cada documento (origen, fecha, autor, etc.) | Columnas extra de una fila |
