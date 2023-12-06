from typing import Any

from .client import get_client


def search(query: str, oauth_token: str = None) -> list[dict[str, Any]]:
    dbx_client = get_client(oauth_token)
    dbx_results = dbx_client.search(query)

    results = []
    for dbx_result in dbx_results.matches:
        if not (metadata := dbx_result.metadata.get_metadata()):
            continue

        if not getattr(metadata, "is_downloadable", False):
            continue

        metadata, f = dbx_client.download_file(metadata.path_display)

        result = {
            "type": "file",
            "title": metadata.name,
            "text": str(f.content),
        }
        # TODO: decode file contents
        results.append(result)

    return results
