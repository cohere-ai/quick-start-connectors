import logging
from typing import Any

from flask import current_app as app

from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    freshservice_client = get_client()
    domain = app.config.get("DOMAIN")

    search_results = freshservice_client.search_tickets(query)

    results = []
    for result in search_results:
        results.append(serialize_search_result(result, domain))

    return results


def serialize_search_result(result, domain):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    serialized = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "subject" in serialized:
        serialized["title"] = serialized.pop("subject")

    if "description_text" in serialized:
        serialized["text"] = serialized.pop("description_text")

    if "id" in serialized:
        serialized["url"] = f"{domain}/a/tickets/{serialized['id']}"

    return serialized
