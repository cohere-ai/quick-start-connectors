# Carbon Quick Start Connector

Connects Cohere to Carbon.

## Limitations

This connector leverages Carbon's [Search API (see documentation)](https://docs.carbon.ai/api-reference/endpoint/embeddings/embeddings). Importantly, the search will only work for files uploaded with the embedding model you specified in the `CARBON_EMBEDDING_MODEL` environment variable. For example, if you have files with embeddings generated using the `OPENAI` model, a search with the `COHERE_MULTILINGUAL_V3` model will not find them. Ensure that you set the embedding variable to the correct one.

## Configuration

To use this connector, create a `.env` variable based on the `.env-template`. You will need a Carbon API key and Customer ID. If you don't have an existing Customer ID, we recommend generating a UUID v4 value to use that will also need to be used to upload your files to Carbon. Use these for the `CARBON_API_KEY` and `CARBON_CUSTOMER_ID` values.

For the `COHERE_EMBEDDING_MODEL` variable, the following are valid options:

- `OPENAI`
- `AZURE_OPENAI`
- `COHERE_MULTILINGUAL_V3`
- `VERTEX_MULTIMODAL`

This value will affect the search - see the (Limitations)[#limitations] section.

To finish configuring the search functionality, add the `CARBON_FIELDS_MAPPING` variable to modify the behavior of the result serialization. The key refers to the Carbon document response and the value will be the modified key name returned by this connector.

Finally, to protect this connector from abuse, the `CARBON_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

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
