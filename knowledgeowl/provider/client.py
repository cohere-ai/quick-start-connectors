import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class KnowledgeOwlClient:
    base_url = "https://app.knowledgeowl.com/api"
    article_base_url = "https://app.knowledgeowl.com/kb/article/id"

    def __init__(self, api_key):
        self.auth = (api_key, "X")

    def search_articles(self, query):
        url = f"{self.base_url}/head/article.json"
        data = {
            "name": {
                "$regex": query,
                "$option": "i",
            }
        }

        response = requests.get(
            url,
            auth=self.auth,
            data=data,
        )

        if response.status_code != 200:
            raise UpstreamProviderError(
                f"Error querying articles with query: `{query}`."
            )

        return response.json()["data"]


def get_client():
    global client

    if client is None:
        assert (
            api_key := app.config.get("API_KEY")
        ), "KNOWLEDGEOWL_API_KEY must be set"
        client = KnowledgeOwlClient(api_key)

    return client
