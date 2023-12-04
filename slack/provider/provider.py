import logging
from typing import Any

from . import UpstreamProviderError
from .client import get_client

logger = logging.getLogger(__name__)


def serialize_results(response):
    results = []
    for match in response["messages"]["matches"]:
        document = extract_message_data(match)
        results.append(document)
    for match in response["files"]["matches"]:
        document = extract_files_data(match)
        results.append(document)

    return results


def extract_message_data(message_json):
    document = {}
    document["type"] = "message"
    if "text" in message_json:
        document["text"] = str(message_json.pop("text"))
    if "permalink" in message_json:
        document["url"] = str(message_json.pop("permalink"))
    if "channel" in message_json and "name" in message_json["channel"]:
        document["title"] = str(message_json["channel"]["name"])

    return document


def extract_files_data(message_json):
    document = {}
    document["type"] = "file"
    if "permalink" in message_json:
        document["url"] = str(message_json.pop("permalink"))
    if "title" in message_json:
        document["title"] = str(message_json["title"])
        document["text"] = str(message_json["title"])

    return document


def search(query: str) -> list[dict[str, Any]]:
    client = get_client()
    response = client.search_all(query)

    if not response["ok"]:
        raise UpstreamProviderError(f"Failed to query Slack: {response['error']}")

    return serialize_results(response)
