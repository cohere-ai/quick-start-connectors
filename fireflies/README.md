# Fireflies Connector

Connects Cohere to Fireflies.

## Configuration

This connector requires the following environment variables:

```
FIREFLIES_API_KEY
```

This variable should contain the API key of the Fireflies account.
To get the API key, use the instructions [here](https://docs.fireflies.ai/)

```
FIREFLIES_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

### Optional configuration

```
FIREFLIES_SEARCH_LIMIT
```

This variable may contain the maximum number of results to return from Fireflies. Default value is 20.
Maximum value is 50.

These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.

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
