from contentful import Client
from flask import current_app as app

client = None

PREVIEW_API_URL = "preview.contentful.com"


class ContentfulApiClient(Client):
    def __init__(
        self, space_id, access_token, environment, content_type, mapping, search_limit
    ):
        super().__init__(
            space_id,
            access_token,
            api_url=PREVIEW_API_URL,
            environment=environment,
            max_include_resolution_depth=20,
            reuse_entries=True,
            content_type_cache=False,
        )
        self.content_type = content_type
        self.mapping = mapping
        self.search_limit = search_limit

    def get_search_limit(self):
        return self.search_limit

    def get_content_type(self):
        return self.content_type

    def get_mapping(self):
        return self.mapping


def get_client():
    global client
    assert (space_id := app.config.get("SPACE_ID")), "CONTENTFUL_SPACE_ID must be set"
    assert (
        access_token := app.config.get("PREVIEW_ACCESS_TOKEN")
    ), "CONTENTFUL_PREVIEW_ACCESS_TOKEN must be set"
    assert (
        environment := app.config.get("ENVIRONMENT")
    ), "CONTENTFUL_ENVIRONMENT must be set"
    limit = app.config.get("SEARCH_LIMIT", 20)
    mapping = app.config.get("FIELDS_MAPPING", {})
    content_type = app.config.get("CONTENT_TYPE_SEARCH", None)

    if not client:
        client = ContentfulApiClient(
            space_id, access_token, environment, content_type, mapping, limit
        )

    return client
