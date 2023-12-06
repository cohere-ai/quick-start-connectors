import logging

from .client import get_client

logger = logging.getLogger(__name__)


def search_projects(data, query):
    results = []
    keywords = query.split(" ")
    if "projects" in data:
        for project in data["projects"]:
            if any(keyword.lower() in project["name"].lower() for keyword in keywords):
                project["title"] = project.get("name")
                project["text"] = project.get("name")
                project["url"] = f"https://console.agora.io/project/{project['id']}"
                results.append({k: str(v) for k, v in project.items()})

    return results


def search(query):
    client = get_client()

    return search_projects(client.get_projects(), query)
