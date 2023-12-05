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

1. [Create a project in Google Cloud Console](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
2. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) and [activate the Google Drive API](https://console.cloud.google.com/apis/api/drive.googleapis.com) in the Google Cloud Console. Make sure that the user(s) you want to search are permitted to use the service account.
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

4. Convert the JSON credentials to a string and save the result in the `GMAIL_SERVICE_ACCOUNT_INFO` environment variable.
5. On the Service Accounts page on GCP, copy the client ID value for your newly created service account, you will then need a super administrator user account to access [API Controls](https://admin.google.com/ac/accountchooser?continue=https://admin.google.com/ac/owl) and click on `Manage Domain Wide Delegation` > `Add new` and paste the client ID from earlier, then add the `https://www.googleapis.com/auth/gmail.readonly` to the OAuth Scopes field. Finally, click Authorize.

### OAuth

When using OAuth for authentication, the connector does not require any additional environment variables. Instead, the OAuth flow should occur outside of the Connector and Cohere's API will forward the user's access token to this connector through the `Authorization` header.

With OAuth the connector will be able to search any e-mails the user has access to.

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
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "charcoal"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
