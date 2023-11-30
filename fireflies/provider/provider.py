import logging

from .client import get_client

logger = logging.getLogger(__name__)


def search_transcripts(client, query, search_limit):
    results = []
    response = client.get_transcripts(search_limit)
    transcripts = (
        response["data"]["transcripts"] if response and "data" in response else []
    )
    keywords = query.split(" ")
    for transcript in transcripts:
        for sentence in transcript["sentences"]:
            if any(
                keyword.lower() in sentence["raw_text"].lower() for keyword in keywords
            ):
                transcript["text"] = " ".join(
                    [row["text"] for row in transcript["sentences"]]
                )
                transcript["url"] = transcript.pop("transcript_url")
                results.append({k: str(v) for k, v in transcript.items()})
                break

    return results


def search(query):
    client = get_client()
    search_limit = client.get_search_limit()
    return search_transcripts(client, query, search_limit)
