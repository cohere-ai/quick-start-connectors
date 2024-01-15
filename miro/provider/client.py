import requests
from flask import current_app as app, request

from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "
DEFAULT_LIMIT = 20


class MiroClient:
    BASE_PATH = "https://api.miro.com/v2"
    BOARDS_ENDPOINT = "/boards"

    def __init__(self, access_token, limit):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
        }
        self.limit = limit

    def search(self, query):
        url = self.BASE_PATH + self.BOARDS_ENDPOINT
        params = {"query": query, "limit": self.limit}
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
        )
        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()["data"]


def get_client():
    access_token = app.config.get("ACCESS_TOKEN", get_access_token())
    limit = app.config.get("LIMIT", DEFAULT_LIMIT)
    if not access_token:
        raise UpstreamProviderError("No access token provided")
    client = MiroClient(access_token, limit)

    return client


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
