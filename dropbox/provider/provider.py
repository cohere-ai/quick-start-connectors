from typing import Any

from .client import get_client
from .unstructured import get_unstructured_client


def search(query: str, oauth_token: str = None) -> list[dict[str, Any]]:
    dbx_client = get_client(oauth_token)
    unstructured_client = get_unstructured_client()
    dbx_results = dbx_client.search(query)

    return serialize_results(dbx_results, dbx_client, unstructured_client)


def serialize_results(dbx_results, dbx_client, unstructured_client):
    results = []

    for dbx_result in dbx_results.matches:
        if not (metadata := dbx_result.metadata.get_metadata()):
            continue

        if not getattr(metadata, "is_downloadable", False):
            continue

        metadata, f = dbx_client.download_file(metadata.path_display)

        import pdb

        result = {
            "id": metadata.id,
            "title": metadata.name,
            "type": "file",
            "raw_content": f.content,
        }

        results.append(result)

    # Group for batch Unstructured requests
    files = [
        (result["id"], result["title"], result["raw_content"]) for result in results
    ]
    unstructured_content = unstructured_client.batch_get(files)

    # Now build text field based off Unstructured return
    for result in results:
        del result["raw_content"]
        file_name = result["title"]

        if file_name in unstructured_content:
            # Build text
            text = ""
            for element in unstructured_content[file_name]:
                text += f' {element.get("text")}'

            if text != "":
                result["text"] = text

    return results
