import time

import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class ReutersClient:
    # Constants
    TOKEN_ENDPOINT = "https://auth.thomsonreuters.com/oauth/token"
    GRAPHQL_ENDPOINT = "https://api.reutersconnect.com/content/graphql"
    GRANT_TYPE = "client_credentials"
    DEFAULT_SCOPE = "https://api.thomsonreuters.com/auth/reutersconnect.contentapi.read"

    token = None
    expires_at = time.time()

    def __init__(self, client_id, client_secret, audience):
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience

    def _build_auth_headers(self):
        # If Token does not exist, or has expired, fetch again
        if not self.token or time.time() > self.expires_at:
            self.fetch_token()

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        return headers

    def _build_query(self, query):
        or_operator = " OR "
        words = query.split(" ")

        if len(words) == 1:
            return query

        return f"({or_operator.join(words)})"

    def fetch_token(self):
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.GRANT_TYPE,
            "audience": self.audience,
            "scope": self.DEFAULT_SCOPE,
        }

        response = requests.post(
            self.TOKEN_ENDPOINT,
            data=body,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        token_data = response.json()

        # Update token and expiry
        self.token = token_data["access_token"]
        self.expires_at = time.time() + token_data["expires_in"]

    def search(self, query):
        headers = self._build_auth_headers()
        graphql = """
            query ($query: String!) {
                search(query: $query) {
                    items {
                        intro 
                        language 
                        slug 
                        type 
                        firstCreated 
                        headLine 
                        fragment 
                        urgency 
                        headLine 
                        versionedGuid 
                        uri 
                        profile 
                        version
                        credit
                        sortTimestamp
                        contentTimestamp
                        productLabel
                    } 
                }
            }
        """

        response = requests.post(
            self.GRAPHQL_ENDPOINT,
            headers=headers,
            json={
                "query": graphql,
                "variables": {"query": f"fulltext:{self._build_query(query)}"},
            },
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()["data"]["search"]["items"]


def get_client():
    global client
    assert (client_id := app.config.get("CLIENT_ID")), "REUTERS_CLIENT_ID must be set"
    assert (
        client_secret := app.config.get("CLIENT_SECRET")
    ), "REUTERS_CLIENT_SECRET must be set"
    assert (audience := app.config.get("AUDIENCE")), "REUTERS_AUDIENCE must be set"

    if not client:
        client = ReutersClient(client_id, client_secret, audience)

    return client
