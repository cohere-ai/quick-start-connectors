# Yext Connector

Connects Cohere to Yext Universal Search.

## Configuration

To use this connector, you must have a Yext account. Yext is a hosted service, and this connector does not include a local database or test data. It uses the Yext Universal Search: Query API.

The required environment variables for this connector are:

- `YEXT_API_KEY`
- `YEXT_ACCOUNT_ID`
- `YEXT_LOCAL`
- `YEXT_EXPERIENCE_KEY`
- `YEXT_V`
- `YEXT_CONNECTOR_API_KEY`

Optional environment variables are:

- `YEXT_LIMIT`
- `YEXT_SOURCE`
- `YEXT_VERSION`

Additionally, there are several optional environment variables. These variables, both required and optional,
directly correspond to the parameters sent to Yext in the search request. They are documented in the
Yext Universal Search: Query API documentation:

https://hitchhikers.yext.com/docs/contentdeliveryapis/search/universalsearch/#operation/query

Environment variables can optionally be placed in a file called `.env`. See `.env-template` for a
full list of available options. This file can be copied to `.env` and modified. Options that are
left empty will be ignored.

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
    --data '{
    "query": "BBQ"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
