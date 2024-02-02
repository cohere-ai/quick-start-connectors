import pytest
import logging
from provider import UpstreamProviderError


def test_search_success(authed_client, mock_search_provider):
    response = authed_client.post(
        "/search",
        json={"query": "test"},
    )

    assert response.status_code == 200
    # Mock returns [] for search results
    assert response.get_json() == {"results": []}


def test_search_query_is_missing_fail(authed_client):
    response = authed_client.post(
        "/search",
        json={},
    )

    assert response.get_json() == {
        "detail": "'query' is a required property",
        "status": 400,
        "title": "Bad Request",
        "type": "about:blank",
    }


def test_search_query_is_empty_string_fail(authed_client):
    response = authed_client.post(
        "/search",
        json={"query": ""},
    )

    assert response.get_json() == {
        "detail": "'' should be non-empty - 'query'",
        "status": 400,
        "title": "Bad Request",
        "type": "about:blank",
    }


def test_search_error_raises_upstream_error(authed_client, caplog):
    caplog.set_level(logging.ERROR)
    authed_client.exception = UpstreamProviderError("test")
    with pytest.raises(UpstreamProviderError) as err:
        authed_client.post(
            "/search",
            json={"query": "test"},
        )

    assert err.type == UpstreamProviderError
    assert err.value.message == "test"
