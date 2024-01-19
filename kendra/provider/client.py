from flask import current_app as app
import botocore
import boto3
from . import UpstreamProviderError

client = None


class KendraClient:
    DEFAULT_FIELDS_MAPPING = {}
    DEFAULT_SEARCH_LIMIT = 10

    def __init__(self, index_id, search_limit=None, fields_mapping=None):
        self.index_id = index_id
        self.search_limit = search_limit or self.DEFAULT_SEARCH_LIMIT
        self.fields_mapping = fields_mapping or self.DEFAULT_FIELDS_MAPPING
        self.kendra = boto3.client("kendra")

    def search(self, query):
        try:
            response = self.kendra.retrieve(
                QueryText=query,
                IndexId=self.index_id,
                PageSize=self.search_limit,
            )
        except botocore.exceptions.ClientError as err:
            raise UpstreamProviderError(str(err)) from err

        return response["ResultItems"]


def get_client():
    global client
    if client is not None:
        return client

    assert (index_id := app.config.get("INDEX_ID")), "KENDRA_INDEX_ID must be set"
    search_limit = app.config.get("SEARCH_LIMIT", None)
    fields_mapping = app.config.get("FIELDS_MAPPING", None)
    client = KendraClient(index_id, search_limit, fields_mapping)

    return client
