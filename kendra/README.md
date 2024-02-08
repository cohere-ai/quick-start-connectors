# Kendra Connector

Connect Cohere to AWS Kendra.

## Configuration

To use this connector, you must first [configure AWS Kendra](https://docs.aws.amazon.com/kendra/latest/dg/setup.html). Once you have Kendra configured, you
will need to set four environment variables in order to use this connector: `AWS_DEFAULT_REGION`, `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY` and `KENDRA_INDEX_ID`.

The `AWS_DEFAULT_REGION` environment variable corresponds to the AWS region that you have configured Kendra in.
The `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` correspond to an IAM user configured with access
to Kendra. The `KENDRA_INDEX_ID` value corresponds to the Kendra index that you would like this
connector to search. The value can be found on the Kendra Index Settings page in AWS Management Console.
You may optionally set the other AWS environment variables that are used by Boto3.

The environment variables can optionally be placed in a file called `.env`. See `.env-template` for a
full list of available options. This file can be copied to `.env` and modified. Options that are
left empty will be ignored.

The Kendra index and returned data can be extensively customized in the AWS Management Console.

Finally, to protect this connector from abuse, the `KENDRA_CONNECTOR_API_KEY` environment variable must be set to a secure value that will be used for this connector's own bearer token authentication.


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
