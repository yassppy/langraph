from os import getenv
from typing import Any, Optional  # 👈 agrega Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=getenv("GEMINI_API_KEY"))


def call_ai(
    message: str,
    temperature: float = 0.1,
    history: Optional[list] = None,
    system: Optional[str] = None,
    response_json_schema: Optional[dict] = None,
    tools: Optional[list] = None,
) -> Any:  # 👈 Any con mayúscula
    """Ejecutar el cliente de IA"""
    config_params: dict = {"temperature": temperature}

    if system:
        config_params["system_instruction"] = system
    if response_json_schema:
        config_params["response_mime_type"] = "application/json"
        config_params["response_schema"] = response_json_schema
    if tools:
        config_params["tools"] = tools

    chat = client.chats.create(
        model="gemini-flash-lite-latest",
        config=types.GenerateContentConfig(**config_params),
        history=history or [],
    )
    response = chat.send_message(message=message)
    if tools:
        return response
    return response.text
