# Readme Connector

Connects Cohere to Readme.

## Configuration

To use this connector, you must have a Readme account. Readme is a hosted service, and this connector
does not have a local database or test data. It uses the Readme Search Docs API:

https://docs.readme.com/main/reference/searchdocs

The required environment variables for this connector are:

- `README_API_KEY`
- `README_CONNECTOR_API_KEY`

Environment variables can optionally be placed in a file called `.env`. See `.env-template` for a
full list of available options. This file can be copied to `.env` and modified. Options that are
left empty will be ignored.

The Readme Search Docs API accepts no parameters except for the search query, therefore this connector offers limited configuration options.

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

The Flask API will be bound to :code:`localhost:5000`.

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
