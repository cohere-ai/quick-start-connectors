# Github Quick Start Connector

This package is a utility for connecting Cohere to GitHub.

It uses GitHub's REST API to perform a code search and return matching files.

## Limitations

The Github connector supports the query syntax defined by `GITHUB_QUERY_TEMPLATE`. By default, it searches for code within a file and returns the matching results (up to 5, by default). You can, however, use the syntax allowed by Github's search, check https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-code for more details.

## Configuration

First, create a `.env` file based off the `.env-template`.

To use this connector, you must have a GitHub account, and configure an access token. It is recommended to create a fine-grained personal access token so you can give explicit access to certain resources to this connector. See: [Github Authentication](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for more details.
Use this value for the `GITHUB_TOKEN` environment variable.

You can optionally modify the other environment variables to customize the search behavior.

The default `GITHUB_QUERY_TEMPLATE` performs a general search across GitHub for the matching keywords. You can
customize the value to restrict the search to certain repositories using the GitHub syntax.

```
GITHUB_QUERY_TEMPLATE="{query} in:file language:js repo:jquery/jquery"
```

For example, the above query template would perform the search in Javascript files in the jquery repo.

The `GITHUB_RESULTS_PER_PAGE` value defaults to 5 in this search connector, although the GitHub default is 30. The
maximum number of results per page supported by GitHub is 100. A separate API call is required for each result,
as this search connector retrieves the full content of each search result. Therefore, it is suggested to keep the number
of results relatively low, if possible.

This search connector does not currently retrieve more than one result page, so the maximum number of results is
effectively 100.

## Development

Before running the Flask server, you must create a `.env` file with a GitHub token, or set it as a regular
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
