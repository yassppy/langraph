from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from src.langchain_section.core.llm import get_llm


def build_assistant_chain(system_prompt: str) -> Runnable:
    """Construir una cadena base del asistente con soporte en el historial"""
    default_prompt = """
    Eres un técnico experto en python e IA, tienes acceso al historial completo de esta conversación.
    Úsalo para dar respuestas contextuales y coherentes.
    Si el usuario hace referencia a algo anterior, recuerdalo.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt or default_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{input}"),
        ]
    )

    return prompt | get_llm() | StrOutputParser()
