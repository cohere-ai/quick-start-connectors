import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    assert (
        domain_name := app.config.get("DOMAIN_NAME")
    ), "EGNYTE_DOMAIN_NAME must be set"
    assert (key := app.config.get("API_KEY")), "EGNYTE_API_KEY must be set"
    url = f"https://{domain_name}/pubapi/v2/search"

    headers = {
        "Authorization": f"Bearer {key}",
    }
    data = {
        "query": query,
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return response.json()["results"]
