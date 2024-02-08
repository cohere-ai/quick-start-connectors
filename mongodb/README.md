# MongoDB Quick Start Connector

Connects Cohere to a MongoDB instance using PyMongo.

## Limitations

The MongoDB connector will search across all defined collections of your MongoDB database. You can set one or many collections using the `MONGODB_COLLECTIONS` environment variable. Note that it will perform a full-text search only on the fields that have a **text index** defined. It will then return the key-value document as-is. We recommend adding a `MONGODB_CONNECTOR_FIELD_MAPPING` variable to map your document keys to the `text` and `title` keys for Cohere to ingest.

## Configuration

1. Setting up your MongoDB connection

To connect your MongoDB instance, you will need a MongoDB user account that has at least read-access enabled. Note down the username and password. Then you will need to retrieve your connection string based on your MongoDB deployment type, see their[documentation](https://www.mongodb.com/basics/mongodb-connection-string).

For example, the connection string should look like `mongodb+srv://MYUSER:MYPASSWORD@mydomain.mongodb.net/?retryWrites=true&w=majority`. Use this value for the `MONGODB_CONNECTION_STRING` environment variable.

Important: For production, make sure you whitelist the IPv4 address of the deployed server to allow the connection to your MongoDB instance.

Then you can specify the Database and Collection(s) using respectively the `MONGODB_DB` and `MONGODB_COLLECTIONS` variables. If you want to search across multiple collections under the same database, you can add a comma separated string. For example, `collection1,collection2`.

2. Creating your indices

Next, for each collection you want to search, add text indices. On MongoDB cloud, you can go to Database > Collections > Select a Collection > Indexes tab > Create Index, then add your index definition. For example, a collection `Users` that you would like to search `name` and `email` would have an index that looks like:

```
{
  "name": "text",
  "email": "text"
}
```

## Development

A development MongoDB server can be started with `docker-compose up`. To load test data into MongoDB,
you can use the following command:

```bash
docker-compose run data-loader
```

```bash
cp .env-template .env
```

To run the Flask server you must first install the dependencies with poetry. We recommend using in-project
virtual environments:

```bash
poetry config virtualenvs.in-project true
poetry install
```

Then start the server:

```bash
poetry run flask --app provider run --debug
```

Once the Mongo and Flask servers are running, you can perform a test request with the following cURL call:

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
