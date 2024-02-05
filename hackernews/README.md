# HackerNews Connector

Connects Cohere to HackerNews, the social news website focusing on computer science and entrepreneurship.

## Configuration

Add a `HACKERNEWS_CONNECTOR_API_KEY` to secure your connector in production environments, otherwise no configuration needed.

You can optionally modify the `HACKERNEWS_SEARCH_LIMIT` variable to modify the maximum number of results returned per search query.

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

For unit testing, please run:

```bash
  poetry run pytest
```
