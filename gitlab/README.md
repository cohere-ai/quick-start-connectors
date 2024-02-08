# GitLab Connector

This package is a utility for connecting Cohere to GitLab.

It uses the GitLab REST API to perform a code search and return matching files.

## Configuration

To use this connector, you must have a GitLab account, and configure an access token.

The GitLab access token must be configured as an environment variable when the Flask server is run. This is required.
Additional environment variables may be set to customize the behaviour of this search connector. These
environment variables can optionally be put into a `.env` file.

```
GITLAB_TOKEN=
GITLAB_RESULTS_PER_PAGE=5
GITLAB_SCOPE=
GITLAB_SEARCH_URL=
```

The `GITLAB_SCOPE` variable is used to control what to search. Possible values include:

- `projects`
- `issues`
- `merge_requests`
- `milestones`
- `snippet_titles`
- `users`
- `blobs`
- `commits`
- `notes`
- `wiki_blobs`

The availability of certain scopes is dependent on the GitLab plan you are subscribed to. Scopes
requiring ElasticSearch integration are not available on the free tier.

By default, this search connector will search the SaaS version of GitLab. If you have a locally hosted,
self-managed version of GitLab, you can configure this search connector to use your self-managed GitLab
by changing the `GITLAB_SEARCH_URL` variable.

Please consult the GitLab documentation
for more information about scopes and configuring access tokens.

Finally, to protect this connector from abuse, the `GITLAB_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

## Development

Before running the Flask server, you must create a `.env` file with a GitLab token, or set it as a regular
environment variable.

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
