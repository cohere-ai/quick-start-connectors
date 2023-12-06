import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

BASE_PATH = "https://app.asana.com/api/1.0"
TASK_PROPERTIES = [
    "actual_time_minutes",
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


def search(query) -> list[dict[str, Any]]:
    assert (token := app.config.get("ACCESS_TOKEN")), "ASANA_ACCESS_TOKEN must be set"
    assert (
        workspace_gid := app.config.get("WORKSPACE_GID")
    ), "ASANA_WORKSPACE_GID must be set"
    url = f"{BASE_PATH}/workspaces/{workspace_gid}/tasks/search"

    headers = {
        "Authorization": f"Bearer {token}",
    }
    # By default, the endpoint returns a compact Task, but they provide
    # a query param that allows you to specify extra properties
    params = {
        "text": query,
        "opt_fields": ",".join(TASK_PROPERTIES),
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return response.json()["data"]
