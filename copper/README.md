# Cohere Copper CRM Search connector

This package is a utility for connecting Cohere to Copper CRM.

## Configuration

The search connector requires the following environment variables:

```
COPPER_API_TOKEN
```

This variable should contain the API token for the Copper account.
To get the API token, use the
instructions [here](https://developer.copper.com/introduction/authentication.html#api-keys)

```
COPPER_API_EMAIL
```

This variable should contain the Copper account email address.

```
COPPER_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

### Optional Configuration

```
COPPER_SEARCH_LIMIT
```

This variable should contain the maximum number of results
that will be returned by the search connector per entity(opportunities and tasks).
If this variable is not set, the search connector will return 20 results.

```
CONTENTFUL_FIELDS_MAPPING
```

This variable should contain a JSON object that maps Copper fields to Cohere fields.
If this variable is not set, the search connector will return results as is.
The JSON object should be in the following format:

```
{
  "opportunity.opportunity_field": "cohere_field",
  "task.task_field": "cohere_field",
  ...
}

for example:

{
    "opportunity.name":"title",
    "opportunity.details":"text",
    "task.name":"title",
    "task.details":"text"
}
```

The search connector requires that the environment variables above
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
