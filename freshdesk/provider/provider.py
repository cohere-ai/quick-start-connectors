import logging
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    freshdesk_client = get_client()

    search_results = freshdesk_client.search(query)
    return [serialize_result(result) for result in search_results]


def serialize_result(entry) -> dict[str, str]:
    serialized_result = {}

    for key, value in entry.items():
        serialized_result[key] = (
            str(value)
            if not isinstance(value, list)
            else ", ".join(str(vl) for vl in value)
        )

    return serialized_result
