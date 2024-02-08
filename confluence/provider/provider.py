import logging

from .client import get_client

logger = logging.getLogger(__name__)


def search(query):
    client = get_client()
    pages = client.search(query)
    return pages
