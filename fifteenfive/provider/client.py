import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class FifteenFiveApiClient:
    def __init__(self, api_url, api_key, allowed_entities):
        self.api_url = api_url
        self.headers = {"Authorization": api_key}
        self.allowed_entities = allowed_entities

    def get_allowed_entities(self):
        return self.allowed_entities

    def get(self, url, params={}):
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def get_entities_by_type(self, entity_type):
        url = f"{self.api_url}/{entity_type}"
        return self.get(url)


def get_client():
    global client
    assert (api_url := app.config.get("API_URL")), "FIFTEENFIVE_API_URL must be set"
    assert (api_key := app.config.get("API_KEY")), "FIFTEENFIVE_API_KEY must be set"
    allowed_entities = app.config.get(
        "ALLOWED_ENTITIES",
        [
            "user",
            "vacation",
            "question",
            "answer",
            "pulse",
            "high-five",
            "objective",
            "review-cycle",
        ],
    )

    if not client:
        client = FifteenFiveApiClient(api_url, api_key, allowed_entities)
    return client
