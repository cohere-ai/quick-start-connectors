from typing import Any

import redis
from flask import current_app as app


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 6379

r = None
fields = None


def search(query) -> list[dict[str, Any]]:
    global r
    global fields

    if not r:
        r = redis.Redis(
            host=app.config.get("HOST", DEFAULT_HOST),
            port=app.config.get("PORT", DEFAULT_PORT),
            decode_responses=True,
        )

    if not fields:
        assert (
            fields := app.config.get("FIELDS")
        ), "REDIS_FIELDS config var must be set"
        fields = fields.split(",")

    assert (index := app.config.get("INDEX")), "REDIS_INDEX config var must be set"

    redisearch_results = r.ft(index).search(query)

    results = []

    for doc in redisearch_results.docs:
        result = {field: getattr(doc, field) for field in fields}
        results.append(result)

    return results
