import requests
from flask import current_app as app

from . import UpstreamProviderError
from .constants import (
    ENTITY_ENV_VAR_ENABLED_MAPPING,
    CONTACT_PARAMETERS,
    SALES_ACCOUNT_PARAMETERS,
    DEAL_PARAMETERS,
)

client = None


class FreshsalesClient:
    def __init__(self, base_path, api_key, search_limit):
        self.base_url = f"https://{base_path}/api"
        self.headers = {
            "Authorization": f"Token token={api_key}",
        }
        self.search_limit = search_limit
        self.entity_types = self.build_entity_types()

    def build_entity_types(self):
        """
        Builds the entity list string for the `includes` query parameter, based
        off environment variables.

        For example, the default returned format will look like 'user,contact,sales_account,deal'
        See: https://developers.freshworks.com/crm/api/#search
        """

        def is_env_var_true(env_var_name):
            value = app.config.get(env_var_name, "False")
            return value.lower() == "true"

        entities = [
            enum.value
            for enum, env_var in ENTITY_ENV_VAR_ENABLED_MAPPING.items()
            if is_env_var_true(env_var)
        ]
        return ",".join(entities)

    def _get(self, url, params={}, raise_on_error=False):
        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=params,
        )

        if response.status_code != 200:
            if raise_on_error:
                message = response.text or f"Error: HTTP {response.status_code}"
                raise UpstreamProviderError(message)

            return None

        return response.json()

    def search(self, query):
        search_url = f"{self.base_url}/search"
        params = {
            "q": query,
            "include": self.entity_types,
            "per_page": self.search_limit,
        }

        return self._get(
            search_url,
            params,
            True,
        )

    def get_contact_details(self, id):
        url = f"{self.base_url}/contacts/{id}"
        params = {"include": ",".join(CONTACT_PARAMETERS)}

        return self._get(
            url,
            params,
        )

    def get_sales_account_details(self, id):
        url = f"{self.base_url}/sales_accounts/{id}"
        params = {"include": ",".join(SALES_ACCOUNT_PARAMETERS)}

        return self._get(
            url,
            params,
        )

    def get_deal_details(self, id):
        url = f"{self.base_url}/deals/{id}"
        params = {"include": ",".join(DEAL_PARAMETERS)}

        return self._get(
            url,
            params,
        )


def get_client():
    global client
    if not client:
        assert (
            base_path := app.config.get("BUNDLE_ALIAS")
        ), "FRESHSALES_BUNDLE_ALIAS must be set"
        assert (api_key := app.config.get("API_KEY")), "FRESHSALES_API_KEY must be set"
        search_limit = app.config.get("SEARCH_LIMIT", 15)

        client = FreshsalesClient(base_path, api_key, search_limit)

    return client
