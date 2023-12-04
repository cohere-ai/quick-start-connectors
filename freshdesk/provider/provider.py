import logging
import json
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    assert (token := app.config.get("API_KEY")), "FRESHDESK_API_KEY must be set"
    assert (
        domain := app.config.get("DOMAIN_NAME")
    ), "FRESHDESK_DOMAIN_NAME must be set"
    assert (
        parameter := app.config.get("TICKET_PARAMETER")
    ), "FRESHDESK_TICKET_PARAMETER must be set"

    url = f"https://{domain}/api/v2/search/tickets"
    params = {"query": f'"{parameter}:{query}"'}
    # Freshdesk uses Basic Auth with this specific format, using the API key
    auth = (token, "X")

    response = requests.get(url, auth=auth, params=params)

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return response.json()["results"]
