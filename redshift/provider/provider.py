import logging
import backoff
from typing import Any

import boto3
from botocore.exceptions import ClientError
from flask import current_app as app
from .client import get_client

from . import UpstreamProviderError


logger = logging.getLogger(__name__)


def parse_data(response_data) -> list[dict[str, Any]]:
    # Extract the metadata for column names
    column_metadata = response_data["ColumnMetadata"]
    column_names = [column["name"] for column in column_metadata]

    # Extract the records and transform them into a list of dictionaries
    records = response_data["Records"]
    formatted_records = []

    for record in records:
        formatted_record = {column_names[i]: value for i, value in enumerate(record)}
        formatted_records.append(formatted_record)

    return formatted_records


@backoff.on_exception(backoff.expo, ClientError, max_time=20, max_tries=10)
def get_statement_with_retry(client, execution_id):
    statement_response = client.get_statement_result(
        Id=execution_id,
    )

    return statement_response


def search(query) -> list[dict[str, Any]]:
    LIMIT_SIZE = app.config.get("LIMIT_SIZE", 100)
    assert (
        db_name := app.config.get("DATABASE_NAME")
    ), "REDSHIFT_DATABASE_NAME must be set"
    assert (
        workgroup_name := app.config.get("WORKGROUP_NAME")
    ), "REDSHIFT_WORKGROUP_NAME must be set"
    assert (
        db_table := app.config.get("DATABASE_TABLE")
    ), "REDSHIFT_DATABASE_TABLE must be set"
    assert (
        db_column := app.config.get("DATABASE_COLUMN")
    ), "REDSHIFT_DATABASE_COLUMN must be set"

    redshift_client = get_client()
    sql_query = f"""
        SELECT * from {db_table}
        WHERE {db_column} ILIKE :query_param LIMIT {LIMIT_SIZE};
    """
    params = [
        {
            "name": "query_param",
            "value": f"%{query}%",
        }
    ]

    try:
        # Execute statement and then fetch the results with retries
        # Redshift executes the statement asynchronously, we have to continuously
        # poll for results with get_statement_result() to know the outcomes
        execution_response = redshift_client.execute_statement(
            WorkgroupName=workgroup_name,
            Database=db_name,
            Sql=sql_query,
            Parameters=params,
        )
        # Get result, with retries on the same execution ID
        results_response = get_statement_with_retry(
            redshift_client, execution_response["Id"]
        )
    except ClientError as err:
        # Finally, if all the retries fail then we can use describe_response()
        # for a better understanding of why the execution failed
        describe_response = redshift_client.describe_statement(
            Id=execution_response["Id"]
        )
        raise UpstreamProviderError(describe_response) from err

    # AWS Redshift response is keyed by type, need to
    # parse to column name instead
    return parse_data(results_response)
