from atlassian import Jira
import requests
from flask import current_app as app, request
from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class JiraClient:
    JIRA_API_URL = "https://api.atlassian.com/ex/jira/"
    JIRA_RESOURCE_URL = "https://api.atlassian.com/oauth/token/accessible-resources"
    DEFAULT_SEARCH_LIMIT = 10

    def __init__(self):
        self.client = None
        self.limit = self.DEFAULT_SEARCH_LIMIT

    def set_limit(self, limit):
        self.limit = limit

    def search(self, query):
        issues = self.client.jql(
            'text ~ "' + query + '"',
            limit=self.limit,
        )["issues"]

        return issues

    def construct_api_request_url(self, token):
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(self.JIRA_RESOURCE_URL, headers=headers)
        if response.status_code != 200:
            raise UpstreamProviderError(
                f"Error while fetching Jira API URL: {response.status_code} {response.reason}"
            )
        data = response.json()
        if not data:
            raise UpstreamProviderError(
                f"Error while fetching Jira API URL: no data found"
            )
        resources = data[0]
        cloud_id = resources["id"] if "id" in resources else None
        return f"{self.JIRA_API_URL}{cloud_id}"

    def setup_oauth_client(self, client_id, token):
        if not token:
            raise UpstreamProviderError(
                f"Error while initializing Jira client: no access token found"
            )
        try:
            url = self.construct_api_request_url(token)
            self.client = Jira(
                url=url,
                oauth2={
                    "client_id": client_id,
                    "token": {"access_token": token, "token_type": "Bearer"},
                },
            )
        except Exception as e:
            raise UpstreamProviderError(
                f"Error while initializing Jira client: {str(e)}"
            )

        return self.client

    def setup_basic_client(self, user_email, org_domain, api_token):
        try:
            self.client = Jira(
                url=org_domain,
                username=user_email,
                password=api_token,
            )
        except Exception as e:
            raise UpstreamProviderError(
                f"Error while initializing Jira client: {str(e)}"
            )

        return self.client


def get_client():
    assert (auth_type := app.config.get("AUTH_TYPE")), "JIRA_AUTH_TYPE must be set"
    jira_client = JiraClient()
    jira_client.set_limit(
        app.config.get("SEARCH_LIMIT", JiraClient.DEFAULT_SEARCH_LIMIT)
    )
    if auth_type == "basic":
        assert (
            user_email := app.config.get("USER_EMAIL")
        ), "JIRA_USER_EMAIL must be set"
        assert (
            org_domain := app.config.get("ORG_DOMAIN")
        ), "JIRA_ORG_DOMAIN must be set"
        assert (api_token := app.config.get("API_TOKEN")), "JIRA_API_TOKEN must be set"
        jira_client.setup_basic_client(user_email, org_domain, api_token)
    elif auth_type == "oauth":
        assert (
            client_id := app.config.get("OAUTH_CLIENT_ID")
        ), "JIRA_OAUTH_CLIENT_ID must be set"
        token = get_access_token()
        jira_client.setup_oauth_client(client_id, token)
    else:
        raise UpstreamProviderError(f"Invalid auth type: {auth_type}")

    return jira_client


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
