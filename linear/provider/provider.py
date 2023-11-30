import logging

from .client import get_client

logger = logging.getLogger(__name__)


def serialize_results(data):
    serialized_data = []
    results = data.get("data", {}).get("searchIssues", {}).get("nodes", [])
    for issue in results:
        issue["text"] = issue.pop("description")
        serialized_data.append({k: str(v) for k, v in issue.items()})
    return serialized_data


def search(query):
    client = get_client()

    return serialize_results(client.search_issues_by_term(query))
