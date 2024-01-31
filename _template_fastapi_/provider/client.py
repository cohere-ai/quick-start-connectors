"""
Client class to retrieve data from a custom data source
"""
from datetime import datetime
from datamodels import DataItem

class CustomClient:
    def __init__(self):
        """
        Initialize the client
        """
        pass

    def search(self, query: str):
        """
        Logic to retrieve data based on query

        Args:
            query (str): Query string

        Returns:
            List[dict]: List of data items
        """
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