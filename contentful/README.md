# Contentful Connector.

This package is a utility for connecting Cohere to Contentful.

## Configuration

This connector requires the following environment variables:

```
CONTENTFUL_SPACE_ID
```

This variable should contain the Space ID of the Contentful Space that will be searched.
You can find the Space ID in the Contentful web app under Settings > General Settings > Space ID.

```
CONTENTFUL_PREVIEW_ACCESS_TOKEN
```

This variable should contain the Preview API access token for the Contentful Space that will be searched.
You can find the Preview API key in the Contentful web app under Settings > API Keys > Content Preview API - access
token.

```
CONTENTFUL_ENVIRONMENT
```

This variable should contain the environment of the Contentful Space that will be searched.
You can find the environment in the Contentful web app under Settings > API Keys > <KEY> > Environments.

```
CONTENTFUL_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.

### Optional Configuration

```
CONTENTFUL_CONTENT_TYPE_SEARCH
```

This variable should contain the Content Type ID of the Contentful Content Type that will be searched.
If this variable is not set, the connector will search all Content Types.

```
CONTENTFUL_SEARCH_LIMIT
```

This variable should contain the maximum number of results that will be returned by the connector. By default, 20 results are returned.

```
CONTENTFUL_FIELDS_MAPPING
```

This variable should contain a JSON object that maps Contentful fields to Cohere fields.
If this variable is not set, the connector will return results as is.
The JSON object should be in the following format:

```
{
  "contentful_content_type.contentful_field_id": "cohere_field",
  "contentful_content_type.contentful_field_id": "cohere_field",
  ...
}

for example:

{
    "pageBlogPost.content":"text",
    "pageBlogPost.slug":"url",
    "componentSeo.page_title":"title"
}
```

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
