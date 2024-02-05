# Klaviyo Connector

This package is a utility for connecting Cohere to Klaviyo.

## Configuration

This connectorrequires the following environment variables:

```
KLAVIYO_API_KEY
```

This variable should contain the API key of the Klaviyo account.
To get the API key, use the instructions [here](https://developers.klaviyo.com/en/docs/retrieve_api_credentials)

```
KLAVIYO_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

### Optional configuration

```
KLAVIYO_CAMPAIGNS_CREATED_AFTER
```

This variable may contain the date after which campaigns should be considered for search.
Date format is `YYYY-MM-DDT00:00:00Z`. If not set, defaults to `2022-01-01`.

```
KLAVIYO_USE_TEMPLATES_FOR_SEARCH
```

This variable may be set to `1` to use Klaviyo campaign templates for search. If not set, defaults to `0`.
Please note using templates for search may have a negative impact on search response time.

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
