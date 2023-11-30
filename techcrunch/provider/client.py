import logging

import requests
from bs4 import BeautifulSoup

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

client = None


class TechCrunchScraper:
    SEARCH_URL = "https://search.techcrunch.com/search"

    def process_search(self, query):
        html_page = requests.get(self.SEARCH_URL, params={"p": query})
        soup = BeautifulSoup(html_page.content, "html.parser")
        results = []
        try:
            article_list = soup.find("ul", {"class": "compArticleList"})
            for article in article_list.children:
                if article.name == "li":
                    article_data = {
                        "title": article.find("h4").find("a").text,
                        "url": article.find("a", {"class": "thmb"})["href"],
                        "text": article.find("p").text,
                        "image": article.find("img")["src"],
                    }
                    results.append(article_data)
        except Exception as e:
            raise UpstreamProviderError(e)
        return results


def get_client():
    global client
    if not client:
        client = TechCrunchScraper()

    return client
