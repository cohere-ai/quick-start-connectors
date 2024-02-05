# Milvus Quick Start Connector

This package is a utility for connecting Cohere to a Milvus database.

It relies on the `pymilvus` package for establishing/managing the connection and performing vector searches. 
This implementation also uses Cohere's embedding API to generate search vectors.

## Limitations

Currently, the search is performed by embedding the search query with Cohere's embedding API.
So the Milvus DB vectors embeddings should be generated using the Cohere embed API.

## Configuration

The search connector requires that an environment variable `MILVUS_COHERE_APIKEY` be set in order to run. 
This environment variable can optionally be put into a `.env` file for development.

A `.env-template` file is provided with all the other environment variable that are used by this demo.

To connect to a Milvus cluster, the following environment variables must be set:

```
MILVUS_CLUSTER_URI
```
This variable should contain the URI of the Milvus cluster to connect to with scheme(http/https).
For the local Milvus cluster, it can be like the `http://localhost:19530`.

```
MILVUS_API_KEY
```
This variable should contain the API key for Milvus and used for [Managed Milvus clusters](https://cloud.zilliz.com/signup). 
To get the API key, refer to the [documentation](https://docs.zilliz.com/docs/manage-api-keys).

```
MILVUS_USER
MILVUS_PASSWORD
```
These variables should contain the username and password for Milvus DB and can be used instead of the API key 
For Managed Milvus clusters see the [documentation](https://docs.zilliz.com/docs/manage-cluster-credentials-gui).

```
MILVUS_COLLECTION
```
This variable should contain the collection name for Milvus.

```
MILVUS_VECTOR_FIELD
```
This variable should contain the vector field name for Milvus collection.

Finally, to protect this connector from abuse, the `MILVUS_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Optional Configuration

```
MILVUS_COHERE_EMBED_MODEL
```
This variable should contain the model name for the Cohere API to call the Co.Embed endpoint.
If not set, the default model is `embed-english-v3.0`.
Available models are listed in the Cohere [documentation](https://docs.cohere.com/reference/embed).

```
MILVUS_FIELDS_MAPPING
```

This variable may contain a JSON object mapping Cohere fields
to Pinecone metadata fields(key is Pinecone metadata field, value is Cohere field).
If it is not set, the response metadata fields will be returned as is.

```
MILVUS_SEARCH_LIMIT
```

This variable may contain the number of results to return.
If it is not set, the default value is 100.


## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

To generate the test data json file, you can run the `generate_embeddings.py` or you can use the provided `bbq_embeddings.json` file.

```bash
  $ poetry run python ./dev/generate_embeddings.py
```

Start the test Milvus cluster and fill it with data by running

```bash
  $ docker-compose run data-loader
```

After running the `data-loader`, the Milvus containers will continue to run in the background. If you need to start them again later, the Milvus cluster can be started again without needing to load the data:

```bash
  $ docker-compose up
```

Finally, start the server

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
