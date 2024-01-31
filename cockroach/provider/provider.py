import logging

import psycopg2
import psycopg2.extras
from flask import current_app as app

logger = logging.getLogger(__name__)
pg_connection = None


def prepare_for_serialization(data, field_to_remove):
    prepared_data = []
    for item in data:
        item.pop(field_to_remove)
        prepared_data.append(item)

    return prepared_data


def serialize_results(data, mappings={}):
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
    global pg_connection
    assert (
        database_url := app.config.get("DATABASE_URL")
    ), "COCKROACH_DATABASE_URL must be set"
    assert (
        database_table := app.config.get("TABLE_NAME")
    ), "COCKROACH_TABLE_NAME must be set"
    assert (
        fts_column := app.config.get("FTS_COLUMN")
    ), "COCKROACH_FTS_COLUMN must be set"
    assert (fts_lang := app.config.get("FTS_LANG")), "COCKROACH_FTS_LANG must be set"

    if pg_connection is None:
        pg_connection = psycopg2.connect(database_url)

    cursor = pg_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    search_query = (
        "SELECT * "
        f"FROM {database_table} "
        f"WHERE {fts_column} @@ to_tsquery('{fts_lang}', %s)"
    )

    query_and = query.replace(" ", " & ")
    cursor.execute(search_query, (query_and,))
    results = cursor.fetchall()
    cursor.close()

    return serialize_results(
        prepare_for_serialization(results, fts_column),
        app.config.get("FIELDS_MAPPING", {}),
    )
