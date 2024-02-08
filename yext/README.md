# Yext Connector

Connects Cohere to Yext Universal Search.

## Configuration

The Yext connector provides two authentication
methods: [API Key](https://hitchhikers.yext.com/guides/get-started-yext-api/)
and [OAuth 2.0](https://hitchhikers.yext.com/guides/oauth-and-permission-scopes/01-oauth/)

To use this connector, you must have a Yext account. Yext is a hosted service, and this connector does not include a local database or test data. 
It uses the Yext Universal Search: [Query API](https://hitchhikers.yext.com/docs/contentdeliveryapis/search/universalsearch/#operation/query).
You need to create an app in Yext. See the [Yext documentation](https://hitchhikers.yext.com/guides/get-started-yext-api/02-create-an-app/) for more details.
To use search you need to configure your search experience and verticals in Yext. See the [Yext documentation](https://help.yext.com/hc/en-us/articles/17565006442907-Create-a-Search-Configuration)

To register the connector with Cohere's API using Oauth 2.0, use the following configuration.
Also, you need to set the Authorization callback URL to `https://api.cohere.com/v1/connectors/oauth/token` on the App settings page.
```bash
 curl  -X POST \
   'https://api.cohere.ai/v1/connectors' \
   --header 'Accept: */*' \
   --header 'Authorization: Bearer {COHERE-API-KEY}' \
   --header 'Content-Type: application/json' \
   --data-raw '{
   "name": "Yext with OAuth",
   "url": "{YOUR_CONNECTOR-URL}",
   "oauth": {
     "client_id": "{Your Yext App CLIENT-ID}",
     "client_secret": "{Your Yext App SECRET}",
     "authorize_url": "https://www.yext.com/oauth2/authorize",
     "token_url": "https://api.yext.com/oauth2/accesstoken",
   }
 }'
```


The required environment variables for this connector are:
```
YEXT_AUTH_TYPE
```
This variable should be set to either `api_key` or `oauth` to use API Key or OAuth 2.0 authentication, respectively.

```
YEXT_API_URL
```
This variable should be set to the base URL of the Yext API. This is typically `https://cdn.yextapis.com`.


```
YEXT_API_KEY
```
This variable should be set to the API key of the app you created in Yext.
Please note that this variable is needed only if you use API Key authentication.

```
YEXT_ACCOUNT_ID
```
This variable should be set to your Yext account ID.

```
YEXT_LOCALE
```
This variable should be set to the locale of the search experience you want to use. This is typically `en`.

```
YEXT_V
```
This variable should be set to the search version date in YYYYMMDD format. You can find this in the Yext UI under Search Experience > Test search.



See the [Yext documentation](https://hitchhikers.yext.com/docs/contentdeliveryapis/search/universalsearch/#operation/query) for more details.

### Optional configuration

```
YEXT_VERSION
```
This variable should be set to the version of the Yext API you want to use. 
The available versions are `STAGING` and `PRODUCTION` and the value should be set to `STAGING` for testing and `PRODUCTION` for production.
The default value is `PRODUCTION`.


```
YEXT_SEARCH_LIMIT
```
This variable may contain a JSON object specifying the limit for each vertical. 
Each key is a vertical key and the value for each of those keys is a number 1-50 that denotes the limit for that vertical. 
If a vertical is not specified, the default limit is 10 for all verticals
You can find more details about verticals in the [Yext documentation](https://hitchhikers.yext.com/tracks/search-backend/search130-vertical-level-config/01-verticals-overview/).
```
YEXT_RESTRICT_VERTICALS
```
This variable may contain a comma-separated list of verticals (e.g. "people,locations"). 
If specified, only results from these verticals will be returned.
By default, all verticals are returned.
You can find more details about verticals in the [Yext documentation](https://hitchhikers.yext.com/tracks/search-backend/search130-vertical-level-config/01-verticals-overview/).

```


```
YEXT_FIELDS_MAPPING
```
This variable may contain a JSON object mapping Cohere fields
to Yext fields(key is Yext field,
the value is Cohere field). If this variable is not set, the data will be returned as is.

```
YEXT_CONNECTOR_API_KEY
```
This variable may contain the API key for the Cohere connector. Don't set this variable if you are using OAuth 2.0 auth flow.


Environment variables can optionally be placed in a file called `.env`. See `.env-template` for a
full list of available options. This file can be copied to `.env` and modified. Options that are
left empty will be ignored.

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
