import snowflake.connector
from flask import current_app as app
from itertools import product
from snowflake.connector import DictCursor
from snowflake.connector.errors import Error as SnowflakeError

from . import UpstreamProviderError

client = None


class SnowflakeClient:
    def __init__(
        self,
        user,
        password,
        warehouse,
        account,
        database,
        schema,
        table,
        mappings,
        search_limit,
    ):
        try:
            self.connection = snowflake.connector.connect(
                user=user,
                password=password,
                warehouse=warehouse,
                account=account,
                database=database,
            )
        except SnowflakeError as err:
            raise UpstreamProviderError("Error connecting to Snowflake") from err

        self.database = database
        self.schema = schema
        self.table = table
        self.mappings = mappings
        self.search_limit = search_limit

    def search(self, query):
        connection = self.connection
        search_fields = list(self.mappings.keys())
        words = query.split(" ")

        constraints = " or ".join(
            map(lambda p: f"contains({p[0]}, %s)", product(search_fields, words))
        )

        connection.cursor().execute(f"USE DATABASE {self.database};")
        query = f"""
            SELECT
            *
            FROM
            {self.schema}.{self.table}
            WHERE {constraints}
            LIMIT
            {self.search_limit};
        """

        cursor = connection.cursor(DictCursor)
        return cursor.execute(query, words * len(search_fields))


def get_client():
    global client
    if not client:
        assert (user := app.config.get("USER")), "SNOWFLAKE_USER must be set"
        assert (
            password := app.config.get("PASSWORD")
        ), "SNOWFLAKE_PASSWORD must be set"
        assert (
            warehouse := app.config.get("WAREHOUSE")
        ), "SNOWFLAKE_WAREHOUSE must be set"
        assert (account := app.config.get("ACCOUNT")), "SNOWFLAKE_WAREHOUSE must be set"
        assert (
            database := app.config.get("DATABASE")
        ), "SNOWFLAKE_DATABASE must be set"
        assert (schema := app.config.get("SCHEMA")), "SNOWFLAKE_SCHEMA must be set"
        assert (table := app.config.get("TABLE")), "SNOWFLAKE_TABLE must be set"
        assert (
            mappings := app.config.get("SEARCH_FIELDS_MAPPING")
        ), "SNOWFLAKE_SEARCH_FIELDS_MAPPINGS must be set"
        search_limit = app.config.get("SEARCH_LIMIT", 10)

        client = SnowflakeClient(
            user,
            password,
            warehouse,
            account,
            database,
            schema,
            table,
            mappings,
            search_limit,
        )

    return client
