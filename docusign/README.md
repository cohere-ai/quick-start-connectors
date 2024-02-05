# Docusign Connector

Connects Cohere to a Docusign.

## Configuration

To use this connector you will need to create an application in your Docusign account.
See the documentation [here](https://developers.docusign.com/platform/build-integration/) to create the application and
use it. After the application is created, you will need to set the following environment variable:

```bash
DOCUSIGN_API_ACCOUNT_ID=<API Account ID from your APP>
```

To use DocuSign API we also need the ACCESS_TOKEN. To get it, please follow the steps described in the documentation
[here](https://developers.docusign.com/platform/auth/). Docusign API uses OAuth2.0 for authentication.
You will need to chose one of the authentication flows described in the documentation above.
For example to use the Implicit Grant flow, you will need to
do [next steps](https://developers.docusign.com/platform/auth/implicit/implicit-get-token/) to get the Token.
Also, please note that the token scope should be set to `signature` when you request it.
Token lifetime is limited. After it expires, you will need to get a new one.
After you get the ACCESS_TOKEN, please set the following environment variable:

```bash
DOCUSIGN_ACCESS_TOKEN=<Access Token>
```

### Optional Configuration

The DocuSign connector has several optional configuration parameters:

```bash
DOCUSIGN_IS_PROD_ENV=<1 or 0>
```

This parameter is used to specify the API environment. By default, it is set to 1 (production environment).
If you want to use the demo environment, please set it to 0. The endpoints base URI depends on this parameter.
For example, if you set it to 1, the base URI will be https://account.docusign.com/oauth.
If you set it to 0, the base URI will be https://account-d.docusign.com/oauth.

```bash
DOCUSIGN_FROM_DATE==<Date From search parameter in the YYYY-MM-DD format>
```

By default, the search will be performed from the 2018-01-01. If you want to change it, please set this parameter.

```bash
DOCUSIGN_TO_DATE==<Date To search parameter in the YYYY-MM-DD format>
```

By default, the search will be performed to the current date. If you want to change it, please set this parameter.

```bash
DOCUSIGN_CONNECTOR_API_KEY
```

This variable should contain the API key for the Docusign connector.

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
