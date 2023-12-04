import asyncio
import functools

from atlassian import Confluence
from flask import current_app as app

from . import UpstreamProviderError

client = None


class ConfluenceClient:
    def __init__(self, url, user, password, space, search_limit=10):
        try:
            self.confluence = Confluence(
                url=url,
                username=user,
                password=password,
            )
            self.space = space
            self.search_limit = search_limit
            self.loop = None
        except Exception as e:
            raise UpstreamProviderError(
                f"Error while initializing Confluence client: {str(e)}"
            )

    def _init_loop(self):
        self.loop = asyncio.new_event_loop()

    def _close_loop(self):
        self.loop.stop()
        self.loop.close()

    async def _gather(self, pages, results):
        tasks = []
        for page in pages:
            page_id = page["content"]["id"]
            tasks.append(self._fetch_page(page_id, results))
        return await asyncio.gather(*tasks)

    async def _fetch_page(self, page_id, fetch_results):
        page_base_url = self.confluence.url + "/spaces/" + self.space + "/pages/"
        full_page = await self.loop.run_in_executor(
            None,
            functools.partial(
                self.confluence.get_page_by_id, page_id=page_id, expand="body.view"
            ),
        )
        page = {
            "title": full_page["title"],
            "text": full_page["body"]["view"]["value"],
            "url": page_base_url + page_id,
        }
        fetch_results.append(page)

    def search_pages(self, query):
        results = self.confluence.cql('text ~ "' + query + '"', limit=self.search_limit)
        return results["results"] if results and "results" in results else []

    def fetch_pages(self, pages):
        results = []
        self._init_loop()
        self.loop.run_until_complete(self._gather(pages, results))
        self._close_loop()
        return results

    def search(self, query):
        pages = self.search_pages(query)
        return self.fetch_pages(pages)


def get_client():
    global client
    if client is not None:
        return client

    assert (url := app.config.get("PRODUCT_URL")), "CONFLUENCE_PRODUCT_URL must be set"
    assert (user := app.config.get("USER")), "CONFLUENCE_USER must be set"
    assert (password := app.config.get("API_TOKEN")), "CONFLUENCE_API_TOKEN must be set"
    assert (space := app.config.get("SPACE_NAME")), "CONFLUENCE_SPACE_NAME must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 10)
    client = ConfluenceClient(url, user, password, space, search_limit)

    return client
