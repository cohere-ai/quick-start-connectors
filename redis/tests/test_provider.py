from provider import UpstreamProviderError


def test_search_success(authed_client, configure_app_env, mock_client_search):
    mock_client_search.return_value = [
        {
            "id": "bbq_B08H18XLP9",
            "rank": "233",
            "brand": "ARC Advanced Royal Champion",
            "name": "ARC SS4242S Propane Burner",
            "features": "The propane burner adopts all-welded stainless steel frame",
            "color": "Stainless Steel",
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
                "id": "bbq_B08H18XLP9",
                "rank": "233",
                "brand": "ARC Advanced Royal Champion",
                "title": "ARC SS4242S Propane Burner",
                "text": "The propane burner adopts all-welded stainless steel frame",
                "color": "Stainless Steel",
                "description": "",
                "country": "us",
            }
        ]
    }
    mock_client_search.assert_called_once_with("test")


def test_search_fail(authed_client, mock_client_search):
    mock_client_search.side_effect = UpstreamProviderError("test error")
    response = authed_client.post(
        "/search",
        json={"query": "test"},
    )

    assert response.status_code == 502
    assert response.get_json() == {
        "detail": "test error",
        "status": 502,
        "title": "Bad Gateway",
        "type": "about:blank",
    }
    mock_client_search.assert_called_once_with("test")
