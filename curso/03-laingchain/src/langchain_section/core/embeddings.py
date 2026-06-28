import os

from langchain_chroma import Chroma
from src.langchain_section.config.setting import setting
from src.langchain_section.core.llm import get_embeddings
from typing_extensions import Optional


def get_or_create_vectorstore(
    collection_name: str,
    persist_path: Optional[str] = None,
) -> Chroma:
    """Obtener un vector existente

    Args:
        collection_name (str): Nombre de la colección
        persist_path (Optional[str]): Ruta de persistencia

    Returns:
        Chroma: Instancia del vector store
    """
    path = persist_path or setting.CHROMA_PATH
    os.makedirs(path, exist_ok=True)
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=path,  # donde se guarda
    )
