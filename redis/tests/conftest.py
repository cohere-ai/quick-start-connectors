import pytest
from unittest.mock import patch
from provider import create_app


class AuthenticatedTestClient:
    """
    Helper class to test logic around connector API calls without
    needing to setup authorization each time. This assumes the authentication
    schema uses Bearer auth.
    """

    exception = None
    DEFAULT_API_KEY = "secret"

    def __init__(self, client):
        self.client = client

    def prepare(self, **kwargs):
        # Raise Exception for certain test scenarios
        if self.exception is not None:
            raise self.exception

        # Set up Authorization Bearer headers
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.DEFAULT_API_KEY}"
        kwargs["headers"] = headers

        return kwargs

    def post(self, *args, **kwargs):
        kwargs = self.prepare(**kwargs)
        return self.client.post(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs = self.prepare(**kwargs)
        return self.client.get(*args, **kwargs)


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def authed_client(app, configure_app_env):
    authed = AuthenticatedTestClient(app.test_client())
    configure_app_env({"CONNECTOR_API_KEY": authed.DEFAULT_API_KEY})

    return authed


@pytest.fixture
def configure_app_env(app):
    # Fixture to configure the app and modify config during test runtime
    # Accepts a dictionary of key-value pairs
    def _configure_app_env(configs):
        for key, value in configs.items():
            app.config[key] = value

    return _configure_app_env


@pytest.fixture
def mock_search_provider():
    with patch("provider.provider.search", return_value=[]) as mock:
        yield mock


@pytest.fixture
def mock_client_search(configure_app_env):
    configure_app_env({"FIELDS_MAPPING": {"features": "text", "name": "title"}})
    configure_app_env({"FIELDS": "id,name,description,brand,color,country,rank"})
    configure_app_env({"INDEX": "bbq_index"})
    with patch("provider.client.RedisClient.search") as mock:
        yield mock
