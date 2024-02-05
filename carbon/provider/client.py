import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class CarbonClient:
    BASE_URL = "https://api.carbon.ai"
    DEFAULT_MEDIA_TYPE = "TEXT"
    DEFAULT_K = 100

    def __init__(self, api_key, customer_id, embedding_model, mappings):
        self.get_access_token_headers = {
            "authorization": f"Bearer {api_key}",
            "customer-id": str(customer_id),
        }
        self.embedding_model = embedding_model
        self.mappings = mappings

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

    def search(self, query, retry=True):
        url = f"{self.BASE_URL}/embeddings"
        payload = {
            "query": query,
            "media_type": self.DEFAULT_MEDIA_TYPE,
            "embedding_model": self.embedding_model,
            "k": self.DEFAULT_K,
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
        )

        if response.status_code != 200:
            # Unauthorized, retry fetching access token and search once
            if response.status_code == 401 and retry:
                self.get_access_token()
                return self.search(query, False)
            else:
                raise UpstreamProviderError(
                    f"Error during Carbon search with query: `{query}`."
                )

        return response.json().get("documents", [])


def get_client():
    global client

    if client is None:
        assert (api_key := app.config.get("API_KEY")), "CARBON_API_KEY must be set"
        assert (
            customer_id := app.config.get("CUSTOMER_ID")
        ), "CARBON_CUSTOMER_ID must be set"
        embedding_model = app.config.get("EMBEDDING_MODEL", "COHERE_MULTILINGUAL_V3")
        mappings = app.config.get("FIELDS_MAPPING", {})

        client = CarbonClient(api_key, customer_id, embedding_model, mappings)
        client.get_access_token()

    return client
