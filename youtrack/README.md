# Youtrack Connector

Connects Cohere to Youtrack, the planning and collaboration tool.

Currently only searches across issues in your Youtrack organization.

## Configuration

To use this connector, follow these steps:

1. Create a Youtrack Permanent Token. You can follow the guide [here.](https://www.jetbrains.com/help/youtrack/server/Manage-Permanent-Token.html) Use this value for the `YOUTRACK_PERMANENT_TOKEN` environment variable.

2. Determine your Youtrack instance's base URL. This can differ if you're using Youtrack Cloud vs self-hosted, you can refer to the [documentation](https://www.jetbrains.com/help/youtrack/devportal/api-url-and-endpoints.html#incloud-url). Use this value for the `YOUTRACK_BASE_URL` env variable. For example, `https://mycompany.youtrack.cloud` if you're using the Cloud version.

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
