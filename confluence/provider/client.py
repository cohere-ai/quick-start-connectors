import asyncio
import aiohttp
import base64
import functools
import logging
import requests
import sys

from collections import OrderedDict
from flask import current_app as app

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

client = None


class ConfluenceClient:
    # Page consts
    PAGE_TYPE = "type"
    PAGE_BODY_FORMAT = "storage"

    # Timeout for async requests
    TIMEOUT_SECONDS = 20

    # Cache size limit to reduce memory over time
    CACHE_LIMIT_BYTES = 20 * 1024 * 1024  # 20 MB to bytes

    def __init__(self, url, user, api_token, search_limit=10):
        self.base_url = url
        self.user = user
        self.api_token = api_token
        self.search_limit = search_limit
        # Manually cache because functools.lru_cache does not support async methods
        self.cache = OrderedDict()
        self.loop = None

    def _cache_size(self):
        # Calculate the total size of values in bytes
        total_size_bytes = functools.reduce(
            lambda a, b: a + b, map(lambda v: sys.getsizeof(v), self.cache.values()), 0
        )

        return total_size_bytes

    def _cache_get(self, key):
        self.cache.move_to_end(key)

        return self.cache[key]

    def _cache_put(self, key, item):
        self.cache[key] = item

        while self._cache_size() > self.CACHE_LIMIT_BYTES:
            self.cache.popitem()

    def _start_session(self):
        self.loop = asyncio.new_event_loop()
        # Create ClientTimeout object to apply timeout for every request in the session
        client_timeout = aiohttp.ClientTimeout(total=self.TIMEOUT_SECONDS)
        self.session = aiohttp.ClientSession(loop=self.loop, timeout=client_timeout)

    async def _close_session(self):
        await self.session.close()

    def _close_session_and_loop(self):
        # Close session and loop, session closing must be done in an async method
        self.loop.run_until_complete(self._close_session())
        self.loop.stop()
        self.loop.close()

    async def _gather(self, pages):
        tasks = [self._get_page(page["id"]) for page in pages if self.PAGE_TYPE in page]

        return await asyncio.gather(*tasks)

    async def _get_page(self, page_id):
        # Check cache
        if page_id in self.cache:
            return self._cache_get(page_id)

        get_page_by_id_url = f"{self.base_url}/wiki/api/v2/pages/{page_id}"
        credentials = f"{self.user}:{self.api_token}"
        credentials_encoded = base64.b64encode(credentials.encode()).decode("ascii")
        params = {"body-format": self.PAGE_BODY_FORMAT}

        async with self.session.get(
            get_page_by_id_url,
            headers={"Authorization": f"Basic {credentials_encoded}"},
            params=params,
        ) as response:
            if not response.ok:
                logger.error(f"Error response from Confluence: {response.text}")
                return None

            content = await response.json()

            serialized_page = {
                "title": content["title"],
                "text": content["body"][self.PAGE_BODY_FORMAT]["value"],
                "url": get_page_by_id_url,
            }

            # Update cache
            self._cache_put(page_id, serialized_page)
            return self._cache_get(page_id)

    def search_pages(self, query):
        search_url = f"{self.base_url}/wiki/rest/api/content/search"

        params = {"cql": f"text ~ {query}", "limit": self.search_limit}

        response = requests.get(
            search_url,
            auth=(self.user, self.api_token),
            params=params,
        )

        if response.status_code != 200:
            raise UpstreamProviderError(
                f"Error during Confluence search: {response.text}"
            )

        return response.json().get("results", [])

    def fetch_pages(self, pages):
        self._start_session()
        results = self.loop.run_until_complete(self._gather(pages))
        self._close_session_and_loop()

        return results

    def search(self, query):
        pages = self.search_pages(query)

        return [page for page in self.fetch_pages(pages) if page is not None]


def get_client():
    global client
    if client is None:
        assert (
            url := app.config.get("PRODUCT_URL")
        ), "CONFLUENCE_PRODUCT_URL must be set"
        assert (user := app.config.get("USER")), "CONFLUENCE_USER must be set"
        assert (
            api_token := app.config.get("API_TOKEN")
        ), "CONFLUENCE_API_TOKEN must be set"
        search_limit = app.config.get("SEARCH_LIMIT", 10)
        client = ConfluenceClient(url, user, api_token, search_limit)

    return client
