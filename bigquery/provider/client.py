import os
from google.cloud import bigquery
from . import UpstreamProviderError

CREDENTIALS_FILE_PATH = "./credentials.json"


def get_client():
    """
    Google BigQuery API client requires user to authenticate with a
    service account's credentials. Make sure to see the README for details.
    """

    assert os.path.exists(
        CREDENTIALS_FILE_PATH
    ), f"credentials.json must be created at {CREDENTIALS_FILE_PATH}, see README"

    try:
        client = bigquery.Client.from_service_account_json(CREDENTIALS_FILE_PATH)
    except Exception as e:
        message = (
            "Error authenticating BigQuery client with the provided credentials.json"
        )
        raise UpstreamProviderError(message)

    return client
