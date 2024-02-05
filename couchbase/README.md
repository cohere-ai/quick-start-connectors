# Couchbase Connector

Connects Cohere to a Couchbase database.

## Configuration

To use this connector you must have access to a Couchbase database. It does
not install a local instance of Couchbase or load test data into it.
Also you need to add the connector host to the list of Allowed IP Addresses in the Couchbase settings.
To deploy the Couchbase connector, use the <b>python:3.11-slim-buster</b> Docker image.

This connector requires the following environment variables:

```
COUCHBASE_CONNECTION_STRING
```

This variable should contain the connection string for the Couchbase database.
This string should be set without the "couchbase://" prefix.
If you are using the Couchbase Cloud, you can get it from the "Connect" tab of the cluster.

```
COUCHBASE_USER
```

This variable should contain the username for the Couchbase database.
If you are using the Couchbase Cloud, you need to create Database Access credentials under the "Settings" -> "
Security" -> "Database Access" tab.

```
COUCHBASE_PASSWORD
```

This variable should contain the password for the Couchbase database.
If you are using the Couchbase Cloud, you need to create Database Access credentials under the "Settings" -> "
Security" -> "Database Access" tab.

```
COUCHBASE_BUCKET
```

This variable should contain the bucket name for the Couchbase database.

```
COUCHBASE_SCOPE
```

This variable should contain the scope name for the Couchbase database.

```
COUCHBASE_SEARCH_INDEX
```

This variable should contain the search index name or Full Text Alias name for the Couchbase database.
You can find the index name in the "Search" tab of the cluster.
Read more about [Full Text Search](https://docs.couchbase.com/cloud/search/search.html).

```
COUCHBASE_CONNECTOR_API_KEY
```

This variable should contain the API key for the Couchbase connector.

### Optional Configuration

```
SNOWFLAKE_SEARCH_FIELDS_MAPPING
```

This variable should contain a JSON object mapping Cohere fields
to Couchbase fields(key is Couchbase field which will be used for search
and should be correct data field from the collections we search through,
the value is Cohere field). If this variable is not set, the results will be returned as is.

```
COUCHBASE_SEARCH_LIMIT
```

This variable should contain the number of results to return from the search.
The default value is 20.

## Development

Copy the `.env-template` file to `.env` and edit the values accordingly.

```
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
