from typing import Any

import requests
from docusign_esign import EnvelopesApi, ApiClient
from flask import current_app as app

from .provider import UpstreamProviderError

client = None


class DocuSignClient:
    """
    A client for the DocuSign API.
    """

    BASE_PATH = "https://account.docusign.com"
    BASE_PATH_DEV = "https://account-d.docusign.com"
    OAUTH_USER_INFO_END_POINT = "/oauth/userinfo"
    API_ENDPOINT = "/restapi"

    def __init__(self, account_id: str, access_token: str, is_prod: bool) -> None:
        self.base_path = self.BASE_PATH if is_prod else self.BASE_PATH_DEV
        self.account_id = account_id
        self.access_token = access_token
        self.api_client = self._get_client()

    def _get_user_info(self) -> dict[str, Any]:
        url = self.base_path + self.OAUTH_USER_INFO_END_POINT
        auth = {"Authorization": "Bearer " + self.access_token}
        response = requests.get(url, headers=auth)
        if response.status_code != 200:
            message = (
                response.text or f"Get user info error: HTTP {response.status_code}"
            )
            raise UpstreamProviderError(message)

        data = response.json()
        if "accounts" not in data:
            message = response.text or f"User Info Error: no data returned"
            raise UpstreamProviderError(message)
        for account in data["accounts"]:
            if account["account_id"] == self.account_id:
                return account
        message = response.text or f"User Info Error: API_ACCOUNT_ID is not valid"
        raise UpstreamProviderError(message)

    def _get_client(self) -> EnvelopesApi:
        user_info = self._get_user_info()
        api_client = ApiClient(
            base_path=user_info["base_uri"],
        )
        api_client.set_default_header(
            header_name="Authorization", header_value=f"Bearer {self.access_token}"
        )
        api_client.host = user_info["base_uri"] + self.API_ENDPOINT
        envelopes_api = EnvelopesApi(api_client)
        return envelopes_api

    def get_list_status_changes(
        self, query: str, from_date: str, to_date: str = None
    ) -> list[dict[str, Any]]:
        envelopes_api = self.api_client
        args = {
            "account_id": self.account_id,
            "from_date": from_date,
            "search_text": query,
        }
        if to_date:
            args["to_date"] = to_date
        try:
            data = envelopes_api.list_status_changes(**args)
        except Exception as error:
            raise UpstreamProviderError(f"DocuSign search error: {error}")

        return data


def get_client():
    global client
    if client:
        return client
    assert (
        access_token := app.config.get("ACCESS_TOKEN")
    ), "DOCUSIGN_ACCESS_TOKEN must be set"
    assert (
        account_id := app.config.get("API_ACCOUNT_ID")
    ), "DOCUSIGN_API_ACCOUNT_ID must be set"
    is_prod = app.config.get("IS_PROD_ENV", 1) == 1
    client = DocuSignClient(
        account_id=account_id, access_token=access_token, is_prod=is_prod
    )
    return client
