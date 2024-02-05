import logging

from . import UpstreamProviderError
from .client import get_client

logger = logging.getLogger(__name__)


def serialize_results(data, mappings):
    serialized_data = {
        k if k not in mappings else mappings[k]: (
            ", ".join(str(vl) for vl in v) if isinstance(v, list) else str(v)
        )
        for k, v in data.items()
    }
    return serialized_data


def search_allowed_entities(client, query):
    results = []
    per_page = client.get_search_limit()
    allowed_entities = client.get_allowed_entities()
    allowed_entity_types = client.get_allowed_entity_types()
    searchable_entities = {
        k: v for k, v in allowed_entity_types.items() if k in allowed_entities
    }
    searchable_entity_types = list(searchable_entities.keys())

    for entity_type in searchable_entity_types:
        search_properties = searchable_entities[entity_type]["search_fields"]
        is_searchable = search_properties[0] == "q"
        response = {entity_type: []}
        try:
            if is_searchable:
                params = {"q": query, "per_page": per_page}
                response = client.get_entities_by_type(entity_type, params)
            else:
                params = {"per_page": per_page}
                response = client.get_entities_by_type(entity_type, params)
        except UpstreamProviderError:
            pass

        query = query.lower()
        keywords = query.split()

        search_results = []
        for entity in response[entity_type]:
            entity["entity_type"] = entity_type
            if "description" in entity and isinstance(entity["description"], dict):
                entity["description"] = entity["description"]["body"]
            if not is_searchable:
                for prop in search_properties:
                    value = entity.get(prop, "")
                    value = value.lower() if isinstance(value, str) else ""
                    if any(keyword in value for keyword in keywords):
                        entity = serialize_results(
                            entity, searchable_entities[entity_type]["mapping"]
                        )
                        results.append(entity)
                        break
            else:
                entity = serialize_results(
                    entity, searchable_entities[entity_type]["mapping"]
                )
                search_results.append(entity)

        results.extend(search_results)
    return results


def search(query):
    client = get_client()
    return search_allowed_entities(client, query)
