from flask import current_app as app
from boxsdk import CCGAuth, Client
from . import UpstreamProviderError


def get_client():
    try:
        auth = CCGAuth(
            client_id=app.config["CLIENT_ID"],
            client_secret=app.config["CLIENT_SECRET"],
            enterprise_id=app.config["ENTERPRISE_ID"],
        )
        box_client = Client(auth)
    except Exception as e:
        raise UpstreamProviderError(str(e)) from e

    return box_client
