import logging
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)


def serialize_results(data, mappings):
    """
    Serialize a list of dictionaries by transforming keys based on provided mappings
    and converting values to strings.

    Parameters:
    - data (list): A list of dictionaries to be serialized.
    - mappings (dict): A dictionary specifying key mappings for transformation.

    Returns:
    list: A serialized list of dictionaries with transformed keys and string-converted values.
    """
    serialized_data = list(
        map(
            lambda item: {
                k.lower() if k.lower() not in mappings else mappings[k.lower()]: (
                    ", ".join(str(vl) for vl in v) if isinstance(v, list) else str(v)
                )
                for k, v in item.items()
            },
            data,
        )
    )
    return serialized_data


def search(query) -> list[dict[str, Any]]:
    if not query:
        return []

    client = get_client()
    search_results_meta = client.search_using_index(
        client.get_search_index(), query, client.get_search_limit()
    )
    search_results = client.get_entities_by_meta(search_results_meta)

    return serialize_results(search_results or [], client.get_mappings())
