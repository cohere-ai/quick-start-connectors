import logging
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    reuters_client = get_client()

    search_results = reuters_client.search(query)
    results = []
    for result in search_results:
        results.append(serialize_result(result))

    return results


def serialize_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_source = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "headLine" in stripped_source:
        stripped_source["title"] = stripped_source["headLine"]
        del stripped_source["headLine"]

    if "fragment" in stripped_source:
        stripped_source["text"] = stripped_source["fragment"]
        del stripped_source["fragment"]

    return stripped_source
