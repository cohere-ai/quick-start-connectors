from atlassian import Jira
from flask import current_app as app
from . import UpstreamProviderError

client = None


def get_client():
    global client

    if not client:
        try:
            client = Jira(
                url=app.config["ORG_DOMAIN"],
                username=app.config["USER_EMAIL"],
                password=app.config["API_TOKEN"],
            )
        except Exception as e:
            raise UpstreamProviderError(f"Error initializing Jira client: {str(e)}")

    return client
