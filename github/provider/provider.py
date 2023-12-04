import logging
from base64 import b64decode
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

GITHUB_SEARCH_CODE_URL = "https://api.github.com/search/code"
DEFAULT_RESULTS_PER_PAGE = 5
DEFAULT_QUERY_TEMPLATE = "{query} in:file"


def serialize_result(result):
    content = fetch_and_decode_content(result["url"])

    if not content:
        return None

    data = {"text": content}
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_resource = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if (title := result.get("path")) is not None:
        data["title"] = title

    if (url := result.get("html_url")) is not None:
        data["url"] = url

    return {
        **stripped_resource,
        **data,
    }


def fetch_and_decode_content(url) -> str | None:
    assert (token := app.config.get("TOKEN")), "GITHUB_TOKEN must be set"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    if not response.ok:
        logger.error(f"Error fetching GitHub file: {response.json()}")
        return None

    return b64decode(response.json()["content"]).decode()


def search(query) -> list[dict[str, Any]]:
    assert (token := app.config.get("TOKEN")), "GITHUB_TOKEN must be set"

    response = requests.get(
        GITHUB_SEARCH_CODE_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        params={
            "q": app.config.get("QUERY_TEMPLATE", DEFAULT_QUERY_TEMPLATE).format(
                query=query
            ),
            "per_page": app.config.get("RESULTS_PER_PAGE", DEFAULT_RESULTS_PER_PAGE),
        },
    )

    if response.status_code != 200:
        message = response.json().get("message", f"Error: HTTP {response.status_code}")
        raise UpstreamProviderError(message)

    results = []
    for item in response.json()["items"]:
        result = serialize_result(item)
        if result:
            results.append(result)

    return results
