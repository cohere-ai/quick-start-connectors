# Vectara Quick Start Connector

A simple connector that will connect Vectara with Cohere.

## Configuration

This connector requires the following environment variables:

```
VECTARA_CUSTOMER_ID

This variable shoud contain the Vectara Customer ID.
```

```
VECTARA_CORPUS_ID

This variable shoud contain the Vectara corpus ID. It can be a single string or a list of IDs, in which case results will return from all the Vectara corpora listed.
```

```
VECTARA_API_KEY
This variable should contain a single API key that provides authentication to Vectara for the corpus specified (or corpora if more than 1 is listed).
```

### Optional configuration

```
VECTARA_CONNECTOR_FIELDS_MAPPING

This variable may contain a JSON object mapping Vectara fields
to Cohere fields(key is Vectara field, value is Cohere field).
If it is not set, the response fields will be returned as is.
```

A `.env-template` file is provided as a reference.

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
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "stainless propane griddle"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
