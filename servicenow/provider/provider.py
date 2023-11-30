import logging
from typing import Any
from urllib.parse import urljoin

import requests
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)


def search(query: str) -> list[dict[str, Any]]:
    assert (
        base_url := app.config.get("INSTANCE_URL")
    ), "SERVICENOW_INSTANCE_URL must be set"
    assert (
        table_name := app.config.get("TABLE_NAME")
    ), "SERVICENOW_TABLE_NAME must be set"
    assert (username := app.config.get("USERNAME")), "SERVICENOW_USERNAME must be set"
    assert (password := app.config.get("PASSWORD")), "SERVICENOW_PASSWORD must be set"

    url = urljoin(base_url, f"/api/now/table/{table_name}")
    params = {
        "sysparm_display_value": True,
        "sysparm_limit": app.config.get("RESULT_LIMIT", 10),
        "sysparm_query": f"GOTO123TEXTQUERY321={query}",
    }
    auth = (username, password)

    response = requests.get(url, auth=auth, params=params)

    if response.status_code != 200:
        raise UpstreamProviderError(f"Failed to query ServiceNow: {response.text}")

    return response.json()["result"]
