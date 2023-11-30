import connexion  # type: ignore
import logging

from dotenv import load_dotenv


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
        API_VERSION,
        resolver=connexion.resolver.RelativeResolver("provider.app"),
    )
    logging.basicConfig(level=logging.INFO)
    flask_app = app.app
    flask_app.config.from_prefixed_env("GITHUB")
    return flask_app
