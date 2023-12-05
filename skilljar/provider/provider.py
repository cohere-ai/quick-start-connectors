import logging
import base64
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

BASE_PATH = "https://api.skilljar.com/v1"


def search(query) -> list[dict[str, Any]]:
    assert (token := app.config.get("API_KEY")), "SKILLJAR_API_KEY must be set"
    assert (
        domain_name := app.config.get("DOMAIN_NAME")
    ), "SKILLJAR_DOMAIN_NAME must be set"

    url = BASE_PATH + f"/domains/{domain_name}/published-courses"

    # Skilljar uses basic auth, need token encoded to base64
    base64_encoded_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    headers = {"Authorization": f"Basic {base64_encoded_token}"}

    params = {
        "search": query,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return response.json()["results"]
