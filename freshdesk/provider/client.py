import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class FreshdeskClient:
    DEFAULT_TICKET_PARAMETERS = ["tag"]

    def __init__(self, api_key, domain, parameters=None):
        self.base_url = f"https://{domain}/api/v2"
        # Freshdesk uses Basic Auth with this specific format, using the API key
        # See: https://developers.freshdesk.com/api/#authentication
        self.basic_auth = (api_key, "X")

        if not parameters or parameters == "":
            parameters = self.DEFAULT_TICKET_PARAMETERS

        self.parameters = parameters

    def build_ticket_query(self, query):
        """
        Future-proofs ticket queries to allow for multiple field searches, including custom ones.
        Joins all search fields from `TICKET_PARAMETERS` with OR conditions.
        """
        queries = [f"{param}:{query}" for param in self.parameters]
        joined = " OR ".join(queries)

        return f'"{joined}"'

    def search(self, query):
        search_url = f"{self.base_url}/search/tickets"
        params = {"query": self.build_ticket_query(query)}

        response = requests.get(search_url, auth=self.basic_auth, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()["results"]


def get_client():
    global client

    if client is None:
        assert (api_key := app.config.get("API_KEY")), "FRESHDESK_API_KEY must be set"
        assert (
            domain := app.config.get("DOMAIN_NAME")
        ), "FRESHDESK_DOMAIN_NAME must be set"
        parameters = app.config.get("TICKET_PARAMETERS")

        client = FreshdeskClient(api_key, domain, parameters)

    return client
