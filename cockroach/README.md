# CockroachDB Connector

This package is a utility for connecting Cohere to a Cockroach database.

## Configuration

This connector requires the following environment variables:

```
COCKROACH_DATABASE_URL
```

This variable should contain the URL for the Cockroach database.
For cloud-based Cockroach databases, you can find the URL in the CockroachDB Console.
Just click on the "Connect" in the Cluster Overview page and copy the DATABASE_URL.
Usually, it looks like this:

```
postgresql://<SQL-USER>:<SQL-USER-PASSWORD>@<instance>.cockroachlabs.cloud:26257/<database>
```

```
COCKROACH_TABLE_NAME
```

This variable should contain the table name for the Cockroach database to search in.

```
COCKROACH_FTS_COLUMN
```

This variable should contain the column name for the Cockroach database to search.
This column should be of type `tsvector`. To create such a column, you can use instructions
[here](https://www.cockroachlabs.com/docs/stable/full-text-search)

```
COCKROACH_FTS_LANG
```

This variable should contain the language for the Cockroach database to search which
was used to create the `tsvector` column.
Please note that you need to create Gin index based on the `tsvector` column.

```
COCKROACH_CONNECTOR_API_KEY
```

This variable should contain the API key for the connector.

## Optional configuration

```
COCKROACH_FIELDS_MAPPING
```

This variable should contain a JSON object mapping Cohere fields
to Cockroach fields(key is Cockroach table field,
the value is Cohere field). If this variable is not set, the data will be returned as is.

## Development

To run the connector locally, you will need to have a Cockroach database running.
To load test data into the database, set the COCKROACH_DATABASE_URL in the .env file to point to your
database.
Then run the load_data.py file.

```bash
  $ python load_data.py
```

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything is working

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
