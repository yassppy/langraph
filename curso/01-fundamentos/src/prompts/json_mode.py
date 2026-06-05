import json

from helpers.ai_client import call_ai

PYTHON_SCHEMA = {
    "type": "object",
    "properties": {
        "language": {"type": "string"},
        "creation_year": {"type": "integer"},
        "creator": {"type": "string"},
        "principal_use": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["language", "creation_year", "creator", "principal_use"],
}


def run_json_mode():
    print("JSON Mode")
    print("=" * 40)

    response = call_ai(
        system="Responder siempre en formato de salida JSON válido",
        message="Dame información sobre el lenguaje Python.",
        response_json_schema=PYTHON_SCHEMA,
    )

    json_data = json.loads(response)
    print("JSON", json_data)
    print("Año de creación", json_data["creation_year"])
