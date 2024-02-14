# Template Quick Start Connector

This is a _template_ for a simple quick start connector that return static data. This can serve as starting point for creating a brand new connector.

## Configuration

Creating a new connector is simple and requires a `TEMPLATE_CONNECTOR_API_KEY` environment variable to be set. This value will be used for Bearer authentication to protect this connector from abuse. The token will need to be passed in the request headers when you call the `/search` endpoint. **This API key only protects the connector's search endpoint itself, it is not the same as the API key that could be required to call a 3rd party service.** 

A `.env-template` is provided as an example. This should be included with all the environment variables for your specific connector.

Note: connector environment variables should be prefixed with the project's name. During initialization of the Flask app, these variables are stored as configs **without** the prefix. For example, given a project with the name `gdrive` and an environment variable `GDRIVE_SEARCH_LIMIT`, the variable can be retrieved with:

```python
from flask import current_app as app

...
search_limit = app.config.get("SEARCH_LIMIT")
```

Importantly, this variable would only be able to be retrieved from the Flask app configs **after** the app has been initialized. For reference, see `provider > __init__.py > create_app()`.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything is working

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
