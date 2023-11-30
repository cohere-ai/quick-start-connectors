import requests
import json
from . import UpstreamProviderError
from flask import current_app as app

client = None


class NotionSearchClient:
    base_url = "https://api.notion.com/v1"
    notion_version = "2022-02-22"

    def __init__(self, key):
        self.headers = {
            "Authorization": f"Bearer {key}",
            "Notion-Version": self.notion_version,
        }

    def _make_request(self, method, url, params={}, data={}):
        response = requests.request(
            method,
            url,
            headers=self.headers,
            params=params,
            data=json.dumps(data),
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def retrieve_child_blocks(self, block_id):
        url = f"{self.base_url}/blocks/{block_id}/children"
        response = self._make_request("GET", url)

        return response["results"]

    def search_documents(self, query):
        url = f"{self.base_url}/search"
        data = {"query": query}
        response = self._make_request("POST", url, {}, data)

        return response["results"]


def get_client():
    global client
    if client is not None:
        return client

    assert (token := app.config.get("API_TOKEN")), "NOTION_API_TOKEN must be set"
    client = NotionSearchClient(token)
    return client
