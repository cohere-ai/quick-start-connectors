# Crunchbase Connector

This package is a utility for connecting Cohere to Crunchbase.

## Configuration

The search connector requires the following environment variables:

```
CRUNCHBASE_API_KEY
```

This variable should contain the API key of the Crunchbase account. To get the API key, use the
instructions [here](https://www.crunchbase.com/account/integrations/crunchbase-api)

```
CRUNCHBASE_CONNECTOR_API_KEY
```

This variable is used to authenticate users using bearer token.

### Optional configuration

```
CRUNCHBASE_SEARCH_LIMIT
```

This variable may contain the maximum number of results to return from Crunchbase. Default value is 20.

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
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Authorization: Bearer <<CRUNCHBASE_CONNECTOR_API_KEY>>' \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "cohere ai"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
