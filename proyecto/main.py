from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict

## Configuración con LM Studio
llm = ChatOpenAI(
    base_url= "http://localhost:1234/v1",
    api_key="lm-studio",
    model="qwen2.5-0.5b-instruct"
)

## Nodo
class State(TypedDict):
    mensaje: str
    respuesta: str

def agente(state: State):
    respuesta = llm.invoke(state["mensaje"])
    return {"respuesta":respuesta.content}

## Grafo

grafo = StateGraph(State)
grafo.add_node("agente",agente)
grafo.set_entry_point("agente")
grafo.add_edge("agente",END)

app = grafo.compile()

resultado = app.invoke({"mensaje":"Dime la fecha actual"})
print(resultado["respuesta"])