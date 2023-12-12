import functools
import sys

import asyncio
import aiohttp
import logging
from collections import OrderedDict
from flask import current_app as app

logger = logging.getLogger(__name__)

CACHE_LIMIT_BYTES = 20 * 1024 * 1024  # 20 MB to bytes

unstructured = None


class UnstructuredRequestSession:
    def __init__(self, unstructured_base_url, api_key):
        self.get_content_url = f"{unstructured_base_url}/general/v0/general"
        # API key optional if self-hosted
        self.headers = {"unstructured-api-key": api_key} if api_key else {}
        # Manually cache because functools.lru_cache does not support async methods
        self.cache = OrderedDict()
        self.start_session()

    def start_session(self):
        self.loop = asyncio.new_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    def close_loop(self):
        self.loop.stop()
        self.loop.close()

    def cache_get(self, key):
        self.cache.move_to_end(key)

        return self.cache[key]

    def cache_size(self):
        # Calculate the total size of values in bytes
        total_size_bytes = functools.reduce(
            lambda a, b: a + b, map(lambda v: sys.getsizeof(v), self.cache.values()), 0
        )

        return total_size_bytes

    def cache_put(self, key, item):
        self.cache[key] = item

        while self.cache_size() > CACHE_LIMIT_BYTES:
            self.cache.popitem()

    async def close_session(self):
        await self.session.close()

    async def get_unstructured_content(self, attachment):
        file_id = attachment["id"]
        file_name = attachment["name"]
        file_data = attachment["content"]

        # Check cache
        if file_id in self.cache:
            return self.cache_get(file_id)

        # Use FormData to pass in files parameter
        data = aiohttp.FormData()
        data.add_field("files", file_data, filename=file_name)

        async with self.session.post(
            self.get_content_url,
            headers=self.headers,
            data=data,
        ) as response:
            content = await response.json()
            if not response.ok:
                logger.error(f"Error response from Unstructured: {content}")
                return None

            if content is not None:
                # Build text
                text = ""
                for element in content:
                    text += f' {element.get("text")}'
                attachment["content"] = text
            # Cache result
            self.cache_put(file_id, (file_name, attachment))

            return self.cache[file_id]

    async def gather(self, attachments):
        tasks = [
            self.get_unstructured_content(attachment) for attachment in attachments
        ]
        return await asyncio.gather(*tasks)

    def batch_get(self, attachments):
        results = self.loop.run_until_complete(self.gather(attachments))
        results = [result for result in results if result is not None]

        result_dict = {
            attachment["id"]: attachment
            for filename, attachment in results
            if attachment is not None
        }

        # Close session and loop
        self.loop.run_until_complete(self.close_session())
        self.close_loop()

        return result_dict


def get_unstructured_client():
    global unstructured
    if unstructured is not None:
        return unstructured

    # Fetch environment variables
    assert (
        unstructured_base_url := app.config.get("UNSTRUCTURED_BASE_URL")
    ), "MSTEAMS_UNSTRUCTURED_BASE_URL must be set"
    api_key = app.config.get("UNSTRUCTURED_API_KEY", None)

    unstructured = UnstructuredRequestSession(unstructured_base_url, api_key)

    return unstructured
