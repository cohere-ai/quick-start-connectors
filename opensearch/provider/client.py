from flask import current_app as app
from opensearchpy import OpenSearch

client = None


class OpensearchClient:
    def __init__(self, host, port, user, password, use_ssl, index, search_limit):
        self.index = index
        self.search_limit = search_limit
        self.es = OpenSearch(
            hosts=[
                {
                    "host": host,
                    "port": port,
                }
            ],
            http_auth=(user, password),
            use_ssl=use_ssl,
            ssl_show_warn=False,
        )

    def search(self, query):
        es_query_body = {"query": {"multi_match": {"query": query}}}

        response = self.es.search(
            index=self.index, body=es_query_body, size=self.search_limit
        )

        return [match["_source"] for match in response["hits"]["hits"]]


def get_client():
    global client
    assert (host := app.config.get("HOST")), "OPENSEARCH_HOST must be set"
    assert (port := app.config.get("PORT")), "OPENSEARCH_PORT must be set"
    assert (user := app.config.get("USER")), "OPENSEARCH_USER must be set"
    assert (password := app.config.get("PASS")), "OPENSEARCH_PASS must be set"
    assert (index := app.config.get("INDEX")), "OPENSEARCH_INDEX must be set"

    use_ssl = app.config.get("USE_SSL", True)
    search_limit = app.config.get("SEARCH_LIMIT", 100)

    if not client:
        client = OpensearchClient(
            host, port, user, password, use_ssl, index, search_limit
        )

    return client
