import base64

import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class AgoraApiClient:
    API_URL = "https://api.agora.io"
    PROJECTS_ENDPOINT = "/dev/v1/projects"

    def __init__(self, customer_id, customer_secret):
        self.credentials = f"{customer_id}:{customer_secret}"
        self.headers = {
            "Authorization": f"basic {self._base64_encode_creds()}",
            "Content-Type": "application/json",
        }

    def _base64_encode_creds(self):
        base64_encoded = base64.b64encode(self.credentials.encode("utf8"))
        return base64_encoded.decode("utf8")

    def get(self, url, params={}):
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def get_projects(self):
        url = f"{self.API_URL}{self.PROJECTS_ENDPOINT}"
        return self.get(url)


def get_client():
    global client
    assert (
        customer_id := app.config.get("CUSTOMER_ID")
    ), "AGORA_CUSTOMER_ID must be set"
    assert (
        customer_secret := app.config.get("CUSTOMER_SECRET")
    ), "AGORA_CUSTOMER_SECRET must be set"

    if not client:
        client = AgoraApiClient(customer_id, customer_secret)

    return client
