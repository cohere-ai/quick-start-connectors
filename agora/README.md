# Agora Quick Start Connector

A connector to integrate AgilityCMS to Cohere, featuring a simple local development setup.

## Limitations

The Agora connector currently searches Projects within your organization. Because Agora's API does not offer any search functionality, we instead list all projects in your org prior to running a keyword matching (e.g: if any keyword in your query matches the project's name, it is returned as a search result). This is further limited by pagination.

## Configuration

This connector requires the following environment variables:

```
AGORA_CUSTOMER_ID
```

This variable should contain the Customer ID of the Agora account.
To get the Customer ID, use the
instructions [here](https://docs.agora.io/en/agora-analytics/reference/restful-authentication)

```
AGORA_CUSTOMER_SECRET
```

This variable should contain the Customer Secret of the Agora account.
To get the Customer Secret, use the
instructions [here](https://docs.agora.io/en/agora-analytics/reference/restful-authentication)

```
AGORA_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

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
