import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

BASE_PATH = "https://api.smartsheet.com"
API_VERSION = "2.0"


def process_response_data(response: requests.Response) -> list[dict[str, Any]]:
    data = response.json()
    if "results" not in data:
        raise UpstreamProviderError("Unexpected response from Smartsheet API")
    # TODO if we need to process pagination or other data fields, we need to do it here
    return data["results"]


def search(query) -> list[dict[str, Any]]:
    url = f"{BASE_PATH}/{API_VERSION}/search"
    assert (
        token := app.config.get("ACCESS_TOKEN")
    ), "SMARTSHEET_ACCESS_TOKEN must be set"
    scopes = app.config.get(
        "SCOPES",
        "cellData,comments,folderNames,reportNames,sheetNames,sightNames,summaryFields,templateNames,workspaceNames",
    )
    page_size = app.config.get(
        "PAGE_SIZE",
        100,
    )
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(
        url,
        headers=headers,
        params={
            "query": query,
            "scopes": scopes,
            "pageSize": page_size,
        },
    )
    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return process_response_data(response)
