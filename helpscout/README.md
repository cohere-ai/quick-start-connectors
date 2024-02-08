# HelpScout Connector

Connects Cohere to a HelpScout.

## Configuration

To use this connector you will need to create an application in your HelpScout account.
To start, head over to your HelpScout account, and from the top-right profile icon > My Apps > Create My APP create new
one.
This one will be used for the `HELPSCOUT_APP_ID` and `HELPSCOUT_APP_SECRET` environment variable.
Also, please note - the API returns only first 25 results.
`HELPSCOUT_CONNECTOR_API_KEY` is the API key for your HelpScout connector.

### Optional Configuration

To customize the search fields, you can set the following environment variables: HELPSCOUT_SEARCH_FIELDS
The query parameter will be splitted by spaces and each word will be searched in the fields specified by OR condition.
By default, the search fields are: subject and body. Example: HELPSCOUT_SEARCH_FIELDS=subject,body
All available search fields can be found
here: [Query fields](https://developer.helpscout.com/mailbox-api/endpoints/conversations/list/#query)

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
