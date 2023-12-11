# Microsoft Teams

This package is a utility for connecting Cohere to Microsoft Teams.

It uses Microsoft Graph API run the search query and return matching Teams chat messages.

## Limitations

The Microsoft Teams connector currently searches for all chat messages within your Teams instance. 
Note that new messages added will require a couple minutes of indexing time to be searchable.

## Configuration

To use this search connector, you must have access to Microsoft 365, with API
credentials configured. This search connector requests default permissions with scope
`https://graph.microsoft.com/.default offline_access`. This requires the permissions for the
client credential to be configured in Azure AD. It is important that the following
permissions must be allowed for MS Graph API:

- `Chat.Read`
- `ChatMessage.Read`
- `ChannelMessage.Read.All`
- `Files.Read.All`
- `offline_access`

The Teams search connector provides OAuth [delegated](https://learn.microsoft.com/en-us/graph/auth-v2-user) authentication only.


#### OAuth

When using OAuth for authentication, the connector does not require any additional environment variables. Instead, the OAuth flow should occur outside of the Connector and Cohere's API will forward the user's access token to this connector through the `Authorization` header.

With OAuth the connector will be able to search any Teams chat messages that the user has access to.

To configure OAuth, follow the same steps in the Configuration section to create a Microsoft 365 App. You will also need to register a redirect URI on that app to `https://api.cohere.com/v1/connectors/oauth/token`.

You can then register the connector with Cohere's API using the following configuration:
Note: Your App key and App secret values correspond to `client_id` and `client_secret` respectively.

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
    "authorize_url": "https://login.microsoftonline.com/{Your APP Tenant ID}/oauth2/v2.0/authorize?client_id={Your APP Client ID}"
    "token_url": "https://login.microsoftonline.com/{Your APP Tenant ID}/oauth2/v2.0/token"
  }
}'
```


To make a search requests to Microsoft Graph API, the connector needs to be authenticated with a token obtained using
Oauth 2.0, and passed to the connector in the Authorization header with the Bearer schema.

The connector will search the chat messages accessible by the user who is authenticated.

## Unstructured

To decode attachment's file contents, this connector leverages [Unstructured](https://unstructured.io). You can generate a free [API key here](https://unstructured.io/api-key).

It is necessary to provide the following values in the `.env`:

- `MSTEAMS_UNSTRUCTURED_BASE_URL`
- `MSTEAMS_UNSTRUCTURED_API_KEY`

Use the API key generated earlier. To quickstart usage, you can use the hosted `https://api.unstructured.io` as the base URL, 
or you can [host your own Unstructured server](https://unstructured-io.github.io/unstructured/apis/usage_methods.html).


## Optional configuration
- `MSTEAMS_GRAPH_SEARCH_LIMIT` 
  This variable may contain the maximum number of results to return from the search. The default is 10.  
- `MSTEAMS_CONNECTOR_API_KEY`
  This variable may contain the API key for the connector.

## Development

Running this connector requires access to Microsoft 365. For development purposes,
you can register for the Microsoft 365 developer program, which will grant temporary
access to a Microsoft 365.

For the connector to work, you must register the application. To do this, go to
Microsoft Entra admin center:

https://entra.microsoft.com/

Navigate to "Applications -> App registrations", and use the "New registration" option.

Select "Web" as the platform, and ensure you add a redirect URL, even if it is optional.
The redirect URL is required for the admin consent step to work. This connector does not
have a redirect page implemented, but you can use http://localhost/ as the redirect URL.

On the app registration page for the app you have created, go to API permissions, and
grant permissions. For development purposes, you can grant:

- `Chat.Read`
- `ChatMessage.Read`
- `ChannelMessage.Read.All`
- `Files.Read.All`
- `offline_access`

This will get you up and running, although it is likely excessive and not recommended
for production environment. For production permission configuration, please refer to
your systems administrator for guidance.

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  poetry config virtualenvs.in-project true
  poetry install --no-root
```

To run the Flask server in development mode, please run:

```bash
  poetry run flask --app connector --debug run
```

The Flask API will be bound to :code:`localhost:5000`.

```bash
  curl --request POST \
    --url http://localhost:3000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "Weber charcoal"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
