import os

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from sqlalchemy import create_engine, text
from src.langchain_section.memory.base import BaseMemory
from typing_extensions import Optional


class PostgreSQLMemory(BaseMemory):
    """Backend de memoria utilizando PostgreSQL."""

    def __init__(self, database_url: Optional[str] = None):
        self._database_url = database_url or os.getenv("DATABASE_URL")
        if not self._database_url:
            raise ValueError("Database URL no configurada")
        if not self._database_url.startswith("postgresql://"):
            raise ValueError("URL de base de datos no válida")

    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        """Retorna el historial de la memoria de una sesión."""
        return SQLChatMessageHistory(
            session_id=session_id, connection=self._database_url
        )

    def clear(self, session_id: str) -> None:
        """Limpia el historial de la memoria de una sesión."""
        history = self.get_history(session_id)
        history.clear()

    def list_sessions(self) -> list[str]:
        """Lista todas las sesiones disponibles."""
        engine = create_engine(str(self._database_url))
        try:
            with engine.connect() as connection:
                result = connection.execute(
                    text("SELECT DISTINCT session_id FROM message_store")
                )
                return [row[0] for row in result]
        except ImportError:
            return []
