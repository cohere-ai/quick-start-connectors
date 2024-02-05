import logging
from functools import reduce

from .client import get_client

logger = logging.getLogger(__name__)


def get_dict_value_by_dotted_key(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def search_publications(publications, query):
    results = []
    keywords = query.split(" ")
    if "data" in publications:
        for publication in publications["data"]:
            if any(
                keyword.lower() in publication["name"].lower() for keyword in keywords
            ) or any(
                keyword.lower() in publication["description"].lower()
                for keyword in keywords
            ):
                publication["title"] = publication.pop("name")
                publication["text"] = publication.pop("description")
                results.append({k: str(v) for k, v in publication.items()})

    return results


def serialize_graphql_results(data):
    results = []
    if peoples := get_dict_value_by_dotted_key(data, "data.search.people.items"):
        for people in peoples:
            item_to_append = people
            item_to_append["title"] = people.pop("name")
            item_to_append["text"] = people.pop("bio")
            url = get_dict_value_by_dotted_key(people, "customDomainState.live.domain")
            if url:
                item_to_append["url"] = f"https://{url}"
            else:
                item_to_append["url"] = f"https://medium.com/@{people['username']}"
            results.append({k: str(v) for k, v in item_to_append.items()})
    if tags := get_dict_value_by_dotted_key(data, "data.search.tags.items"):
        for tag in tags:
            item_to_append = tag
            item_to_append["title"] = tag.pop("displayTitle")
            item_to_append["text"] = tag.pop("id")
            url = tag.pop("normalizedTagSlug", None)
            if url:
                item_to_append["url"] = f"https://medium.com/tag/{url}"
            results.append({k: str(v) for k, v in item_to_append.items()})
    if posts := get_dict_value_by_dotted_key(data, "data.search.posts.items"):
        for post in posts:
            item_to_append = post
            item_to_append["title"] = post.pop("title")
            paragraphs = get_dict_value_by_dotted_key(
                post, "extendedPreviewContent.bodyModel.paragraphs"
            )
            if paragraphs:
                all_text = ""
                for paragraph in paragraphs:
                    all_text += paragraph["text"]
                item_to_append["text"] = all_text
            url = post.get("mediumUrl", None)
            if url:
                item_to_append["url"] = url
            results.append({k: str(v) for k, v in item_to_append.items()})
    if publications := get_dict_value_by_dotted_key(
        data, "data.search.collections.items"
    ):
        for publication in publications:
            item_to_append = publication
            item_to_append["title"] = publication.pop("name")
            item_to_append["text"] = publication.pop("shortDescription")
            url = publication.pop("slug", None)
            if url:
                item_to_append["url"] = f"https://medium.com/{url}"
            results.append({k: str(v) for k, v in item_to_append.items()})
    if catalogs := get_dict_value_by_dotted_key(data, "data.search.catalogs.items"):
        for catalog in catalogs:
            item_to_append = catalog
            item_to_append["title"] = catalog.pop("name")
            if "text" not in item_to_append:
                if text := catalog.get("description"):
                    item_to_append["text"] = text
                else:
                    item_to_append["text"] = item_to_append["title"]

            creator_name = catalog["creator"].pop("username", None)
            if creator_name:
                item_to_append["url"] = (
                    f"https://medium.com/@{creator_name}/list/{catalog.get('id')}"
                )
            results.append({k: str(v) for k, v in item_to_append.items()})

    return results


def search(query):
    client = get_client()
    if not client.is_graph_ql_used():
        user = client.get_user()
        if not user:
            return []
        user_publications = client.get_user_publications(user["data"]["id"])
        search_results = search_publications(user_publications, query)
    else:
        search_results = serialize_graphql_results(client.get_graphql_results(query))

    return search_results
