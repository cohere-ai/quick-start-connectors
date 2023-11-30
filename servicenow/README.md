# ServiceNow Connector

Connects Cohere to ServiceNow.

## Configuration

This connector requires that the following environment variables are set in order to run:

```
SERVICENOW_INSTANCE_URL
SERVICENOW_TABLE_NAME
SERVICENOW_USERNAME
SERVICENOW_PASSWORD
SERVICENOW_CONNECTOR_API_KEY
```

These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.

Finally, to protect this connector from abuse, the `SERVICENOW_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry shell
  $ flask --app provider --debug run --port 5000
```

and check with curl to see that everything is working

```bash
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "stainless propane griddle"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
