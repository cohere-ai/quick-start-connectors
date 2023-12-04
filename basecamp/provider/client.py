import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class BaseCampClient:
    API_URL = "https://3.basecampapi.com"
    API_PROJECTS_ENDPOINT = "projects.json"

    def __init__(self, api_token, account_id, search_entities, depth):
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.endpoint = f"{self.API_URL}/{account_id}/"
        self.search_entities = search_entities
        self.depth = depth

    def get_depth(self):
        return self.depth

    def get_search_entities(self):
        return self.search_entities

    def get(self, url, params={}):
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def get_projects(self):
        url = self.endpoint + self.API_PROJECTS_ENDPOINT
        return self.get(url)


def get_client():
    global client
    assert (
        account_id := app.config.get("ACCOUNT_ID")
    ), "BASECAMP_ACCOUNT_ID must be set"
    assert (
        access_token := app.config.get("ACCESS_TOKEN")
    ), "BASECAMP_ACCESS_TOKEN must be set"
    depth = app.config.get("VAULTS_DEPTH", 0)
    search_entities = app.config.get("PROJECT_SEARCH_ENTITIES", ["vault"])

    if not client:
        client = BaseCampClient(access_token, account_id, search_entities, depth)

    return client
