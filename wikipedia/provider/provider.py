import logging
import re
from typing import Any

from .client import get_client

logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    wikipedia_client = get_client()

    search_results = wikipedia_client.search_articles(query)

    results = []
    for page in search_results:
        results.append(serialize_search_result(page))

    return results


def strip_html_tags(html_text):
    clean = re.compile("<.*?>")
    plain_text = re.sub(clean, "", html_text)
    return plain_text


def serialize_search_result(result):
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_result = {
        key: str(value)
        for key, value in result.items()
        if isinstance(value, (str, int, bool))
    }

    if "text" in stripped_result:
        stripped_result["text"] = strip_html_tags(stripped_result["text"])

    # Build URL manually with pageid
    if "pageid" in result:
        wikipedia_client = get_client()
        stripped_result["url"] = (
            f"{wikipedia_client.BASE_ARTICLE_URL}{stripped_result['pageid']}"
        )

    return stripped_result
