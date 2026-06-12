import math
from os import getenv

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=getenv("GEMINI_API_KEY"))


def get_embedding(text: str) -> list[float]:
    """Convertir el texto a vector con embedding"""
    response = client.models.embed_content(model="gemini-embedding-001", contents=text)
    if response.embeddings is None:
        raise ValueError("No se pudo generar el embedding")
    embedding = response.embeddings[0].values
    if embedding is None:
        raise ValueError("No se pudo generar el embedding")
    return embedding


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Calcular la similitud coseno entre dos vectores"""
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )  # zip convertir en interable una tupla de 2 valores como a1 lo uno con b1 ....
    magnitude_a = math.sqrt(sum(a**2 for a in vector_a))
    magnitude_b = math.sqrt(sum(b**2 for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    print("=" * 40)
    print("Embedding: Buscar por vector")
    print("=" * 40)

    embedding_vector_a = get_embedding("Café")
    embedding_vector_b = get_embedding("Té")

    similarity = cosine_similarity(embedding_vector_a, embedding_vector_b)
    print(similarity)
