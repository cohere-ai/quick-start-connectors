def test_bearer_auth_valid_token_200(client, configure_app_env, mock_search_provider):
    configure_app_env({"CONNECTOR_API_KEY": "secret"})

    response = client.post(
        "/search",
        headers={"Authorization": "Bearer secret"},
        json={"query": "test"},
    )

    assert response.status_code == 200
    # Mock returns [] for search results
    assert response.get_json() == {"results": []}


def test_bearer_auth_invalid_token_401(client, configure_app_env, mock_search_provider):
    configure_app_env({"CONNECTOR_API_KEY": "secret"})

    response = client.post(
        "/search",
        headers={"Authorization": "Bearer not-secret"},
        json={"query": "test"},
    )

    assert response.status_code == 401


def test_bearer_auth_missing_token_401(client, configure_app_env, mock_search_provider):
    configure_app_env({"CONNECTOR_API_KEY": "secret"})

    response = client.post(
        "/search",
        json={"query": "test"},
    )

    assert response.status_code == 401


def test_bearer_auth_missing_env_variable_with_header_401(client, mock_search_provider):
    client.application.config.pop("CONNECTOR_API_KEY", None)

    response = client.post(
        "/search",
        headers={"Authorization": "Bearer secret"},
        json={"query": "test"},
    )

    assert response.status_code == 401


def test_bearer_auth_missing_env_variable_without_header_401(
    client, mock_search_provider
):
    client.application.config.pop("CONNECTOR_API_KEY", None)

    response = client.post(
        "/search",
        json={"query": "test"},
    )

    assert response.status_code == 401
