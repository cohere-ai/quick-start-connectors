# Weaviate Quick Start Connector

Connectors Cohere to a Weaviate database.

It relies on the `weaviate-python` package for managing the connection and uses Weaviate's GraphQL API under the hood.

## Limitations

The Weaviate connector performs a near-text search for a defined class and properties. The nearText operator Weaviate provides converts the query to a vector using Cohere's inference API and uses that vector as the basis for a vector search.

# Configuration

This connector requires the following environment variables:

```
WEAVIATE_SERVER_URL

This variable should contain the URL of the Weaviate instance.
```

```
WEAVIATE_SCHEMA_CLASS

This variable should contain the name of the class to search on.
```

```
WEAVIATE_CONNECTOR_API_KEY

This variable should contain the API key for the connector.
```

### Optional configuration

```
WEAVIATE_CONNECTOR_FIELDS_MAPPING

This variable may contain a JSON object mapping Cohere fields
to Weaviate fields(key is Weaviate field, value is Cohere field).
If it is not set, the response fields will be returned as is.
```

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

A Weaviate database is available as a Docker container. It uses Cohere for vectorizing data and requires
the `COHERE_APIKEY` environment variable to be set.

```bash
  $ export COHERE_APIKEY=<Your Cohere API key>
```

Start the test Weaviate database and fill it with data by running

```bash
  $ docker-compose run data-loader
```

After running the `data-loader`, the Weaviate instance will continue to run in the background. If you need to start it
again later, Weaviate can be started again without needing to load the data:

Finally, start the server

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
