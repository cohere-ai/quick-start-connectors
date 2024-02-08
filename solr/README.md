# Solr Quick Start Connector

This project allows you to create a simple connection to Solr that can be used with Cohere's API.

## Limitations

Solr only allows search on a specific field inside a collection, this is defined by the `SOLR_DEFAULT_FIELD` environment variable. As it is essentially a key-value document store, the document will be returned as-is. It is preferable however to set the `SOLR_CONNECTOR_FIELDS_MAPPING` environment variable to map some of your fields to the `text` and `title` keys. For this variable, the key should be the field name in your Solr collection, and the value is the key name it is returned as to Cohere. See the `.env-template` for an example.

## Configuration

This connector requires the following environment variables:

```
SOLR_SERVER_URL

This variable should contain the URL of the Solr instance.
```

```
SOLR_COLLECTION

This variable should contain the name of the Solr collection.
```

```
SOLR_DEFAULT_FIELD

Default field to search on
```

```
SOLR_CONNECTOR_API_KEY

This variable should contain the API key for the connector.
```

### Optional configuration

```
SOLR_CONNECTOR_FIELDS_MAPPING

This variable may contain a JSON object mapping Cohere fields
to Solr fields(key is Solr field, value is Cohere field).
If it is not set, the response fields will be returned as is.
```

## Development

Start Solr and fill it with data by running

```bash
  $ docker-compose run data-loader
```

After running the `data-loader`, the Solr instance will continue to run in the background. If you need to start it
again later, Solr can be started again without needing to load the data:

```bash
  $ docker-compose up
```

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry shell
  $ flask --app provider --debug run --port 5000
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
