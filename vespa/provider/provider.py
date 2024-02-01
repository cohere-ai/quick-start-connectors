import json
import logging
from urllib.parse import urljoin

import requests
from flask import current_app as app

logger = logging.getLogger(__name__)


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
    assert (server_url := app.config.get("SERVER_URL")), "VESPA_SERVER_URL must be set"

    vespa_search_url = urljoin(server_url, "/search/")
    search_request = {
        "yql": "select * from sources * where userQuery()",
        "query": query,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        vespa_search_url, data=json.dumps(search_request), headers=headers
    )
    response.raise_for_status()
    results = response.json()["root"].get("children", [])
    mappings = app.config.get("CONNECTOR_FIELD_MAPPING", {})
    return serialize_results([result["fields"] for result in results], mappings)
