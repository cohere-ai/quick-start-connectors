import logging

from .client import get_client

logger = logging.getLogger(__name__)


def serialize_results(data):
    serialized_data = []
    for k, v in data.items():
        if k == "messages":
            for message in v["messages"]:
                message["title"] = message.pop("content_excerpt")
                message["text"] = message["body"]["plain"]
                message["api_url"] = message.pop("url")
                message["url"] = message.pop("web_url")
                message["type"] = "message"
                message = {key: str(value) for key, value in message.items()}
                serialized_data.append(message)
        if k == "users":
            for user in v:
                user["title"] = user.pop("full_name")
                user["text"] = user.pop("job_title")
                user["api_url"] = user.pop("url")
                user["url"] = user.pop("web_url")
                user = {key: str(value) for key, value in user.items()}
                serialized_data.append(user)
        if k == "groups":
            for group in v:
                group["title"] = group.pop("full_name")
                group["text"] = group.pop("description")
                group["api_url"] = group.pop("url")
                group["url"] = group.pop("web_url")
                group = {key: str(value) for key, value in group.items()}
                serialized_data.append(group)
        if k == "topics":
            for topic in v:
                topic["title"] = topic.pop("name")
                topic["text"] = topic.pop("description")
                topic = {key: str(value) for key, value in topic.items()}
                serialized_data.append(topic)
    return serialized_data


def search(query):
    client = get_client()
    response = client.search(query)

    return serialize_results(response)
