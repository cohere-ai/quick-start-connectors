# Atera Quick Start Connector

Connects Cohere to Atera, the IT management tool.

## Limitations

Currently only searches Tickets within your Atera org. Note that because Atera's API only offers a List endpoint for Tickets, the search is performed at the connector level using keyword matching (e.g: any keyword of your query matching the Ticket's title or description is returned).

## Configuration

To use this connector, you will require access to your Atera dashboard, and have the `Admin` tab available on the left hand side.
Click on `Admin`, then under the `Customer Facing` section click `API`, then copy the API key value. Use this for the `ATERA_API_KEY` environment variable.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  poetry config virtualenvs.in-project true
  poetry install --no-root
```

To run the Flask server in development mode, please run:

```bash
  poetry run flask --app provider --debug run
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
