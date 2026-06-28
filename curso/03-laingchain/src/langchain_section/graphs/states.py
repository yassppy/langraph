from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class RAGAgentState(TypedDict):
    """Estados que cada campo representa una pieza de información que los nodos comparten"""

    messages: Annotated[list, add_messages]  # mensajes del usuario y del sistema
    question: str  # pregunta del usuario
    retrieve_docs: list[str]  # lista de JSON recuperados con chromadb
    response: str  # respuesta generada por el modelo
    needs_retrieval: bool  # decisión del nodo del análisis
    sources: list[dict]  # metadatos de los documentos recuperados
