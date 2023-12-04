import pymongo

from flask import current_app as app

client = None


def get_client():
    assert (
        connection_string := app.config.get("CONNECTION_STRING")
    ), "MONGODB_CONNECTION_STRING must be set"
    global client

    if not client:
        client = pymongo.MongoClient(
            connection_string,
        )

    return client
