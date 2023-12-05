import logging

import os
from typing import Any

from .client import get_client

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

BIGQUERY_TABLE_NAME = os.environ.get("BIGQUERY_TABLE_NAME")
BIGQUERY_COLUMN_NAME = os.environ.get("BIGQUERY_COLUMN_NAME")

"""
Explanation: BigQuery SQL's most search-like feature is REGEXP_CONTAINS.
This method builds the regex to support it.

(?i):       enables case-insensitive matching
.*<term>.*: enables partial matching
|:          enables multiple terms
"""


def build_regex(query) -> str:
    # Assumes query delimiter is whitespace
    search_terms = query.split(" ")
    separator = ".*|.*"

    return f"(?i).*{separator.join(search_terms)}.*"


def search(query) -> list[dict[str, Any]]:
    client = get_client()

    regex = build_regex(query)

    QUERY = f"""
        SELECT * from {BIGQUERY_TABLE_NAME}
        WHERE REGEXP_CONTAINS({BIGQUERY_COLUMN_NAME}, r'{regex}');
    """

    try:
        # API request, returns async job
        query_job = client.query(QUERY)
        # Wait for async job completion
        rows = query_job.result()
    except Exception as e:
        message = f"Encountered exception: `{str(e)}` during BigQuery query."
        raise UpstreamProviderError(message)

    # Convert response to array of dictionaries
    records = [dict(row) for row in rows]

    return records
