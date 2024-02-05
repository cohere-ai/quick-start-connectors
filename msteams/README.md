# Microsoft Teams

This package is a utility for connecting Cohere to Microsoft Teams.

It uses Microsoft Graph API to run the search query and return matching Teams chat messages.

## Limitations

The Microsoft Teams connector currently searches for all chat messages within your Teams instance. 
Note that new messages added will require a couple minutes of indexing time to be searchable.

## Configuration
The Teams search connector provides two authentication
methods: [app-only](https://learn.microsoft.com/en-us/graph/auth-v2-service)
and [delegated](https://learn.microsoft.com/en-us/graph/auth-v2-user)

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


### Service Authentication
To use service to service authentication, set the following environment variables:

- `MSTEAMS_GRAPH_AUTH_TYPE` to `application`
- `MSTEAMS_GRAPH_TENANT_ID`
- `MSTEAMS_GRAPH_CLIENT_ID`
- `MSTEAMS_GRAPH_CLIENT_SECRET`
- `MSTEAMS_USER_ID`

These can be read from a .env file. See `.env-template`.

The values for `MSTEAMS_TENANT_ID`, `MSTEAMS_CLIENT_ID` and `MSTEAMS_CLIENT_SECRET` come from
Microsoft 365 admin. You must create an app registration in Microsoft 365 admin, and grant
the appropriate permissions. The `MSTEAMS_USER_ID` represents the user ID of the individual who registered the app.
To obtain the user ID, you can use the Microsoft Entra admin center Identity -> Users -> All Users menu and select
your user. The user ID is the "Object ID" field. This information is essential for app-only authentication and is
relevant to the limitations of the Microsoft Graph API search functionality.



#### OAuth

When using OAuth for authentication, set the following environment variable:

- `MSTEAMS_GRAPH_AUTH_TYPE` to `user`

The OAuth flow should occur outside of the Connector and Cohere's API will forward the user's access token
to this connector through the `Authorization` header.

With OAuth the connector will be able to search any Teams chat messages that the user has access to.

To configure OAuth, follow the same steps in the Configuration section to create a Microsoft 365 App. 
You will also need to register a redirect URI on that app to `https://api.cohere.com/v1/connectors/oauth/token`.

You can then register the connector with Cohere's API using the following configuration:
Note: Your `MSTEAMS_GRAPH_CLIENT_ID` and `MSTEAMS_GRAPH_CLIENT_SECRET` values correspond to `client_id` and `client_secret` respectively.

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
    "authorize_url": "https://login.microsoftonline.com/{Your App TENANT-ID}/oauth2/v2.0/authorize",
    "token_url": "https://login.microsoftonline.com/{Your App TENANT-ID}/oauth2/v2.0/token",
    "scope": ".default offline_access"
  }
}'
```
No more configuration is needed here and after successfully registration, 
Cohere will take care of OAuth steps including passing in the correct headers to your connector.

## Unstructured

To decode attachment's file contents, this connector leverages [Unstructured](https://unstructured.io). You can generate a free [API key here](https://unstructured.io/api-key).

It is necessary to provide the following value in the `.env`:

- `MSTEAMS_UNSTRUCTURED_BASE_URL`


To quickstart usage, you can use the hosted `https://api.unstructured.io` as the base URL, 
or you can [host your own Unstructured server](https://unstructured-io.github.io/unstructured/apis/usage_methods.html). 
If you are using the hosted version, it is necessary to provide the API key generated earlier in the `.env`:

- `MSTEAMS_UNSTRUCTURED_API_KEY`


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
The redirect URL is required for the admin consent step to work. 

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
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
