import logging
import re
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

BASE_PATH = "https://api.app.shortcut.com/api/v3"


def serialize_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    data = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "description" in data:
        data["text"] = data["description"]
        del data["description"]

    if "name" in data:
        data["title"] = data["name"]
        del data["name"]

    if "app_url" in data:
        data["url"] = data["app_url"]
        del data["app_url"]

    return data


def search(query) -> list[dict[str, Any]]:
    url = BASE_PATH + "/search"
    assert (token := app.config.get("API_TOKEN")), "SHORTCUT_API_TOKEN must be set"

    headers = {
        "Shortcut-Token": token,
    }
    data = {
        "detail": "full",
        "page_size": 25,
        "query": query,
    }

    response = requests.get(
        url,
        headers=headers,
        json=data,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    search_results = response.json()["stories"]["data"]
    results = []
    for result in search_results:
        results.append(serialize_result(result))

    return results
