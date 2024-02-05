# Techcrunch Connector

This package is a utility for connecting Cohere to Techcrunch.
Note: this connector is just a scraper for Techcrunch search results,
it will require changes if Techcrunch's search page DOM model is modified.

## Configuration

The search connector requires the following environment variables:

```
TECHCRUNCH_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Next, start up the search provider server:

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
