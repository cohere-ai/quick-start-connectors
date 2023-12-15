import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class CrunchbaseApiClient:
    API_URL = "https://api.crunchbase.com/api/v4/autocompletes"

    def __init__(self, api_key, search_limit):
        self.user_key = api_key
        self.search_limit = search_limit

    def get(self, params={}):
        response = requests.get(self.API_URL, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def autocomplete(self, term):
        # @see: https://data.crunchbase.com/docs/using-autocomplete-api
        params = {"query": term, "limit": self.search_limit, "user_key": self.user_key}
        return self.get(params)


def get_client():
    global client
    assert (api_key := app.config.get("API_KEY")), "CRUNCHBASE_API_KEY must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 20)

    if not client:
        client = CrunchbaseApiClient(api_key, search_limit)

    return client
