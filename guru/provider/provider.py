import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)


def extract_card_data(card_json):
    return {
        "text": card_json["content"],
        "highlightedBodyContent": card_json["highlightedBodyContent"],
        "highlightedTitleContent": card_json["highlightedTitleContent"],
        "permalink": "https://app.getguru.com/card/" + card_json["slug"],
        "author": " ".join(
            [
                card_json["lastModifiedBy"].get("firstName", ""),
                card_json["lastModifiedBy"].get("lastName", ""),
            ]
        ),
    }


def search(query: str) -> list[dict[str, Any]]:
    url = "https://api.getguru.com/api/v1/search/query"
    headers = {"accept": "application/json"}
    params = {"searchTerms": query}
    auth = (app.config["USER_EMAIL"], app.config["API_TOKEN"])

    response = requests.get(url, headers=headers, auth=auth, params=params)

    if response.status_code != 200:
        raise UpstreamProviderError(f"Failed to query Guru: {response.text}")

    return [extract_card_data(card) for card in response.json()]
