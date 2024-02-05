# MySQL Quick Start Connector

This project allows you to create a simple connection to MySQL that can be used with Cohere's API.

## Limitations

The MySQL connector only allows search within a specific table, and for specific text columns. Ideally, you should add indices on these columns to speed up the query time. There is no way currently to add complex conditions, or JOINs of any kind.

## Development

Start MySQL server with:

```bash
$ docker-compose up --build
```

This will create a MySQL database called :code:`bbq`, with test data.

To start your local Flask server, create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

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
