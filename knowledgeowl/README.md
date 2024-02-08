# Knowledge Owl Connector

Connects Cohere to Knowledge Owl, the planning and collaboration tool.

## Configuration

To use this connector you will require a Knowledge Owl organization. Then, head to your Account > API and generate an API key. Cohere will only require the `GET` permissions. Use this value for the `KNOWLEDGEOWL_API_KEY` environment variable.

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
