import logging
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    github_client = get_client()

    search_results = github_client.search(query)

    results = []
    for item in search_results:
        result = serialize_result(github_client, item)
        if result:
            results.append(result)

    return results


def serialize_result(github_client, result) -> dict[str, Any]:
    content = github_client.fetch_and_decode_content(result["url"])

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
