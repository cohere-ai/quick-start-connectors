from typing import Any
from flask import current_app as app

from .client import get_client


def search(query) -> list[dict[str, Any]]:
    assert (db := app.config.get("DB")), "MONGODB_DB must be set"
    assert (
        collections := app.config.get("COLLECTIONS")
    ), "MONGODB_COLLECTIONS must be set"

    client = get_client()
    search_collections = collections.split(",")
    db = client[db]

    results = []
    for collection in search_collections:
        collection_results = db[collection].find({"$text": {"$search": query}})

        for result in collection_results:
            results.append(serialize_result(dict(result)))

    return results


def flatten_obj(d, parent_key="", sep="_"):
    flattened = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            flattened.update(flatten_obj(v, new_key, sep=sep))
        elif isinstance(v, list):
            flattened[new_key] = ", ".join(str(item) for item in v)
        else:
            flattened[new_key] = str(v)
    return flattened


def serialize_result(result):
    mappings = app.config.get("CONNECTOR_FIELD_MAPPING")

    # Add any connector mappings, e.g: text, title
    for key, value in mappings.items():
        if key in result:
            result[value] = result.pop(key)

    # Serialize ID object
    result["id"] = str(result.pop("_id"))

    # Flatten any nested dictionaries and arrays
    result = flatten_obj(result)

    return result
