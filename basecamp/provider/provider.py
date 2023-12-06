import logging

from .client import get_client

logger = logging.getLogger(__name__)


def check_content(content, keywords):
    return any(keyword.lower() in content.lower() for keyword in keywords)


def process_vaults_recursively(client, vault, depth_level, results, keywords):
    if vault["documents_count"] > 0 and vault["documents_url"]:
        documents = client.get(vault["documents_url"])
        for doc in documents:
            if check_content(doc["content"], keywords):
                item_to_append = doc
                item_to_append["type"] = "document"
                item_to_append["text"] = doc.pop("content")
                item_to_append["api_url"] = doc.pop("url")
                item_to_append["url"] = doc.pop("app_url")
                item_to_append = {k: str(v) for k, v in item_to_append.items()}
                results.append(item_to_append)
    if depth_level == 0:
        return results
    if vault["vaults_count"] > 0:
        vaults = client.get(vault["vaults_url"])
        for vl in vaults:
            process_vaults_recursively(client, vl, depth_level - 1, results, keywords)
    return results


def get_filtered_results(client, projects, search_entities, query):
    results = []
    keywords = query.split()
    depth = client.get_depth()
    for project in projects:
        found = False
        if "dock" in project and project["dock"]:
            needed_entities = [
                d for d in project["dock"] if d["name"] in search_entities
            ]
            for entity in needed_entities:
                if entity["name"] == "message_board":
                    board_data = client.get(entity["url"])
                    messages = client.get(board_data["messages_url"])
                    for message in messages:
                        if check_content(message["content"], keywords) or check_content(
                            message["subject"], keywords
                        ):
                            found = True
                            item_to_append = message
                            item_to_append["type"] = "message"
                            item_to_append["text"] = message.pop("content")
                            item_to_append["api_url"] = message.pop("url")
                            item_to_append["url"] = message.pop("app_url")
                            item_to_append["project_id"] = project["id"]
                            item_to_append = {
                                k: str(v) for k, v in item_to_append.items()
                            }
                            results.append(item_to_append)
                if entity["name"] == "vault":
                    vault = client.get(entity["url"])
                    count_before_processing = len(results)
                    results = process_vaults_recursively(
                        client, vault, depth, results, keywords
                    )
                    found = len(results) > count_before_processing
        if found or check_content(project["name"], keywords):
            item_to_append = project
            item_to_append["type"] = "project"
            item_to_append["title"] = project.pop("name")
            item_to_append["text"] = project.pop("description")
            item_to_append["api_url"] = project.pop("url")
            item_to_append["url"] = project.pop("app_url")
            item_to_append = {k: str(v) for k, v in item_to_append.items()}
            results.insert(0, item_to_append)
    return results


def search(query):
    client = get_client()

    projects = client.get_projects()
    search_entities = client.get_search_entities()
    results = get_filtered_results(client, projects, search_entities, query)

    return results
