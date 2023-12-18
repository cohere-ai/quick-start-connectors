import logging


from flask import current_app as app
from .client import get_client

logger = logging.getLogger(__name__)


def serialize_result(issue):
    data = {}
    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_resource = {
        key: str(value)
        for key, value in issue["fields"].items()
        if isinstance(value, (str, int, bool))
    }

    data.update({**stripped_resource})

    if (task_name := issue.get("key")) is not None:
        data["title"] = task_name
        data["url"] = f"{app.config['ORG_DOMAIN']}/browse/{task_name}"

    if (description := issue.get("fields", {}).get("description")) is not None:
        data["text"] = description

    return data


def search(query):
    client = get_client()

    issues = client.search(query)

    results = []
    for issue in issues:
        result = serialize_result(issue)
        results.append(result)

    return results
