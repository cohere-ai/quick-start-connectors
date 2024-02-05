import logging
from typing import Dict, List

from config import AppConfig

logger = logging.getLogger(__name__)

client = None
config = AppConfig()


class CustomClient:
    """
    Client class to retrieve data from a custom data source
    """

    def __init__(self, token: str, search_limit: int):
        """
        You might need to adapt the headers and authentication method.

        Args:
            token (str): Authentication token
            search_limit (int): Maximum number of results to return
        """
        self.headers = {"Authorization": f"Bearer {token}"}
        self.search_limit = search_limit

    def search(self, query: str) -> List[Dict]:
        """
        Retrieve data based on the query.

        Args:
            query (str): Query string

        Returns:
            List[Dict]: List of data items.
        """
        logger.debug(f"search:query: {query}")

        # TODO: Replace mock data with actual data retrieval logic.
        data = [
            {
                "id": 1,
                "url": "https://example.com/article1",
                "title": "The Future of Technology",
                "text": "An in-depth analysis of emerging technology trends...",
                "timestamp": "2024-01-30 15:30:00",
            },
            {
                "id": 2,
                "url": "https://example.com/article2",
                "title": "Exploring the Natural World",
                "text": "A journey through the wonders of our planet...",
                "timestamp": "2024-01-31 10:00:00",
            },
        ]
        return data


def get_client() -> CustomClient:
    """
    Create or Retrieve a global singleton Client instance.

    Returns:
        CustomClient: Client instance
    """
    global client
    if client is None:
        client = CustomClient(config.CLIENT_AUTH_TOKEN, config.CLIENT_SEARCH_LIMIT)
    return client
