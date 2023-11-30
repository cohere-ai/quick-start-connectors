import functools
import asyncio
import aiohttp
import logging

TIMEOUT = aiohttp.ClientTimeout(total=15)
loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)


def perform(id_to_urls: dict[str, str], access_token: str) -> dict[str, str]:
    return loop.run_until_complete(_download_files(id_to_urls, access_token))


async def _download_files(
    id_to_urls: dict[str, str], access_token: str
) -> dict[str, str]:
    async with aiohttp.ClientSession() as session:
        tasks = [
            _download(session, id, url, access_token)
            for (id, url) in id_to_urls.items()
        ]
        id_to_texts = await asyncio.gather(*tasks)
        return functools.reduce(lambda x, y: x | y, id_to_texts)


async def _download(
    session: aiohttp.ClientSession, id: str, url: str, access_token: str
):
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        async with session.get(url, headers=headers, timeout=TIMEOUT) as response:
            return {id: await response.text()}
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return {}
