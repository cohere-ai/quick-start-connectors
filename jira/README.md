# Jira Quick Start Connector

This package is a utility for connecting Cohere to Jira.

## Limitations

The Jira connector will perform a full-text search based on the subject and description of the tickets in your org, by default it will return a maximum of 10 results.

## Configuration

The Jira connector provides two authentication
methods: [Basic](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/)
and [OAuth 2.0 (3LO)](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/)

To use <b>Basic</b> auth flow this connector requires the following environment variables:

```
JIRA_AUTH_TYPE=basic
JIRA_USER_EMAIL
JIRA_API_TOKEN
JIRA_ORG_DOMAIN
```

It uses Basic Auth with a user email and API token pair. To create an API token, click on your top-right profile icon, select Manage Account > Security > Create API Token. 
The org domain is the URL for your organization's Jira board, including the https:// scheme. 
You will need to put these environment variables in a `.env` file for development, see `.env-template`.

In order to use the `dev/load_data.py` script to load test tickets, the additional env var `JIRA_ISSUE_KEY` should be set. The key is typically a two-letter sequence that forms part of the issue number.

To use <b>OAuth 2.0 (3LO)</b> auth flow this connector requires the following environment variables:
```
JIRA_OAUTH_CLIENT_ID
```
You need to register your app in Jira and get the client ID. See [here](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/) for more details.
You need to set the Jira API Permissions to `View Jira issue data(read:jira-work)` on the App Permissions page. 
Also, you need to set the Authorization callback URL to `https://api.cohere.com/v1/connectors/oauth/token` on the App Authorization page.

Next, register the connector with Cohere's API using the following configuration.
Please note that here we need to add `offline_access` to the scope, 
so that we can get a refresh token and use it to get a new access token when the current one expires.

```bash
 curl  -X POST \
   'https://api.cohere.ai/v1/connectors' \
   --header 'Accept: */*' \
   --header 'Authorization: Bearer {COHERE-API-KEY}' \
   --header 'Content-Type: application/json' \
   --data-raw '{
   "name": "Jira with OAuth",
   "url": "{YOUR_CONNECTOR-URL}",
   "oauth": {
     "client_id": "{Your Jira CLIENT-ID}",
     "client_secret": "{Your Jira App SECRET}",
     "authorize_url": "https://auth.atlassian.com/authorize",
     "token_url": "https://auth.atlassian.com/oauth/token",
     "scope": "read:jira-work offline_access"
   }
 }'
```

Once properly registered, whenever a search request is made Cohere will take care of authorizing the current user and passing the correct access tokens in the request headers.



## Optional Configuration

```
JIRA_SEARCH_LIMIT
JIRA_CONNECTOR_API_KEY
```

The `JIRA_SEARCH_LIMIT` variable may contain the maximum number of results to return for a search. If this variable is not set, the default is 10.
The `JIRA_CONNECTOR_API_KEY` variable may contain the API key for the Cohere connector. Don't set this variable if you are using OAuth 2.0 (3LO) auth flow.


## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

To load some test issues into Jira, this repo provides a `load_data.py` script in `dev/`. Be careful not to run this script on a real Jira project!

```bash
  $ poetry shell
  $ python dev/load_data.py
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
