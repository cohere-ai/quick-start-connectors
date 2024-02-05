# Zendesk Connector

Connects Cohere to Zendesk.

## Configuration

This connector requires the following environment variables:

```
ZENDESK_DOMAIN

This variable should contain the domain of the Zendesk instance.
```

```
ZENDESK_EMAIL

This variable should contain the email of the Zendesk user.
```

```
ZENDESK_API_TOKEN

This variable should contain the API token of the Zendesk user.
```

You can generate an API token using
the instructions [here](https://support.zendesk.com/hc/en-us/articles/226022787-Generating-a-new-API-token-)

```
ZENDESK_CONNECTOR_API_KEY

This variable should contain the API key for the Cohere connector.
```

### Optional configuration

```
ZENDESK_SEARCH_LIMIT

This variable may contain the maximum number of results to return from Zendesk. Default value is 20.
```

This connector requires that the environment variables above
be set in order to run. These variables can optionally be put into a `.env` file for development.
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
