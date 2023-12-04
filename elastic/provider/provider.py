import logging

from elasticsearch import Elasticsearch
from flask import current_app as app

logger = logging.getLogger(__name__)
es_client = None

MIN_TEXT_LENGTH = 25


def create_es_client():
    connection_params = {}

    if cloud_id := app.config.get("CLOUD_ID"):
        connection_params["cloud_id"] = cloud_id
    elif url := app.config.get("URL"):
        connection_params["hosts"] = [url]
    else:
        raise ValueError("Either ELASTIC_CLOUD_ID or ELASTIC_URL env vars must be set.")

    if api_key := app.config.get("API_KEY"):
        connection_params["api_key"] = api_key
    elif (user := app.config.get("USER")) and (password := app.config.get("PASS")):
        connection_params["basic_auth"] = (user, password)
    else:
        raise ValueError(
            "Either ELASTIC_APIKEY or both ELASTIC_USER and ELASTIC_PASS env vars must be set."
        )

    return Elasticsearch(**connection_params)


def build_text(match):
    if "highlight" in match:
        return match["highlight"]["content"][0]

    text = ""
    for value in match["_source"].values():
        if isinstance(value, str) and len(value) >= MIN_TEXT_LENGTH:
            text += value

    return text


def serialize_result(match):
    source = match["_source"]
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_source = {
        key: str(value)
        for key, value in source.items()
        if isinstance(value, (str, int, bool))
    }

    return {
        **stripped_source,
        "text": build_text(match),
    }


def search(query):
    global es_client

    if not es_client:
        es_client = create_es_client()

    es_query_body = {
        "query": {"multi_match": {"query": query}},
        "highlight": {"pre_tags": [""], "post_tags": [""], "fields": {"content": {}}},
    }

    response = es_client.search(index=app.config["INDEX"], body=es_query_body, size=20)

    results = []
    for match in response["hits"]["hits"]:
        results.append(serialize_result(match))

    return results
