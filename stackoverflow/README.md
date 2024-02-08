# StackOverflow (for Teams) Quick Start Connector

Connects Cohere to StackOverflow for Teams.

## Limitations

This connector does NOT search StackOverflow's public forums, but rather is configured to search your private StackOverflow instance, allowing you to search for Questions by title.

## Configuration

This connector requires the name of your StackOverflow Team, and a Personal Access Token. Set these inside a `.env` file for the `STACKOVERFLOW_TEAM` and `STACKOVERFLOW_PAT` variables respectively. For reference, see the `.env-template`.

To retrieve your PAT, head over to your StackOverflow for Teams org and go to Account Settings. Under the left-hand side API tab you should see Personal Access Tokens. Go to this page and Create a new PAT, with the required Team, Read-only scope, and expiration date (if needed).

To secure your connector, you can set the `STACKOVERFLOW_CONNECTOR_API_KEY` environment variable to a secure value for this connector's Bearer Authentication.

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
