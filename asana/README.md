# Asana Quick Start Connector

A connector to integrate Asana, the project management tool, to Cohere. Featuring a simple local development setup.

## Limitations

The Asana connector only offers full-text search for Task objects.

## Configuration

To use this connector, head to your Asana Developer Console. From here, you can create a new Personal Access Token. Use this value for the `ASANA_ACCESS_TOKEN` environment variable. Then, head to your Admin Console. The URL at the top of your web browser should look like `https://app.asana.com/admin/<workspace_gid>`, grab the `<workspace_gid>` value and use it for `ASANA_WORKSPACE_GID`.

Also, to protect this connector from abuse, the `ASANA_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for bearer token authentication.

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
    --data '{
    "query": "BBQ"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
