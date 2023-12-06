from typing import Any

import requests
from flask import current_app as app

from .provider import UpstreamProviderError

client = None


class HelpScoutClient:
    """
    A client for the HelpScout API.
    """

    BASE_PATH = "https://api.helpscout.net"
    API_VERSION = "v2"
    OAUTH_TOKEN_END_POINT = "oauth2/token"
    CONVERSATION_END_POINT = "conversations"

    def __init__(self, app_id: str, app_secret: str, search_fields: str) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.search_fields = search_fields

    def _get_access_token(self) -> str:
        url = f"{self.BASE_PATH}/{self.API_VERSION}/{self.OAUTH_TOKEN_END_POINT}"
        response = requests.post(
            url,
            data={
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "grant_type": "client_credentials",
            },
        )
        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)
        return response.json()["access_token"]

    def _prepare_query(self, query) -> str:
        result_query = ""
        if self.search_fields and query:
            query_params = []
            for field in self.search_fields.split(","):
                for keyword in query.split():
                    query_params.append(f'{field}:"{keyword}"')
            if query_params:
                result_query = " OR ".join(query_params)
                result_query = f"({result_query})"
        return result_query

    def get_conversations(self, query) -> list[dict[str, Any]]:
        query = self._prepare_query(query)
        url = f"{self.BASE_PATH}/{self.API_VERSION}/{self.CONVERSATION_END_POINT}"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {self._get_access_token()}",
            },
            params={
                "query": query,
            },
        )
        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)
        return response.json()


def get_client():
    global client
    assert (app_id := app.config.get("APP_ID")), "HELPSCOUT_APP_ID must be set"
    assert (
        app_secret := app.config.get("APP_SECRET")
    ), "HELPSCOUT_APP_SECRET must be set"
    search_fields = app.config.get("SEARCH_FIELDS", "subject,body")
    if client is not None:
        return client

    client = HelpScoutClient(app_id, app_secret, search_fields)
    return client
