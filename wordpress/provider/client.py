import requests
from flask import current_app as app, request
import asyncio
import aiohttp
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from . import UpstreamProviderError

DEFAULT_SEARCH_LIMIT = 20


class WordpressClient:
    SEARCH_ENDPOINT = "/?rest_route=/wp/v2/search"
    POSTS_ENDPOINT = "/?rest_route=/wp/v2/posts/"

    def __init__(self, base_url, username, password, search_limit=5):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.search_limit = search_limit
        self.session = None
        self.loop = None
        self._start_session()

    def _close_loop(self):
        self.loop.stop()
        self.loop.close()

    def _start_session(self):
        self.loop = asyncio.new_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def _close_session(self):
        await self.session.close()

    async def _gather_posts(self, posts):
        posts = [self._get_post(post) for post in posts]
        return await asyncio.gather(*posts)

    async def _get_post(self, post):
        url = f"{self.base_url}{self.POSTS_ENDPOINT}{post['id']}"

        async with self.session.get(
            url,
            auth=aiohttp.BasicAuth(self.username, self.password),
        ) as response:
            if not response.ok:
                return None
            content = await response.json()

            soup = BeautifulSoup(content["content"]["rendered"], "html.parser")
            post = {
                "title": content["title"]["rendered"],
                "text": soup.get_text(),
                "url": content["link"],
            }
            return post

    def _process_posts(self, posts):
        return self.loop.run_until_complete(self._gather_posts(posts))

    def search(self, query):
        params = {"search": query, "per_page": self.search_limit}
        url = urljoin(self.base_url, self.SEARCH_ENDPOINT)
        response = requests.get(url, params=params, auth=(self.username, self.password))
        if not response.ok:
            raise UpstreamProviderError(
                f"Error while searching Wordpress: {response.text}"
            )
        results = self._process_posts(response.json())
        self.loop.run_until_complete(self._close_session())
        self._close_loop()
        return results


def get_client():
    assert (base_url := app.config.get("URL")), "WORDPRESS_URL must be set"
    assert (username := app.config.get("USERNAME")), "WORDPRESS_USERNAME must be set"
    assert (password := app.config.get("PASSWORD")), "WORDPRESS_PASSWORD must be set"
    search_limit = app.config.get("SEARCH_LIMIT", DEFAULT_SEARCH_LIMIT)

    client = WordpressClient(base_url, username, password, search_limit)

    return client
