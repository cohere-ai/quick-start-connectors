import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

BASE_PATH = "https://coda.io/apis/v1"


def search(query) -> list[dict[str, Any]]:
    url = BASE_PATH + "/docs"
    assert (token := app.config.get("API_TOKEN")), "CODA_API_TOKEN must be set"

    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "query": query,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return response.json()["items"]
