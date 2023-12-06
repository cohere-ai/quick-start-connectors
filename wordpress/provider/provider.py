import logging
from typing import Any
from urllib.parse import urljoin

import requests
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)


def extract_page_data(page_id):
    page_data = requests.get(
        urljoin(app.config["URL"], f"/?rest_route=/wp/v2/posts/{page_id}"),
        auth=(app.config["USERNAME"], app.config["PASSWORD"]),
    ).json()

    return {
        "title": page_data["title"]["rendered"],
        "text": page_data["content"]["rendered"],
        "url": page_data["link"],
    }


def search(query: str) -> list[dict[str, Any]]:
    assert (base_url := app.config.get("URL")), "WORDPRESS_URL must be set"
    assert (username := app.config.get("USERNAME")), "WORDPRESS_USERNAME must be set"
    assert (password := app.config.get("PASSWORD")), "WORDPRESS_PASSWORD must be set"

    url = urljoin(base_url, "/?rest_route=/wp/v2/search")
    params = {"search": query, "per_page": 10}

    response = requests.get(url, params=params, auth=(username, password))

    if not response.ok:
        raise UpstreamProviderError("Unable to query WordPress")

    results = response.json()
    search_data = [extract_page_data(page["id"]) for page in results]

    return search_data
