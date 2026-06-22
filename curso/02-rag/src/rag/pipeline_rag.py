import time
import uuid
from os import getenv

import chromadb
import numpy as np
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings, Metadata
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

genai_client = genai.Client(api_key=getenv("GEMINI_API_KEY"))


class GeminiEmbeddingFunction(EmbeddingFunction):
    """Convertir texto a embeddings usando la API de Gemini."""

    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        """Devolvera la cantidad de vectores en base a la cantidad de documentos ingresados."""
        response = genai_client.models.embed_content(
            model="gemini-embedding-001",
            contents=input,
        )
        if response.embeddings is None:
            raise ValueError("No se pudieron generar los embeddings")

        # Contruyendo la lista de embeddings
        embeddings: Embeddings = []
        for e in response.embeddings:
            if e.values is None:
                raise ValueError("Un embedding vino vacío")
            embeddings.append(np.array(e.values, dtype=np.float32))

        return embeddings


class RAGPipeline:
    """
    Pipeline RAG completo con Gemini.

    Flujo:
      1. index_texts()  → guarda textos como vectores en ChromaDB
      2. retrieve_context() → busca los fragmentos más relevantes
      3. answer()       → recupera contexto + genera respuesta con el LLM
    """

    def __init__(self, collection_name: str, db_path: str = "./data/chromadb"):
        """
        Inicializa ChromaDB y la colección.

        - db_path: carpeta donde ChromaDB guarda los datos en disco.
        - collection_name: nombre de la "tabla" donde vivirán los documentos.
        """
        self.chroma_client = chromadb.PersistentClient(path=db_path)

        self.embedding_fn = GeminiEmbeddingFunction()

        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},  # similitud coseno explícita
        )

        print(
            f"RAG Pipeline iniciado | Colección: {collection_name} | "
            f"Documentos: {self.collection.count()}"
        )

    def index_texts(
        self,
        texts: list[str],
        metadatas: list[Metadata] | None = None,
    ) -> None:
        """
        Agrega textos a ChromaDB.

        ChromaDB llama automáticamente a GeminiEmbeddingFunction
        para convertir cada texto en vector antes de guardarlo.
        No tienes que llamar a embed_content manualmente aquí.

        - texts: lista de strings a indexar.
        - metadatas: lista de dicts con info extra (fuente, página, etc.).
          Si no pasas nada, se usa {"fuente": "manual"} por defecto.
        """
        if not texts:
            return

        # Generamos IDs únicos para cada documento
        ids = [f"doc_{uuid.uuid4().hex[:8]}" for _ in texts]

        if metadatas is None:
            metadatas = [{"fuente": "manual"} for _ in texts]

        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
        )

        print(
            f"{len(texts)} fragmentos indexados | "
            f"Total en DB: {self.collection.count()}"
        )

    def retrieve_context(
        self,
        question: str,
        n_fragments: int = 3,
    ) -> list[dict]:
        """
        Busca los fragmentos más relevantes para una pregunta.

        ChromaDB convierte la pregunta a vector (usando GeminiEmbeddingFunction),
        lo compara contra todos los vectores guardados y devuelve los más cercanos.

        - similarity > 0.3: filtramos fragmentos poco relevantes.
          Con coseno, 1.0 = idéntico, 0.0 = sin relación.
        """
        results = self.collection.query(
            query_texts=[question],
            n_results=min(n_fragments, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        # Validamos cada campo antes de usarlo
        if results["documents"] is None:
            return []
        if results["distances"] is None:
            return []
        if results["metadatas"] is None:
            return []
        if len(results["documents"]) == 0:
            return []

        fragments = []

        documents = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]

        for i in range(len(documents)):
            # Con hnsw:space=cosine, distances va de 0 (igual) a 2 (opuesto)
            # Por eso: similitud = 1 - distance  → rango 0.0 a 1.0
            similarity = round(1 - distances[i], 3)

            if similarity > 0.3:
                fragments.append(
                    {
                        "texto": documents[i],
                        "metadata": metadatas[i],
                        "similitud": similarity,
                    }
                )

        return fragments

    def answer(
        self,
        question: str,
        n_fragments: int = 3,
        verbose: bool = False,
    ) -> dict:
        """
        Pipeline RAG completo: recupera contexto y genera respuesta.

        Pasos:
          1. retrieve_context() → fragmentos relevantes de ChromaDB
          2. Construye un prompt con esos fragmentos como contexto
          3. Llama a Gemini para generar la respuesta final

        - verbose: si True, imprime los fragmentos recuperados.
        """

        # PASO 1: Recuperar contexto
        fragments = self.retrieve_context(question, n_fragments)

        if not fragments:
            return {
                "respuesta": "No encontré información relevante en la base de conocimiento.",
                "fragmentos_usados": [],
                "tiene_contexto": False,
            }

        if verbose:
            print(f"\nFragmentos recuperados para: '{question}'")
            for f in fragments:
                print(f"  [{f['similitud']}] {f['texto'][:80]}...")

        # PASO 2: Construir contexto para el LLM
        # Unimos todos los fragmentos en un solo bloque de texto
        # con su fuente, para que Gemini sepa de dónde viene cada parte
        context_text = "\n\n---\n\n".join(
            [
                f"[Fuente: {f['metadata'].get('fuente', 'desconocida')}]\n{f['texto']}"
                for f in fragments
            ]
        )

        # PASO 3: Generar respuesta con Gemini
        system_prompt = """Eres un asistente experto que responde preguntas
basándote ÚNICAMENTE en el contexto proporcionado.
Reglas:
- Si la respuesta está en el contexto, respóndela directamente y con precisión.
- Si el contexto no contiene suficiente información, dilo honestamente.
- Cita la fuente cuando sea relevante.
- No inventes información que no esté en el contexto.
- Responde en el mismo idioma de la pregunta."""

        user_prompt = f"""Contexto disponible:
{context_text}

Pregunta: {question}"""

        response = genai_client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.1,  # Respuestas más precisas, menos creativas
            ),
        )

        return {
            "respuesta": response.text,
            "fragmentos_usados": fragments,
            "tiene_contexto": True,
        }


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    DOCUMENTS = [
        {
            "texto": "Python fue creado por Guido van Rossum y lanzado en 1991. "
            "Es un lenguaje de programación de alto nivel, interpretado y de propósito general.",
            "metadata": {"fuente": "python_history.txt", "tema": "historia"},
        },
        {
            "texto": "Las listas en Python son colecciones ordenadas y mutables. "
            "Se crean con corchetes: mi_lista = [1, 2, 3]. "
            "Puedes agregar elementos con .append() y eliminar con .remove().",
            "metadata": {"fuente": "python_basics.txt", "tema": "estructuras_datos"},
        },
        {
            "texto": "Los decoradores en Python son funciones que modifican el comportamiento "
            "de otras funciones. Se usan con la sintaxis @nombre_decorador. "
            "Son muy comunes en frameworks como FastAPI y Django.",
            "metadata": {"fuente": "python_advanced.txt", "tema": "avanzado"},
        },
        {
            "texto": "Para manejar errores en Python se usa try/except. "
            "Ejemplo: try: resultado = 10/0 except ZeroDivisionError: print('División por cero'). "
            "También existe finally para código que siempre se ejecuta.",
            "metadata": {"fuente": "python_basics.txt", "tema": "manejo_errores"},
        },
        {
            "texto": "Los virtual environments (entornos virtuales) en Python aislan "
            "las dependencias de cada proyecto. Se crean con: python -m venv .venv "
            "y se activan con: source .venv/bin/activate en Linux/Mac.",
            "metadata": {"fuente": "python_setup.txt", "tema": "configuracion"},
        },
    ]

    print("=" * 60)
    print("RAG PIPELINE - Gemini")
    print("=" * 60)

    rag = RAGPipeline("python_knowledge_base_gemini")

    if rag.collection.count() == 0:
        print("\nIndexando base de conocimientos...\n")
        texts = [doc["texto"] for doc in DOCUMENTS]
        metas = [doc["metadata"] for doc in DOCUMENTS]
        rag.index_texts(texts, metas)

    questions = [
        # "¿Quién creó Python?",
        # "¿Cómo manejo excepciones en Python?",
        # "¿Para qué sirven los decoradores?",
        "¿Cómo instalo Django?",  # No está en los docs → respuesta honesta
    ]

    print("\n" + "=" * 60)
    print("Consultas al sistema RAG")
    print("=" * 60)

    for question in questions:
        print(f"\nPREGUNTA: {question}")
        result = rag.answer(question, n_fragments=2, verbose=True)
        print(f"RESPUESTA:\n{result['respuesta']}")
        print(f"Fragmentos usados: {len(result['fragmentos_usados'])}")
        print(f"Tiene contexto: {result['tiene_contexto']}")
        time.sleep(5)
