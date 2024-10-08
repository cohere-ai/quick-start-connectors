# Google Drive Quick Start Connector

This project demonstrates how to create a simple connector for Google Drive that can be used in Cohere's API.

## Limitations

Currently this connector can only search for Google Docs, Google Sheets, and Google Slide files. It does not support searching for other file types.

## Authentication

This connector supports two types of authentication: Service Account and OAuth.

### Service Account

For service account authentication this connector requires two environment variables:

#### `GDRIVE_SERVICE_ACCOUNT_INFO`

The `GDRIVE_SERVICE_ACCOUNT_INFO` variable should contain the JSON content of the service account credentials file. To get the credentials file, follow these steps:

1. [Create a project in Google Cloud Console](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
2. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) and [activate the Google Drive API](https://console.cloud.google.com/apis/api/drive.googleapis.com) in the Google Cloud Console.
3. [Create a service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and download the credentials file as JSON. The credentials file should look like this:

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

4. Convert the JSON credentials to a string through `json.dumps(credentials)` and save the result in the `GDRIVE_SERVICE_ACCOUNT_INFO` environment variable.
5. Make sure to [share the folder(s) you want to search with the service account email address](https://support.google.com/a/answer/7337554?hl=en).

#### `GDRIVE_CONNECTOR_API_KEY`

The `GDRIVE_CONNECTOR_API_KEY` should contain an API key for the connector. This value must be present in the `Authorization` header for all requests to the connector.

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
  "name": "GDrive with OAuth",
  "url": "{YOUR_CONNECTOR-URL}",
  "oauth": {
    "client_id": "{GOOGLE-OAUTH-CLIENT-ID}",
    "client_secret": "{GOOGLE-OAUTH-CLIENT-SECRET}",
    "authorize_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://oauth2.googleapis.com/token",
    "scope": "https://www.googleapis.com/auth/drive.readonly"
  }
}'
```

With OAuth the connector will be able to search any Google Drive folders that the user has access to.

## Optional Configuration

This connector also supports a few optional environment variables to configure the search:

1. `GDRIVE_SEARCH_LIMIT` - Number of results to return. Default is 10.
2. `GDRIVE_FOLDER_ID` - ID of the folder to search in. If not provided, the search will be performed in the whole drive.

## Caching

This connector has an optional caching feature, which will cache the documents it downloads from Google Drive. This
will prevent the same documents from being downloaded repeatedly when a user continues a conversation on the same
topic, or multiple users are asking questions related to the same documents.

By default, the caching feature is not enabled. To enable it, set the env var `GDRIVE_CACHE_TYPE` to either:

* `memory` - to cache the documents in the Python process itself using TTLCache from cachetools.
* `redis` - to cache the documents in Redis.

When using caching, the following env vars are also available:

* `GDRIVE_REDIS_HOST` - Redis host to connect to
* `GDRIVE_REDIS_PORT` - Redis port to connect to
* `GDRIVE_REDIS_DB` - Redis database number to connect to
* `GDRIVE_CACHE_MAXSIZE` - Maximum number of documents to store in the TTL cache when using TTL cache 
* `GDRIVE_CACHE_EXPIRE_TIME` - The number of seconds to cache documents for, with either Redis or TTL cache

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Next, start up the search connector server:

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything works:

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
