import requests
from flask import current_app as app

from . import UpstreamProviderError


class FreshdeskClient:
    def __init__(self, api_key, domain, parameter):
        self.base_url = f"https://{domain}/api/v2"
        # Freshdesk uses Basic Auth with this specific format, using the API key
        self.basic_auth = (api_key, "X")
        self.ticket_parameter = parameter

    def search(self, query):
        search_url = f"{self.base_url}/search/tickets"
        params = {"query": f'"{self.ticket_parameter}:{query}"'}

        response = requests.get(search_url, auth=self.basic_auth, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()["results"]


def get_client():
    assert (api_key := app.config.get("API_KEY")), "FRESHDESK_API_KEY must be set"
    assert (
        domain := app.config.get("DOMAIN_NAME")
    ), "FRESHDESK_DOMAIN_NAME must be set"
    assert (
        parameter := app.config.get("TICKET_PARAMETER")
    ), "FRESHDESK_TICKET_PARAMETER must be set"

    return FreshdeskClient(api_key, domain, parameter)