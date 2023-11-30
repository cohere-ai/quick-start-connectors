import os

import boto3

from . import UpstreamProviderError

client = None


def get_client():
    global client
    assert (
        AWS_ACCESS_KEY_ID := os.environ.get("AWS_ACCESS_KEY_ID")
    ), "AWS_ACCESS_KEY_ID must be set"
    assert (
        AWS_SECRET_ACCESS_KEY := os.environ.get("AWS_SECRET_ACCESS_KEY")
    ), "AWS_SECRET_ACCESS_KEY must be set"
    assert (AWS_REGION := os.environ.get("AWS_REGION")), "AWS_REGION must be set"

    if not client:
        try:
            client = boto3.client(
                "redshift-data",
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
        except Exception as e:
            message = (
                f"Error {str(e)} while initializing redshift-data client through boto3."
            )
            raise UpstreamProviderError(message)

    return client
