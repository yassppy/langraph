from google.genai import types
from helpers.ai_client import call_ai
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

console = Console()

FEW_SHOT_HISTORY = [
    types.Content(role="user", parts=[types.Part(text="Clasifica: 'Me encantó'")]),
    types.Content(role="model", parts=[types.Part(text="POSITIVO")]),
    types.Content(role="user", parts=[types.Part(text="Clasifica: 'Qué asco'")]),
    types.Content(role="model", parts=[types.Part(text="NEGATIVO")]),
    types.Content(
        role="user", parts=[types.Part(text="Clasifica: 'Está bien pero falta esto'")]
    ),
    types.Content(role="model", parts=[types.Part(text="NEUTRAL")]),
]


def few_shot():
    console.print(Rule("[bold yellow]Técnica Few Shot"))
    few_shot = call_ai(
        message="""
        Clasifica: 'Me encantó el producto pero la entrega tardó mucho'
        """,
        history=FEW_SHOT_HISTORY,
        system="""
        Eres un clasificador de comentarios. Solamente clasifica los comentarios como POSITIVO, NEGATIVO o NEUTRAL.
        """,
    )

    table = Table(title="Comparación")
    table.add_column("Técnica", style="cyan")
    table.add_column("Resultado", style="magenta")
    table.add_row("Few Shot", few_shot)
    console.print(table)
