import logging

import opsgenie_sdk
from flask import current_app as app
from opsgenie_sdk.exceptions import ApiException

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

incident_api = None


def prepare_query(query: object) -> object:
    prepared = "".join(("*", "*".join(query.split(" ")), "*"))
    return f"message={prepared} OR tag={prepared}"


def serialize_results(data):
    """
    Serialize a list of dictionaries by getting the values of the needed keys and transforming them into a string.
    """
    assert (domain := app.config.get("DOMAIN_URL")), "OPSGENIE_DOMAIN_URL must be set"
    results = []
    for item in data:
        result = {
            "text": item["message"] if "message" in item and item["message"] else "",
            "url": f"{domain}/incident/detail/{item['id']}",
            "tags": (
                ", ".join(item["tags"])
                if "tags" in item and isinstance(item["tags"], list)
                else ""
            ),
        }
        for key, value in item.items():
            if key not in ["message", "tags"]:
                result.update({key: str(value)})

        results.append(result)

    return results


def search(query):
    global incident_api
    assert (api_key := app.config.get("API_KEY")), "OPSGENIE_API_KEY must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 20)
    results = []
    if not incident_api:
        conf = opsgenie_sdk.configuration.Configuration()
        conf.api_key["Authorization"] = api_key
        client = opsgenie_sdk.api_client.ApiClient(configuration=conf)
        incident_api = opsgenie_sdk.IncidentApi(api_client=client)

    try:
        query = prepare_query(query)
        list_response = incident_api.list_incidents(query, limit=search_limit)
        if "data" in list_response.to_dict():
            results = list_response.to_dict()["data"]
    except ApiException as err:
        raise UpstreamProviderError(f"Failed to query Opsgenie: {err}")

    return serialize_results(results)
