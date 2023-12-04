import logging

from bs4 import BeautifulSoup

from .client import get_client

logger = logging.getLogger(__name__)

cached_pages = {}
token = None


def strip_html_tags(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()


def serialize_results(results):
    return [
        {
            "title": result["subject"],
            "text": strip_html_tags(result["body"]["content"]),
            "url": result["webLink"],
            "date": result["receivedDateTime"],
            "author": result["from"]["emailAddress"]["name"],
            "from": result["from"]["emailAddress"]["address"],
            "has_attachments": str(result["hasAttachments"]),
        }
        for result in results
    ]


def search(query):
    client = get_client()
    results = client.search(query)
    return serialize_results(results)
