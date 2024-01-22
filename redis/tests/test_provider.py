from provider import UpstreamProviderError


def test_search_success(authed_client, configure_app_env, mock_client_search):
    configure_app_env({"REDIS_FIELDS_MAPPING": {"features": "text", "name": "title"}})
    mock_client_search.return_value = [
        {
            "id": "bbq_B07WYJTB3P",
            "rank": "240",
            "brand": "ProCom",
            "name": "ProCom FBNSD28T Ventless Dual Fuel Firebox Insert, 29 in",
            "color": "29 In.",
            "description": "",
            "country": "us",
        }
    ]

    response = authed_client.post(
        "/search",
        json={"query": "test"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "results": [
            {
                "id": "bbq_B07WYJTB3P",
                "rank": "240",
                "brand": "ProCom",
                "title": "ProCom FBNSD28T Ventless Dual Fuel Firebox Insert, 29 in",
                "color": "29 In.",
                "description": "",
                "country": "us",
            }
        ]
    }
    mock_client_search.assert_called_once_with("test")


def test_search_fail(authed_client, mock_client_search):
    mock_client_search.return_value = UpstreamProviderError

    response = authed_client.post(
        "/search",
        json={"query": "test"},
    )

    assert response.status_code == 500
    assert response.get_json() == {
        "detail": "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.",
        "status": 500,
        "title": "Internal Server Error",
        "type": "about:blank",
    }
    mock_client_search.assert_called_once_with("test")
