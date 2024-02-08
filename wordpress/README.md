# Wordpress Connector

Connects Cohere to Wordpress.

## Configuration

This connector requires that the environment variables `WORDPRESS_URL`,`WORDPRESS_USERNAME`, `WORDPRESS_PASSWORD` be set in order to run.
These variables can optionally be put into a `.env` file for development.
A `.env-template` file is provided as a reference.

`WORDPRESS_URL`
This variable should contain the URL of the Wordpress instance to connect to.

`WORDPRESS_USERNAME`
This variable should contain the username of the Wordpress user to connect as.

`WORDPRESS_PASSWORD`
To set this variable go to your user settings and generate an Application Password for your account.

`WORDPRESS_CONNECTOR_API_KEY`
This variable should contain the API key for the connector.

## Optional Configuration
```
WORDPRESS_SEARCH_LIMIT
```
This variable may contain the maximum number of results to return from the search. The default is 20.

## Development

A docker-compose file is provided for local testing. Start it with

```bash
  $ docker-compose up
```

and complete the setup by visiting http://localhost:8000 and completing the installation. Once installation is finished log in to your account, navigate to user settings, and create
an Application Password that will be used by this development environment. Set this password as the value of `WORDPRESS_PASSWORD` in your `.env` file.

To start the connector, create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

A script is provided in `dev/` to generate test data. Invoke it with

```bash
  $ poetry shell
  $ python dev/load_data.py
```

To start the server, run the following commands

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
