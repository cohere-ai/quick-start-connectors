# Crunchbase Connector

This package is a utility for connecting Cohere to Crunchbase.

## Limitations

The Crunchbase API has a limit of 200 requests per minute.

The [Autocomplete API](https://data.crunchbase.com/docs/using-autocomplete-api) included in API v4.0 is intended to help you quickly find the entity you are looking for by suggesting a list of entities based on your query string & the defined collection(s) you are interested in. As such, the API is designed to return a small number of results (10 by default) that are the best matches for the query string. The API is not designed to return all possible matches for a query string, and as such, it is not recommended to use the API to drive a machine process to find the entity you are looking for.

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
  curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
