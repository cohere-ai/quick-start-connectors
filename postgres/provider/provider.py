import logging

import psycopg2
import psycopg2.extras
from flask import current_app as app

logger = logging.getLogger(__name__)
pg_connection = None


def search(query):
    global pg_connection

    if pg_connection is None:
        pg_connection = psycopg2.connect(app.config["DSN"])

    cursor = pg_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    search_query = (
        "SELECT * "
        f'FROM {app.config["TABLE_NAME"]} '
        f'WHERE {app.config["FTS_COLUMN"]} @@ to_tsquery(\'{app.config["FTS_LANG"]}\', %s)'
    )

    query_and = query.replace(" ", " & ")
    cursor.execute(search_query, (query_and,))
    response = cursor.fetchall()
    cursor.close()

    return response
