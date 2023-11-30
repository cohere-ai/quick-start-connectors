# Snowflake Connector

Connects Cohere to a Snowflake database.

Note: Snowflake does not have a fulltext search feature.

## Configuration

To use this connector you must have access to a Snowflake database. This connector does
not install a local instance of Snowflake or load test data into it.

It requires the following environment variables:

```
SNOWFLAKE_USER

This variable should contain the username for the Snowflake database.
```

```
SNOWFLAKE_PASSWORD

This variable should contain the password for the Snowflake database.
```

```
SNOWFLAKE_ACCOUNT

This variable should contain the account name for the Snowflake database.
```

```
SNOWFLAKE_WAREHOUSE

This variable should contain the warehouse name for the Snowflake database.
```

```
SNOWFLAKE_DATABASE

This variable should contain the database name for the Snowflake database.
```

```
SNOWFLAKE_SCHEMA

This variable should contain the schema name for the Snowflake database.
```

```
SNOWFLAKE_TABLE

This variable should contain the table name for the Snowflake database.
```

```
SNOWFLAKE_CONNECTOR_API_KEY

This variable should contain the API key for the Snowflake connector.
```

```
SNOWFLAKE_SEARCH_FIELDS_MAPPING

This variable should contain a JSON object mapping Cohere fields
to Snowflake fields(key is Snowflake field which will be used for search
and should be correct data field from table we search through,
the value is Cohere field).
```

## Using Test Data

Snowflake has a 30-day trial. For local development of this connector, you can use a Snowflake trial account with the Standard Edition.

The values in `.env-template` are based on creating a Snowflake database named `bbq`, with a schema called
`bbq`, and the `testdata/bbq.csv` file from this repo being imported into the Snowflake database, using the
GUI tool on the Snowflake Account Admin page.

Before importing the CSV, you must create the `bbq` table.

```sql
create table bbq2
(
    ID          text,
    Name        text,
    Description text,
    Features    text,
    Brand       text,
    Color       text,
    Country     text,
    Rank        text
);
```

## Development

Copy the `.env-template` file to `.env` and edit the values accordingly.

```bash
cp .env-template .env
```

To run the Flask server you must first install the dependencies with poetry. We recommend using in-project
virtual environments:

```bash
poetry config virtualenvs.in-project true
poetry install
```

Then start the server:

```bash
poetry run flask --app provider run --debug
```

Once the Mongo and Flask servers are running, you can perform a test request with the following cURL call:

```bash
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "charcoal"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
