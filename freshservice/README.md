# Freshservice Connector

Connects Cohere to Freshservice, the customer support tool.

## Configuration

To use this connector you will need to have access to your Freshservice support portal. Then, from your Profile Settings, you should see an API key on the right-hand side. Use this value for the `FRESHSERVICE_API_KEY` environment variable.

You will also need your domain name, which is formatted like `https://mydomain.freshservice.com`, use this for `FRESHSERVICE_DOMAIN`.

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
