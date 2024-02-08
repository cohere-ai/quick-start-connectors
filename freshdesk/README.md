# Freshdesk Quick Start Connector

Connects Cohere to Freshdesk, the cloud-based customer service management tool.

## Limitations

This connector uses Freshdesk's [Filter Tickets](https://developers.freshdesk.com/api/#filter_tickets) API, which does not have full-text search enabled for the subject or description of tickets. It uses strict matching on Ticket fields (see documentation for details).

## Configuration

To use this connector, you will need a Freshdesk support portal. From there, click your profile picture
in the top-right corner, go to Profile Settings and click View API key. Use this value for the
`FRESHDESK_API_KEY` environment variable.

Now grab your domain name from your support portal's URL, this will look like `mycompany.freshdesk.com`.
Use this value for `FRESHDESK_DOMAIN_NAME`.

Also, use the `FRESHDESK_TICKET_PARAMETERS` value to determine which field(s) the match will be performed on.

Finally, to protect this connector from abuse, the `FRESHDESK_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

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
