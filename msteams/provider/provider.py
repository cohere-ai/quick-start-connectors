import logging

from bs4 import BeautifulSoup
from .unstructured import get_unstructured_client
from .client import get_client

logger = logging.getLogger(__name__)

cached_pages = {}
token = None


def strip_html_tags(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()


def serialize_results(results):
    serialized_results = []
    for result in results:
        data_to_append = {
            "id": str(result["id"]),
            "text": strip_html_tags(result["body"]["content"]),
            "summary": str(result["summary"]),
            "url": str(
                result["link"]
                if "link" in result
                else result["webUrl"] if "webUrl" in result else ""
            ),
            "has_attachments": str(len(result["attachments"]) > 0),
            "date": str(result["createdDateTime"]),
        }
        if "subject" in result:
            data_to_append["title"] = str(result["subject"])

        serialized_results.append(data_to_append)

    return serialized_results


def prepare_attachments_to_parse(results):
    attachments_to_parse = []
    for result in results:
        attachments_to_parse.extend(
            [
                attachment
                for attachment in result["attachments"]
                if attachment["contentType"] == "reference"
            ]
        )
    return attachments_to_parse


def update_attachments_content(results, parsed_results):
    for result in results:
        for attachment in result["attachments"]:
            attachment["content"] = (
                parsed_results[attachment["id"]]["content"]
                if attachment["id"] in parsed_results
                else ""
            )
            result["body"]["content"] += attachment["content"]


def parse_results_attachments(results):
    attachments_to_unstructured = prepare_attachments_to_parse(results)
    if len(attachments_to_unstructured) > 0:
        unstructured_client = get_unstructured_client()
        unstructured_client.start_session()
        unstructured_results = unstructured_client.batch_get(
            attachments_to_unstructured
        )
        update_attachments_content(results, unstructured_results)
    return results


def filter_results_by_query(results, query):
    filtered_results = []
    keywords = query.split()
    for result in results:
        if any(
            keyword.lower() in result["body"]["content"].lower() for keyword in keywords
        ):
            filtered_results.append(result)
    return filtered_results


def search(query):
    client = get_client()
    results = client.search(query)
    results = parse_results_attachments(results)
    if client.get_auth_type() == client.APPLICATION_AUTH:
        results = filter_results_by_query(results, query)

    return serialize_results(results)
