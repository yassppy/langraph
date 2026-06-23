from src.langchain_section.demos.demo_lcel import (
    demo_batch,
    demo_passthrough,
    demo_simple_chain,
    demo_steps_inspection,
    demo_streaming,
)
from src.langchain_section.demos.demo_memory import build_chatbot, run_chat_session
from src.langchain_section.memory.postgresql_memory import PostgreSQLMemory
from src.langchain_section.memory.sqlite import SqliteMemoryBackend

if __name__ == "__main__":
    # print("Iniciando la app desde la raíz...")
    # demo_simple_chain()
    # demo_steps_inspection()
    # demo_batch()
    # demo_streaming()
    # demo_passthrough()

    print("=" * 50)
    print("Memoria persistente con SQLite y PostgreSQL")
    print("=" * 50)

    print("\n¿Qué backend memory usar?")
    print("1. SQLite")
    print("2. PostgreSQL")

    choice = input("Seleccione una opción (1 o 2): ").strip()

    if choice == "2":
        try:
            backend = PostgreSQLMemory()
            print("✅ Conectado a PostgreSQL")
        except ValueError as e:
            print(f"❌ {e}")
            print("Usando SQLite como respaldo...")
            backend = SqliteMemoryBackend()
    else:
        backend = SqliteMemoryBackend()
        print("✅ Conectado a SQLite")

    chatbot = build_chatbot(backend)
    run_chat_session(chatbot, backend, session_id="user_demo_001")
