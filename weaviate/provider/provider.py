import logging

import weaviate
from flask import current_app as app

logger = logging.getLogger(__name__)
client = None


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
                k if k not in mappings else mappings[k]: (
                    ", ".join(str(vl) for vl in v) if isinstance(v, list) else str(v)
                )
                for k, v in item.items()
            },
            data,
        )
    )
    return serialized_data


def configure_client(url):
    global client
    client = weaviate.Client(
        url=url,
    )


def get_schema_properties(schema_class, url):
    if not client:
        configure_client(url)

    schema = client.schema.get()
    schema_properties = []

    for class_info in schema["classes"]:
        if class_info["class"] == schema_class:
            schema_properties = [prop["name"] for prop in class_info["properties"]]
            break

    return schema_properties


def search(query):
    assert (url := app.config.get("SERVER_URL")), "WEAVIATE_SERVER_URL must be set"
    assert (
        schema_class := app.config.get("SCHEMA_CLASS")
    ), "WEAVIATE_SCHEMA_CLASS must be set"
    if not client:
        configure_client(url)

    schema_properties = get_schema_properties(schema_class, url)

    nearText = {"concepts": [query]}
    response = (
        client.query.get(schema_class, list(schema_properties))
        .with_near_text(nearText)
        .with_limit(10)
        .do()
    )
    mappings = app.config.get("CONNECTOR_FIELDS_MAPPING", {})
    results = (
        response["data"]["Get"][schema_class]
        if response["data"]["Get"][schema_class]
        else []
    )
    return serialize_results(results, mappings)
