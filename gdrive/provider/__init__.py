import logging
import os
import nltk
import connexion
from dotenv import load_dotenv
from provider import cache


load_dotenv()

# download nltk data
nltk.download("stopwords")
nltk.download("punkt")

API_VERSION = "api.yaml"


class UpstreamProviderError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir="../../.openapi")

    app.add_api(
        API_VERSION, resolver=connexion.resolver.RelativeResolver("provider.app")
    )
    logging.basicConfig(level=logging.INFO)
    flask_app = app.app
    config_prefix = os.path.split(os.getcwd())[1].upper()
    flask_app.config.from_prefixed_env(config_prefix)
    flask_app.config["APP_ID"] = config_prefix
    cache.init(flask_app.config.get("CACHE_TYPE"), flask_app.config)
    return flask_app
