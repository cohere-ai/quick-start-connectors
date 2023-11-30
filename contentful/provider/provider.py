import logging

from .client import get_client

logger = logging.getLogger(__name__)


def process_content(node):
    if isinstance(node, list):
        values = [process_content(item) for item in node]
        return " ".join(values)
    elif isinstance(node, dict):
        if "content" in node:
            return process_content(node["content"])
        elif "value" in node:
            return node["value"]
    return str(node)


def serialize_results(results, mapping):
    data = []
    for result in results:
        item = {"content_type": result.content_type.id, "id": result.id}
        for key, value in result.fields().items():
            item[key] = str(value)
            if key == "content":
                item[key] = process_content(value)
            type_key = f"{result.content_type.id}.{key}"
            if type_key in mapping:
                item[mapping[type_key]] = item.pop(key)

        data.append(item)
    return data


def search(query):
    client = get_client()

    params = {"query": query, "limit": client.get_search_limit()}
    content_type = client.get_content_type()
    if content_type:
        params["content_type"] = content_type
    results = client.entries(params)

    return serialize_results(results.items, client.get_mapping())
