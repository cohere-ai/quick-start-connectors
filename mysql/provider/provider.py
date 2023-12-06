import logging
import os

from mysql import connector
from flask import current_app as app

logger = logging.getLogger(__name__)


def search(query):
    assert (host := app.config.get("HOST")), "MYSQL_HOST must be set"
    assert (user := app.config.get("USER")), "MYSQL_USER must be set"
    assert (password := app.config.get("PASSWORD")), "MYSQL_PASSWORD must be set"
    assert (database := app.config.get("DATABASE")), "MYSQL_DATABASE must be set"
    assert (table_name := app.config.get("TABLE_NAME")), "MYSQL_TABLE_NAME must be set"
    assert (columns := app.config.get("FTS_COLUMNS")), "MYSQL_FTS_COLUMNS must be set"

    connection = connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    cursor = connection.cursor(dictionary=True)

    search_query = f"""
        SELECT *
        FROM {table_name}
        WHERE
        MATCH({columns})
        AGAINST(%s);
    """

    logger.debug(f'Querying for "{query}"')
    cursor.execute(search_query, (query,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data
