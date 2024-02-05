# Shortcut Connector

Connects Cohere with Shortcut, the task tracking tool.

Currently it supports searching through Stories created in your Shortcut org.

## Configuration

To start, head over to https://app.shortcut.com/settings/account/api-tokens to generate an API token, then use this value for the `SHORTCUT_API_TOKEN` environment variable.

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
