# Medium Connector

Connects Cohere to Medium.
This connector uses two types of APIs for searching.
The REST API only allows searching the current user's publications,
The GraphQL API allows a more general search but please note
that this API is not an official API and may change in the future.

## Configuration

This connector requires the following environment variables:

```
MEDIUM_SEARCH_API_TYPE
```

This variable may contain the type of search to perform. It can be either `graphql` or `api`.
If `graphql` is used, the GraphQL API will be used to search for entities.
If `api` is used, the REST API will be used to search for entities.
If this variable is not set, the default is `graphql`.

```
MEDIUM_API_TOKEN
```

This variable should contain the API token for the Medium account.
This token will be used if the `MEDIUM_SEARCH_API_TYPE` is set to `api`.
To get the API token, use the
instructions [here](https://github.com/Medium/medium-api-docs#21-self-issued-access-tokens)

```
MEDIUM_GRAPHQL_ENTITIES
```

This variable may contain a comma-separated list of entities to search for.
The valid entities are `users`, `tags`, `posts`, `publications`, `lists`.
If this variable is not set, defaults is `["posts", "publications"]`.

```
MEDIUM_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

## Optional Configuration
```
MEDIUM_GRAPHQL_SEARCH_LIMIT
```

This variable may contain the maximum number of results to return for a GraphQL search per entity.
If this variable is not set, the default is 10.

This connector requires that the environment variables above
be set in order to run. These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.

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
  curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
