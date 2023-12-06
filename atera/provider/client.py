import requests
import json
from . import UpstreamProviderError
from flask import current_app as app

client = None


class AteraClient:
    DEFAULT_SEARCH_LIMIT = 50
    BASE_URL = "https://app.atera.com/api/v3"

    def __init__(self, key):
        self.headers = {
            "X-API-KEY": key,
        }

    def search_tickets(self, query):
        url = f"{self.BASE_URL}/tickets"
        params = {
            "itemsInPage": self.DEFAULT_SEARCH_LIMIT,
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
        )

        if response.status_code != 200:
            raise UpstreamProviderError((f"Error fetching tickets."))

        # Perform search manually
        results = []
        for ticket in response.json()["items"]:
            text = ticket.get("TicketTitle", "") + ticket.get("FirstComment", "")
            if any(keyword in text for keyword in query.split()):
                results.append(ticket)

        return results


def get_client():
    assert (key := app.config.get("API_KEY")), "ATERA_API_KEY must be set"

    global client
    if client is not None:
        return client

    client = AteraClient(key)
    return client
