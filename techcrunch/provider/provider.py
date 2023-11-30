from .client import get_client


def search(query):
    client = get_client()
    return client.process_search(query)
