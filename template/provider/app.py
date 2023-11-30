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
            "id": "0",
            "title": "Tall penguins",
            "text": "Emperor penguins are the tallest",
            "url": "https://en.wikipedia.org/wiki/Penguin",
        }
    ]

    return {"results": data}


# This function is run for all endpoints to ensure requests are using a valid API key
def apikey_auth(token):
    if token != app.config.get("CONNECTOR_API_KEY"):
        raise Unauthorized()
    # successfully authenticated
    return {}
