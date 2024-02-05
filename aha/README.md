# Aha! Quick Start Connector

A connector to integrate Aha! to Cohere, featuring a simple local development setup.

## Limitations

The Aha! connector searches across all entity types defined by the `AHA_ALLOWED_ENTITIES` environment variable, which by default searches for ["users","capacity_scenarios","epics","features","goals","ideas","initiatives","integrations","products","release_phases","strategy_models","strategy_positions","strategy_visions","teams","tasks"].

## Configuration

This connector requires the following environment variables:

```
AHA_DOMAIN

This variable should contain the domain of the your Aha! account.
```

```
AHA_API_KEY

This variable should contain the API key of the Aha!
```

You can generate an API token using
the instructions [here](https://www.aha.io/api#authentication)

```
AHA_CONNECTOR_API_KEY

This variable should contain the API key for the Cohere connector.
```

### Optional configuration

```
AHA_ALLOWED_ENTITIES

This variable may contain a comma separated list of entity types to search.
Default value is ["users","capacity_scenarios","epics","features","goals","ideas","initiatives","integrations","products","release_phases","strategy_models","strategy_positions","strategy_visions","teams","tasks"].
```

```
AHA_SEARCH_LIMIT

This variable may contain the maximum number of results to return from Aha!. Default value is 20.
```

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
