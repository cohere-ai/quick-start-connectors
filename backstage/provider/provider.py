import logging

import requests
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)


def prepare_for_serialization(data, server_url):
    prepared_data = []
    for item in data:
        to_append = item.copy()
        for key, value in item.items():
            if key == "document":
                for d_key, d_value in value.items():
                    to_append[d_key] = (
                        f"{server_url}{d_value}" if d_key == "location" else d_value
                    )
                to_append.pop(key)
        if "highlight" in to_append:
            to_append.pop("highlight")
        prepared_data.append(to_append)

    return prepared_data


def serialize_results(data, mappings):
    """
    Serialize a list of dictionaries by transforming keys based on provided mappings
    and converting values to strings.

    Parameters:
    - data (list): A list of dictionaries to be serialized.
    - mappings (dict): A dictionary specifying key mappings for transformation.

    Returns:
    list: A serialized list of dictionaries with transformed keys and string-converted values.
    """
    serialized_data = list(
        map(
            lambda item: {
                k if k not in mappings else mappings[k]: (
                    ", ".join(str(vl) for vl in v) if isinstance(v, list) else str(v)
                )
                for k, v in item.items()
            },
            data,
        )
    )
    return serialized_data


def search(query):
    assert (host := app.config.get("SERVER_URL")), "BACKSTAGE_SERVER_URL must be set"
    search_endpoint = app.config.get("SEARCH_ENDPOINT", "/api/search/query")
    search_term = app.config.get("SEARCH_TERM", "term")
    token = app.config.get("ACCESS_TOKEN", None)
    search_url = f"{host}{search_endpoint}?{search_term}={query}"

    headers = None
    if token:
        headers = {
            "Authorization": f"Bearer {token}",
        }

    kwargs = {
        "url": search_url,
    }
    if headers:
        kwargs["headers"] = headers

    response = requests.get(**kwargs)

    if response.status_code != 200:
        message = response.text or f"Error: HTTP {response.status_code}"
        raise UpstreamProviderError(message)

    mappings = app.config.get("CONNECTOR_FIELDS_MAPPING", {})
    results = prepare_for_serialization(response.json().get("results", []), host)
    return serialize_results(results, mappings)
