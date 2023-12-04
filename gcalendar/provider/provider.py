import logging
import base64
from typing import Any

from .client import get_client


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    gcalendar_client = get_client()
    search_results = gcalendar_client.search_events(query)

    results = []
    for event in search_results:
        result = serialize_result(event)
        results.append(result)

    return results


def flatten_dict(d, parent_key="", sep="_"):
    flattened = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            flattened.update(flatten_dict(v, new_key, sep=sep))
        else:
            flattened[new_key] = v
    return flattened


def serialize_result(event):
    data = flatten_dict(event)
    stripped_data = {
        key: str(value)
        for key, value in data.items()
        if isinstance(value, (str, int, bool))
    }

    if "description" in stripped_data:
        stripped_data["text"] = stripped_data["description"]
        del stripped_data["description"]

    if "summary" in stripped_data:
        stripped_data["title"] = stripped_data["summary"]
        del stripped_data["summary"]

    if "htmlLink" in stripped_data:
        stripped_data["url"] = stripped_data["htmlLink"]
        del stripped_data["htmlLink"]

    return stripped_data
