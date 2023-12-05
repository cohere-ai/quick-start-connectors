import logging
from typing import Any

from . import UpstreamProviderError
from .client import get_client

logger = logging.getLogger(__name__)


def process_response_data(data) -> list[dict[str, Any]]:
    results = []
    if "_embedded" in data and "conversations" in data["_embedded"]:
        for conversation in data["_embedded"]["conversations"]:
            results.append(conversation)
    else:
        logger.error(f"HelpScout search error: {data}")
        raise UpstreamProviderError(f"HelpScout search error: {data}")
    return results


def search(query) -> list[dict[str, Any]]:
    scout_client = get_client()
    data = scout_client.get_conversations(query)
    return process_response_data(data)
