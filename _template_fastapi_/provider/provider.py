import logging
from typing import List

from pydantic import ValidationError

from client import get_client
from datamodels import DataItem
from exceptions import UpstreamProviderError


logger = logging.getLogger(__name__)


def search(query: str) -> List[DataItem]:
    """
    Handles search requests and returns a list of DataItem objects.

    Args:
        query (str): Query string

    Returns:
        List[DataItem]: A list of data items resulting from the search.
    """
    client = get_client()

    try:
        data = client.search(query=query)
    except Exception as error:
        logger.error(f"search_error: {error}")
        raise UpstreamProviderError("Error retrieving data from the search") from error

    try:
        data_items = [DataItem(**d) for d in data]
    except ValidationError as error:
        logger.error(f"Data validation error: {error}")
        raise UpstreamProviderError(
            "Invalid data format received from the search"
        ) from error

    return data_items
