import logging
from typing import Any

import botocore
import boto3
from flask import current_app as app

from . import UpstreamProviderError


logger = logging.getLogger(__name__)


def search(query) -> list[dict[str, Any]]:
    assert (index_id := app.config.get("INDEX_ID")), "KENDRA_INDEX_ID must be set"

    kendra = boto3.client("kendra")

    try:
        response = kendra.retrieve(QueryText=query, IndexId=index_id)
    except botocore.exceptions.ClientError as err:
        raise UpstreamProviderError(str(err)) from err

    return response["ResultItems"]
