import logging

from .client import get_client

logger = logging.getLogger(__name__)

def serialize_results(data):
    # debug data
    logger.debug(f"Raw data: {data}")

    serialized_data = []
    results = data.get("entities", [])
    for entity in results:
        identifier = entity.pop("identifier", {})
        serialized_data.append({
            "text": entity.pop("short_description"),
            "title": identifier.pop("value"),
            "url": f"https://www.crunchbase.com/{identifier.pop('entity_def_id')}/{identifier.pop('permalink')}",
            "id": identifier.pop("uuid"),
        })
    return serialized_data


def search(query):
    client = get_client()

    return serialize_results(client.autocomplete(query))
