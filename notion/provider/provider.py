import logging
from typing import Any


from .client import get_client

logger = logging.getLogger(__name__)


def decorate_and_serialize_search_results(page):
    """
    By default Notion does not return page contents, need to fetch each child block of a
    page and stick together to form the text.
    """
    notion_client = get_client()

    if page.get("id") is None:
        return

    blocks = notion_client.retrieve_child_blocks(page["id"])

    text = ""
    # Notion will return a sub-dictionary keyed by the type of block that contains
    # the plain-text we are looking for
    for block in blocks:
        type = block.get("type")
        if type in block:
            rich_text = block[type].get("rich_text", [])
            if rich_text:
                text += rich_text[0]["plain_text"]

    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_page = {
        key: str(value)
        for key, value in page.items()
        if isinstance(value, (str, int, bool))
    }

    data = {
        **stripped_page,
        "text": text,
    }

    if (title := page.get("properties", {}).get("title")) is not None:
        data["title"] = title["title"][0]["plain_text"]

    return data


def search(query) -> list[dict[str, Any]]:
    notion_client = get_client()

    search_results = notion_client.search_documents(query)

    results = []
    for page in search_results:
        results.append(decorate_and_serialize_search_results(page))

    return results
