# Snowflake Quick StartConnector

Connects Cohere to a Snowflake database.

## Limitations

Snowflake does not offer full-text search. Instead, this connector uses SQL constraints to retrieve rows in your DB.

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
SNOWFLAKE_SEARCH_FIELDS_MAPPING

This variable should contain a JSON object mapping Cohere fields
to Snowflake fields(key is Snowflake field which will be used for search
and should be correct data field from table we search through,
the value is Cohere field).
```

```
SNOWFLAKE_CONNECTOR_API_KEY

This variable should contain the API key for the Snowflake connector.
```

## Setting up Dev Environment and loading Test Data

Snowflake provides a free [30-day trial](https://signup.snowflake.com/) that you can use to setup a local development environment. For our purposes, selecting the Standard Edition will suffice.

Note that the default values in the `.env-template` file are based on the data in `dev/bbq.csv` being loaded into a Snowflake database named `bbq`, with a schema called `bbq`.

To load this data, go to your newly created Snowflake instance and follow these steps:

1. Under Data > Databases, select `+ Database` and add a new Database named `bbq`.
2. Under your newly created `bbq` Database, select `+ Schema` and add a new Schema named `bbq`.
3. Select the `bbq` schema and created a new Table, copy paste the following into the create command:

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

4. After creating the table, you can then select it and click `Load Data`, where you can then upload the `dev/bbq.csv` file. Select the option to ignore headers and to have optional enclosing double quotes.

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
