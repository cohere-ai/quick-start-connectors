# Algolia Quick Start Connector

A connector to integrate Algolia to Cohere, featuring a simple local development setup.

## Limitations

The Algolia connector searches within a specific index of your Algolia server. Because Algolia is a key-value document store, the document is returned as-is after being serialized for the `text` and `url` values currently.

## Configuration

This connector requires that the environment variables `ALGOLIA_APP_ID`, `ALGOLIA_API_KEY`, and `ALGOLIA_INDEX_NAME` be set in order to run. Additionally, if the source documents use relative URLs then `ALGOLIA_DOCUMENT_BASE_URL` can be set to ensure the final results return absolute URLs. These variables can optionally be put into a `.env` file for development.

Also, to protect this connector from abuse, the `ALGOLIA_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for bearer token authentication.

A `.env-template` file is provided with all the environment variables that are used by this demo.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```shell
$ poetry config virtualenvs.in-project true
$ poetry install --no-root

```

and start the server

```shell

$ poetry run flask --app provider --debug run --port 5000
```

This will start your server on `localhost:5000`, you can then check that the search works with:

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
