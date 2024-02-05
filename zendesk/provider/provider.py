import logging

import requests
from flask import current_app as app
from .client import get_client
from . import UpstreamProviderError

logger = logging.getLogger(__name__)


def serialize_results(data):
    """
    Serialize a list of dictionaries by getting the values of the needed keys and transforming them into a string.
    """

    results = []
    for item in data:
        result = {
            "title": item["subject"] if "subject" in item and item["subject"] else "",
            "text": (
                item["description"]
                if "description" in item and item["description"]
                else ""
            ),
            "url": item["url"] if "url" in item and item["url"] else "",
            "tags": (
                ", ".join(item["tags"])
                if "tags" in item and isinstance(item["tags"], list)
                else ""
            ),
        }
        for key, value in item.items():
            if key not in ["subject", "description", "url", "tags"]:
                result.update({key: str(value)})

        results.append(result)

    return results


def search(query):
    zendesk_client = get_client()

    return serialize_results(zendesk_client.search(query))
