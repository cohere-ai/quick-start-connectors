import json
from flask import current_app as app
import redis
from redis.commands.search.query import Query
from . import UpstreamProviderError

client = None


class RedisClient:
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 6379
    DEFAULT_SEARCH_LIMIT = 10

    def __init__(
        self,
        index,
        fields,
        host=None,
        port=None,
        username=None,
        password=None,
        search_limit=None,
        fields_mapping={},
    ):
        self.index = index
        self.fields = fields
        self.fields_mapping = fields_mapping
        self.host = host or self.DEFAULT_HOST
        self.port = port or self.DEFAULT_PORT
        self.username = username
        self.password = password
        self.search_limit = search_limit or self.DEFAULT_SEARCH_LIMIT
        self.redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            decode_responses=True,
        )

    def search(self, query):
        try:
            q = Query(query).paging(0, self.search_limit)
            search_results = self.redis_client.ft(self.index).search(q)
        except Exception as e:
            raise UpstreamProviderError(f"Redis search error: {e}")

        return [doc.__dict__ for doc in search_results.docs]


def get_client():
    global client
    if client is not None:
        return client

    assert (fields := app.config.get("FIELDS")), "REDIS_FIELDS config var must be set"
    assert (index := app.config.get("INDEX")), "REDIS_INDEX config var must be set"
    fields = fields.split(",")
    username = app.config.get("USER", None)
    password = app.config.get("PASSWORD", None)
    host = app.config.get("HOST", None)
    port = app.config.get("PORT", None)
    search_limit = app.config.get("SEARCH_LIMIT", None)
    fields_mapping = app.config.get("FIELDS_MAPPING", {})
    client = RedisClient(
        index, fields, host, port, username, password, search_limit, fields_mapping
    )

    return client
