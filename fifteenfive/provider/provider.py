import logging
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)

ALLOWED_ENTITY_TYPES = {
    "user": {
        "search_fields": ["first_name", "last_name", "email"],
        "mapping": {"full_name": "text", "email": "title"},
    },
    "vacation": {"search_fields": ["note"], "mapping": {"note": "text"}},
    "question": {
        "search_fields": ["question_text", "group"],
        "mapping": {"question_text": "text"},
    },
    "answer": {
        "search_fields": ["question", "answer_text"],
        "mapping": {"answer_text": "text"},
    },
    "pulse": {"search_fields": ["report", "value"], "mapping": {"value": "text"}},
    "high-five": {"search_fields": ["text", "report"], "mapping": {"text": "text"}},
    "objective": {
        "search_fields": ["description"],
        "mapping": {"description": "text"},
    },
    "review-cycle": {"search_fields": ["name"], "mapping": {"name": "text"}},
}


def serialize_results(data, mappings):
    serialized_data = {
        k if k not in mappings else mappings[k]: (
            ", ".join(str(vl) for vl in v) if isinstance(v, list) else str(v)
        )
        for k, v in data.items()
    }
    return serialized_data


def search_allowed_entities(client, query, allowed_entities):
    results = []
    searchable_entities = {
        k: v for k, v in ALLOWED_ENTITY_TYPES.items() if k in allowed_entities
    }
    searchable_entity_types = list(searchable_entities.keys())
    for entity_type in searchable_entity_types:
        response = client.get_entities_by_type(entity_type)
        query = query.lower()
        keywords = query.split()
        search_properties = searchable_entities[entity_type]["search_fields"]
        search_results = []
        for entity in response["results"]:
            for prop in search_properties:
                value = entity.get(prop, "")
                value = value.lower() if isinstance(value, str) else ""

                if any(keyword in value for keyword in keywords):
                    entity["entity_type"] = entity_type
                    if entity_type == "user":
                        entity["full_name"] = (
                            f"{entity['first_name']} {entity['last_name']}"
                        )
                    entity = serialize_results(
                        entity, searchable_entities[entity_type]["mapping"]
                    )
                    search_results.append(entity)
                    break

        results.extend(search_results)
    return results


def search(query) -> list[dict[str, Any]]:
    client = get_client()
    allowed_entities = client.get_allowed_entities()
    return search_allowed_entities(client, query, allowed_entities)
