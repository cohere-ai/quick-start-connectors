# Miro Quick Start Connector

Connects Cohere to Miro, the planning and collaboration tool.

## Limitations

The Miro connector currently allows full-text search of a board's title and description, including partial matching.

## Configuration

To configure this connector you will have to either create a new Miro app, see [here](https://developers.miro.com/docs/rest-api-build-your-first-hello-world-app#step-1-create-your-app-in-miro), or configuring an existing app.

Your app will require at the least the `board:read` permission to allow searching your boards, once that is done you can save and install the app, a message should notify you that the app was successfully installed, and give you an access token. Use this token for the `MIRO_ACCESS_TOKEN` environment variable.

Finally, to protect this connector from abuse, the `MIRO_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.


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
