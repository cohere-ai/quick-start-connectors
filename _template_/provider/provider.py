import logging
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    """
    Main business logic for the /search endpoint. This should handle:
    - Instantiating a client (if exists)
    - Calling the search
    - Performing any necessary transformations/serializations
    """
    example_client = get_client()

    search_results = example_client.search(query)
    return [serialize_result(result) for result in search_results]


def serialize_result(entry) -> dict[str, str]:
    """
    Transforms each search result into a Coral-friendly format.
    It is recommended to add the following keys (if they exist in the result payload):
    - title: name of the result
    - text: main body of content
    - url: link to the result

    In addition, all values must be returned as str
    """
    serialized_result = {}

    for key, value in entry.items():
        serialized_result[key] = (
            str(value)
            if not isinstance(value, list)
            else ", ".join(str(vl) for vl in value)
        )

    return serialized_result
