import logging
from typing import Any
from . import UpstreamProviderError

from algoliasearch.search_client import SearchClient
from algoliasearch.exceptions import AlgoliaException
from flask import current_app as app

logger = logging.getLogger(__name__)


def extract_document_data(document):
    # fields depend on the schema of the original documents
    url = f"{app.config.get('ALGOLIA_DOCUMENT_BASE_URL', '')}{document['internalLink']}"
    return {"text": document["body"], "url": url}


def search(query: str) -> list[dict[str, Any]]:
    algolia_client = SearchClient.create(
        app.config["ALGOLIA_APP_ID"], app.config["ALGOLIA_API_KEY"]
    )

    index = algolia_client.init_index(app.config["ALGOLIA_INDEX_NAME"])

    logger.info(f'Querying Algolia for "{query}"')

    try:
        response = index.search(query)
    except AlgoliaException:
        logger.error(f"Failed to query {query}")
        raise UpstreamProviderError(f"Failed to query {query}")

    logger.info(f"Found {response['nbHits']} results")

    results = [extract_document_data(document) for document in response["hits"]]

    return {"results": results}
