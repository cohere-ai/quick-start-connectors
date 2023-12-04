import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class FreshserviceClient:
    def __init__(self):
        assert (domain := app.config.get("DOMAIN")), "FRESHSERVICE_DOMAIN must be set"
        assert (key := app.config.get("API_KEY")), "FRESHSERVICE_API_KEY must be set"

        self.base_url = f"{domain}/api/v2"
        # Freshservice uses Basic Auth with (<api key>, "X") as user, pass
        self.auth = (key, "X")

    def _make_request(self, method, url, params={}, data={}):
        response = requests.request(
            method,
            url,
            auth=self.auth,
            params=params,
            json=data,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def search_tickets(self, query):
        url = f"{self.base_url}/tickets"
        response = self._make_request("GET", url, {}, {})
        tickets = response["tickets"]

        # Perform search manually
        results = []
        for ticket in tickets:
            text = ticket.get("subject", "") + ticket.get("description_text", "")

            if query.lower() in text.lower():
                results.append(ticket)

        return results


def get_client():
    global client
    if client is not None:
        return client

    client = FreshserviceClient()
    return client
