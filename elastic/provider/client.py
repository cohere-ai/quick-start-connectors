import cohere
from elasticsearch import Elasticsearch
from flask import current_app as app

from . import UpstreamProviderError

client = None


class ElasticsearchClient:
    def __init__(
        self, connection_params=None, index=None, search_limit=10, search_type=None
    ):
        if not connection_params:
            raise ValueError(
                "No connection parameters provided to the Elasticsearch "
                "client during initialization."
            )
        if not index:
            raise ValueError(
                "No index provided to the Elasticsearch "
                "client during initialization."
            )

        self.client = Elasticsearch(**connection_params)
        self.index = index
        self.search_limit = search_limit

        self.do_vector = False
        if search_type == "vector":
            assert (
                "embedding"
                in self.client.indices.get(index=index)[index]["mappings"]["properties"]
            ), f"Supplied index, {index}, is not a vector index"

            if api_key := app.config.get("COHERE_API_KEY"):
                self.co = cohere.Client(api_key=api_key)
            else:
                raise ValueError(
                    "If doing vector search, a Cohere API key must be provided."
                )

            self.do_vector = True

    def search(self, query):
        if self.do_vector:
            return self.vector_search(query)
        return self.default_search(query)

    def default_search(self, query):
        es_query_body = {
            "query": {"multi_match": {"query": query}},
            "highlight": {
                "pre_tags": [""],
                "post_tags": [""],
                "fields": {"content": {}},
            },
        }

        response = self.client.search(
            index=self.index, body=es_query_body, size=self.search_limit
        )

        if response.get("hits", {}).get("hits") is None:
            raise UpstreamProviderError(
                "Error while searching Elasticsearch with " f"query: '{query}'."
            )

        return response["hits"]["hits"]

    def vector_search(self, query):
        response = self.client.search(
            index=self.index,
            knn={
                "field": "embedding",
                "query_vector": self.get_query_embedding(query),
                "num_candidates": 50,
                "k": 10,
            },
            size=self.search_limit,
        )

        if response.get("hits", {}).get("hits") is None:
            raise UpstreamProviderError(
                "Error while searching Elasticsearch with " f"query: '{query}'."
            )

        return response["hits"]["hits"]

    def get_query_embedding(self, query):
        r = self.co.embed(
            texts=[query], model="embed-english-v3.0", input_type="search_query"
        )

        return r.embeddings[0]


def get_client():
    global client
    if not client:
        connection_params = {}

        # Retrieve environment details
        if cloud_id := app.config.get("CLOUD_ID"):
            connection_params["cloud_id"] = cloud_id
        elif url := app.config.get("URL"):
            connection_params["hosts"] = [url]
        else:
            raise ValueError(
                "To connect to your Elasticsearch instance, either ELASTIC_CLOUD_ID "
                "or ELASTIC_URL must be provided as a valid environment variable. "
                "See the README for more details."
            )

        # Retrieve credentials
        if api_key := app.config.get("API_KEY"):
            connection_params["api_key"] = api_key
        elif (user := app.config.get("USER")) and (password := app.config.get("PASS")):
            connection_params["basic_auth"] = (user, password)
        else:
            raise ValueError(
                "To authenticate your Elasticsearch connection, either ELASTIC_API_KEY or the ELASTIC_USER "
                "and ELASTIC_PASS pair must be provided as valid environment variables. "
                "See the README for more details."
            )

        assert (index := app.config.get("INDEX")), "ELASTIC_INDEX must be set"
        search_limit = app.config.get("SEARCH_LIMIT", 10)

        search_type = app.config.get("SEARCH_TYPE")

        client = ElasticsearchClient(
            connection_params, index, search_limit, search_type
        )

    return client
