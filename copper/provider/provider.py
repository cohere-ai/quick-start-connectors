import logging

from .client import get_client

logger = logging.getLogger(__name__)


def search_results(results, query):
    keywords = query.split()
    results = [
        result
        for result in results
        if any(keyword.lower() in result["name"].lower() for keyword in keywords)
        or any(keyword.lower() in result["details"].lower() for keyword in keywords)
    ]
    return results


def serialize_results(results, mapping):
    data = []
    for result in results:
        item = {}
        for key, value in result.items():
            item[key] = str(value)
            type_key = f"{result['entity_type']}.{key}"
            if type_key in mapping:
                item[mapping[type_key]] = item.pop(key)

        data.append(item)
    return data


def search(query):
    client = get_client()
    opportunities = client.get_opportunities()
    tasks = client.get_tasks()
    mapping = client.get_mapping()
    return serialize_results(search_results([*opportunities, *tasks], query), mapping)
