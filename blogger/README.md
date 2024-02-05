# Google Blogger Connector

This package is a utility for connecting Cohere to Google Blogger.

## Configuration

The search connector requires the following environment variables:

```
BLOGGER_USER_ACCOUNT_INFO
```

This variable should contain the JSON content of the user account credentials file.
To get this file use instructions from [here](https://developers.google.com/blogger/docs/3.0/using#auth).

```
BLOGGER_CONNECTOR_API_KEY
```

**Note:** You should download credentials file in JSON format.
You will also need a `token.json` file in order to use this connector. If this
application is run on a desktop OS, outside of the Docker container, and there is
no `token.json` file found, it will open a browser window with a Google OAuth
authorization page. Once the app is authorized, the search connector will save a
`token.json` file with the response.

This will only work if a browser is available, however. When running on a server or in
a Docker container, then the `token.json` file will need to be saved another way
(such as through CI build tools).

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

Next, start up the search provider server:

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
