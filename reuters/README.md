# Reuters Quick Start Connector

Connects Cohere to Reuters, enabling search across news content.

## Limitations

The Reuters connector allows multi-keyword full-text search for the body, headline, and caption fields of a Reuters
article.

## Configuration

To use this connector, you will need a Reuters paid account, and have the following credentials stored inside a `.env`
at the root of this project:

- REUTERS_CLIENT_ID
- REUTERS_CLIENT_SECRET
- REUTERS_AUDIENCE
- REUTERS_CONNECTOR_API_KEY (optional - used for the Reuters Connector security)

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
