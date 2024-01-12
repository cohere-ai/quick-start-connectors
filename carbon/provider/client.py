import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class CarbonClient:
    BASE_URL = "https://api.carbon.ai"
    DEFAULT_MEDIA_TYPE = "TEXT"

    def __init__(self, api_key, customer_id, embedding_model):
        self.get_access_token_headers = {
            "authorization": f"Bearer {api_key}",
            "customer-id": str(customer_id),
        }
        self.embedding_model = embedding_model

    def get_access_token(self):
        get_token_url = f"{self.BASE_URL}/auth/v1/access_token"

        response = requests.get(get_token_url, headers=self.get_access_token_headers)

        if response.status_code != 200:
            message = (
                response.text
                or f"{response.status_code} response: Error generating access token, make sure your API key is valid."
            )
            raise UpstreamProviderError(message)

        self.headers = {
            "authorization": f"Token {response.json()['access_token']}",
        }

    def search(self, query):
        url = f"{self.BASE_URL}/embeddings"
        payload = {
            "query": query,
            "media_type": self.DEFAULT_MEDIA_TYPE,
            "embedding_model": self.embedding_model,
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
        )

        import pdb

        pdb.set_trace()

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
        client.get_access_token()

    return client
