# Opensearch Quick Start Connector

This package connects Cohere to Opensearch. It features a simple local development setup.

# Limitations

The Opensearch connector features full-text search but only currently searches within a single index of your cluster. Note that since Opensearch is a key-value document store, the document is returned as-is, it is highly recommended to set the `OPENSEARCH_FIELDS_MAPPING` environment variable to return a document format ingestable by Cohere. This should include `snippet`, `title`, and `url` (if exists) keys.

## Configuration

This connector requires the following environment variables:

```
OPENSEARCH_HOST
```

This variable should contain the hostname of the Opensearch instance.

```
OPENSEARCH_PORT
```

This variable should contain the port of the Opensearch instance.

```
OPENSEARCH_USER
```

This variable should contain the username of the Opensearch instance.

```
OPENSEARCH_PASS
```

This variable should contain the user password of the Opensearch instance.

```
OPENSEARCH_INDEX
```

This variable should contain the index name of the Opensearch instance to search through.

```
OPENSEARCH_USE_SSL
```

This variable should contain a boolean value(true, false) to indicate whether to use SSL or not.
If this variable is not set, it will default to true.

```
OPENSEARCH_SEARCH_LIMIT
```

This variable may contain the maximum number of results to return from Opensearch. Default value is 100.

```
OPENSEARCH_FIELDS_MAPPING
```

This variable may contain a JSON object mapping Cohere fields
to Opensearch fields(key is Opensearch field, value is Cohere field).
If it is not set, the response fields will be returned as is.

```
OPENSEARCH_CONNECTOR_API_KEY
```

This variable should contain the API key for the connector.

These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.

## Development

To start OpenSearch locally and fill it with data run the following command:

```bash
$ docker-compose run data-loader
```

After running the `data-loader`, the OpenSearch instance will continue to run in the background.
If you need to start it again later, OpenSearch can be started again without needing to load the data:

```bash
 $ docker-compose up
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
