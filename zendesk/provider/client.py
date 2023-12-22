import base64
import requests
from flask import current_app as app

from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "
DEFAULT_LIMIT = 20

client = None


class ZendeskClient:
    def __init__(self, email, domain, access_token, limit):
        credentials = f"{email}/token:{access_token}"
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}"
        }
        self.search_url = f"https://{domain}/api/v2/search.json"
        self.limit = limit

    def search(self, query):
        params = {"query": query, "per_page": self.limit}
        response = requests.get(self.search_url, params=params, headers=self.headers)
        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json().get("results", [])


def get_client():
    global client
    if client is None:
        assert (email := app.config.get("EMAIL")), "ZENDESK_EMAIL must be set"
        assert (domain := app.config.get("DOMAIN")), "ZENDESK_DOMAIN must be set"
        assert (token := app.config.get("API_TOKEN")), "ZENDESK_API_TOKEN must be set"
        limit = app.config.get("SEARCH_LIMIT", DEFAULT_LIMIT)

        client = ZendeskClient(email, domain, token, limit)

    return client
