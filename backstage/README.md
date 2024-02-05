# Backstage Connector

Connects Cohere with Backstage.io, featuring a simple local development setup.

## Configuration

This connector requires the following environment variables:

```
BACKSTAGE_SERVER_URL

This variable should contain the URL to the Backstage server.
```

```
BACKSTAGE_CONNECTOR_API_KEY

This variable should contain the API key for the connector.
```

### Optional configuration

```
BACKSTAGE_ACCESS_TOKEN

This variable may contain the access token for the Backstage API if used.
```

```
BACKSTAGE_SEARCH_ENDPOINT

This variable may contain the endpoint for the search API. By default it is set to "api/search/query"
```

```
BACKSTAGE_SEARCH_TERM

This variable may contain the name of the query parameter for the search query of your Backstage Search API. By default it is set to "term"
```

```
BACKSTAGE_CONNECTOR_FIELDS_MAPPING

This variable may contain a JSON object mapping Cohere fields
to Backstage fields(key is Backstage field, value is Cohere field).
If it is not set, the response fields will be returned as is.
```

## Development

Setup Backstage locally by following the instructions [here](https://backstage.io/docs/getting-started/create-an-app).
Or you can use the [Docker](https://backstage.io/docs/deployment/docker).
Please note that the [Backstage Search](https://backstage.io/docs/features/search/) needs to be set up as well.
Then start the Backstage.
Or you can use the [Backstage demo server](https://demo.backstage.io/)

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
