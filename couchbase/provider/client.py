from datetime import timedelta

import couchbase.search as search
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, SearchOptions
from flask import current_app as app

client = None


class CouchbaseClient:
    def __init__(
        self,
        endpoint,
        username,
        password,
        bucket_name,
        scope,
        search_index,
        mappings,
        search_limit,
    ):
        auth = PasswordAuthenticator(username, password)
        options = ClusterOptions(auth)
        options.apply_profile("wan_development")
        self.cluster = Cluster("couchbases://{}".format(endpoint), options)
        self.cluster.wait_until_ready(timedelta(seconds=10))
        self.bucket = self.cluster.bucket(bucket_name)
        self.scope = self.bucket.scope(scope)
        self.collection = self.bucket.default_collection()
        self.search_index = search_index
        self.mappings = mappings
        self.search_limit = search_limit

    def get_search_index(self):
        return self.search_index

    def get_mappings(self):
        return self.mappings

    def get_search_limit(self):
        return self.search_limit

    def search_using_index(self, index_name, query):
        query = "+" + "+".join(query.replace("+", "").split(" "))
        return self.cluster.search_query(
            index_name,
            search.QueryStringQuery(query),
            SearchOptions(fields=["*"], limit=self.search_limit),
        )

    def get_entities_by_meta(self, meta_data):
        results = []
        if not meta_data:
            return []
        meta_parsed = {}
        for item in meta_data.rows():
            entity_type = item.fields.get("_$c")
            entity_id = item.id

            if entity_type in meta_parsed:
                meta_parsed[entity_type].append(entity_id)
            else:
                meta_parsed[entity_type] = [entity_id]

        for entity_type, ids in meta_parsed.items():
            docs = self.scope.collection(entity_type).get_multi(ids)
            for doc_id, doc in docs.results.items():
                if doc.success:
                    value = doc.content_as[dict]
                    value["full_id"] = doc_id
                    results.append(value)
        return results


def get_client():
    global client
    assert (
        connection_string := app.config.get("CONNECTION_STRING")
    ), "COUCHBASE_CONNECTION_STRING must be set"
    assert (user := app.config.get("USER")), "COUCHBASE_USER must be set"
    assert (password := app.config.get("PASSWORD")), "COUCHBASE_PASSWORD must be set"
    assert (bucket := app.config.get("BUCKET")), "COUCHBASE_BUCKET must be set"
    assert (scope := app.config.get("SCOPE")), "COUCHBASE_SCOPE must be set"
    assert (
        search_index := app.config.get("SEARCH_INDEX")
    ), "COUCHBASE_SEARCH_INDEX must be set"
    mappings = app.config.get("SEARCH_FIELDS_MAPPING", {})
    search_limit = app.config.get("SEARCH_LIMIT", 20)

    if not client:
        client = CouchbaseClient(
            connection_string,
            user,
            password,
            bucket,
            scope,
            search_index,
            mappings,
            search_limit,
        )

    return client
