import logging
from itertools import product
from typing import Any

import snowflake.connector
from flask import current_app as app
from snowflake.connector import DictCursor
from snowflake.connector.errors import Error as SnowflakeError

from . import UpstreamProviderError

logger = logging.getLogger(__name__)


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
                k.lower()
                if k.lower() not in mappings
                else mappings[k.lower()]: ", ".join(str(vl) for vl in v)
                if isinstance(v, list)
                else str(v)
                for k, v in item.items()
            },
            data,
        )
    )
    return serialized_data


def search(query) -> list[dict[str, Any]]:
    assert (user := app.config.get("USER")), "SNOWFLAKE_USER must be set"
    assert (password := app.config.get("PASSWORD")), "SNOWFLAKE_PASSWORD must be set"
    assert (warehouse := app.config.get("WAREHOUSE")), "SNOWFLAKE_WAREHOUSE must be set"
    assert (account := app.config.get("ACCOUNT")), "SNOWFLAKE_WAREHOUSE must be set"
    assert (database := app.config.get("DATABASE")), "SNOWFLAKE_DATABASE must be set"
    assert (schema := app.config.get("SCHEMA")), "SNOWFLAKE_SCHEMA must be set"
    assert (table := app.config.get("TABLE")), "SNOWFLAKE_TABLE must be set"
    assert (
        mappings := app.config.get("SEARCH_FIELDS_MAPPING")
    ), "SNOWFLAKE_SEARCH_FIELDS_MAPPING must be set"
    assert (max_results := app.config.get("MAX_RESULTS", 10)), "MAX_RESULTS must be set"

    if not query:
        return []

    search_fields = list(mappings.keys())

    try:
        connection = snowflake.connector.connect(
            user=user,
            password=password,
            warehouse=warehouse,
            account=account,
            database=database,
        )
    except SnowflakeError as err:
        raise UpstreamProviderError("Error connecting to Snowflake") from err

    words = query.split(" ")

    constraints = " or ".join(
        map(lambda p: f"contains({p[0]}, %s)", product(search_fields, words))
    )

    connection.cursor().execute(f"USE DATABASE {database};")
    query = f"""
        SELECT
        *
        FROM
        {schema}.{table}
        WHERE {constraints}
        LIMIT
        {max_results};
    """

    cursor = connection.cursor(DictCursor)
    cursor.execute(query, words * len(search_fields))

    return serialize_results(cursor.fetchall() or [], mappings)
