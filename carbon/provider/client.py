import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class CarbonClient:
    BASE_URL = "https://api.carbon.ai"

    def __init__(self, api_key, customer_id):
        self.headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {api_key}",
            "customer-id": customer_id,
        }

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
        assert (api_key := app.config.get("API_KEY")), "CARBON_API_KEY must be set"
        assert (
            customer_id := app.config.get("CUSTOMER_ID")
        ), "CARBON_CUSTOMER_ID must be set"

        client = CarbonClient(api_key, customer_id)

    return client
