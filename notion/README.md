# Notion Quick Start Connector

This search connector is for connecting Cohere to Notion, the planning and collaboration tool.

## Limitations

The Notion connector can currently only search documents in your Notion space by title. In addition, only pages and subpages with your integration enabled will be included in the search. See the `Configuration` section of this README for more details.

## Configuration

To use this connector you will need to have Workspace Owner privileges over your Notion space, and to create a
new integration.

To do so, click on Settings & members > My connections > Develop or manage integrations,
then create a new internal integration. You can then generate a secret token for that integration. Use this
for the `NOTION_API_TOKEN` environment variable.

Then, to expose any page and subpage to the integration, you will need to go to that page
and click from the top-right, ... > Add connections > [Your connection name].

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
