from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class LangchainSettings(BaseSettings):
    # Dejamos que Pydantic valide que exista en el entorno
    GEMINI_API_KEY: str = str(getenv("GEMINI_API_KEY"))

    # Modelos e hiperparámetros actualizados según documentación
    CHAT_MODEL: str = "gemini-3.1-flash-lite"
    EMBEDDING_MODEL: str = "gemini-embedding-001"

    # ¡OJO!: La doc dice que para Gemini 3+, la temperatura recomendada es 1.0
    DEFAULT_TEMPERATURE: float = 1.0
    LOW_TEMPERATURE: float = 0.1
    MAX_RETRIES: int = 2  # Cambiado a 2 según el ejemplo estándar de inicialización

    # Rutas de persistencia
    SQLITE_DB_PATH: str = "data/chat_history.db"
    CHROMA_PATH: str = "./data/langchain_chroma"

    # Configuración de Chunks
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5


setting = LangchainSettings()
