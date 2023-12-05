import logging
import os

import connexion
from dotenv import load_dotenv, dotenv_values

load_dotenv()

API_VERSION = "api.yaml"


class UpstreamProviderError(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


def create_app() -> connexion.FlaskApp:
    app = connexion.FlaskApp(__name__, specification_dir="../../.openapi")
    app.add_api(
        API_VERSION, resolver=connexion.resolver.RelativeResolver("provider.app")
    )
    logging.basicConfig(level=logging.INFO)
    flask_app = app.app
    config_prefix = os.path.split(os.getcwd())[
        1
    ].upper()  # Current directory name, upper-cased
    flask_app.config.from_prefixed_env(config_prefix)
    flask_app.config["APP_ID"] = config_prefix
    flask_app.config.from_mapping(dotenv_values())
    return flask_app
