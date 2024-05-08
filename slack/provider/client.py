import logging

from flask import request, current_app as app
from slack_sdk import WebClient

logger = logging.getLogger(__name__)

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class SlackClient:
    def __init__(self, api_token, search_limit=20):
        self.client = WebClient(token=api_token)
        self.search_limit = search_limit

    def search_all(self, query):
        return self.client.search_all(query=query, count=self.search_limit)


def get_client():
    api_key = str(app.config.get("CONNECTOR_API_KEY", ""))
    api_token = None
    if api_key == "":
        api_token = get_access_token()
    if api_token is None:
        assert (
            api_token := app.config.get("OAUTH_ACCESS_TOKEN")
        ), "SLACK_OAUTH_ACCESS_TOKEN must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 20)
    client = SlackClient(api_token, search_limit)

    return client


def get_access_token() -> str | None:
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
