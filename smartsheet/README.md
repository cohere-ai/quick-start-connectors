# Smartsheet Connector

Connects Cohere to a SmartSheet.

## Configuration

To use this connector you will need to get a Smartsheet API access token.
This one will be used for the `SMARTSHEET_ACCESS_TOKEN` environment variable.
To get the access token, please follow these steps:

1. Click the "Account" button in the lower-left corner of the Smartsheet screen, and then click "Personal Settings".
2. Click the "API Access" tab.
3. Click the "Generate new access token" button to obtain an access token.

Finally, to protect this connector from abuse, the `SMARTSHEET_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

### Optional Configuration

To set the search scope for the connector, you will need to set the `SMARTSHEET_SEARCH_SCOPE` environment variable
using available scopes separated by comma.
By default, the connector will search through all available scopes:

1. cellData - Data in cells
2. comments - Comments on sheets
3. folderNames - Names of folders
4. reportNames - Names of reports
5. sheetNames - Names of sheets
6. sightNames - Names of sights
7. summaryFields - Summary fields
8. templateNames - Names of templates
9. workspaceNames - Names of workspaces

Example of setting the SMARTSHEET_SEARCH_SCOPE environment variable:

```bash
SMARTSHEET_SEARCH_SCOPE=cellData,comments
```

By default, the connector will return 100 results per search.
To change this, set the `SMARTSHEET_PAGE_SIZE` environment variable.
Please note that the minimum page size is 100.

```bash
SMARTSHEET_PAGE_SIZE=150
```

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
