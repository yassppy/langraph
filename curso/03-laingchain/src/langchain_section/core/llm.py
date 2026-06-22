"""Cliente LLM centralizado adaptado al nuevo SDK google-genai"""

from functools import lru_cache
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from src.langchain_section.config.setting import setting


@lru_cache(maxsize=1)
def get_llm(temperature: Optional[float] = None) -> ChatGoogleGenerativeAI:
    """Retorna un cliente LLM de Google Gemini utilizando la detección automática de entorno."""
    return ChatGoogleGenerativeAI(
        model=setting.CHAT_MODEL,
        temperature=temperature
        if temperature is not None
        else setting.DEFAULT_TEMPERATURE,
        max_retries=setting.MAX_RETRIES,
    )


@lru_cache(maxsize=1)
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Retorna un cliente de embeddings de Google Gemini."""
    return GoogleGenerativeAIEmbeddings(
        model=setting.EMBEDDING_MODEL,
    )
