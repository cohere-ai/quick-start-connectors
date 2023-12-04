import base64
import logging

import requests
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)


def serialize_results(data):
    """
    Serialize a list of dictionaries by getting the values of the needed keys and transforming them into a string.
    """

    results = []
    for item in data:
        result = {
            "title": item["subject"] if "subject" in item and item["subject"] else "",
            "text": item["description"]
            if "description" in item and item["description"]
            else "",
            "url": item["url"] if "url" in item and item["url"] else "",
            "tags": ", ".join(item["tags"])
            if "tags" in item and isinstance(item["tags"], list)
            else "",
        }
        for key, value in item.items():
            if key not in ["subject", "description", "url", "tags"]:
                result.update({key: str(value)})

        results.append(result)

    return results


def search(query):
    assert (email := app.config.get("EMAIL")), "ZENDESK_EMAIL must be set"
    assert (domain := app.config.get("DOMAIN")), "ZENDESK_DOMAIN must be set"
    assert (token := app.config.get("API_TOKEN")), "ZENDESK_API_TOKEN must be set"

    per_page = app.config.get("SEARCH_LIMIT", 20)

    credentials = f"{email}/token:{token}"
    auth_header = {
        "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}"
    }
    search_url = f"https://{domain}/api/v2/search.json"
    params = {"query": query, "per_page": per_page}

    response = requests.get(search_url, params=params, headers=auth_header)

    if response.status_code != 200:
        raise UpstreamProviderError(f"Failed to query Zendesk: {response.text}")

    return serialize_results(response.json().get("results", []))
