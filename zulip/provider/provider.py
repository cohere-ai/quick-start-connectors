import logging
import re
from typing import Any

from .client import get_client


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    client = get_client()
    params = {
        "anchor": "newest",
        "num_before": 100,
        "num_after": 0,
        "narrow": [
            {"operator": "streams", "operand": "public"},
            {"operator": "search", "operand": query},
        ],
    }

    messages = client.get_messages(params)

    results = [serialize_result(message) for message in messages["messages"]]

    return results


def serialize_result(message):
    serialized = {
        key: str(value)
        for key, value in message.items()
        if isinstance(value, (str, int, bool))
    }

    if "content" in serialized:
        serialized["text"] = strip_html_tags(serialized.pop("content"))

    if "subject" in serialized:
        serialized["title"] = serialized.pop("subject")

    return serialized


def strip_html_tags(html_text):
    clean = re.compile("<.*?>")
    plain_text = re.sub(clean, "", html_text)
    return plain_text
