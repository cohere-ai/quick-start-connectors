# Asana Quick Start Connector

A connector to integrate Asana, the project management tool, to Cohere. Featuring a simple local development setup.

## Limitations

The Asana connector only offers full-text search for Task objects.

## Configuration
The Asana connector provides two authentication methods: [Personal Access Token](https://developers.asana.com/docs/personal-access-token) and [OAuth 2.0](https://developers.asana.com/docs/oauth)

### (Method 1) Personal Access Token
If you are using a personal access token, you need to set the following environment variables:
```
ASANA_AUTH_TYPE=access_token
```
and head to your Asana Developer Console. From here, you can create a new Personal Access Token. Use this value for the `ASANA_ACCESS_TOKEN` environment variable.
Additionally, to safeguard the connector from abuse, set the `ASANA_CONNECTOR_API_KEY` environment variable to a secure value for bearer token authentication. 
Do not set this variable if you are using OAuth 2.0 authentication.

### (Method 2) OAuth 2.0
If you are using OAuth 2.0, you need to set the following environment variables:
```
ASANA_AUTH_TYPE=oauth
```
and head to your Asana Developer Console. From here, you can create a new OAuth App. Use the Client ID and Client Secret values
to register the connector with Cohere's API using Oauth 2.0.
Also, you need to set the Redirect URL to `https://api.cohere.com/v1/connectors/oauth/token` on the Oauth App settings page.
Here is an example of how to register the connector with Cohere's API using Oauth 2.0:
```bash
 curl  -X POST \
   'https://api.cohere.ai/v1/connectors' \
   --header 'Accept: */*' \
   --header 'Authorization: Bearer {COHERE-API-KEY}' \
   --header 'Content-Type: application/json' \
   --data-raw '{
   "name": "Asana with OAuth",
   "url": "{YOUR_CONNECTOR-URL}",
   "oauth": {
     "client_id": "{Your Asana App CLIENT-ID}",
     "client_secret": "{Your Asana App SECRET}",
     "authorize_url": "https://app.asana.com/-/oauth_authorize",
     "token_url": "https://app.asana.com/-/oauth_token",
   }
 }'
```

Then, head to your Admin Console. The URL at the top of your web browser should look like `https://app.asana.com/admin/<workspace_gid>`, 
grab the `<workspace_gid>` value and use it for `ASANA_WORKSPACE_GID`.
This variable is required for both authentication methods.

## Optional Configuration
```
ASANA_TASK_PROPERTIES
```
This variable may contain a comma-separated list of task properties (e.g. ["name","notes"]).
See the documentation [here](https://developers.asana.com/reference/tasks#task).
By default, the following task properties are returned:
```
[
        "actual_time_minutes",
        "name",
        "notes",
        "permalink_url",
        "approval_status",
        "assignee",
        "assignee.name",
        "assignee_section",
        "assignee_section.name",
        "assignee_status",
        "completed",
        "completed_at",
        "completed_by",
        "completed_by.name",
        "created_at",
        "created_by",
        "dependencies",
        "due_at",
        "due_on",
        "external",
        "hearts",
        "likes",
        "parent",
        "parent.name",
        "projects",
        "projects.name",
        "tags",
        "tags.name",
        "workspace",
        "workspace.name",
    ]
```

```
ASANA_SEARCH_LIMIT
```
This variable may contain the maximum number of results to return. It should be not greater than 100.
By default, 10 results are returned.

```
ASANA_FIELDS_MAPPING
```
This variable may contain a JSON object mapping Cohere fields
to Asana fields(key is Asana field,
the value is Cohere field). If this variable is not set, the data will be returned as is.


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
