# Miro Quick Start Connector

Connects Cohere to Miro, the planning and collaboration tool.

## Limitations

The Miro connector currently allows full-text search of a board's title and description, including partial matching.

## Configuration

To configure this connector you will have to either create a new Miro app, see [here](https://developers.miro.com/docs/rest-api-build-your-first-hello-world-app#step-1-create-your-app-in-miro), or configuring an existing app.

Your app will require at the least the `board:read` permission to allow searching your boards, once that is done you can save and install the app.
A message should notify you that the app was successfully installed, and give you an access token. Use this token for the `MIRO_ACCESS_TOKEN` environment variable.
The `MIRO_ACCESS_TOKEN` environment variable must be set if you didn't select the "Expire user authorization token" checkbox during app creation.
If you selected that checkbox, you will need to use the OAuth flow.

### OAuth flow
The OAuth flow should occur outside of the Connector by calling Cohere's API. Once authorized,
Cohere's API will forward the user's access token to this connector through the `Authorization` header.

To configure OAuth, follow the same steps to create a Miro App and select the "Expire user authorization token" checkbox. 
You will also need to register a redirect URI on that app to `https://api.cohere.com/v1/connectors/oauth/token`.

You can then register the connector with Cohere's API using the following configuration:
Note: Your app `CLIENT-ID` and app `CLIENT-SECRET` values correspond to `client_id` and `client_secret` respectively.

```bash
curl  -X POST \
  'https://api.cohere.ai/v1/connectors' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {COHERE-API-KEY}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name": "MS Teams with OAuth",
  "url": "{YOUR_CONNECTOR-URL}",
  "oauth": {
    "client_id": "{Your App CLIENT-ID}",
    "client_secret": "{Your App CLIENT-SECRET}",
    "authorize_url": "https://miro.com/oauth/authorize",
    "token_url": "https://api.miro.com/v1/oauth/token",
  }
}'
```
No more configuration is needed here and after successfully registration, 
Cohere will take care of OAuth steps including passing in the correct headers to your connector.
If you are not using Coral/Playground, you will have to complete the authorization flow by navigating to the URL returned at 
`https://api.cohere.ai/v1/connectors/{CONNECTOR-ID}/oauth/authorize`.


## Optional Configuration
```
MIRO_CONNECTOR_API_KEY
```
To protect this connector from abuse, the `MIRO_CONNECTOR_API_KEY` environment variable may be set to a secure value
that will be used for this connector's own bearer token authentication.
Do not set this variable if you want to use the Oauth flow.

```
MIRO_FIELDS_MAPPING
```

This variable may contain a JSON object mapping Cohere fields
to Miro fields(key is Miro field, value is Cohere field).
If it is not set, the response fields will be returned as is.

```
MIRO_SEARCH_LIMIT
```

This variable may contain the number of results to return.
If it is not set, the default value is 20.


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


