import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    assert (api_key := app.config.get("API_KEY")), "YEXT_API_KEY must be set"
    assert (account_id := app.config.get("ACCOUNT_ID")), "YEXT_ACCOUNT_ID must be set"
    assert (locale := app.config.get("LOCALE")), "YEXT_LOCAL must be set"
    assert (
        experience_key := app.config.get("EXPERIENCE_KEY")
    ), "YEXT_EXPERIENCE_KEY must be set"
    assert (v := app.config.get("V")), "YEXT_V must be set"

    url = "https://liveapi.yext.com/v2/accounts/me/search/query"

    params = {
        "api_key": api_key,
        "account_id": account_id,
        "experienceKey": experience_key,
        "input": query,
        "limit": app.config.get("LIMIT", "{}"),
        "locale": locale,
        "sessionTrackingEnabled": False,
        "source": app.config.get("SOURCE", "STANDARD"),
        "v": v,
        "version": app.config.get("VERSION", "PRODUCTION"),
    }

    response = requests.get(
        url,
        params=params,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    data = response.json()

    if data["meta"]["errors"]:
        raise UpstreamProviderError(str(data["meta"]["errors"]))

    if "response" not in data:
        return []

    cleaned_data = []

    for module in data["response"]["modules"]:
        cleaned_data.extend(module["results"])

    return cleaned_data
