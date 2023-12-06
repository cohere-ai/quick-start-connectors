import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class AhaApiClient:
    ALLOWED_ENTITY_TYPES = {
        "users": {
            "search_fields": ["name", "email"],
            "mapping": {"name": "text", "email": "title"},
        },
        "capacity_scenarios": {
            "search_fields": ["name"],
            "mapping": {"name": "text"},
        },
        "epics": {
            "search_fields": ["q"],
            "mapping": {"name": "text", "reference_num": "title"},
        },
        "features": {
            "search_fields": ["q"],
            "mapping": {"name": "text", "reference_num": "title"},
        },
        "goals": {
            "search_fields": ["name", "reference_num", "description"],
            "mapping": {"description": "text", "name": "title"},
        },
        "ideas": {
            "search_fields": ["q"],
            "mapping": {"description": "text", "name": "title"},
        },
        "initiatives": {
            "search_fields": ["q"],
            "mapping": {"description": "text", "name": "title"},
        },
        "integrations": {"search_fields": ["name"], "mapping": {"name": "text"}},
        "products": {
            "search_fields": ["name"],
            "mapping": {"name": "text", "reference_prefix": "title"},
        },
        "release_phases": {
            "search_fields": ["name", "description"],
            "mapping": {"description": "text", "name": "title"},
        },
        "strategy_models": {
            "search_fields": ["name", "kind"],
            "mapping": {"name": "text", "kind": "title"},
        },
        "strategy_positions": {
            "search_fields": ["name", "kind"],
            "mapping": {"name": "text", "kind": "title"},
        },
        "strategy_visions": {
            "search_fields": ["name", "description"],
            "mapping": {"description": "text", "name": "title"},
        },
        "teams": {"search_fields": ["name"], "mapping": {"name": "text"}},
        "tasks": {"search_fields": ["name"], "mapping": {"name": "text"}},
    }

    def __init__(self, domain, api_key, allowed_entities, search_limit):
        self.api_url = f"https://{domain}.aha.io/api/v1/"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.allowed_entities = allowed_entities
        self.search_limit = search_limit

    def get_allowed_entities(self):
        return self.allowed_entities

    def get_allowed_entity_types(self):
        return self.ALLOWED_ENTITY_TYPES

    def get_search_limit(self):
        return self.search_limit

    def get(self, url, params={}):
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def get_entities_by_type(self, entity_type, params={}):
        url = f"{self.api_url}/{entity_type}"
        return self.get(url, params)


def get_client():
    global client
    assert (domain := app.config.get("DOMAIN")), "AHA_DOMAIN must be set"
    assert (api_key := app.config.get("API_KEY")), "AHA_API_KEY must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 20)
    allowed_entities = app.config.get(
        "ALLOWED_ENTITIES",
        [
            "users",
            "capacity_scenarios",
            "epics",
            "features",
            "goals",
            "ideas",
            "initiatives",
            "integrations",
            "products",
            "release_phases",
            "strategy_models",
            "strategy_positions",
            "strategy_visions",
            "teams",
            "tasks",
        ],
    )

    if not client:
        client = AhaApiClient(domain, api_key, allowed_entities, search_limit)

    return client
