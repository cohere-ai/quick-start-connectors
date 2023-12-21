import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class CarbonClient:
    BASE_URL = "https://api.carbon.ai"
    DEFAULT_MEDIA_TYPE = "TEXT"

    def __init__(self, api_key, customer_id, embedding_model):
        self.headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {api_key}",
            "customer-id": customer_id,
        }
        self.embedding_model = embedding_model

    def search_articles(self, query):
        url = f"{self.BASE_URL}/embeddings"
        data = {
            "query": query,
            "media_type": self.DEFAULT_MEDIA_TYPE,
            "embedding_model": self.embedding_model,
        }

        response = requests.post(
            url,
            headers=self.headers,
            data=data,
        )

        if response.status_code != 200:
            raise UpstreamProviderError(
                f"Error during Carbon search with query: `{query}`."
            )

        return response.json()


def get_client():
    global client

    if client is None:
        assert (api_key := app.config.get("API_KEY")), "CARBON_API_KEY must be set"
        assert (
            customer_id := app.config.get("CUSTOMER_ID")
        ), "CARBON_CUSTOMER_ID must be set"
        embedding_model = app.config.get("EMBEDDING_MODEL", "COHERE_MULTILINGUAL_V3")

        client = CarbonClient(api_key, customer_id, embedding_model)

    return client
