import logging
from typing import Any


from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    atera_client = get_client()

    search_results = atera_client.search_tickets(query)

    results = []
    for page in search_results:
        results.append(serialize_search_result(page))

    return results


def serialize_search_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_result = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "TicketTitle" in stripped_result:
        stripped_result["title"] = stripped_result.pop("TicketTitle")

    if "FirstComment" in stripped_result:
        stripped_result["text"] = stripped_result.pop("FirstComment")

    return stripped_result
