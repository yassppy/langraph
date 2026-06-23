from langchain_core.runnables import RunnableWithMessageHistory
from src.langchain_section.chain.base import build_assistant_chain
from src.langchain_section.memory.base import BaseMemory


def build_chatbot(backend: BaseMemory) -> RunnableWithMessageHistory:
    """Construye un chatbot
    Args:
        backend: El backend de memoria para gestionar el historial de mensajes.
    Returns:
        Un `RunnableWithMessageHistory` que gestiona el chatbot con el historial de mensajes.
    """
    chain = build_assistant_chain("")
    return RunnableWithMessageHistory(
        chain,
        backend.get_history,
        input_messages_key="input",
        history_messages_key="history",
    )


def run_chat_session(
    chatbot: RunnableWithMessageHistory, backend: BaseMemory, session_id: str
) -> None:
    print(f"Running chat session: {session_id}")

    messages = backend.get_history(session_id).messages

    if messages:
        print(f"Retomando la conversación {len(messages)} mensajes previos")
    else:
        print("Nueva conversación")

    print("Comandos: 'historial'| 'limpiar' | 'sessiones' | 'salir'\n")
    while True:
        try:
            user_input = input("Tu: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "salir":
                print("Saliendo...")
                break
            if user_input.lower() == "historial":
                messages = backend.get_history(session_id).messages
                if not messages:
                    print("[Historial vacío]")
                    continue
                print(f"\n Últimos mensajes: {session_id}")
                for message in messages[-6:]:
                    rol = "Tu" if message.type == "human" else "IA"
                    print(f"{rol}: {message.content[:70]}...")
            if user_input.lower() == "limpiar":
                backend.clear(session_id)
                messages = []
                print("Historial limpiado")
                continue
            if user_input.lower() == "sessiones":
                print("Sessions:", backend.list_sessions())
                continue

            response = chatbot.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
            response_text = str(response)
            print(f"IA: {response_text[:70]}...")
            messages.append(response)

        except KeyboardInterrupt:
            print("Hasta luego")
            break
        except Exception as e:
            print(f"Error: {e}\n")
