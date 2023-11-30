import logging
from typing import Any

from docusign_esign.models.envelopes_information import EnvelopesInformation
from flask import current_app as app

from . import UpstreamProviderError
from .client import get_client

logger = logging.getLogger(__name__)


def process_response_data(data: EnvelopesInformation):
    envelopes = data.envelopes
    results = []
    if envelopes:
        for envelope in envelopes:
            results.append(envelope.to_dict())
    return results


def search(query: str) -> list[dict[str, Any]]:
    api_client = get_client()
    from_date = app.config.get("FROM_DATE", "2018-01-01")
    to_date = app.config.get("TO_DATE", False)

    data = api_client.get_list_status_changes(query, from_date, to_date)
    if not data:
        logger.error(f"DocuSign provider error: {data}")
        raise UpstreamProviderError(f"DocuSign provider error: {data}")
    return process_response_data(data)
