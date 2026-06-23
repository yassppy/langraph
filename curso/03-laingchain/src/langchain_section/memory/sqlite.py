import os

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from sqlalchemy import create_engine, text
from src.langchain_section.config.setting import setting
from src.langchain_section.memory.base import BaseMemory
from typing_extensions import Optional


class SqliteMemoryBackend(BaseMemory):
    """Backend de memoria persistente usando SQLite."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or setting.SQLITE_DB_PATH
        os.makedirs(
            os.path.dirname(self.db_path), exist_ok=True
        )  # Crea el directorio si no existe
        self._connection_string = f"sqlite:///{self.db_path}"

    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        """Retorna el historial de la memoria de una sesión."""
        return SQLChatMessageHistory(
            session_id=session_id, connection=self._connection_string
        )

    def clear(self, session_id: str) -> None:
        """Limpia el historial de la memoria de una sesión."""
        history = self.get_history(session_id)
        history.clear()

    def list_sessions(self) -> list[str]:
        """Lista todas las sesiones disponibles."""
        engine = create_engine(self._connection_string)
        try:
            with engine.connect() as connection:
                result = connection.execute(
                    text("SELECT DISTINCT session_id FROM message_store")
                )
                return [row[0] for row in result]
        except ImportError:
            return []
