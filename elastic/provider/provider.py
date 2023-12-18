import logging

from .client import get_client

logger = logging.getLogger(__name__)

MIN_TEXT_LENGTH = 25


def search(query):
    elasticsearch_client = get_client()

    search_results = elasticsearch_client.search(query)

    results = []
    for match in search_results:
        results.append(serialize_result(match))

    return results


def build_text(match):
    if "highlight" in match:
        return match["highlight"]["content"][0]

    text = ""
    for value in match["_source"].values():
        if isinstance(value, str) and len(value) >= MIN_TEXT_LENGTH:
            text += value

    return text


def serialize_result(match):
    source = match["_source"]
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_source = {
        key: str(value)
        for key, value in source.items()
        if isinstance(value, (str, int, bool))
    }

    return {
        **stripped_source,
        "text": build_text(match),
    }
