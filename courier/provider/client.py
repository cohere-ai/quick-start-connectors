import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class CourierClient:
    base_url = "https://api.courier.com"

    def __init__(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}

    def list_messages(self):
        url = f"{self.base_url}/messages"
        response = requests.get(
            url,
            headers=self.headers,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()["results"]

    def get_message_content(self, message_id):
        url = f"{self.base_url}/messages/{message_id}/output"
        response = requests.get(
            url,
            headers=self.headers,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        text_fields = ["subject", "text"]
        content_body = response.json()["results"][0]["content"]

        return {key: value for key, value in content_body.items() if key in text_fields}


def get_client():
    global client
    assert (token := app.config.get("API_TOKEN")), "COURIER_API_TOKEN must be set"
    if client is not None:
        return client

    client = CourierClient(token)
    return client
