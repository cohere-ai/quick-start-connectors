# Opsgenie Connector

This package is a utility for connecting Cohere to Opsgenie.

## Configuration

The search connector requires the following environment variables:

```
OPSGENIE_DOMAIN_URL
```

This variable should contain the URL of your Opsgenie domain.

```
OPSGENIE_API_KEY
```

This variable should contain the API key for the Opsgenie domain. To get an API key, use
this [link](https://docs.opsgenie.com/docs/api-key-management).

```
OPSGENIE_CONNECTOR_API_KEY
```

This variable should contain the API key for the connector.

## Optional Configuration

```
OPSGENIE_SEARCH_LIMIT
```

This variable might contain the maximum number of results to return from Opsgenie. Max is 100, default is 20.

## Development

Create a virual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Next, start up the search connector server:

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything works:

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
