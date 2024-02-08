# ServiceNow Connector

Connects Cohere to ServiceNow.

## Limitations
The ServiceNow connector currently only supports the search through the available tables.
The [Table API](https://docs.servicenow.com/bundle/utah-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html) is used to search through the available tables.

## Configuration
To use this connector you need to create a [new application](https://developer.servicenow.com/dev.do#!/learn/courses/utah/app_store_learnv2_buildmyfirstapp_utah_build_my_first_application/app_store_learnv2_buildmyfirstapp_utah_guided_app_creator_and_servicenow_studio/app_store_learnv2_buildmyfirstapp_utah_creating_an_application) in your ServiceNow account.
After creating the application, you need to create [tables](https://developer.servicenow.com/dev.do#!/learn/courses/utah/app_store_learnv2_buildmyfirstapp_utah_build_my_first_application/app_store_learnv2_buildmyfirstapp_utah_guided_app_creator_and_servicenow_studio/app_store_learnv2_buildmyfirstapp_utah_guided_app_creator_data_pane) and populate them with data.
Then create an [Experience](https://developer.servicenow.com/dev.do#!/learn/courses/utah/app_store_learnv2_uibuilder_utah_ui_builder/app_store_learnv2_uibuilder_utah_create_pages_in_ui_builder/UCP_CreatingAnExperience_Utah) for the application.

The ServiceNow connector offers two authentication methods: Basic Authentication and OAuth 2.0. 
See the [ServiceNow documentation](https://docs.servicenow.com/bundle/utah-api-reference/page/integrate/inbound-rest/concept/c_RESTAPI.html#d792755e650)

### Basic Authentication
If you are using Basic Authentication, you need to set the following environment variables:
```
SERVICENOW_AUTH_TYPE=basic
```
This variable configures the authentication type to Basic Authentication.

```
SERVICENOW_USERNAME
```
This variable is the username of the ServiceNow instance account.

```
SERVICENOW_PASSWORD
```
This variable is the password of the ServiceNow instance account.

```
SERVICENOW_CONNECTOR_API_KEY
```
This variable must be set to a secure value that will be used for this connector's own bearer token authentication.
Do not set this variable for OAuth 2.0 authentication.

### OAuth 2.0
If you are using OAuth 2.0, you need to set the following environment variables:
```
SERVICENOW_AUTH_TYPE=oauth
```
This variable configures the authentication type to OAuth 2.0.
Also, you need to set up your ServiceNow instance as an OAuth Client.
Use this [article](https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0778194) to set up your ServiceNow instance as an OAuth Client.
Please note that we use [OAuth authorization code grant flow](https://docs.servicenow.com/bundle/vancouver-platform-security/page/administer/security/concept/c_OAuthAuthorizationCodeFlow.html) for this connector.
Use the Client ID and Client Secret values from the OAuth Client settings page
to register the connector with Cohere's API using Oauth 2.0.
Also, you need to set the Redirect URL to `https://api.cohere.com/v1/connectors/oauth/token` on the All -> System OAuth -> Application Registries -> `Your app registry` page.
Here is an example of how to register the connector with Cohere's API using Oauth 2.0:
```bash
 curl  -X POST \
   'https://api.cohere.ai/v1/connectors' \
   --header 'Accept: */*' \
   --header 'Authorization: Bearer {COHERE-API-KEY}' \
   --header 'Content-Type: application/json' \
   --data-raw '{
   "name": "ServiceNow with OAuth",
   "url": "{YOUR_CONNECTOR-URL}",
   "oauth": {
     "client_id": "{Your Asana App CLIENT-ID}",
     "client_secret": "{Your Asana App SECRET}",
     "authorize_url": "https://dev221936.service-now.com/oauth_auth.do",
     "token_url": "https://dev221936.service-now.com/oauth_token.do",
   }
 }'
```


For both authentication methods mentioned above, you need to set the following environment variables:

```
SERVICENOW_INSTANCE_URL
```
This variable is the URL of your ServiceNow instance.

```
SERVICENOW_TABLE_NAME
```
This variable is the name of the table that you want to search through.

## Optional Configuration
The following environment variables are optional:

```
SERVICENOW_SEARCH_LIMIT
```
This variable may contain the maximum number of results to return. It should be not greater than 100.
By default, 10 results are returned.

```
SERVICENOW_FIELDS_MAPPING
```
This variable may contain a JSON object mapping Cohere fields
to ServiceNow fields(key is ServiceNow field,
the value is Cohere field). If this variable is not set, the data will be returned as is.


These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided with all the environment variables that are used by this demo.



## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Then start the server

```bash
  $ poetry run flask --app provider --debug run --port 5000
```

and check with curl to see that everything is working

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
