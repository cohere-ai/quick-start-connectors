import logging
from urllib.parse import urljoin

import requests
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)
POST_LIMIT = 10


def extract_post_data(post_json):
    return {
        "text": post_json.get("raw"),
        "link": urljoin(
            app.config["API_HOST"],
            f"/t/{post_json.get('topic_slug')}/{post_json.get('topic_id')}",
        ),
        "username": post_json.get("username"),
        "created_at": post_json.get("created_at"),
        "reply_count": post_json.get("reply_count"),
        "reactions": post_json.get("reactions"),
    }


def search(query):
    headers = {
        "Accept": "application/json",
        "Api-Key": app.config["API_KEY"],
        "Api-Username": app.config["API_USERNAME"],
    }
    search_url = urljoin(app.config["API_HOST"], "/search")
    response = requests.get(search_url, params={"q": query}, headers=headers)

    if response.status_code != 200:
        logger.error(f"Failed to query {search_url}")
        raise UpstreamProviderError(f"Failed to query {search_url}")

    post_url = urljoin(app.config["API_HOST"], "/posts/")
    posts = [
        extract_post_data(
            requests.get(post_url + str(result["id"]), headers=headers).json()
        )
        for result in response.json()["posts"][:POST_LIMIT]
    ]

    return posts
