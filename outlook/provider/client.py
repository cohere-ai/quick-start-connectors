import requests
from flask import current_app as app, request
from msal import ConfidentialClientApplication

from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class OutlookClient:
    DEFAULT_SCOPES = ["https://graph.microsoft.com/.default"]
    SEARCH_URL = "https://graph.microsoft.com/v1.0/search/query"
    APPLICATION_AUTH = "application"
    DELEGATED_AUTH = "user"

    def __init__(self, auth_type, search_limit=5):
        self.access_token = None
        self.user = None
        self.auth_type = auth_type
        self.search_limit = search_limit

    def set_user(self, user):
        self.user = user

    def set_app_access_token(self, tenant_id, client_id, client_secret):
        try:
            credential = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=f"https://login.microsoftonline.com/{tenant_id}",
            )

            token_response = credential.acquire_token_for_client(
                scopes=self.DEFAULT_SCOPES,
            )
            if "access_token" not in token_response:
                raise UpstreamProviderError(
                    "Error while retrieving access token from Microsoft Graph API"
                )
            self.access_token = token_response["access_token"]
        except Exception as e:
            raise UpstreamProviderError(
                f"Error while initializing Outlook client: {str(e)}"
            )

    def set_user_access_token(self, token):
        self.access_token = token

    def _app_search(self, query, user):
        results = []

        graph_api_url = f"https://graph.microsoft.com/v1.0/users/{user}/messages"

        # Set up the request headers
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        params = {
            "$search": f'"{query}"',
            "$select": "id,subject,bodyPreview,body,from,receivedDateTime,webLink,toRecipients,hasAttachments",
            "$top": self.search_limit,
        }
        # Make a request to the Microsoft Graph API to get messages
        response = requests.get(graph_api_url, headers=headers, params=params)
        if not response.ok:
            raise UpstreamProviderError(
                f"Error while searching Outlook: {response.text}"
            )
        data = response.json()
        if "value" in data:
            results.extend(data["value"])

        return results

    def _get_messages(self, hit):
        params = {
            "$filter": f"internetMessageId eq '{hit['resource']['internetMessageId']}'",
            "$select": "id,subject,bodyPreview,body,from,receivedDateTime,webLink,toRecipients,hasAttachments",
        }
        body_response = requests.get(
            url=f"https://graph.microsoft.com/v1.0/me/messages",
            params=params,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if body_response.ok:
            return body_response.json()["value"]
        return None

    def _user_search(self, query):
        results = []
        response = requests.post(
            self.SEARCH_URL,
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={
                "requests": [
                    {
                        "entityTypes": ["message"],
                        "query": {"queryString": query},
                        "from": 0,
                        "size": self.search_limit,
                    }
                ]
            },
        )
        if not response.ok:
            raise UpstreamProviderError(
                f"Error while searching Outlook: {response.text}"
            )
        for hit_container in response.json()["value"][0]["hitsContainers"]:
            if hit_container["total"]:
                for hit in hit_container["hits"]:
                    if hit["resource"]["@odata.type"] == "#microsoft.graph.message":
                        matching_messages = self._get_messages(hit)
                        if matching_messages is not None:
                            results.extend(matching_messages)

        return results

    def search(self, query):
        if self.access_token is None:
            raise UpstreamProviderError("Access token not set")
        if self.auth_type == self.APPLICATION_AUTH:
            results = self._app_search(query, self.user)
        elif self.auth_type == self.DELEGATED_AUTH:
            results = self._user_search(query)
        else:
            raise UpstreamProviderError(f"Invalid auth type: {self.auth_type}")
        return results


def get_client():
    assert (
        auth_type := app.config.get("GRAPH_AUTH_TYPE")
    ), "OUTLOOK_GRAPH_AUTH_TYPE must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 10)
    client = OutlookClient(auth_type, search_limit)
    if auth_type == client.APPLICATION_AUTH:
        assert (
            tenant_id := app.config.get("GRAPH_TENANT_ID")
        ), "OUTLOOK_GRAPH_TENANT_ID must be set"
        assert (
            client_id := app.config.get("GRAPH_CLIENT_ID")
        ), "OUTLOOK_GRAPH_CLIENT_ID must be set"
        assert (
            client_secret := app.config.get("GRAPH_CLIENT_SECRET")
        ), "OUTLOOK_GRAPH_CLIENT_SECRET must be set"
        assert (user := app.config.get("USER_ID")), "OUTLOOK_USER_ID must be set"
        client.set_app_access_token(tenant_id, client_id, client_secret)
        client.set_user(user)
    elif auth_type == client.DELEGATED_AUTH:
        token = get_access_token()
        if token is None:
            raise UpstreamProviderError("No access token provided in request")
        client.set_user_access_token(token)
    else:
        raise UpstreamProviderError(f"Invalid auth type: {auth_type}")
    return client


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
