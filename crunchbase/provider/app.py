import logging
from flask import current_app as app
from flask import abort
from connexion.exceptions import Unauthorized
from . import UpstreamProviderError, provider


logger = logging.getLogger(__name__)


def search(body):
    logger.debug(f'Search request: {body["query"]}')
    try:
        data = provider.search(body["query"])
        logger.info(f"Found {len(data)} results")
    except UpstreamProviderError as error:
        logger.error(f"Upstream search error: {error.message}")
        abort(502, error.message)
    except AssertionError as error:
        logger.error(f"Crunchbase config error: {error}")
        abort(502, f"Crunchbase config error: {error}")

    return {"results": data}, 200, {"X-Connector-Id": app.config.get("APP_ID")}


# This function is run for all endpoints to ensure requests are using a valid API key
def apikey_auth(token):
    if token != app.config.get("CONNECTOR_API_KEY"):
        raise Unauthorized()
    # successfully authenticated
    return {}
