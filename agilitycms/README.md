# AgilityCMS Quick Start Connector

A connector to integrate AgilityCMS to Cohere, featuring a simple local development setup.

## Limitations

The AgilityCMS currently searches Post objects in your organization. It features full-text search on the post's title and content.

## Configuration

This connector requires the following environment variables:

```
AGILITYCMS_API_URL
```

This variable should contain the API URL of the AgilityCMS instance.
https://api.aglty.io is for Agility content hosted in USA.
For alternative hosting locations use next URLs:

```
Canada: https://api-ca.aglty.io
Europe: https://api-eu.aglty.io
Australia: https://api-aus.aglty.io
```

```
AGILITYCMS_API_GUID
```

This variable should contain the GUID of the AgilityCMS instance.

```
AGILITYCMS_API_KEY
```

This variable should contain the API Key of the AgilityCMS instance.

```
AGILITYCMS_API_LOCALE
```

This variable should contain the locale of the AgilityCMS instance.

```
AGILITYCMS_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

### Optional configuration

```
AGILITYCMS_SEARCH_LIMIT
```

This variable may contain the maximum number of results to return from AgilityCMS. Default value is 20.
Maximum value is 20.

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
