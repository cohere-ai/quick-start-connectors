from typing import Any
from .client import get_client


def serialize_results(data, mappings={}):
    """
    Serialize a list of dictionaries by transforming keys based on provided mappings
    and converting values to strings.

    Parameters:
    - data (list): A list of dictionaries to be serialized.
    - mappings (dict): A dictionary specifying key mappings for transformation.

    Returns:
    list: A serialized list of dictionaries with transformed keys and string-converted values.
    """

    def serialize_item(item):
        serialized_item = {}

        for k, v in item.items():
            key = k if k not in mappings else mappings[k]
            serialized_item[key] = (
                str(v) if not isinstance(v, list) else ", ".join(str(vl) for vl in v)
            )

        return serialized_item

    return list(map(serialize_item, data))


def search(query) -> list[dict[str, Any]]:
    client = get_client()
    search_results = client.search(query)

    return serialize_results(search_results, client.fields_mapping)
