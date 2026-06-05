from helpers.ai_client import call_ai
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

console = Console()


def zero_shot():
    console.print(Rule("[bold yellow]Técnica Zero Shot"))
    zero_shot = call_ai(
        """
        Clasifica este email como URGENTE o NORMAL:
        contenido del email: 'El servidor de producción está caído, los clientes no pueden acceder'
        """
    )

    table = Table(title="Comparación")
    table.add_column("Técnica", style="cyan")
    table.add_column("Resultado", style="magenta")
    table.add_row("Zero Shot", zero_shot)
    console.print(table)
