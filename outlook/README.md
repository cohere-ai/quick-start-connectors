# Microsoft Outlook 365

This package is a utility for connecting Cohere to Microsoft Outlook 365.

It uses Microsoft Graph API run the search query and return matching messages.

## Configuration

To use this search connector, you must have access to Microsoft 365, with API
credentials configured. This search connector requests default permissions with scope
`https://graph.microsoft.com/.default offline_access`. This requires the permissions for the
client credential to be configured in Azure AD. It is important that the following
permissions must be allowed for MS Graph API:

- `Mail.Read`
- `offline_access`

The app registration for the connector in Microsoft Entra admin center requires
permissions to read mail messages.

The Outlook search connector provides two authentication
methods: [app-only](https://learn.microsoft.com/en-us/graph/auth-v2-service)
and [delegated](https://learn.microsoft.com/en-us/graph/auth-v2-user)

To use app-only authentication, set the following environment variables:

- `OUTLOOK_GRAPH_AUTH_TYPE` to `application`
- `OUTLOOK_GRAPH_TENANT_ID`
- `OUTLOOK_GRAPH_CLIENT_ID`
- `OUTLOOK_GRAPH_CLIENT_SECRET`
- `OUTLOOK_USER_ID`

These can be read from a .env file. See `.env-template`.

The values for `OUTLOOK_TENANT_ID`, `OUTLOOK_CLIENT_ID` and `OUTLOOK_CLIENT_SECRET` come from
Microsoft 365 admin. You must create an app registration in Microsoft 365 admin, and grant
the appropriate permissions. The OUTLOOK_USER_ID represents the user ID of the individual who registered the app.
To obtain the user ID, you can use the Microsoft Entra admin center Identity -> Users -> All Users menu and select
your user. The user ID is the "Object ID" field. This information is essential for app-only authentication and is
relevant to the limitations of the Microsoft Graph API search functionality.

To use delegated authentication, set the following environment variables:

- `OUTLOOK_GRAPH_AUTH_TYPE` to `user`

To make a search requests to Microsoft Graph API, the connector needs to be authenticated with a token obtained using
Oauth 2.0, and passed to the connector in the Authorization header with the Bearer schema.
If the connector is configured to use a delegated authentication, the `OUTLOOK_USER_ID` environment variable is not
required.
The connector will search the mailbox of the user who is authenticated.

- `OUTLOOK_CONNECTOR_API_KEY`
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

- `Mail.Read`
- `offline_access`

This will get you up and running, although it is likely excessive and not recommended
for production environment. For production permission configuration, please refer to
your systems administrator for guidance.

Once you have Microsoft 365 configured with an app registration for this search connector and going to use it with
app-only authentication
take the credentials (:code:`GRAPH_TENANT_ID`, :code:`GRAPH_CLIENT_ID` and :code:`GRAPH_CLIENT_SECRET`)
and put them into a :code:`.env` file or set them as environment variables in your preferred way.

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
