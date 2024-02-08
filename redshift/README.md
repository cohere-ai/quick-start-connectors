# Amazon Redshift Connector

Connects Cohere to Amazon's Redshift, their petabyte-scale cloud data warehouse.

## Configuration

To use this connector, you must first setup your AWS Redshift instance with a database setup. Then,
create a new IAM user for this connector. The IAM user will require either the `AmazonRedshiftFullAccess`
policy, but it is recommended to add the `AmazonRedshiftReadOnlyAccess` policy with `Redshift Serverless` permissions
instead, to give your user read-only access.

From this IAM user, you can then retrieve the values to input for `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for
authentication. You will also need to retrieve information about your Redshift instance, see the `.env-template` file
for what is required.

Finally, to protect this connector from abuse, the `REDSHIFT_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.

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
