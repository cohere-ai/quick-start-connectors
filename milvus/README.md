# Milvus Quick Start Connector

This package is a utility for connecting Cohere to a Milvus database.

It relies on the `pymilvus` package for managing establishing the connection and performing vector searches. This implementation also uses Cohere's embedding API to generate search vectors.

## Limitations

Currently the search is performed by embedding the search query with Cohere's embedding API.

## Configuration

The search connector requires that an environment variable `MILVUS_COHERE_APIKEY` be set in order to run. This environment variable can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the other environment variable that are used by this demo.

Finally, to protect this connector from abuse, the `MILVUS_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Start the test Milvus cluster and fill it with data by running

```bash
  $ docker-compose run data-loader
```

After running the `data-loader`, the Milvus containers will continue to run in the background. If you need to start them again later, the Milvus cluster can be started again without needing to load the data:

```bash
  $ docker-compose up
```

Finally, start the server

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything is working

```bash
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "stainless propane griddle"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
