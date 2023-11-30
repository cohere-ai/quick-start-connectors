import logging
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

OPTIONAL_PARAMS = (
    "idBoards",
    "idOrganizations",
    "idCards",
    "modelTypes",
    "board_fields",
    "boards_limit",
    "board_organization",
    "card_fields",
    "cards_limit",
    "cards_page",
    "card_board",
    "card_list",
    "card_members",
    "card_stickers",
    "card_attachments",
    "organization_fields",
    "organizations_limit",
    "member_fields",
    "members_limit",
    "partial",
)


def search(query) -> list[dict[str, Any]]:
    url = "https://api.trello.com/1/search"
    assert (key := app.config.get("API_KEY")), "TRELLO_API_KEY must be set"
    assert (token := app.config.get("API_TOKEN")), "TRELLO_API_TOKEN must be set"

    params = {
        "query": query,
        "key": key,
        "token": token,
    }

    for optional_param in OPTIONAL_PARAMS:
        value = app.config.get(optional_param.upper())

        if value is not None and value != "":
            params[optional_param] = value

    response = requests.get(
        url,
        params=params,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    return response.json()
