import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class WikipediaClient:
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    BASE_ARTICLE_URL = "https://en.wikipedia.org/?curid="

    def __init__(self, search_limit):
        self.SEARCH_LIMIT = search_limit

    def search_articles(self, query):
        url = self.BASE_URL
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srlimit": self.SEARCH_LIMIT,
            "srsearch": query,
        }

        response = requests.get(
            url,
            params=params,
        )

        if response.status_code != 200:
            raise UpstreamProviderError(
                f"Error searching articles with query: `{query}`."
            )

        return response.json()["query"]["search"]


def get_client():
    global client
    if client is not None:
        return client
    search_limit = app.config.get("SEARCH_LIMIT", 10)
    client = WikipediaClient(search_limit)
    return client
