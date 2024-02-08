# Basecamp Connector

This package is a utility for connecting Cohere to Basecamp.

## Configuration

The search connector requires the following environment variables:

```
BASECAMP_ACCOUNT_ID
```

This variable should contain the account ID of the Basecamp account that will be searched.
You can find the account ID in the you account Basecamp URL -> https://3.basecamp.com/<ACCOUNT_ID>/projects.

```
BASECAMP_ACCESS_TOKEN
```

This variable should contain the Oauth2 access token for the Basecamp account that will be searched.
To get the access token please follow the
instructions [here](https://github.com/basecamp/api/blob/master/sections/authentication.md#oauth-2)
Please note that after access token is expired you will need to generate a new one.
This connector does not support refresh tokens.

```
BASECAMP_CONNECTOR_API_KEY
```

This variable should contain the API key for the Cohere connector.

The search connector requires that the environment variables above
be set in order to run. These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.

### Optional Configuration

```
BASECAMP_PROJECT_SEARCH_ENTITIES
```

This variable should contain the list of entities that will be searched.
The connector provides two types of entities: `documents` and `messages`.
To search through documents this variable should be set to the `["vault"]` value.
To search through messages this variable should be set to the `["message_board"]` value.
To search through both documents and messages this variable should be set to the `["vault","message_board"]` value.
Please note when we use both `vault` and `message_board` entities the response time will be slower.
If not set the connector will search through documents only

```
BASECAMP_VAULTS_DEPTH
```

This variable should contain the depth of the vaults(folders) that will be searched.
By default the connector will search through only top levels documents.
Please note when we increase the depth the response time will be slower.

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
