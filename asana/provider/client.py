import requests
from flask import current_app as app, request
from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class AsanaClient:
    BASE_URL = "https://app.asana.com"
    API_URL = f"{BASE_URL}/api/1.0"
    DEFAULT_SEARCH_LIMIT = 10
    DEFAULT_TASK_PROPERTIES = [
        "actual_time_minutes",
        "name",
        "notes",
        "approval_status",
        "assignee",
        "assignee.name",
        "assignee_section",
        "assignee_section.name",
        "assignee_status",
        "completed",
        "completed_at",
        "completed_by",
        "completed_by.name",
        "created_at",
        "created_by",
        "dependencies",
        "due_at",
        "due_on",
        "external",
        "hearts",
        "likes",
        "parent",
        "parent.name",
        "projects",
        "projects.name",
        "tags",
        "tags.name",
        "workspace",
        "workspace.name",
    ]

    def __init__(
        self,
        access_token,
        workspace_gid,
        task_properties=None,
        search_limit=None,
        fields_mapping={},
    ):
        self.task_properties = task_properties or self.DEFAULT_TASK_PROPERTIES
        self.access_token = access_token
        self.workspace_gid = workspace_gid
        self.search_limit = search_limit or self.DEFAULT_SEARCH_LIMIT
        self.fields_mapping = fields_mapping
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def add_task_url_to_results(self, results):
        for result in results:
            result["url"] = f"{self.BASE_URL}/0/0/{result['gid']}"
        return results

    def search(self, query):
        search_url = f"{self.API_URL}/workspaces/{self.workspace_gid}/tasks/search"
        params = {
            "text": query,
            "opt_fields": ",".join(self.task_properties),
            "limit": self.search_limit,
        }

        response = requests.get(
            search_url,
            headers=self.headers,
            params=params,
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return self.add_task_url_to_results(response.json()["data"])


def get_client():
    assert (auth_type := app.config.get("AUTH_TYPE")), "ASANA_AUTH_TYPE must be set"
    if auth_type == "access_token":
        assert (
            access_token := app.config.get("ACCESS_TOKEN")
        ), "ASANA_ACCESS_TOKEN must be set"
    elif auth_type == "oauth":
        access_token = get_access_token()
        if access_token is None:
            raise UpstreamProviderError("No oauth access token found")
    else:
        raise UpstreamProviderError(f"Unknown auth type: {auth_type}")

    assert (
        workspace_gid := app.config.get("WORKSPACE_GID")
    ), "ASANA_WORKSPACE_GID must be set"

    search_limit = app.config.get("SEARCH_LIMIT", None)
    task_properties = app.config.get("TASK_PROPERTIES", None)
    fields_mapping = app.config.get("FIELDS_MAPPING", {})
    client = AsanaClient(
        access_token,
        workspace_gid,
        task_properties,
        search_limit,
        fields_mapping,
    )

    return client


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
