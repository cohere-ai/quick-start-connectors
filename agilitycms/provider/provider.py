import logging

from flask import current_app as app

from .client import get_client

logger = logging.getLogger(__name__)


def serialize_results(data):
    results = data["items"] if data["items"] else []
    serialized_data = []
    for result in results:
        to_append = result
        if result["fields"]:
            for field, value in result["fields"].items():
                if field == "content":
                    to_append["text"] = value
                else:
                    to_append[field] = value
        to_append.pop("fields")
        to_append = {key: str(value) for key, value in to_append.items()}
        serialized_data.append(to_append)
    return serialized_data


def build_filter(query_string, fields=["fields.title", "fields.content"]):
    filter_parts = []
    for field in fields:
        filter_parts.append(f'{field}[like]"{query_string}"')

    return " or ".join(filter_parts)


def search_posts(client, query, limit):
    params = {
        "reference_name": "posts",
        "take": limit,
        "filter_": build_filter(query),
        "content_link_depth": 1,
        "expand_all_content_links": True,
    }
    posts = client.list(**params)
    return posts


def search(query):
    assert (api_domain := app.config.get("API_URL")), "AGILITYCMS_API_URL must be set"
    assert (api_guid := app.config.get("API_GUID")), "AGILITYCMS_API_GUID must be set"
    assert (api_key := app.config.get("API_KEY")), "AGILITYCMS_API_KEY must be set"
    assert (
        api_locale := app.config.get("API_LOCALE")
    ), "AGILITYCMS_API_LOCALE must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 20)

    client = get_client(api_domain, api_guid, api_key, api_locale)
    results = search_posts(client, query, search_limit)
    return serialize_results(results)
