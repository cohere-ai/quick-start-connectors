# Jira Quick Start Connector

This package is a utility for connecting Cohere to Jira.

## Limitations

The Jira connector will perform a full-text search based on the subject and description of the tickets in your org, by default it will return a maximum of 10 results.

## Configuration

This connector requires the following environment variables to enable Jira's search API.

```
JIRA_USER_EMAIL
JIRA_API_TOKEN
JIRA_ORG_DOMAIN
```

It uses Basic Auth with a user email and API token pair. To create an API token, click on your top-right profile icon, select Manage Account > Security > Create API Token. The org domain is the URL for your organization's Jira board, including the https:// scheme. You will need to put these environment variables in a `.env` file for development, see `.env-template`.

In order to use the `dev/load_data.py` script to load test tickets, the additional env var `JIRA_ISSUE_KEY` should be set. The key is typically a two-letter sequence that forms part of the issue number.

## Development

Create a virtual environment and install dependencies with poetry. We recommend using in-project virtual environments:

```bash
  $ poetry config virtualenvs.in-project true
  $ poetry install --no-root
```

To load some test issues into Jira, this repo provides a `load_data.py` script in `dev/`. Be careful not to run this script on a real Jira project!

```bash
  $ poetry shell
  $ python dev/load_data.py
```

Next, start up the search connector server:

```bash
  $ poetry shell
  $ flask --app provider --debug run --port 5000
```

and check with curl to see that everything works:

```bash
  $ curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --data '{
    "query": "stainless propane griddle"
  }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://localhost:5000/ui/
