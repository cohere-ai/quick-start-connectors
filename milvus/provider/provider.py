import logging

from flask import current_app as app
from .client import get_cohere_client, get_milvus_client

logger = logging.getLogger(__name__)


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
    serialized_data = list(
        map(
            lambda item: {
                k
                if k not in mappings
                else mappings[k]: ", ".join(str(vl) for vl in v)
                if isinstance(v, list)
                else str(v)
                for k, v in item.items()
            },
            data,
        )
    )
    return serialized_data


def search(query):
    cohere_client = get_cohere_client()
    milvus_client = get_milvus_client()

    xq = cohere_client.get_embeddings(query)

    output_fields = milvus_client.get_search_fields()
    search_results = milvus_client.search(xq)
    milvus_client.close_connection()

    results = [
        {field: result.entity.get(field) for field in output_fields}
        for result in search_results[0]
    ]
    mapping = app.config.get("FIELDS_MAPPING", {})
    return serialize_results(results, mapping)
