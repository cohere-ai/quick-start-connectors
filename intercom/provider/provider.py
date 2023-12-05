import logging
import re
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

BASE_PATH = "https://api.intercom.io"


def strip_html_tags(html_text):
    clean = re.compile("<.*?>")
    plain_text = re.sub(clean, "", html_text)
    return plain_text


def serialize_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    data = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if (raw_body := result.get("source", {}).get("body")) is not None:
        data["text"] = strip_html_tags(raw_body)

    return data


def search(query) -> list[dict[str, Any]]:
    url = BASE_PATH + "/conversations/search"
    assert (
        token := app.config.get("ACCESS_TOKEN")
    ), "INTERCOM_ACCESS_TOKEN must be set"

    headers = {
        "Authorization": f"Bearer {token}",
    }
    data = {
        "query": {
            "operator": "OR",
            "value": [
                {
                    "field": "source.body",
                    "operator": "~",
                    "value": query,
                },
                {
                    "field": "source.subject",
                    "operator": "~",
                    "value": query,
                },
            ],
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    search_results = response.json()["conversations"]
    results = []
    for result in search_results:
        results.append(serialize_result(result))

    return results
