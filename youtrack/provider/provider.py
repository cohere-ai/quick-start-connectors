import logging
from typing import Any

from flask import current_app as app

from .client import get_client

logger = logging.getLogger(__name__)


def serialize_search_result(result):
    base_url = app.config.get("BASE_URL")

    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    serialized = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "description" in serialized:
        serialized["text"] = serialized["description"]
        del serialized["description"]

    if "idReadable" in serialized:
        issue_code = serialized["idReadable"]
        serialized["title"] = issue_code
        serialized["url"] = f"{base_url}/issue/{issue_code}"
        del serialized["idReadable"]

    return serialized


def search(query) -> list[dict[str, Any]]:
    youtrack_client = get_client()

    search_results = youtrack_client.search_issues(query)

    results = []
    for result in search_results:
        results.append(serialize_search_result(result))

    return results
