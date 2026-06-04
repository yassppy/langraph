from os import getenv

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

try:
    GEMINI_API_KEY = getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("No se encontró la variable GEMINI_API_KEY en el archivo .env")

    client = genai.Client(api_key=GEMINI_API_KEY)

    SYSTEM_PROMPT_BASIC = "Eres un asistente útil de ventas de la plataforma EDteam."
    SYSTEM_PROMPT_PROFESSIONALE = """
    ## ROL
    Eres un asesor de ventas experto para la plataforma EDteam, tu misión es ayudar al cliente a elegir un nuevo curso
    en base al nivel de conocimiento y línea de carrera.
    ## COMPORTAMIENTO
    - Responde en el idioma del usuario
    - Responde de manera clara y concisa: máximo 3 párrafos por respuesta.
    - Usa bullets cuando listes más de 2 items.
    - Haz preguntas para entender mejor al cliente antes de recomendar.
    - Si no tienes información suficiente para recomendar, haz preguntas para entender mejor al cliente.
    ## RESTRICCIONES
    - No compartas precios de competidores ni hables negativamente de ellos.
    - No prometas fechas de entrega de nuevos cursos.
    - Para problemas de pago o soporte técnico, redirige a: https://ayuda.ed.team o WhatsApp: +51942370443
    ## FORMATO DE RESPUESTA
    **Para el cliente [nombre si lo sabes]:**
    - 🎯 **Te recomiendo**: [curso/escuela/plan]
    - 💡 **Por qué**: [razón basada en su perfil]
    - 💰 **Inversión**: [precio y plan sugerido]
    - 🔗 **Empieza aquí**: ed.team/[ruta]
    ## CONTEXTO
    - Plataforma: EDteam (ed.team)
    - Versión del prompt: 2.0
    - Última actualización: 2025-06
    - Sede: Lima, Bogotá y Cochabamba
    """

    question = "¿Quiero formarme en data engineering que cursos me recomiendas?"

    for name, system in [
        ("amateur", SYSTEM_PROMPT_BASIC),
        ("profesional", SYSTEM_PROMPT_PROFESSIONALE),
    ]:
        print(f"\n{'=' * 50}")
        print(f"SYSTEM PROMPT: {name}")
        print("=" * 50)

        chat = client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(system_instruction=system),
        )
        response = chat.send_message(message=question)
        print(response.text)

except ValueError as e:
    print(f"Error: {e}")
