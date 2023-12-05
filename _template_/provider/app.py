import logging
from flask import current_app as app
from connexion.exceptions import Unauthorized

logger = logging.getLogger(__name__)


# This function is run for the /search endpoint
# the results that are returned here will be passed to Cohere's model for RAG
def search(body):
    logger.debug(f'Search request: {body["query"]}')

    # the final data can include anything but must be a flat dictionary with string keys and string values
    # we also recommend that you include:
    #   - an id field that uniquely identifies the data
    #   - a text field that contains the bulk of your textual data
    #   - a title field that describes the data
    #   - a url field that points to the source of the data
    data = [
        {
            "id": "1",
            "title": "Tall penguins",
            "text": "The tallest penguin is the Emperor penguin",
            "url": "https://en.wikipedia.org/wiki/Penguin",
        },
        {
            "id": "2",
            "title": "Emperor penguins",
            "text": "The latin name for Emperor penguin is Aptenodytes forsteri",
            "url": "https://en.wikipedia.org/wiki/Penguin",
        },
        {
            "id": "3",
            "title": "Small penguins",
            "text": "The smallest penguin is the fairy penguin",
            "url": "https://en.wikipedia.org/wiki/Penguin",
        },
        {
            "id": "4",
            "title": "Eudyptula penguis",
            "text": "The latin name for fairy penguin is Eudyptula minor",
            "url": "https://en.wikipedia.org/wiki/Penguin",
        },
    ]

    return {"results": data}, 200, {"X-Connector-Id": app.config.get("APP_ID")}


# This function is run for all endpoints to ensure requests are using a valid API key
def apikey_auth(token):
    if token != app.config.get("CONNECTOR_API_KEY"):
        raise Unauthorized()
    # successfully authenticated
    return {}
