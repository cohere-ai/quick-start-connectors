# Pinecone Quick Start Connector

This package is a utility for connecting Cohere to Pinecone DB.
Note: vector database indexes and stores vector embeddings, so we need to generate embeddings
from the initial data and then load them into the database.
We use Cohere API to generate vector embeddings.
Here is the Cohere API [documentation](https://docs.cohere.com/reference/embed).

## Limitations

Currently, this connector will perform full-text search,
but only for a single vector search index of your Pinecone DB.
Also, please note that the connector uses Cohere's vector embeddings
based on your query to search your Pinecone DB.
So the Pinecone DB vectors embeddings should be generated using Cohere embed API.

## Configuration

The search connector requires the following environment variables:

```
PINECONE_COHERE_API_KEY
```

This variable should contain the API key for the Cohere API to call the Co.Embed endpoint.
You can get the API key from the Cohere [dashboard](https://dashboard.cohere.com/api-keys).

```
PINECONE_COHERE_EMBED_MODEL
```

This variable should contain the model name for the Cohere API to call the Co.Embed endpoint.
Available models are listed in the Cohere [documentation](https://docs.cohere.com/reference/embed).

```
PINECONE_API_KEY
```

This variable should contain the API key for Pinecone.
Use these [instructions](https://docs.pinecone.io/docs/authentication#finding-your-pinecone-api-key) to get the API key.


```
PINECONE_INDEX
```

This variable should contain the index name for Pinecone.
Refer to the [documentation](https://docs.pinecone.io/docs/indexes) for understanding indexes.

```
PINECONE_CONNECTOR_API_KEY
```

This variable should contain the API key for the Pinecone Connector.

### Optional configuration

```
PINECONE_FIELDS_MAPPING
```

This variable may contain a JSON object mapping Cohere fields
to Pinecone metadata fields(key is Pinecone metadata field, value is Cohere field).
If it is not set, the response metadata fields will be returned as is.

```
PINECONE_SEARCH_LIMIT
```

This variable may contain the number of results to return.
If it is not set, the default value is 100.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  poetry config virtualenvs.in-project true
  poetry install --no-root
```

The `generate_embeddings.py` script will generate embeddings for the BBQ dataset
and save them to a file called `bbq_embeddings.json`

```
$ poetry shell
$ python dev/generate_embeddings.py
```

The `load_data.py` script will load vectors from the `bbq_embeddings.json` file into Pinecone and will generate an
appropriate index if one doesn't already exist.

```
$ poetry shell
$ python dev/load_data.py
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
