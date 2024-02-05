import logging
from typing import Any


from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    knowledgeowl_client = get_client()

    search_results = knowledgeowl_client.search_articles(query)

    results = []
    for page in search_results:
        results.append(serialize_search_result(page))

    return results


def serialize_search_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_result = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "name" in stripped_result:
        stripped_result["title"] = stripped_result.pop("name")

    if "summary" in stripped_result:
        stripped_result["text"] = stripped_result.pop("summary")

    # Both fields required to build URL manually
    if all(key in stripped_result for key in ["project_id", "id"]):
        knowledgeowl_client = get_client()
        stripped_result["url"] = (
            f"{knowledgeowl_client.article_base_url}/{stripped_result['project_id']}/aid/{stripped_result['id']}"
        )

    return stripped_result
