# Yammer Connector

Connects Cohere to Yammer.

## Configuration

This connector requires the following environment variables:

```
YAMMER_API_TOKEN
```

To get a Yammer API token, you need to register an app with Yammer. You can do this by following the
instructions [here](https://learn.microsoft.com/en-us/rest/api/yammer/app-registration).
Yammer connector uses the Server-Side Flow to obtain the token.
You can follow the instructions [here](https://learn.microsoft.com/en-us/rest/api/yammer/oauth-2)
to get the token.

```
YAMMER_CONNECTOR_API_KEY
```

This variable should contain the API key for the connector.

```
YAMMER_SEARCH_LIMIT
```

This variable may contain the maximum number of results to return from Yammer. Default value is 20.

These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.

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
