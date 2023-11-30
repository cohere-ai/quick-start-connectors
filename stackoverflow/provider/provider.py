import logging

from .client import get_client

logger = logging.getLogger(__name__)


def search(query):
    stackoverflow_client = get_client()
    data = stackoverflow_client.search(query)

    results = []
    for item in data["items"]:
        result = {
            "title": item["title"],
            "url": item["link"],
            "tags": item["tags"],
        }

        if "accepted_answer_id" in item:
            result["accepted_answer_id"] = item["accepted_answer_id"]

        text = ""
        question_data = stackoverflow_client.get_question(item["question_id"])
        if (
            question_data
            and "items" in question_data
            and len(question_data["items"]) > 0
        ):
            text += question_data["items"][0]["body"]

        if "accepted_answer_id" in item:
            answer_data = stackoverflow_client.get_answer(item["accepted_answer_id"])
            if answer_data and "items" in answer_data and len(answer_data["items"]) > 0:
                text += answer_data["items"][0]["body"]

        result["text"] = text
        results.append(result)

    return results
