import requests

from msal import ConfidentialClientApplication
from flask import current_app as app, request

from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class SharepointClient:
    DEFAULT_SCOPES = ["https://graph.microsoft.com/.default"]
    DEFAULT_REGION = "NAM"
    BASE_URL = "https://graph.microsoft.com/v1.0"
    SEARCH_ENTITY_TYPES = ["driveItem"]
    APPLICATION_AUTH = "application"
    DELEGATED_AUTH = "user"

    def __init__(self, auth_type, search_limit):
        self.access_token = None
        self.user = None
        self.auth_type = auth_type
        self.search_limit = search_limit

    def get_auth_type(self):
        return self.auth_type

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
                f"Error while initializing Teams client: {str(e)}"
            )

    def set_user_access_token(self, token):
        self.access_token = token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def search(self, query):
        response = requests.post(
            f"{self.BASE_URL}/search/query",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={
                "requests": [
                    {
                        "entityTypes": self.SEARCH_ENTITY_TYPES,
                        "region": self.DEFAULT_REGION,
                        "query": {
                            "queryString": query,
                            "size": self.search_limit,
                        },
                    }
                ]
            },
        )

        if not response.ok:
            raise UpstreamProviderError(
                f"Error while searching Sharepoint: {response.text}"
            )

        return response.json()["value"][0]["hitsContainers"]

    def get_drive_item_content(self, parent_drive_id, resource_id):
        response = requests.get(
            f"{self.BASE_URL}/drives/{parent_drive_id}/items/{resource_id}/content",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        # Fail gracefully when retrieving content
        if not response.ok:
            return {}

        return response.content


def get_client():
    assert (
        auth_type := app.config.get("AUTH_TYPE")
    ), "SHAREPOINT_AUTH_TYPE must be set"

    search_limit = app.config.get("SEARCH_LIMIT", 5)
    client = SharepointClient(auth_type, search_limit)

    if auth_type == client.APPLICATION_AUTH:
        assert (
            tenant_id := app.config.get("TENANT_ID")
        ), "SHAREPOINT_TENANT_ID must be set"
        assert (
            client_id := app.config.get("CLIENT_ID")
        ), "SHAREPOINT_CLIENT_ID must be set"
        assert (
            client_secret := app.config.get("CLIENT_SECRET")
        ), "SHAREPOINT_CLIENT_SECRET must be set"
        client.set_app_access_token(tenant_id, client_id, client_secret)
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
