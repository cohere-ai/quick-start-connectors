"""
Client class to retrieve data from a custom data source
"""
import os
import logging
from datetime import datetime
from datamodels import DataItem

logger = logging.getLogger(__name__)

DEFAULT_SEARCH_LIMIT = 5

client = None

class CustomClient:
    def __init__(self, token: str, search_limit: int):
        """
        You might need to adapt the headers and authentication method.

        Args:
            token (str): Authentication token
            search_limit (int): Maximum number of results to return
        """
        self.headers = {
            "Authorization": f"Bearer {token}",
        }
        self.search_limit = search_limit

    def search(self, query: str):
        """
        Logic to retrieve data based on query

        Args:
            query (str): Query string

        Returns:
            List[dict]: List of data items
        """
        logger.debug(f"search:query: {query}")

        data = [
            {
                "id": 1,
                "url": "https://example.com/article1",
                "title": "The Future of Technology",
                "text": "An in-depth analysis of emerging technology trends...",
                "timestamp": "2024-01-30 15:30:00"
            },
            {
                "id": 2,
                "url": "https://example.com/article2",
                "title": "Exploring the Natural World",
                "text": "A journey through the wonders of our planet...",
                "timestamp": "2024-01-31 10:00:00"
            }
        ]
        return data

def get_client():
    """
    Create or Retrieve a global singleton Client instance.

    Returns:
        CustomClient: Client instance
    """
    global client
    if client is not None:
        return client

    assert (token := os.getenv("CLIENT_AUTH_TOKEN")), "CLIENT_AUTH_TOKEN must be set"
    search_limit = int(os.getenv("CLIENT_SEARCH_LIMIT")) or DEFAULT_SEARCH_LIMIT
    client = CustomClient(token, search_limit)

    return client