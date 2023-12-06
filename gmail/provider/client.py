import logging
import os

from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import request, current_app as app
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "
DEFAULT_SEARCH_LIMIT = 5
USER_ME = "me"


class GoogleMailClient:
    FORMAT = "full"
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
    ]

    def __init__(self, service_account_info, access_token, user_id, search_limit):
        self.user_id = user_id
        self.search_limit = search_limit
        self.service = build(
            "gmail",
            "v1",
            credentials=self._request_credentials(service_account_info, access_token),
        )

    def _request_credentials(self, service_account_info=None, access_token=None):
        if service_account_info is not None:
            logger.debug("Using Service Account credentials")
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=self.SCOPES
            )
            if credentials.expired or not credentials.valid:
                credentials.refresh(Request())

            # For Service Account auth, need to set user email for delegated access
            credentials_delegated = credentials.with_subject(self.user_id)

            return credentials_delegated
        elif access_token is not None:
            logger.debug("Using Oauth credentials")
            return Credentials(access_token)
        else:
            raise UpstreamProviderError(
                "No Service Account or Oauth credentials provided"
            )

    def _request(self, request):
        try:
            return request.execute()
        except HttpError as http_error:
            raise UpstreamProviderError(message=str(http_error)) from http_error

    def search_mail(self, query):
        request = (
            self.service.users()
            .messages()
            .list(
                userId=self.user_id,
                maxResults=self.search_limit,
                q=query,
            )
        )

        search_results = self._request(request)

        return search_results

    def get_message(self, message_id):
        request = (
            self.service.users()
            .messages()
            .get(format=self.FORMAT, userId=self.user_id, id=message_id)
        )

        message = self._request(request)

        return message

    def batch_get_messages(self, message_ids):
        # Use ThreadPoolExecutor for I/O bound tasks
        with ThreadPoolExecutor() as executor:
            future_to_message_id = {
                executor.submit(self.get_message, id): id for id in message_ids
            }
            results = []

            for future in as_completed(future_to_message_id):
                id = future_to_message_id[future]

                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    logger.info(f"Error fetching message with id {id}: {e}")

        return results


def get_client():
    service_account_info = app.config.get("SERVICE_ACCOUNT_INFO", None)
    access_token = get_access_token()
    user_id = app.config.get("USER_ID")
    search_limit = app.config.get("SEARCH_LIMIT", DEFAULT_SEARCH_LIMIT)

    if service_account_info is None and access_token is None:
        raise AssertionError("No service account or oauth credentials provided")

    # Using Oauth, use "me" user for current authenticated user
    if service_account_info is None and access_token is not None:
        user_id = USER_ME

    return GoogleMailClient(service_account_info, access_token, user_id, search_limit)


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
