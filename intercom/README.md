# Intercom Connector

Connects Cohere to Intercom, the customer support portal.

Currently, this connector only searches within Conversations.

## Configuration

To use this connector, follow these steps:

1. Create a [new Intercom developer app here.](https://app.intercom.com/a/developer-signup)
2. Retrieve your app's Authentication Access token. Use this value for the `INTERCOM_ACCESS_TOKEN` environment variable.

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
