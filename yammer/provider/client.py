import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class YammerApiClient:
    API_BASE_URL = "https://www.yammer.com/api/v1"
    SEARCH_ENDPOINT = "search.json"

    def __init__(self, api_token, search_limit):
        self.api_token = api_token
        self.search_limit = search_limit
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def get_search_limit(self):
        return self.search_limit

    def get(self, url, params={}):
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def search(self, query):
        url = f"{self.API_BASE_URL}/{self.SEARCH_ENDPOINT}"
        params = {"search": query, "num_per_page": self.get_search_limit()}

        return self.get(url, params)


def get_client():
    global client
    assert (api_token := app.config.get("API_TOKEN")), "YAMMER_API_TOKEN must be set"
    per_page = app.config.get("SEARCH_LIMIT", 20)

    if not client:
        client = YammerApiClient(api_token, per_page)

    return client
