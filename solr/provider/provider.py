import logging

import pysolr
from flask import current_app as app

logger = logging.getLogger(__name__)
solr = None


def serialize_results(data, mappings):
    """
    Serialize a list of dictionaries by transforming keys based on provided mappings
    and converting values to strings.

    Parameters:
    - data (list): A list of dictionaries to be serialized.
    - mappings (dict): A dictionary specifying key mappings for transformation.

    Returns:
    list: A serialized list of dictionaries with transformed keys and string-converted values.
    """
    serialized_data = list(
        map(
            lambda item: {
                k if k not in mappings else mappings[k]: (
                    ", ".join(str(vl) for vl in v) if isinstance(v, list) else str(v)
                )
                for k, v in item.items()
            },
            data,
        )
    )
    return serialized_data


def search(query):
    global solr
    assert (host := app.config.get("SERVER_URL")), "SOLR_SERVER_URL must be set"
    assert (collection := app.config.get("COLLECTION")), "SOLR_COLLECTION must be set"
    assert (
        default_field := app.config.get("DEFAULT_FIELD")
    ), "SOLR_DEFAULT_FIELD must be set"

    if solr is None:
        core_url = f"{host}/solr/{collection}"
        solr = pysolr.Solr(core_url)

    response = solr.search(query, df=default_field)

    mappings = app.config.get("CONNECTOR_FIELDS_MAPPING", {})
    return serialize_results(response.docs, mappings)
