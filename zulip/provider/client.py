import zulip
from flask import current_app as app

from . import UpstreamProviderError

client = None


def get_client():
    global client
    if not client:
        assert (api_key := app.config.get("API_KEY")), "ZULIP_API_KEY must be set"
        assert (bot_email := app.config.get("BOT_EMAIL")), "ZULIP_BOT_EMAIL must be set"
        assert (site := app.config.get("SITE")), "ZULIP_SITE must be set"

        try:
            client = zulip.Client(api_key=api_key, email=bot_email, site=site)
        except Exception as e:
            raise UpstreamProviderError(str(e))

    return client
