import requests
from flask import current_app as app, request
from . import UpstreamProviderError

DEFAULT_LIMIT = {}
AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class YextClient:
    SEARCH_ENDPOINT = "/v2/accounts/me/search/query"

    def __init__(
        self,
        api_url,
        auth_type,
        api_key,
        version,
        account_id,
        locale,
        restrict_verticals,
        search_limit,
        mapping,
        experience_key,
        v,
    ):
        self.search_url = f"{api_url}{self.SEARCH_ENDPOINT}"
        self.auth_type = auth_type
        self.api_key = api_key
        self.version = version
        self.account_id = account_id
        self.restrict_verticals = restrict_verticals
        self.locale = locale
        self.search_limit = search_limit
        self.mapping = mapping
        self.experience_key = experience_key
        self.v = v

    def search(self, query):
        params = {
            "account_id": self.account_id,
            "experienceKey": self.experience_key,
            "input": query,
            "limit": self.search_limit,
            "locale": self.locale,
            "version": self.version,
            "v": self.v,
        }
        if self.restrict_verticals is not None:
            params["restrictVerticals"] = self.restrict_verticals
        if self.auth_type == "api_key":
            params["api_key"] = self.api_key
        elif self.auth_type == "oauth":
            params["access_token"] = self.api_key

        response = requests.get(
            self.search_url,
            params=params,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        data = response.json()
        if data["meta"]["errors"]:
            raise UpstreamProviderError(str(data["meta"]["errors"]))

        if "response" not in data:
            return []

        return data["response"]["modules"]


def get_client():
    assert (auth_type := app.config.get("AUTH_TYPE")), "YEXT_AUTH_TYPE must be set"
    if auth_type == "api_key":
        assert (api_key := app.config.get("API_KEY")), "YEXT_API_KEY must be set"
    elif auth_type == "oauth":
        auth_token = get_access_token()
        if auth_token is None:
            raise UpstreamProviderError("No oauth access token found")
    else:
        raise UpstreamProviderError(f"Unknown auth type: {auth_type}")

    assert (api_url := app.config.get("API_URL")), "YEXT_API_URL must be set"
    assert (account_id := app.config.get("ACCOUNT_ID")), "YEXT_ACCOUNT_ID must be set"
    assert (locale := app.config.get("LOCALE")), "YEXT_LOCALE must be set"
    assert (
        experience_key := app.config.get("EXPERIENCE_KEY")
    ), "YEXT_EXPERIENCE_KEY must be set"
    assert (v := app.config.get("V")), "YEXT_V must be set"
    restrict_verticals = app.config.get("RESTRICT_VERTICALS", None)
    search_limit = app.config.get("LIMIT", DEFAULT_LIMIT)
    version = app.config.get("VERSION", "PRODUCTION")
    mapping = app.config.get("FIELDS_MAPPING", {})
    client = YextClient(
        api_url,
        auth_type,
        api_key if auth_type == "api_key" else auth_token,
        version,
        account_id,
        locale,
        restrict_verticals,
        search_limit,
        mapping,
        experience_key,
        v,
    )

    return client


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
