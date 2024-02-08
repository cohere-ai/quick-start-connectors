# Elasticsearch Quick Start Connector

This project allows you to create a simple connection to Elasticsearch that can be used with Cohere's API.

## Limitations

Currently this connector will perform full-text search, but only for a single index of your Elasticsearch cluster. Since Elasticsearch is essentially a key-value store, it will return the full document as-is to Cohere.

## Configuration

You will need to configure this connector with the connection details and authentication credentials to your Elasticsearch instance. These will need to be set in your environment variables, we recommend creating a `.env` file that you can base off the `.env-template`.

1. To configure your connection details, _either_ `ELASTIC_CLOUD_ID` or `ELASTIC_URL` need to be provided. Then, you will need to specify the `ELASTIC_INDEX` to query.

2. To authorize your connection, supply _either_ `ELASTICS_API_KEY` or both `ELASTIC_USER` and `ELASTIC_PASS`.

Optionally, you can set the `ELASTIC_SEARCH_LIMIT` parameter to determine the maximum number of results returned by a search.

Finally, to protect this connector from abuse, the `ELASTIC_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Development

(Optional) For local development, you can start Elasticsearch and fill it with data by running:

```bash
  $ docker-compose run data-loader
```

After running the command, your Elasticsearch instance will run in the background on the default localhost:9200. To start it again later, you can
run:

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
  $ poetry run flask --app provider --debug run
```

Check with curl to see that everything is working

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
