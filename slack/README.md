# Slack Connector

Connects Cohere with Slack.

## Configuration

This connector requires that the environment variable `SLACK_OAUTH_ACCESS_TOKEN` is set in order to run. This variable
can optionally be put into a `.env` file for development.
A`.env-template` file is provided as a reference.

### Steps to create an OAuth Access Token

- Visit [Slack API](https://api.slack.com/apps) and create a new app.
- Select the workspace where you want to install the app.
- Go to the "OAuth & Permissions" page, and add the search:read scope under "User Token Scopes."
- Install the app in your workspace.
  You'll be provided with an OAuth Access Token. Set the env var `SLACK_OAUTH_ACCESS_TOKEN` to this value.

### Optional Configuration

```
SLACK_CONNECTOR_API_KEY
```

This variable can be set to a string that will be used to authenticate requests to the connector.

```
SLACK_SEARCH_LIMIT
```

This variable can be set to limit the number of results returned from Slack. The default is 20

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
