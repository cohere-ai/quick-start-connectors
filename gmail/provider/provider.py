import logging
import base64
from typing import Any

from .client import get_client


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    gmail_client = get_client()

    search_results = gmail_client.search_mail(query)

    # Prepare message IDs and perform a batch GET using multi-threading
    search_result_messages = search_results.get("messages", [])
    message_ids = [message["id"] for message in search_result_messages]
    messages = gmail_client.batch_get_messages(message_ids)

    results = []
    for message in messages:
        results.append(serialize_result(message))

    return results


def decode_base64_raw(raw):
    return base64.urlsafe_b64decode(raw).decode("utf-8")


def serialize_result(message):
    data = {}
    payload = message["payload"]

    # Find subject title
    if (headers := payload.get("headers")) is not None:
        # Get miscellaneous header values in K-V format
        headers_dict = {header["name"]: header["value"] for header in headers}
        stripped_headers = {
            key: str(value)
            for key, value in headers_dict.items()
            if isinstance(value, (str, int, bool))
        }

        data.update(stripped_headers)

        if "Subject" in data:
            data["title"] = data.pop("Subject")

    # Build text
    if (part := payload.get("parts")) is not None:
        if (body := part[0].get("body", {}).get("data")) is not None:
            text = decode_base64_raw(body)
            data["text"] = text.replace("\r\n", "")

    # Remove metadata fields
    METADATA_PREFIXES = ["ARC", "DKIM", "X"]
    data = {
        key: value
        for key, value in data.items()
        if key.split("-")[0] not in METADATA_PREFIXES
    }

    return data
