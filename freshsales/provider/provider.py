import logging
from typing import Any

from .enums import EntityChoices
from .client import get_client


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    freshsales_client = get_client()
    search_results = freshsales_client.search(query)

    results = []
    # Contact, Sales Account and Deals can be fetched with extra details
    for entry in search_results:
        type = entry["type"]
        decorated_entry = None
        if type == EntityChoices.CONTACT.value:
            decorated_entry = freshsales_client.get_contact_details(entry["id"])
        elif type == EntityChoices.SALES_ACCOUNT.value:
            decorated_entry = freshsales_client.get_sales_account_details(entry["id"])
        elif type == EntityChoices.DEAL.value:
            decorated_entry = freshsales_client.get_deal_details(entry["id"])

        if decorated_entry is not None:
            entry = decorated_entry

        results.append(serialize_result(entry))

    return results


def serialize_result(entry):
    serialized_result = {}

    for key, value in entry.items():
        serialized_result[key] = (
            str(value)
            if not isinstance(value, list)
            else ", ".join(str(vl) for vl in value)
        )

    return serialized_result
