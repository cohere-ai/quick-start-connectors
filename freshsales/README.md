# Freshsales Quick Start Connector

Connects Cohere to Freshsales, the sales CRM tool.

## Limitations

The Freshsales connector features full-text search on 4 types of entities: Users, Contacts, Sales accounts, and Deals. These are based off your environment variables, which are set to `True` by default. Because the search API returns only a compact version of the entity, another API call is required to fetch the full entity details.

## Configuration

To use this connector you will need a Freshsales workspace. Then, from your top-right avatar, click
Settings > API Settings > Confirm API key. You should see your API key and bundle alias values, use these
for the `FRESHSALES_API_KEY` and `FRESHSALES_BUNDLE_ALIAS` environment variables.

There are additional environment variables that define which entities are enabled for search. Currently,
Freshsales allows searching Users, Contacts, Deals, and Sales Accounts, by default the `.env-template` file has
these values enabled.

Optionally, the `FRESHSALES_SEARCH_LIMIT` variable can be set to set the maximum number of search results returned. By default, this is set to 15.

Finally, to protect this connector from abuse, the `FRESHSALES_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

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
