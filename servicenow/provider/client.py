import requests
from flask import current_app as app, request
from urllib.parse import urljoin
from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class ServiceNowClient:
    SEARCH_ENDPOINT = "/api/now/table/{table_name}"
    DEFAULT_FIELDS_MAPPING = {}
    DEFAULT_SEARCH_LIMIT = 10

    def __init__(
        self,
        auth_type,
        base_url,
        table_name,
        user_name=None,
        password=None,
        access_token=None,
        fields_mapping=None,
        search_limit=None,
    ):
        self.auth_type = auth_type
        self.base_url = base_url
        self.fields_mapping = fields_mapping or self.DEFAULT_FIELDS_MAPPING
        self.search_limit = search_limit or self.DEFAULT_SEARCH_LIMIT
        self.table_name = table_name
        self.user_name = user_name
        self.password = password
        self.access_token = access_token
        self.search_url = urljoin(
            base_url, self.SEARCH_ENDPOINT.format(table_name=table_name)
        )
        self.headers = {
            "Authorization": f"{BEARER_PREFIX} {self.access_token}",
        }

    def search(self, query):
        params = {
            "sysparm_display_value": True,
            "sysparm_limit": self.search_limit,
            "sysparm_query": f"GOTO123TEXTQUERY321={query}",
        }
        if self.auth_type == "oauth":
            response = requests.get(
                self.search_url, headers=self.headers, params=params
            )
        elif self.auth_type == "basic":
            auth = (self.user_name, self.password)
            response = requests.get(self.search_url, auth=auth, params=params)

        if response.status_code != 200:
            raise UpstreamProviderError(f"Failed to query ServiceNow: {response.text}")

        return response.json()["result"]


def get_client():
    assert (
        auth_type := app.config.get("AUTH_TYPE")
    ), "SERVICENOW_AUTH_TYPE must be set"
    user_name = password = access_token = None
    if auth_type == "basic":
        assert (
            user_name := app.config.get("USERNAME")
        ), "SERVICENOW_USERNAME must be set"
        assert (
            password := app.config.get("PASSWORD")
        ), "SERVICENOW_PASSWORD must be set"
    elif auth_type == "oauth":
        access_token = get_access_token()
        if access_token is None:
            raise UpstreamProviderError("No oauth access token found")
    else:
        raise UpstreamProviderError(f"Unknown auth type: {auth_type}")

    assert (
        base_url := app.config.get("INSTANCE_URL")
    ), "SERVICENOW_INSTANCE_URL must be set"
    assert (
        table_name := app.config.get("TABLE_NAME")
    ), "SERVICENOW_TABLE_NAME must be set"
    search_limit = app.config.get("SEARCH_LIMIT", None)
    fields_mapping = app.config.get("FIELDS_MAPPING", None)
    client = ServiceNowClient(
        auth_type,
        base_url,
        table_name,
        user_name,
        password,
        access_token,
        fields_mapping,
        search_limit,
    )

    return client


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
