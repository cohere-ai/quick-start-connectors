# Coda Quick Start Connector

Connects Cohere to Coda, the collaborative document editor.

## Limitations

The Coda connector can only search Document titles, with in-order search terms.

Note: ONLY Enterprise accounts will return the document body using their API. Regular accounts will only return document metadata, without any of the contents.

## Configuration

To use this connector, you will need a Coda account. Then click on the top-right user icon and go to
Account Settings. Now in the Api Settings section you can generate an API Token. Use this value
for the `CODA_API_TOKEN`.

Environment variables can optionally be placed in a file called `.env`. See `.env-template` for a
full list of available options. This file can be copied to `.env` and modified. Options that are
left empty will be ignored.

Finally, to protect this connector from abuse, the `CODA_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  poetry config virtualenvs.in-project true
  poetry install --no-root
```

To run the Flask server in development mode, please run:

```bash
  poetry run flask --app provider --debug run
```

The Flask API will be bound to :code:`http://127.0.0.1:5000`.

```bash
  curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://127.0.0.1:5000/ui/
