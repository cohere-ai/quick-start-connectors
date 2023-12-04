from flask import current_app as app
import logging

import cohere
from pymilvus import connections, Collection


logger = logging.getLogger(__name__)
milvus_connection = None
cohere_client = None


def search(query):
    global milvus_connection
    global cohere_client

    if not cohere_client:
        assert (
            apikey := app.config.get("COHERE_APIKEY")
        ), "MILVUS_COHERE_APIKEY env var must be set"
        cohere_client = cohere.Client(apikey)
    if not milvus_connection:
        milvus_connection = connections.connect(
            alias="default",
            host=app.config["CLUSTER_HOST"],
            port=app.config["CLUSTER_PORT"],
        )

    # Since we need a vector in order to query Milvus, we'll use the Cohere API to generate an embedding.
    # Naturally, you should use the same embedding model that you used to generate the vectors for the original data.
    xq = cohere_client.embed(
        [query],
        model=app.config["COHERE_EMBED_MODEL"],
    ).embeddings

    collection = Collection(name=app.config["COLLECTION"])
    collection.load()

    top_k = 10
    params = {"metric_type": "L2", "params": {"nprobe": 10}}
    output_fields = [
        field.name
        for field in collection.schema.fields
        if field.name != app.config["VECTOR_FIELD"]
    ]

    search_results = collection.search(
        xq,
        anns_field=app.config["VECTOR_FIELD"],
        param=params,
        limit=top_k,
        output_fields=output_fields,
    )

    connections.remove_connection(alias="default")

    results = [
        {field: result.entity.get(field) for field in output_fields}
        for result in search_results[0]
    ]

    return results
