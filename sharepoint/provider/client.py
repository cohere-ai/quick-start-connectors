from functools import lru_cache
from azure.identity import ClientSecretCredential
from flask import current_app as app
from msgraph.core import GraphClient, APIVersion
from urllib.parse import urlparse

from . import UpstreamProviderError
from .consts import CACHE_SIZE

client = None


class SharepointClient:
    DEFAULT_SCOPES = ["https://graph.microsoft.com/.default"]
    DEFAULT_REGION = "NAM"
    SEARCH_ENTITY_TYPES = ["driveItem", "listItem"]
    SEARCH_URL = "/search/query"
    SEARCH_LIMIT = 3

    graph_client = None

    def __init__(self, tenant_id, client_id, client_secret, search_limit=5):
        try:
            credential = ClientSecretCredential(
                tenant_id,
                client_id,
                client_secret,
            )

            self.graph_client = GraphClient(
                credential=credential,
                scopes=self.DEFAULT_SCOPES,
                api_version=APIVersion.beta,
            )
        except Exception as e:
            raise UpstreamProviderError(
                f"Error while initializing Sharepoint client: {str(e)}"
            )

        self.search_limit = search_limit

    @lru_cache(CACHE_SIZE)
    def search(self, query):
        search_response = self.graph_client.post(
            self.SEARCH_URL,
            json={
                "requests": [
                    {
                        "entityTypes": self.SEARCH_ENTITY_TYPES,
                        "query": {
                            "queryString": query,
                            "size": self.SEARCH_LIMIT,
                        },
                        "region": self.DEFAULT_REGION,
                    }
                ]
            },
        )

        if not search_response.ok:
            message = (
                search_response.json()
                .get("error", {})
                .get("message", "Error calling Microsoft Graph API")
            )
            raise UpstreamProviderError(message)

        return search_response.json()["value"][0]["hitsContainers"]

    @lru_cache(CACHE_SIZE)
    def get_pages(self, site_id):
        page_url = f"/sites/{site_id}/pages"
        response = self.graph_client.get(page_url)

        if not response.ok:
            return []

        return response.json()

    @lru_cache(CACHE_SIZE)
    def fetch_page(self, url):
        parsed_url = urlparse(url)
        site_id = parsed_url.netloc
        pages = self.get_pages(site_id)

        # Find page by path
        matching_page = None
        for page in pages["value"]:
            normalized_page_path = f"/{page['webUrl']}"
            if normalized_page_path == parsed_url.path:
                matching_page = page
                break

        return matching_page

    @lru_cache(CACHE_SIZE)
    def get_drive_item(self, parent_drive_id, resource_id):
        drive_item_url = f"/drives/{parent_drive_id}/items/{resource_id}/content"

        get_response = self.graph_client.get(drive_item_url)

        # Fail gracefully when retrieving content
        if not get_response.ok:
            return {}

        return get_response.content

    @lru_cache(CACHE_SIZE)
    def get_list_item(self, site_id, page_id):
        list_item_url = (
            f"/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage/webParts"
        )
        get_response = self.graph_client.get(list_item_url)

        # Fail gracefully when retrieving content
        if not get_response.ok:
            return {}

        return get_response.json()


def get_client():
    global client
    if client is not None:
        return client

    # Fetch environment variables
    assert (
        tenant_id := app.config.get("TENANT_ID")
    ), "SHAREPOINT_TENANT_ID must be set"
    assert (
        client_id := app.config.get("CLIENT_ID")
    ), "SHAREPOINT_CLIENT_ID must be set"
    assert (
        client_secret := app.config.get("CLIENT_SECRET")
    ), "SHAREPOINT_CLIENT_SECRET must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 5)

    client = SharepointClient(tenant_id, client_id, client_secret, search_limit)

    return client
