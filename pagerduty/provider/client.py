import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class PagerdutySearchClient:
    base_url = "https://api.pagerduty.com"
    get_users_endpoint = "/users"
    get_teams_endpoint = "/teams"
    get_incidents_endpoint = "/incidents"

    def __init__(self, key, search_types):
        self.headers = {"Authorization": f"Token token={key}"}
        self.search_types = search_types

    def get_search_types(self):
        return self.search_types

    def _make_request(self, url, params={}):
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def search_incidents(self, query):
        url = f"{self.base_url}{self.get_incidents_endpoint}"
        params = {
            "limit": 100,
        }
        response = self._make_request(url, params)

        # GET Incidents does not have an in-built query feature, it only returns a list of incidents
        # Perform search locally on certain incident properties
        query = query.lower()
        keywords = query.split()
        search_properties = ["title", "description", "summary"]
        results = []
        for incident in response["incidents"]:
            for prop in search_properties:
                value = incident.get(prop, "").lower()

                if any(keyword in value for keyword in keywords):
                    results.append(incident)

        return results

    def search_users(self, query):
        url = f"{self.base_url}{self.get_users_endpoint}"
        params = {"query": query}
        response = self._make_request(url, params)

        return response["users"]

    def search_teams(self, query):
        url = f"{self.base_url}{self.get_teams_endpoint}"
        params = {"query": query}
        response = self._make_request(url, params)

        return response["teams"]


def get_client():
    global client
    assert (key := app.config.get("API_KEY")), "PAGERDUTY_API_KEY must be set"
    enabled_search_types = app.config.get("ENABLED_SEARCH_TYPES", ["incidents"])

    if not client:
        client = PagerdutySearchClient(key, enabled_search_types)

    return client
