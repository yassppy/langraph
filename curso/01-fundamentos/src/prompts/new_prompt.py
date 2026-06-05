import json
import os

from dotenv import load_dotenv
from helpers.ai_client import call_ai
from services.new_service import NewService

load_dotenv()

new_service = NewService(os.getenv("NEWS_API_KEY"))
news = new_service.get_lastes_news()

FACTURA_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "company": {
            "type": "string",
        },
        "top_news": {
            "type": "string",
        },
        "date": {
            "type": "string",
        },
    },
}


def extract_factura_data():
    response = call_ai(
        message=news,
        system="""Eres un extractor de noticias y vas a devolver en un JSON válido""",
        response_json_schema=FACTURA_JSON_SCHEMA,
    )
    extract_data = json.loads(response)
    for key, value in extract_data.items():
        print(f"{key}: {value}")
