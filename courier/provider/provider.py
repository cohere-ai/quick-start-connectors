import logging
from typing import Any


from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    courier_client = get_client()

    messages = courier_client.list_messages()

    results = []
    for message in messages:
        content = courier_client.get_message_content(message["id"])
        search_text = f"{content.get('text', '')}{content.get('text', '')}"
        message.update(content)

        if query.lower() in search_text.lower():
            results.append(serialize_search_result(message))

    return results


def serialize_search_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_result = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "subject" in stripped_result:
        stripped_result["title"] = stripped_result.pop("subject")

    if "text" in stripped_result:
        stripped_result["text"] = stripped_result.pop("text")

    return stripped_result
