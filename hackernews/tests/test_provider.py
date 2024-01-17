def test_search_success(authed_client, mock_client_search, mock_client_get_item):
    mock_client_search.return_value = [{"objectID": 1}]
    mock_client_get_item.return_value = {"text": "hello"}

    response = authed_client.post(
        "/search",
        json={"query": "test"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"results": [{"objectID": "1", "text": "hello"}]}
    mock_client_search.assert_called_once_with("test")
    mock_client_get_item.asset_called_once_with("1")
