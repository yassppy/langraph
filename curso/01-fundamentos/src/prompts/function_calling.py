import json

from google.genai import types
from helpers.ai_client import call_ai

TOOLS = TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_weather",
                description="Obtener el clima de una ciudad. Usar cuando el usuario pregunta por el tiempo o clima.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "city": types.Schema(
                            type=types.Type.STRING,
                            description="Nombre de la ciudad, ejemplo: 'Madrid', 'Lima', 'London'",
                        ),
                        "unit": types.Schema(
                            type=types.Type.STRING,
                            description="Unidad de temperatura: celsius o fahrenheit",
                        ),
                    },
                    required=["city"],
                ),
            )
        ]
    )
]


def get_weather(city: str, unit: str = "celsius") -> dict:
    """Función real que simula obtener el clima"""
    simulated_data = {
        "madrid": {"temperature": 18, "wind_speed": 10.2},
        "mexico city": {"temperature": 22, "wind_speed": 1.0},
        "london": {"temperature": 12, "wind_speed": 2.0},
        "lima": {"temperature": 19, "wind_speed": 3.5},
    }
    data = simulated_data.get(city.lower(), {"temperature": 20, "wind_speed": 1.0})
    temp = data["temperature"]
    if unit == "fahrenheit":
        temp = (temp * 9 / 5) + 32
    return {
        "city": city,
        "temperature": f"{temp}°{'C' if unit == 'celsius' else 'F'}",
        "wind_speed": f"{data['wind_speed']} km/h",
    }


AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather,
}


def execute_tool(name: str, arguments: dict) -> str:
    """Ejecuta la función y devuelve el resultado como string JSON"""
    if name not in AVAILABLE_FUNCTIONS:
        return json.dumps({"error": f"Función no encontrada: {name}"})
    result = AVAILABLE_FUNCTIONS[name](**arguments)
    return json.dumps(result, ensure_ascii=False)


def run_chat_with_tools(user_message: str) -> str:
    # 1 Primera llamada — el modelo decide si usar una tool
    response = call_ai(
        message=user_message,
        system="Eres un asistente útil que puede usar herramientas para responder preguntas.",
        tools=TOOLS,
    )

    part = response.candidates[0].content.parts[0]

    # 2 El modelo pidió usar una función
    if part.function_call:
        fn_name = part.function_call.name
        fn_args = dict(part.function_call.args)

        print(f"🔧 Llamando función: {fn_name}({fn_args})")
        tool_result = execute_tool(fn_name, fn_args)
        print(f"📦 Resultado: {tool_result}")

        # 3 Segunda llamada — le devolvemos el resultado al modelo
        response2 = call_ai(
            message=user_message,
            system="Eres un asistente útil que puede usar herramientas para responder preguntas.",
            tools=TOOLS,
            history=[
                types.Content(role="user", parts=[types.Part(text=user_message)]),
                types.Content(role="model", parts=[part]),
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=fn_name, response=json.loads(tool_result)
                            )
                        )
                    ],
                ),
            ],
        )
        return response2.text

    # El modelo respondió directo sin usar tools
    return part.text
