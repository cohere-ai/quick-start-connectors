# Trello Connector

Connects Cohere to the Trello project management tool.

## Configuration

To use this connector you must create a Power-Up in your Trello account. Once you have created
a Power-Up, you will be able to see an API Key for the Power-Up. Beside the API key in the Trello
settings page for the Power-Up, there is a link to generate a token. Click the "Token" link and
generate a token. After you have authorized the Power-Up, a token will be displayed. Use this
value for `TRELLO_API_TOKEN`. Note that this is these credentials are associated with the Trello
Power-Up, and is not an Atlassian API token for your user account.

The required environment variables for this connector are `TRELLO_API_KEY`, `TRELLO_API_TOKEN`, and `TRELLO_CONNECTOR_API_KEY`.
Additionally, there are 20 optional environment variables. These directly correspond to the
optional parameters sent to Trello in the search request. They are documented in the Trello Search
API documentation:

https://developer.atlassian.com/cloud/trello/rest/api-group-search/#api-search-get

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
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
