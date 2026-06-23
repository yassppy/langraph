from abc import ABC, abstractmethod

from langchain_core.chat_history import BaseChatMessageHistory


class BaseMemory(ABC):
    """Contrato que cumple cualquier backend de memoria."""

    @abstractmethod
    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        """Retorna el historial de la memoria de una sesión."""

    @abstractmethod
    def clear(self, session_id: str) -> None:
        """Limpia el historial de la memoria de una sesión."""

    @abstractmethod
    def list_sessions(self) -> list[str]:
        """Lista todas las sesiones disponibles."""
