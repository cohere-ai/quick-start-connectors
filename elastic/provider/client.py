from elasticsearch import Elasticsearch
from flask import current_app as app

client = None


class ElasticsearchClient:
    def __init__(self, connection_params=None, index=None, search_limit=10):
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

    def search(self, query):
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

        return response["hits"]["hits"]


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

        client = ElasticsearchClient(connection_params, index, search_limit)

    return client
