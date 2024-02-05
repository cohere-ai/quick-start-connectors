import logging
from typing import Any


from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    carbon_client = get_client()
    search_results = carbon_client.search(query)

    return serialize_results(search_results, carbon_client.mappings)


def serialize_results(data, mappings):
    """
    Serialize a list of dictionaries by transforming keys based on provided mappings
    and converting values to strings.

    Parameters:
    - data (list): A list of dictionaries to be serialized.
    - mappings (dict): Optional, a dictionary specifying key mappings for transformation.

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
