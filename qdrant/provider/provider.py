from flask import current_app as app
import logging

import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, UpdateStatus, VectorParams


logger = logging.getLogger(__name__)
qdrant_client = None
cohere_client = None


def search(query):
    global qdrant_client
    global cohere_client

    if not cohere_client:
        assert (
            apikey := app.config.get("COHERE_APIKEY")
        ), "QDRANT_COHERE_APIKEY env var must be set"
        cohere_client = cohere.Client(apikey)
    if not qdrant_client:
        qdrant_client = QdrantClient(
            app.config["CLUSTER_HOST"], port=app.config["CLUSTER_PORT"]
        )

    # Since we need a vector in order to query Qdrant, we'll use the Cohere API to generate an embedding.
    # Naturally, you should use the same embedding model that you used to generate the vectors for the original data.
    xq = cohere_client.embed(
        [query],
        model=app.config["COHERE_EMBED_MODEL"],
    ).embeddings

    search_result = qdrant_client.search(
        collection_name=app.config["COLLECTION"], query_vector=xq[0], limit=10
    )

    results = [
        {"pid": result.payload["pid"], "text": result.payload["text"]}
        for result in search_result
    ]

    return results
