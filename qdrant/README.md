# Qdrant Quick Start Connector

Connects Cohere to a Qdrant database.

It relies on the `qdrant-client` package for managing establishing the connection and performing vector searches. This implementation also uses Cohere's
embedding API to generate search vectors.

## Limitations

The Qdrant connector performs a vector search of the DB by embedding the search query with Cohere's embedding API.

## Configuration

This connector requires that an environment variables `QDRANT_COHERE_APIKEY` and `QDRANT_CONNECTOR_API_KEY` be set in order to run. This environment variable can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the other environment variable that are used by this demo.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Start the test Qdrant cluster and fill it with data by running

```bash
  $ docker-compose run data-loader
```

After running the `data-loader`, the Qdrant container will continue to run in the background. If you need to start it again later, the Qdrant can be started again without needing to load the data:

```bash
  $ docker-compose up
```

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
