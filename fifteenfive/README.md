# 15Five Connector

Connects Cohere to 15Five.

## Configuration

To use this connector, you will need to set the following environment variables:

```
FIFTEENFIVE_API_URL

This url is the base url for the 15Five API.
It should be set to the following value: https://<your 15Five company subdomain>.15five.com/api/public
```

```
FIFTEENFIVE_API_KEY

This variable should contain the API key for the 15Five API.
```

To create an API key please follow the
instructions [here](https://success.15five.com/hc/en-us/articles/360002699631-API#h_01G6X8X5ZAS1A1VG4A0S4FGP6S)

```
FIFTEENFIVE_CONNECTOR_API_KEY

This variable should contain the API key for the connector.
```

### Optional Configuration

```
FIFTEENFIVE_ALLOWED_ENTITIES

This variable should contain a comma separated list of entities that are allowed to be searched.
The default value is: ["user","vacation","question","answer","pulse","high-five","objective","review-cycle"]
```

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
