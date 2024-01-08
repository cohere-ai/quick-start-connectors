import requests
from flask import current_app as app
from functools import lru_cache

from . import UpstreamProviderError

CACHE_SIZE = 256

client = None


class HackerNewsClient:
    BASE_URL = "https://hn.algolia.com/api/v1"

    def __init__(self, search_limit):
        self.search_limit = search_limit

    @lru_cache(maxsize=CACHE_SIZE)
    def search(self, query):
        url = f"{self.BASE_URL}/search"
        params = {
            "query": query,
            "hitsPerPage": self.search_limit,
        }
        response = requests.get(
            url,
            params=params,
        )

        if response.status_code != 200:
            raise UpstreamProviderError(
                f"Error searching HackerNews with query: `{query}`."
            )

        return response.json()["hits"]

    @lru_cache(maxsize=CACHE_SIZE)
    def get_item(self, item_id):
        url = f"{self.BASE_URL}/items/{item_id}"
        response = requests.get(
            url,
        )

        if response.status_code != 200:
            return {}

        return response.json()


def get_client():
    global client
    search_limit = app.config.get("SEARCH_LIMIT", 5)
    if client is not None:
        return client

    client = HackerNewsClient(search_limit)
    return client
