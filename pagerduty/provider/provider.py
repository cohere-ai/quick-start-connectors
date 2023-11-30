import logging
from typing import Any

from .client import get_client
from .enums import SearchTypes

logger = logging.getLogger(__name__)

BASE_PATH = "https://api.pagerduty.com"


def search(query) -> list[dict[str, Any]]:
    client = get_client()
    search_type_method_mapping = {
        SearchTypes.INCIDENTS.value: client.search_incidents,
        SearchTypes.USERS.value: client.search_users,
        SearchTypes.TEAMS.value: client.search_teams,
    }

    search_results = []
    for search_type in client.get_search_types():
        if search_type in search_type_method_mapping.keys():
            results = search_type_method_mapping[search_type](query)
            search_results.extend(results)

    return search_results
