import logging
import requests
import itertools
import functools
from .client import get_client
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 16


@dataclass
class Context:
    session: requests.Session
    unstructured_base_url: str
    unstructured_api_key: str
    file_extensions: str


def get_content(ctx: Context, item):
    """
    Retrieve file contents in a parsable JSON format using Unstructured.
    See README for more details.
    """
    files = {"files": (item.name, item.content())}
    headers = {
        "Accept": "application/json",
        "unstructured-api-key": ctx.unstructured_api_key,
    }

    try:
        response = ctx.session.post(
            f"{ctx.unstructured_base_url}/general/v0/general",
            headers=headers,
            files=files,
            data={"strategy": "fast"},
            timeout=TIMEOUT_SECONDS,
        )
    except requests.exceptions.Timeout:
        logger.error(f"Timeout from Unstructured parsing: {item.name}")
        return

    if not response.ok:
        logger.error(f"Error from Unstructured: {response.json()}")
        return

    content = ""
    for element in response.json():
        content += f' {element.get("text")}'

    return {
        "id": item.id,
        "title": item.name,
        "url": f"https://app.box.com/file/{item.id}",
        "text": content,
    }


def search(query):
    limit = app.config.get("SEARCH_LIMIT", 2)
    file_extensions = app.config.get("FILE_EXTENSIONS", "pdf,doc,docx,txt")
    box_client = get_client()

    try:
        search_results = box_client.search().query(
            query=query,
            limit=limit,
            result_type="file",
            fields=["name", "id", "content"],
            file_extensions=file_extensions.split(","),
        )

    except Exception as e:
        raise UpstreamProviderError(str(e)) from e

    assert (
        unstructured_base_url := app.config.get("UNSTRUCTURED_BASE_URL")
    ), "BOX_UNSTRUCTURED_BASE_URL must be set"
    unstructured_key = app.config.get("UNSTRUCTURED_API_KEY")

    context = Context(
        session=requests.Session(),
        unstructured_base_url=unstructured_base_url,
        unstructured_api_key=unstructured_key,
        file_extensions=file_extensions,
    )

    # bind context to provide each thread with a copy of necessary configuration
    get_content_with_context = functools.partial(get_content, context)

    with app.app_context():
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = list(
                pool.map(
                    get_content_with_context, itertools.islice(search_results, limit)
                )
            )

    return results
