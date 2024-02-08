# Gmail Quick Start Connector

Connects Cohere to Google Mail. It uses the Gmail Python SDK to search for emails.

## Authentication

This connector supports two types of authentication: Service Account and OAuth.

For Service Account authentication, domain-wide delegation is required, and can only search one user's mail at a time.

### Service Account

Service Account authentication requires two environment variables:
`GMAIL_SERVICE_ACCOUNT_INFO`: Containing the JSON of your Service Account's credentials.
`GMAIL_USER_ID`: Containing the email of the user who's emails you would like to search.

#### `GMAIL_SERVICE_ACCOUNT_INFO`

The `GMAIL_SERVICE_ACCOUNT_INFO` variable should contain the JSON content of the service account credentials file. To get the credentials file, follow these steps:

1. [Create a project in Google Cloud Console](https://cloud.google.com/resource-manager/docs/creating-managing-projects). If you have an existing GCP project, use that one instead.
2. [Active the Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com).
3. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) and [activate the Google Drive API](https://console.cloud.google.com/apis/api/drive.googleapis.com) in the Google Cloud Console. Make sure that the user(s) you want to search are permitted to use the service account.
4. [Create a service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and download the credentials file as JSON. The credentials file should look like this:

```json
{
  "type": "service_account",
  "project_id": "{project id}",
  "private_key_id": "{private_key_id}",
  "private_key": "{private_key}",
  "client_email": "{client_email}",
  "client_id": "{client_id}",
  "auth_uri": "{auth_uri}",
  "token_uri": "{token_uri}",
  "auth_provider_x509_cert_url": "{auth_provider_x509_cert_url}",
  "client_x509_cert_url": "{client_x509_cert_url}",
  "universe_domain": "{universe_domain}"
}
```

5. Convert the JSON credentials to a string and save the result in the `GMAIL_SERVICE_ACCOUNT_INFO` environment variable.
6. On the Service Accounts page on GCP, copy the client ID value for your newly created service account, you will then need a super administrator user account to access [API Controls](https://admin.google.com/ac/accountchooser?continue=https://admin.google.com/ac/owl) and click on `Manage Domain Wide Delegation` > `Add new` and paste the client ID from earlier, then add the `https://www.googleapis.com/auth/gmail.readonly` to the OAuth Scopes field. Finally, click Authorize.

### OAuth

When using OAuth for authentication, the connector does not require any additional environment variables. Instead, the OAuth flow should occur outside of the Connector and Cohere's API will forward the user's access token to this connector through the `Authorization` header.

To use OAuth, you must first create a Google OAuth client ID and secret. You can follow Google's [guide](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) to get started. When creating your application use `https://api.cohere.com/v1/connectors/oauth/token` as the redirect URI.

Once your Google OAuth credentials are ready, you can register the connector in Cohere's API with the following configuration:

```bash
curl  -X POST \
  'https://api.cohere.ai/v1/connectors' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {COHERE-API-KEY}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name": "Gmail with OAuth",
  "url": "{YOUR_CONNECTOR-URL}",
  "oauth": {
    "client_id": "{GOOGLE-OAUTH-CLIENT-ID}",
    "client_secret": "{GOOGLE-OAUTH-CLIENT-SECRET}",
    "authorize_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://oauth2.googleapis.com/token",
    "scope": "https://www.googleapis.com/auth/gmail.readonly"
  }
}'
```

With OAuth the connector will be able to search any emails the authenticated user has access to.

#### `GMAIL_CONNECTOR_API_KEY`

The `GMAIL_CONNECTOR_API_KEY` should contain an API key for the connector. This value must be present in the `Authorization` header for all requests to the connector.

#### Optional

Optionally, you can modify the `GMAIL_SEARCH_LIMIT` variable to change the number of maximum results obtained by a search query.

## Development

This search connector has no test data and can only be used with an existing Gmail account.

Copy the `.env-template` file to `.env` and edit the values accordingly.

```bash
cp .env-template .env
```

To run the Flask server you must first install the dependencies with poetry:

```bash
poetry install
poetry run flask --app provider run --debug
```

Once the Flask server is running, you can perform a test request with the following cURL call:

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
