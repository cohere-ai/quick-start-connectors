import logging

from connexion.exceptions import Unauthorized
from flask import abort
from flask import current_app as app

from . import UpstreamProviderError, provider

logger = logging.getLogger(__name__)


def search(body):
    logger.debug(f'Search request: {body["query"]}')
    data = []
    try:
        data = provider.search(body["query"])
        logger.info(f"Found {len(data)} results")
    except UpstreamProviderError as error:
        logger.error(f"Docusign search error: {error.message}")
        abort(502, error.message)
    except AssertionError as error:
        logger.error(f"Docusign config error: {error}")
        abort(502, f"Docusign config error: {error}")

    return {"results": data}, 200, {"X-Connector-Id": app.config.get("APP_ID")}


def apikey_auth(token):
    api_key = str(app.config.get("CONNECTOR_API_KEY", ""))
    if api_key != "" and token != api_key:
        raise Unauthorized()
    # successfully authenticated
    return {}
