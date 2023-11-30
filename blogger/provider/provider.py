from .client import get_client


def serialize_results(results):
    serialized_results = []
    for result in results:
        item_to_append = result
        item_to_append["text"] = result["content"]
        item_to_append = {k: str(v) for k, v in item_to_append.items()}
        serialized_results.append(item_to_append)
    return serialized_results


def search(query):
    client = get_client()
    results = client.get_blogs_posts(query)

    return serialize_results(results)
