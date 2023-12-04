# Google Calendar Connector

This connects Cohere to Google Calendar, allowing searching events.

## Credentials

To use this connector, you will need to enable the Google Calendar API in a Google Cloud project. There are several steps to follow, please refer to the following [guide.](https://developers.google.com/calendar/api/quickstart/python)

You will need to:

1. Enable the API
2. Configure OAuth consent: use the Google account that will be used for the Calendar integration
3. Create credentials for your app, making sure to select the "Desktop app" option, then download the `credentials.json` file

Once this is done, save the `credentials.json` file into this directory.

This connector will also require a `token.json` file that is generated automatically once you authorize the app. After you deploy it, head to your hosted connector server's `/ui` page. For example, `https://myconnector.com/ui`, and trigger an initial `/search` request. This will bring up the Google OAuth page, where you can login to the same email as step 2 earlier.

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
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "charcoal"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
