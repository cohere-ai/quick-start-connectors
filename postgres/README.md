# Postgres Quick Start Connector

This package is a utility for connecting Cohere to a postgres database. It supports PostgreSQL server versions 7.4 and above.

## Limitations

Currently this connector is configured to only search within a single table of your PostgreSQL cluster, using a single column for full-text search. This column should be indexed to speed up query times.

## Configuration

To protect this connector from abuse, the `POSTGRES_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Development

Start your Postgres server and fill it with data by running

```bash
  $ docker-compose run data-loader
```

After running the `data-loader`, the postgres instance will continue to run in the background. If you need to start it again later, postgres can be started again without needing to load the data:

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
