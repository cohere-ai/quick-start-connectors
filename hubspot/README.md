# HubSpot Quick Start Connector

This package is a utility for connecting Cohere to HubSpot CRM.

## Limitations

The HubSpot connector features full-text search of companies, contacts, notes, and tasks in your organization.

## Configuration

This search connector requires the following environment variables:

```
HUBSPOT_ACCESS_TOKEN

This variable should contain the access token for the HubSpot CRM.
```

To generate an access token, follow the instructions [here](https://developers.hubspot.com/docs/api/private-apps)

```
HUBSPOT_HUB_ID

This variable should contain the Hub ID for the HubSpot CRM.
Hub ID can be found in the URL of the HubSpot CRM.
```

```
HUBSPOT_CONNECTOR_API_KEY

This variable should contain the API key for the connector.
```

### Optional configuration

```

HUBSPOT_SEARCH_LIMIT

This variable may contain the maximum number of results to return. By default, it is set to 20.
```

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
