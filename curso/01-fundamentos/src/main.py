# from prompts.few_shot import few_shot
# from prompts.zero_shot import zero_shot
# from prompts.json_mode import run_json_mode
from prompts.function_calling import run_chat_with_tools
from prompts.new_prompt import extract_factura_data
from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    console.print(Panel.fit("[bold cyan]Técnicas de prompting\n"))
    # zero_shot()
    # few_shot()
    # run_json_mode()
    # extract_factura_data()
    print(run_chat_with_tools("¿Qué clima hace en Lima hoy?"))
    print(run_chat_with_tools("¿Cuánto es 2 + 2?"))  # sin tool

    console.print("\n[bold green]✔️ Ejecución completada")


if __name__ == "__main__":
    main()
