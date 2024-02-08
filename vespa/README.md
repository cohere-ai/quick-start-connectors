# Vespa Quick Start Connector

A simple connector that will connect Vespa with Cohere.

## Limitations

The Vespa connector will perform a full-text search on all sources of the specified Vespa server, and return the key-value documents as-is. Note that it is highly recommended to set the `VESPA_CONNECTOR_FIELD_MAPPING` environment variable so you can specify a `text` and `title` key for Cohere to ingest. See the `.env-template` for an example.

## Configuration

This connector requires the following environment variables:

```
VESPA_SERVER_URL

This variable should contain the hostname of the Vespa instance.
```

```
VESPA_CONNECTOR_API_KEY

This variable should contain the API key for the connector.
```

### Optional configuration

```
VESPA_CONNECTOR_FIELDS_MAPPING

This variable may contain a JSON object mapping Vespa fields
to Cohere fields(key is Vespa field, value is Cohere field).
If it is not set, the response fields will be returned as is.
```

A `.env-template` file is provided as a reference.

## Development

Start Vespa and fill it with data by running

```bash
  $ docker-compose run data-loader
```

This will bring up Vespa, deploy a simple application, and fill it with sample data. If you need to start the Vespa
service again later,
it can be started again without needing to load the data:

```bash
  $ docker-compose up
```

Next, create a virtual environment and install dependencies with poetry. We recommend using in-project virtual
environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Start the connector's server:

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything works:

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
