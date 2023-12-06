import logging
import os
from typing import Any

import requests
from flask import current_app as app

from . import UpstreamProviderError
from .enums import EntityChoices
from .constants import (
    BASE_PATH,
    API_TOKEN,
    RESULTS_LIMIT,
    ENTITY_ENV_VAR_ENABLED_MAPPING,
    CONTACT_PARAMETERS,
    SALES_ACCOUNT_PARAMETERS,
    DEAL_PARAMETERS,
)


logger = logging.getLogger(__name__)


"""
Builds the entity list string for the `includes` query parameter, based
off environment variables.

For example, the default returned format will look like 'user,contact,sales_account,deal'
See: https://developers.freshworks.com/crm/api/#search
"""


def get_entity_types() -> str:
    def is_env_var_true(env_var_name):
        value = app.config.get(env_var_name, "False")
        return value.lower() == "true"

    entities = [
        enum.value
        for enum, env_var in ENTITY_ENV_VAR_ENABLED_MAPPING.items()
        if is_env_var_true(env_var)
    ]
    return ",".join(entities)


def get_contact_details(id):
    url = f"{BASE_PATH}/contacts/{id}"
    params = {"include": ",".join(CONTACT_PARAMETERS)}
    headers = {
        "Authorization": f"Token token={API_TOKEN}",
    }
    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        return None

    return response.json()


def get_sales_account_details(id):
    url = f"{BASE_PATH}/sales_accounts/{id}"
    params = {"include": ",".join(SALES_ACCOUNT_PARAMETERS)}
    headers = {
        "Authorization": f"Token token={API_TOKEN}",
    }
    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        return None

    return response.json()


def get_deal_details(id):
    url = f"{BASE_PATH}/deals/{id}"
    params = {"include": ",".join(DEAL_PARAMETERS)}
    headers = {
        "Authorization": f"Token token={API_TOKEN}",
    }
    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        return None

    return response.json()


def search(query) -> list[dict[str, Any]]:
    assert API_TOKEN, "FRESHSALES_API_KEY must be set"

    url = f"{BASE_PATH}/search"
    entities = get_entity_types()

    params = {
        "q": query,
        "include": entities,
        "per_page": RESULTS_LIMIT,
    }
    headers = {
        "Authorization": f"Token token={API_TOKEN}",
    }
    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    results = []
    # Contact, Sales Account and Deals can be fetched with extra details
    for entry in response.json():
        type = entry["type"]
        decorated_entry = None
        if type == EntityChoices.CONTACT.value:
            decorated_entry = get_contact_details(entry["id"])
        elif type == EntityChoices.SALES_ACCOUNT.value:
            decorated_entry = get_sales_account_details(entry["id"])
        elif type == EntityChoices.DEAL.value:
            decorated_entry = get_deal_details(entry["id"])

        if decorated_entry is not None:
            results.append(decorated_entry)
        else:
            results.append(entry)

    return results
