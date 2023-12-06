import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class CopperApiClient:
    API_BASE_URL = "https://api.copper.com"
    API_VERSION = "v1"
    API_APPLICATION = "developer_api"
    OPPORTUNITIES_SEARCH_ENDPOINT = "/opportunities/search"
    TASKS_SEARCH_ENDPOINT = "/tasks/search"

    def __init__(self, api_token, api_email, search_limit, mapping):
        self.headers = {
            "X-PW-AccessToken": api_token,
            "X-PW-Application": self.API_APPLICATION,
            "X-PW-UserEmail": api_email,
            "Content-Type": "application/json",
        }
        self.api_url = f"{self.API_BASE_URL}/{self.API_APPLICATION}/{self.API_VERSION}"
        self.search_limit = search_limit
        self.mapping = mapping

    def get_search_limit(self):
        return self.search_limit

    def get_mapping(self):
        return self.mapping

    def post(self, url, params={}):
        response = requests.post(url, headers=self.headers, json=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def _get_entities(self, entity_endpoint):
        url = f"{self.api_url}{entity_endpoint}"
        params = {"page_size": self.search_limit}
        return self.post(url, params)

    def get_opportunities(self):
        opportunities = self._get_entities(self.OPPORTUNITIES_SEARCH_ENDPOINT)
        return list(map(lambda d: {**d, "entity_type": "opportunity"}, opportunities))

    def get_tasks(self):
        tasks = self._get_entities(self.TASKS_SEARCH_ENDPOINT)
        return list(map(lambda d: {**d, "entity_type": "task"}, tasks))


def get_client():
    global client
    assert (api_token := app.config.get("API_TOKEN")), "COPPER_API_KEY must be set"
    assert (api_email := app.config.get("API_EMAIL")), "COPPER_API_EMAIL must be set"

    search_limit = app.config.get("SEARCH_LIMIT", 20)
    mapping = app.config.get("FIELDS_MAPPING", {})

    if not client:
        client = CopperApiClient(api_token, api_email, search_limit, mapping)

    return client
