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
    return {"results": data}, 200, {"X-Connector-Id": app.config.get("APP_ID")}


def apikey_auth(token):
    api_key = app.config.get("CONNECTOR_API_KEY", "")
    if api_key != "" and token != api_key:
        raise Unauthorized()

    return {}
