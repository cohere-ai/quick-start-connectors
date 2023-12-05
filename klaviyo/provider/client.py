from flask import current_app as app
from klaviyo_api import KlaviyoAPI

client = None


def get_client():
    global client
    assert (api_key := app.config.get("API_KEY")), "KLAVIYO_API_KEY must be set"

    if not client:
        client = KlaviyoAPI(api_key)

    return client
