# Zulip Quick Start Connector

Connects Cohere to Zulip, the messaging platform.

## Limitations

The Zulip connector currently searches across all messages that the Bot user you create is subscribed to. Notably, messages created before the Bot is subscribed to a stream will NOT be searchable. It will return the contents of the message(s), but not any uploaded file contents.

## Configuration

To use this connector you will need to configure a `.env` file. See the `.env-template` for reference.

To start, head over to your Zulip org and click on the top-right cog icon > Personal Settings > Bots > Add a new bot. Use the bot's email and API key for the `ZULIP_BOT_EMAIL` and `ZULIP_API_KEY` environment variables, respectively. Then retrieve the URL domain of your Zulip org for the `ZULIP_SITE` variable, e.g: `mysite.zulipchat.com`.

Finally, to protect this connector from abuse, the `ZULIP_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

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
