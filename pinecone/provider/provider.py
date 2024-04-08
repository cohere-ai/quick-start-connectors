import logging

from flask import current_app as app

from .client import get_cohere_client, get_pinecone_client

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
                k if k not in mappings else mappings[k]: (
                    ", ".join(str(vl) for vl in v) if isinstance(v, list) else str(v)
                )
                for k, v in item.items()
            },
            data,
        )
    )
    return serialized_data


def search(query):
    assert (api_key := app.config.get("API_KEY")), "PINECONE_API_KEY must be set"
    assert (index := app.config.get("INDEX")), "PINECONE_INDEX must be set"
    assert (
        cohere_api_key := app.config.get("COHERE_API_KEY")
    ), "PINECONE_COHERE_API_KEY must be set"
    assert (
        cohere_embed_model := app.config.get("COHERE_EMBED_MODEL")
    ), "PINECONE_COHERE_EMBED_MODEL must be set"

    cohere_client = get_cohere_client(cohere_api_key)
    # Pulling just the query embedding vector
    xq = cohere_client.get_embeddings(query, cohere_embed_model)[0]

    pinecone_client = get_pinecone_client(api_key, index)

    search_limit = app.config.get("SEARCH_LIMIT", 100)

    pinecone_results = pinecone_client.query(xq, search_limit)

    results = [
        {"id": match["id"], **match["metadata"]}
        for match in pinecone_results["matches"]
    ]

    mapping = app.config.get("FIELDS_MAPPING", {})
    return serialize_results(results, mapping)
