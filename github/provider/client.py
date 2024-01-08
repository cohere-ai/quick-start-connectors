import requests
import logging
from base64 import b64decode
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

DEFAULT_SEARCH_LIMIT = 5
DEFAULT_QUERY_TEMPLATE = "{query} in:file"

client = None


class GithubClient:
    HEADER_GITHUB_API_VERSION = "2022-11-28"
    HEADER_ACCEPT = "application/vnd.github+json"
    SEARCH_ENDPOINT = "https://api.github.com/search/code"

    def __init__(self, token, search_limit, query_template):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": self.HEADER_ACCEPT,
            "X-GitHub-Api-Version": self.HEADER_GITHUB_API_VERSION,
        }
        self.search_limit = search_limit
        self.query_template = query_template

    def search(self, query):
        response = requests.get(
            self.SEARCH_ENDPOINT,
            headers=self.headers,
            params={
                "q": self.query_template.format(query=query),
                "per_page": self.search_limit,
            },
        )

        if response.status_code != 200:
            message = response.json().get(
                "message", f"Error: HTTP {response.status_code}"
            )
            raise UpstreamProviderError(message)

        return response.json()["items"]

    def fetch_and_decode_content(self, url):
        response = requests.get(
            url,
            headers=self.headers,
        )

        if not response.ok:
            logger.error(f"Error fetching GitHub file: {response.json()}")
            return None

        return b64decode(response.json()["content"]).decode()


def get_client():
    global client
    if not client:
        assert (token := app.config.get("TOKEN")), "GITHUB_TOKEN must be set"
        search_limit = app.config.get("SEARCH_LIMIT", DEFAULT_SEARCH_LIMIT)
        query_template = app.config.get("QUERY_TEMPLATE", DEFAULT_QUERY_TEMPLATE)
        client = GithubClient(token, search_limit, query_template)

    return client
