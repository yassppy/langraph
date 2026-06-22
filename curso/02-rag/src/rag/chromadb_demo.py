from os import getenv

import chromadb
import numpy as np
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv
from google import genai

load_dotenv()
genai_client = genai.Client(api_key=getenv("GEMINI_API_KEY"))


class GeminiEmbeddingFunction(EmbeddingFunction):
    """Embedding function para ChromaDB usando Gemini"""

    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        response = genai_client.models.embed_content(
            model="gemini-embedding-001",
            contents=input,
        )

        if response.embeddings is None:
            raise ValueError("No se pudieron generar los embeddings")

        embeddings: Embeddings = []
        for e in response.embeddings:
            if e.values is None:
                raise ValueError("Un embedding vino vacío")
            embeddings.append(np.array(e.values, dtype=np.float32))

        return embeddings


def create_chroma_client(persist: bool = True):
    """Crear un cliente en chromadb"""
    if persist:
        return chromadb.PersistentClient(path="./data/chromadb")  # Guardar en disco
    else:
        return chromadb.EphemeralClient()  # Guardar en memoria


def create_collection(client, name: str):
    """Crear una colección"""
    gemini_em = GeminiEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=name,
        embedding_function=gemini_em,
        metadata={"description": "Base de conocimiento del curso"},
    )

    return collection


def add_documents(collection, documents: list[dict]) -> None:
    """Agrega documentos a ChromaDB"""
    collection.add(
        ids=[doc["id"] for doc in documents],
        documents=[doc["texto"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
    )

    print(f"OK {len(documents)} documentos agregados a ChromaDB")


def search_similar(collection, question: str, n_results: int = 3) -> list[dict]:
    """Busca documentos más relevantes"""
    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    formatted_docs = []

    for i in range(len(results["documents"][0])):
        formatted_docs.append(
            {
                "texto": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similitud": round(1 - (results["distances"][0][i]), 3),
            }
        )

    return formatted_docs


if __name__ == "__main__":
    print("=" * 40)
    print("ChromaDB")
    print("=" * 40)

    # 1. Crear cliente
    client = create_chroma_client(persist=True)
    collection = create_collection(client, "base_conocimientos_devtalles")

    # 2. Agregar documentos
    if collection.count() == 0:
        print("\nPrimera ejecución, agregando documentos...")
        add_documents(
            collection,
            [
                {
                    "id": "doc_001",
                    "texto": "Para reiniciar el servidor Nginx en Ubuntu ejecuta: sudo systemctl restart nginx. Verifica el estado con: sudo systemctl status nginx.",
                    "metadata": {
                        "fuente": "manual_ops.pdf",
                        "seccion": "Servidores",
                        "pagina": 12,
                    },
                },
                {
                    "id": "doc_002",
                    "texto": "Las variables de entorno se configuran en el archivo .env en la raíz del proyecto. Nunca subas el archivo .env a Git. Usa .env.example como plantilla.",
                    "metadata": {
                        "fuente": "guia_dev.pdf",
                        "seccion": "Configuración",
                        "pagina": 3,
                    },
                },
                {
                    "id": "doc_003",
                    "texto": "El límite de rate en nuestra API es de 1000 requests por minuto por usuario. Si lo superas recibirás un error 429. Implementa exponential backoff en el cliente.",
                    "metadata": {
                        "fuente": "api_docs.pdf",
                        "seccion": "Rate Limits",
                        "pagina": 8,
                    },
                },
                {
                    "id": "doc_004",
                    "texto": "Para hacer deploy a producción: 1) Corre los tests con pytest, 2) Build la imagen Docker, 3) Push al registry, 4) Aplica el helm chart con kubectl.",
                    "metadata": {
                        "fuente": "deploy_guide.pdf",
                        "seccion": "DevOps",
                        "pagina": 22,
                    },
                },
                {
                    "id": "doc_005",
                    "texto": "La base de datos PostgreSQL corre en el puerto 5432. Las credenciales están en Vault bajo el path secret/prod/postgres. Nunca uses las credenciales de prod en local.",
                    "metadata": {
                        "fuente": "infra_docs.pdf",
                        "seccion": "Base de Datos",
                        "pagina": 5,
                    },
                },
                {
                    "id": "doc_006",
                    "texto": "Para restaurar un backup de la base de datos: pg_restore -U postgres -d mydb backup.dump. Los backups se generan automáticamente cada noche a las 2am UTC.",
                    "metadata": {
                        "fuente": "infra_docs.pdf",
                        "seccion": "Base de Datos",
                        "pagina": 7,
                    },
                },
            ],
        )
    else:
        print(f"\nYa existen {collection.count()} documentos en la colección.")

    # 3. Buscar documentos similares
    pregunta = "¿Cómo reinicio el servidor web?"
    resultados = search_similar(collection, pregunta)

    print(f"\nPregunta: {pregunta}\n")
    for r in resultados:
        print(f"- ({r['similitud']}) {r['texto']} | {r['metadata']}")
