import logging
from typing import Any

from . import UpstreamProviderError
from .client import get_client

logger = logging.getLogger(__name__)


def serialize_results(results, mapping):
    data = []
    for module in results:
        for result in module["results"]:
            item = {}
            for key, value in result["data"].items():
                item[key] = str(value)
                if key in mapping:
                    item[mapping[key]] = item.pop(key)
            data.append(item)
    return data


def search(query) -> list[dict[str, Any]]:
    client = get_client()
    return serialize_results(client.search(query), client.mapping)
