import json
from typing import Literal

from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, HumanMessage
from src.langchain_section.config.setting import setting
from src.langchain_section.core.llm import get_llm
from src.langchain_section.graphs.states import RAGAgentState


def node_analyze(state: RAGAgentState) -> dict:
    """Nodo que decide si la pregunta necesita buscar documentos"""
    llm = get_llm(temperature=0.1)

    recent_context = ""
    if state.get("messages") and len(state["messages"]) >= 2:
        last_two = state["messages"][-2:]
        recent_context = "\n".join(
            [
                f"{'Usuario' if message.type == 'human' else 'IA'}: {message.content[:150]}"
                for message in last_two
                if hasattr(message, "content") and message.content
            ]
        )

    prompt = f"""Analiza si esta pregunta necesita buscar en la base de conocimiento empresarial.
Contexto inmediato (últimos 2 mensajes):
{recent_context if recent_context else "Sin contexto previo"}
Pregunta actual: {state["question"]}
Responde ÚNICAMENTE con este JSON (sin markdown):
{{"needs_retrieval": true, "reason": "razón breve"}}
REGLAS ESTRICTAS:
needs_retrieval = true SIEMPRE que:
  - La pregunta pida información específica (políticas, procedimientos, datos)
  - Mencione documentos, manuales, contratos o información interna
  - Sea una pregunta factual sobre la empresa o sus procesos
  - Haya cualquier duda
needs_retrieval = false SOLO cuando sea OBVIO:
  - Saludos puros: "hola", "gracias", "adiós"
  - Aclaración de lo que la IA dijo en el mensaje inmediato anterior
En caso de duda: needs_retrieval = true"""

    result = llm.invoke([HumanMessage(content=prompt)])

    try:
        raw = result.content
        if isinstance(raw, str):
            content = raw
        elif isinstance(raw, list):
            first = raw[0]
            content = first if isinstance(first, str) else first["text"]
        else:
            content = str(raw)
        content = content.strip()
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        decision = json.loads(content.strip())
        needs_retrieval = decision.get("needs_retrieval", True)
        reason = decision.get("reason", "")

    except json.JSONDecodeError:
        needs_retrieval = True
        reason = "Error de parseo, buscando por defecto"

    print(f"[analyze] needs_retrieval={needs_retrieval} | {reason}")

    return {"needs_retrieval": needs_retrieval}


def node_retrieve(state: RAGAgentState, vectorstore: Chroma) -> dict:
    """Busca los chunks más relevantes en ChromaDB"""
    question = state["question"]
    # print(f" [retrieve] Buscando: '{state['question'][:60]}...'")
    query = question

    docs = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": setting.TOP_K_RESULTS}
    ).invoke(query)

    retrieve_texts = [doc.page_content for doc in docs]

    sources = [
        {
            "file": doc.metadata.get("file_name", "desconocida"),
            "page": doc.metadata.get("page", "N/A"),
        }
        for doc in docs
    ]

    print(f" [retrieve] {len(docs)} chunks encontrados")

    for src in sources:
        print(f" -> {src['file']} (pág. {src['page']})")

    return {"retrieve_docs": retrieve_texts, "sources": sources}


def node_generate(state: RAGAgentState) -> dict:
    """Genera la respuesta"""
    llm = get_llm(temperature=setting.LOW_TEMPERATURE)

    if state.get("retrieve_docs"):
        docs_text = "\n\n --- \n\n".join(state["retrieve_docs"])
        context_section = f"""INFORMACION DE LOS DOCUMENTOS EMPRESARIALES: {docs_text}
        INSTRUCCIÓN: Basa tu respuesta principalmente en estos documentos.
        Si la información no está aquí, dilo claramente.
        """

    else:
        context_section = (
            "No se encontraron documentos relevantes. Responde con conocimiento general"
        )

    history_text = ""
    if state.get("messages"):
        previous_msgs = state["messages"][:-1]
        recent_msgs = previous_msgs[-6:] if len(previous_msgs) > 6 else previous_msgs
        if recent_msgs:
            history_text = "\n".join(
                [
                    f"{'Usuario' if message.type == 'human' else 'Asistente'}: {message.content[:200]}"
                    for message in recent_msgs
                    if hasattr(message, "content") and message.content
                ]
            )

    prompt = f"""Eres un asistente de conocimiento empresarial experto.
{context_section}
HISTORIAL RECIENTE:
{history_text if history_text else "Inicio de conversación"}
PREGUNTA: {state["question"]}
INSTRUCCIONES:
- Si tienes documentos, úsalos como fuente principal
- Cita los documentos cuando sea relevante
- Si algo no está en los documentos, dilo honestamente
- Usa el historial solo para referencias contextuales
- Responde en español de forma clara y profesional"""

    result = llm.invoke([HumanMessage(content=prompt)])

    used_docs = "Con documentos" if state.get("retrieve_docs") else "Sin documentos"

    print(f" [generate] {used_docs} ({len(result.content)} chars)")

    return {"response": result.content, "messages": [AIMessage(content=result.content)]}


def decide_retrieval_path(state: RAGAgentState) -> Literal["retrieve", "generate"]:
    """Función de decisión"""
    if state.get("needs_retrieval", True):
        return "retrieve"
    return "generate"
