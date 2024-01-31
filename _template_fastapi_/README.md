# Template Quick Start Connector

This is a _template_ based on `FastAPI` and `Pydantic` for a simple quick start connector that returns static data. This can serve as starting point for creating a brand new connector.

## Configuration

This connector is very simple and only needs a `CONNECTOR_API_KEY` environment variable to be set. This value will be used for bearer token authentication to protect this connector from abuse.

A `.env-template` file is provided with all the environment variables that are used by this connector.

Set also your connector name, description and authors in the `pyproject.toml` configuration file.

Define your own `Pydantic` models in `provider/datamodels.py`.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry run uvicorn app:app --app-dir provider --port 5000 --reload
```

and check with curl to see that everything is working

```bash
$ curl --request POST \
       --url http://localhost:5000/search \
       --header 'Content-Type: application/json' \
       --header 'Authorization: Bearer YOUR_BEARER_TOKEN' \
       --data '{"query": "what are the latest tech news?"}'
  ```