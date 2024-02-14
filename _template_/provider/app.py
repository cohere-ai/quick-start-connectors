import logging
from flask import abort, current_app as app
from connexion.exceptions import Unauthorized

from . import UpstreamProviderError, provider

logger = logging.getLogger(__name__)


def search(body):
    """
    Entrypoint for the /search endpoint. Most of the search
    logic should be in provider.search
    """
    logger.debug(f'Search request: {body["query"]}')

    try:
        data = provider.search(body["query"])
        logger.info(f"Found {len(data)} results")
    except UpstreamProviderError as error:
        logger.error(f"Upstream search error: {error.message}")
        abort(502, error.message)

    return {"results": data}, 200, {"X-Connector-Id": app.config.get("APP_ID")}


# This function is run for all endpoints to ensure requests are using a valid API key
def apikey_auth(token):
    if token != app.config.get("CONNECTOR_API_KEY"):
        raise Unauthorized()
    # successfully authenticated
    return {}
