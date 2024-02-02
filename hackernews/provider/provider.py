import logging
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    hn_client = get_client()

    search_results = hn_client.search(query)

    results = []
    for page in search_results:
        results.append(decorate_and_serialize_search_result(page))

    return results


def decorate_and_serialize_search_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_result = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    # Fetch content, fails gracefully if none found
    hn_client = get_client()
    content = hn_client.get_item(stripped_result.get("objectID"))

    if content:
        if content.get("text") is not None:
            stripped_result["text"] = content["text"]
        else:
            text_list = [child.get("text") for child in content.get("children")]

            if len(text_list) > 0:
                stripped_result["text"] = "".join(text_list)

    return stripped_result
