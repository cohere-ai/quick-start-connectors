import json

import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class YoutrackClient:
    ISSUE_FIELDS = [
        "idReadable",
        "comments",
        "commentsCount",
        "created",
        "description",
        "isDraft",
        "draftOwner",
        "project",
        "reporter",
        "resolved",
        "summary",
        "updated",
    ]

    def __init__(self, base_url, token):
        self.base_url = f"{base_url}/api"
        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def _make_request(self, method, url, params={}, data={}):
        response = requests.request(
            method,
            url,
            headers=self.headers,
            params=params,
            data=json.dumps(data),
        )

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def search_issues(self, query):
        url = f"{self.base_url}/issues"
        params = {
            "fields": ",".join(self.ISSUE_FIELDS),
            "query": query,
        }

        return self._make_request("GET", url, params)


def get_client():
    global client
    if client is not None:
        return client

    assert (base_url := app.config.get("BASE_URL")), "YOUTRACK_BASE_URL must be set"
    assert (
        token := app.config.get("PERMANENT_TOKEN")
    ), "YOUTRACK_PERMANENT_TOKEN must be set"
    client = YoutrackClient(base_url, token)
    return client
