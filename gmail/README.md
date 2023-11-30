# Gmail Connector

Connects Cohere to Google Gmail. It uses the Gmail messages API to search
for emails.

## Configuration

The following configuration variables should be set as environment variables, or put into a `.env` file
to control the behaviour of this connector:

```
GMAIL_USER_ID=scott@lightsonsoftware.com
GMAIL_MAX_RESULTS=10
```

## Credentials

To use this connector, you will need to turn on the Gmail API in a Google Cloud project. There are a couple of steps to follow, please refer to the following [guide.](https://developers.google.com/gmail/api/quickstart/python)

You will need to:

1. Enable the API
2. Configure Oauth consent: use the user with the same email as the `GMAIL_USER_ID` environment variable
3. Create credentials for your app, and download the credentials.json file, making sure that you've whitelisted your hosted server's address as the redirect uri for the credentials

Once this is done, save the `credentials.json` file into this directory.

This connector will also require a `token.json` file that is generated automatically once you authorize the app. After you deploy it, head to your hosted connector server's `/ui` page. For example, `https://myconnector.com/ui`, and trigger an initial `/search` request. This will bring up the Google OAuth page, where you can login to the same email as step 2 earlier.

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
