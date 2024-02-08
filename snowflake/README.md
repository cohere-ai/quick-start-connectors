# Snowflake Quick Start Connector

Connects Cohere to a Snowflake database.

## Limitations

Snowflake does not offer full-text search. Instead, this connector uses SQL constraints to retrieve rows in your DB.

## Configuration

To use this connector you must have access to a Snowflake database. For testing, this connector offers a development setup guide below.

Once you have the dev setup ready, or if you have an existing Snowflake instance, you can create a `.env` based off the `.env-template` file.

Fill in these variables to setup your connection to Snowflake:

- `SNOWFLAKE_USER`: User to access the DB
- `SNOWFLAKE_PASSWORD`: Password associated with the above User
- `SNOWFLAKE_ACCOUNT`: Snowflake Account, this should be visible in your URL and look like abcdefg-ab12345
- `SNOWFLAKE_WAREHOUSE`: Warehouse
- `SNOWFLAKE_DATABASE`: Database
- `SNOWFLAKE_SCHEMA`: Schema
- `SNOWFLAKE_TABLE`: Table you want to search

To configure the search functionality:

- `SNOWFLAKE_SEARCH_FIELDS_MAPPING`: Contains a JSON object mapping Snowflake fields to Cohere fields, determines what the request response will look like. For example, a DB row containing {"id": 5, "description": "I am a row"} could be mapped to {"description": "text"}. This will return the description as the `text` key value for Coral to ingest. We recommend adding `text`, `title` and `url` (if exists) fields. Other document keys that are not present in the mapping will be returned as-is.

- `SNOWFLAKE_SEARCH_LIMIT` (Optional): Configures the max amount of search results returned

Finally, to configure Connector-level Bearer auth, you can set the `SNOWFLAKE_CONNECTOR_API_KEY`.

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
  curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
