import logging

from connexion.exceptions import Unauthorized
from flask import abort, current_app as app

from . import UpstreamProviderError, provider

logger = logging.getLogger(__name__)


def search(body):
    try:
        data = provider.search(body["query"])
    except UpstreamProviderError as error:
        logger.error(f"Upstream search error: {error.message}")
        abort(502, error.message)
    except AssertionError as error:
        logger.error(f"Blogger config error: {error}")
        abort(502, f"Blogger config error: {error}")

    return {"results": data}


def apikey_auth(token):
    api_key = app.config.get("CONNECTOR_API_KEY", "")
    if api_key != "" and token != api_key:
        raise Unauthorized()
    # successfully authenticated
    return {}
