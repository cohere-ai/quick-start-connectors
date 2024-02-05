# Redis RediSearch Connector

Connects Cohere to a Redis database. It uses the Redis RediSearch module for
performing a fulltext search in the Redis database.

## Configuration

The following configuration variables can be set as environment variables, or put into a `.env` file
to control the behaviour of this connector:

```
REDIS_HOST=localhost
REDIS_PORT=63709
REDIS_USER=
REDIS_PASSWORD=
REDIS_INDEX=bbq_index
REDIS_FIELDS=id,name,description,brand,color,country,rank
REDIS_FIELDS_MAPPING={}
REDIS_SEARCH_LIMIT=10
REDIS_CONNECTOR_API_KEY=
```
The `REDIS_HOST` and `REDIS_PORT` variables are used to connect to the Redis server. If the Redis server
requires authentication, the `REDIS_USER` and `REDIS_PASSWORD` variables can be set to the username and
password to use when connecting to the Redis server. If these are not set, the connector will connect
without authentication to the local Redis server on the 63709 port.
The `REDIS_INDEX` config variable should be set to the name of the index to search in Redis. The
`load_data.py` script will create one called `bbq_index` for testing, but in production use this should be changed.

The `REDIS_FIELDS` config variable contains the fields from the index, which should be returned in the
results from the Flask app. These correspond to the schema that was used when the Redis `FT.CREATE` command
was run. It is not necessary to return all fields from the index but the fields in this comma separate list
must be fields from the index. This connector does not look up other keys that are not part of the index
when returning results.

To use the test data during development, you must copy the `.env-template` file to `.env`, or set the
environment variables manually.

Finally, to protect this connector from abuse, the `REDIS_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

### Optional configuration
```
REDIS_SEARCH_LIMIT
```
The `REDIS_SEARCH_LIMIT` config variable can be used to limit the number of results returned from the Redis. The default value is 10.

```
REDIS_FIELDS_MAPPING
```
The `REDIS_FIELDS_MAPPING` config variable can be used to map the fields returned from Redis to the fields returned from the connector. 
This is useful if the fields returned from Redis are not the same as the fields returned from the connector.
For example, if the Redis index contains a field called `name` but the connector should return a field called `title`, the `REDIS_FIELDS_MAPPING` config variable can be set to `{"name": "title"}`.
This will map the `name` field returned from Redis to the `title` field returned from the connector.
By default, the fields returned from Redis will be returned from the connector as is.

## Development

A development Redis server can be started with `docker-compose up`. This will start a Redis server with the
Redisearch module. To load test data into the Redis db, you can use the following command:

```bash
docker-compose run data-loader
```

```bash
cp .env-template .env
```

To run the Flask server you must first install the dependencies with poetry:

```bash
poetry install
poetry run flask --app provider run --debug
```

Once the Redis and Flask servers are running, you can perform a test request with the following cURL call:

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
