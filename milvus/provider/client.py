import logging
from flask import current_app as app
import cohere
from pymilvus import connections, Collection

logger = logging.getLogger(__name__)

cohere_client = None


class MilvusConnectorClient:
    DEFAULT_SEARCH_LIMIT = 10
    DEFAULT_ALIAS = "default"

    def __init__(
        self,
        cluster_uri,
        collection_name,
        vector_field,
        user=None,
        password=None,
        api_key=None,
    ):
        if api_key is not None:
            connections.connect(
                alias=self.DEFAULT_ALIAS, uri=cluster_uri, token=api_key
            )
        else:
            connections.connect(
                alias=self.DEFAULT_ALIAS, uri=cluster_uri, token=f"{user}:{password}"
            )
        self.collection = Collection(name=collection_name)
        self.vector_field = vector_field
        self.search_limit = self.DEFAULT_SEARCH_LIMIT

    def set_search_limit(self, search_limit):
        self.search_limit = search_limit

    def get_search_fields(self):
        output_fields = [
            field.name
            for field in self.collection.schema.fields
            if field.name != self.vector_field
        ]
        return output_fields

    def search(self, embeddings):
        self.collection.load()
        params = {"metric_type": "L2", "params": {"nprobe": 10}}
        search_results = self.collection.search(
            embeddings,
            anns_field=self.vector_field,
            param=params,
            limit=self.search_limit,
            output_fields=self.get_search_fields(),
        )
        return search_results

    def close_connection(self):
        connections.remove_connection(alias=self.DEFAULT_ALIAS)


class CohereClient:
    def __init__(self, cohere_api_key, model):
        self.client = cohere.Client(cohere_api_key)
        self.model = model

    def get_embeddings(self, query, input_type="search_query"):
        return self.client.embed(
            [query], model=self.model, input_type=input_type
        ).embeddings


def get_milvus_client():
    assert (
        cluster_uri := app.config.get("CLUSTER_URI")
    ), "MILVUS_CLUSTER_URI must be set"
    assert (
        collection_name := app.config.get("COLLECTION")
    ), "MILVUS_COLLECTION must be set"
    assert (
        vector_field := app.config.get("VECTOR_FIELD")
    ), "MILVUS_VECTOR_FIELD must be set"

    api_key = app.config.get("API_KEY", None)
    user = app.config.get("USER", "")
    password = app.config.get("PASSWORD", "")
    search_limit = app.config.get("SEARCH_LIMIT", 100)

    milvus_client = MilvusConnectorClient(
        cluster_uri, collection_name, vector_field, user, password, api_key
    )
    milvus_client.set_search_limit(search_limit)

    return milvus_client


def get_cohere_client():
    global cohere_client
    assert (
        api_key := app.config.get("COHERE_APIKEY")
    ), "MILVUS_COHERE_APIKEY env var must be set"
    model = app.config.get("COHERE_EMBED_MODEL", "embed-english-v3.0")
    if not cohere_client:
        cohere_client = CohereClient(api_key, model)

    return cohere_client
