from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from src.langchain_section.core.llm import get_llm

llm = get_llm(temperature=0.1)


def demo_simple_chain() -> None:
    "cadena simple"
    # ChatPromptTemplate (Role, Contenido)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un experto en {tema}. Responde de forma concisa, máximo una oración.",
            ),
            ("user", "{pregunta}"),
        ]
    )

    # StrOutputParser
    parser = StrOutputParser()

    # Cadena (chain)
    chain = prompt | llm | parser

    # Ejecutar la cadena
    response = chain.invoke(
        {"tema": "programación", "pregunta": "¿Qué es un decorador?"}
    )
    print("Simple chain")
    print(response)


def demo_steps_inspection() -> None:
    """Invocar cada componente de la cadena"""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un asistente tecnico.",
            ),
            ("user", "{pregunta}"),
        ]
    )
    parser = StrOutputParser()
    input_message = {"pregunta": "¿Qué es una API REST en simples palabras?"}

    # Sin el chain

    # Paso 1 prompt
    messages = prompt.invoke(input_message)
    print("PASO 1 - Prompt output")
    print(f"Tipo: {type(messages).__name__}")
    for msg in messages.to_messages():
        print(f" -> [{msg.type.upper()}]: {msg.content}")

    # Paso 2 LLM -> AIMessage
    ai_message = llm.invoke(messages)
    print("PASO 2 - LLM output")
    print(f"Tipo: {type(ai_message).__name__}")
    print(f"Texto extraído (.text): {ai_message.text[:150]}...")
    print(f"Tokens usados: {ai_message.usage_metadata}")

    # Paso 3 parser
    parsed = parser.invoke(ai_message)
    print("PASO 3 - Parser output")
    print(f"Tipo: {type(parsed).__name__}")
    print(f"Respuesta: {parsed}")


def demo_batch() -> None:
    """Procesar multiples inputs en paralelo"""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Clasifica los sentimientos solamente en POSITIVO, NEGATIVO o NEUTRO.",
            ),
            ("user", "{texto}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    input_messages = [
        {"texto": "Me encanta este producto, es increíble!"},
        {"texto": "No me gusta, es muy malo."},
        {"texto": "Está bien, no es peor que lo esperaba."},
    ]
    results = chain.batch(input_messages)
    print("BATCH PROCESSING")
    for input_message, result in zip(input_messages, results):
        print(f"Input: {input_message['texto'][:50]}...")
        print(f"Result: {result}")
    print()


def demo_streaming() -> None:
    """Procesando efecto de chatgpt, ya no esperamos a que cargue si no da ese efecto en tiempo real"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Explicar conceptos técnicos de forma clara."),
            ("user", "Explica el concepto de {concepto} en 1 párrafo simple."),
        ]
    )
    chain = prompt | llm | StrOutputParser()  # cadena
    print("STREAMING PROCESSING")
    print("IA", end="", flush=True)

    for chunk in chain.stream({"concepto": "langchain"}):
        print(chunk, end="", flush=True)


def demo_passthrough() -> None:
    """Pemitir el paso de datos sin modificarlo"""

    def search_concepto(input_data: dict[str, Any]) -> str:
        question = input_data.get("question", "")
        contexts = {
            "langchain": "LangChain es una plataforma de desarrollo de aplicaciones basada en modelos de lenguaje.",
            "modelo": "Los modelos de lenguaje son sistemas que aprenden a generar texto a partir de datos.",
        }
        for keyboard, context in contexts.items():
            if keyboard.lower() in question.lower():
                return context
        return "No se encontro contexto relevante"

    retriever = RunnableLambda(search_concepto)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Responde utilizando solamente este contexto: {context}"),
            ("user", "{question}"),
        ]
    )
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke({"question": "Explica el concepto de langchain"})
    print(response)
