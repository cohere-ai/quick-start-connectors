# Egnyte Connector

Connects Cohere to Egnyte.

## Configuration

To use this connector, you will an Egnyte organization. First, fetch your Egnyte org's domain by looking at the URL of the web app when you're logged in. It should look like `mycompany.egnyte.com`. Use this value for the `EGNYTE_DOMAIN_NAME` environment variable.

Then, you will need to create an API key. Follow the [instructions](https://developers.egnyte.com/docs/read/Getting_Started#Request-an-API-Key) here to request an API key from Egnyte. Based on their docs, it can take up to a day to receive one because it requires manual approval. Once you have one, use it for the `EGNYTE_API_KEY` variable.

Finally, to protect this connector from abuse, the `EGNYTE_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

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
