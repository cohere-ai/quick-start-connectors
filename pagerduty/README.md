# Pagerduty Quick Start Connector

This search connector is for connecting Cohere to Pagerduty, the incident response platform.

## Limitations

Currently, this connector will search across your Incidents, Users, and Teams. It is important to note that full-text search is only available through their API for Users and Teams, and that Incidents are searched using keyword matching at the connector level. See the `client.py` implementation for more details.

## Configuration

To use this connector, your Pagerduty account administrator will need to generate an API key.
From the web app, navigate to Integrations > API Access Keys > Developer Tools, then you can create an API key. Only read-access is required.

Finally, to protect this connector from abuse, the `PAGERDUTY_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  poetry config virtualenvs.in-project true
  poetry install --no-root
```

To run the Flask server in development mode, please run:

```bash
  poetry run flask --app connector --debug run
```

The Flask API will be bound to :code:`localhost:5000`.

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
