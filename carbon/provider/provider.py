import logging
from typing import Any


from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    carbon_client = get_client()

    search_results = carbon_client.search(query)

    results = []
    for result in search_results:
        results.append(serialize_result(result))

    return results


def serialize_result(entry):
    serialized_result = {}

    for key, value in entry.items():
        serialized_result[key] = (
            str(value)
            if not isinstance(value, list)
            else ", ".join(str(vl) for vl in value)
        )

    return serialized_result
