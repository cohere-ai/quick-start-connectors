# Google Calendar Connector

This connects Cohere to Google Calendar, allowing searching events.

## Authentication

This connector supports two types of authentication: Service Account and OAuth.

### Service Account

For service account authentication this connector requires two environment variables:

#### `GCALENDAR_SERVICE_ACCOUNT_INFO`
#### `GCALENDAR_CALENDAR_ID`

The `GCALENDAR_SERVICE_ACCOUNT_INFO` variable should contain the JSON content of the service account credentials file.
To get the credentials file, follow these steps:

1. [Create a project in Google Cloud Console](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
2. [Create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts)
   and [activate the Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com) in
   the Google Cloud Console.
3. [Create a service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and download
   the credentials file as JSON. The credentials file should look like this:

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

4. Convert the JSON credentials to a string through `json.dumps(credentials)` and save the result in
   the `GCALENDAR_SERVICE_ACCOUNT_INFO` environment variable.
5. Make sure to [share the calendar you want to search with the service account email address](https://support.google.com/calendar/answer/37082?hl=en&sjid=5073623986746929940-EU).
6. Assign the `GCALENDAR_CALENDAR_ID` environment variable the value of the calendar owner's email address.

#### `GCALENDAR_CONNECTOR_API_KEY`

The `GCALENDAR_CONNECTOR_API_KEY` should contain an API key for the connector. This value must be present in
the `Authorization` header for all requests to the connector.

### OAuth

When using OAuth for authentication, the connector does not require any additional environment variables. Instead, the
OAuth flow should occur outside of the Connector and Cohere's API will forward the user's access token to this connector
through the `Authorization` header.


## Optional Configuration

This connector also supports a few optional environment variables to configure the search:

1. `GCALENDAR_SEARCH_LIMIT` - Number of results to return. Default is 10.
2. `GCALENDAR_CALENDAR_ID` - ID of the calendar to search in. If not provided, the search will be performed in the primary calendar.
For the service account authentication method, this value should be the email address of the calendar owner.

## Development

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
