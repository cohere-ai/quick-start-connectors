import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    assert (api_key := app.config.get("API_KEY")), "README_API_KEY must be set"

    url = "https://dash.readme.com/api/v1/docs/search"

    params = {
        "search": query,
    }

    auth = requests.auth.HTTPBasicAuth(api_key, "")
    response = requests.post(url, params=params, auth=auth)

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    data = response.json()
    return data["results"]
