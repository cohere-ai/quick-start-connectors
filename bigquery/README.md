# BigQuery Quick Start Connector

Connects Cohere to BigQuery, Google's cloud-based big data store.

## Limitations

Because BigQuery uses SQL under the hood, the BigQuery connector only allows search within a specific table, and for a specific column. Ideally, you should add indices on this column to speed up the query time. There is no way currently to add complex conditions, or JOINs of any kind.

## Configuration

To use this connector, you will need a GCP organization and a user with the necessary IAM role to
create a Service Account for BigQuery. Here are the steps required for authenticating your BigQuery client:

1. From your Google Cloud Console, head to the Credentials page.
2. Look for the section with Service Accounts, then click Manage service accounts.
3. Create a new Service Account here. Fill it with the relevant info, then limit the scope to BigQuery, giving it at least read-access. Then you can associate your user to this Service Account.
4. From the newly created Service Account, open the Keys tab and click Add Key. Then create a private key in JSON format (important!). Download the generated .json file, and then either move it or copy paste it's contents to `bigquery/credentials.json`

Next, create a `.env` file that replicates the `.env-template`. You will need to fill out the table and column name to perform matching with. See the values in `.env-template` for examples.

Finally, to protect this connector from abuse, the `BIGQUERY_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

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

The Flask API will be bound to :code:`http://127.0.0.1:5000`.

```bash
  curl --request POST \
    --url http://localhost:5000/search \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <CONNECTOR_API_KEY>' \
    --data '{
      "query": "BBQ"
    }'
```

Alternatively, load up the Swagger UI and try out the API from a browser: http://127.0.0.1:5000/ui/
