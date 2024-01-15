import logging
from typing import Any
from .client import get_client


logger = logging.getLogger(__name__)


def search(query: str) -> list[dict[str, Any]]:
    client = get_client()

    return client.search(query)
