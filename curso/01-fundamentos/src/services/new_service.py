import requests


class NewService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/top-headlines?"

    def get_lastes_news(self) -> str:
        """Traer las últimas noticias"""
        params = {
            "category": "technology",
            "from": "2026-06-05&",
            "sortBy": "popularity",
            "apiKey": self.api_key,
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()

        if not data.get("articles"):
            return "No se encontraron noticias disponibles"
        article = data.get("articles")[0]
        return f"""
        {article.get("title")}
        {article.get("description")}
        """
