import logging
import os

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from flask import current_app as app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

CACHE_SIZE = 256

client = None


class GoogleMailClient:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
    ]

    def __init__(self, user_id, search_limit):
        self.user_id = user_id
        self.search_limit = search_limit

        credentials = None

        # Handle Authentication
        if os.path.exists("token.json"):
            logger.debug("Found token.json file")
            credentials = Credentials.from_authorized_user_file(
                "token.json", self.SCOPES
            )

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or credentials.expired or not credentials.valid:
            logger.debug("No valid credentials found")

            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(credentials.to_json())

        self.service = build("gmail", "v1", credentials=credentials)

    def _request(self, request):
        try:
            return request.execute()
        except HttpError as http_error:
            raise UpstreamProviderError(message=str(http_error)) from http_error

    @lru_cache(maxsize=CACHE_SIZE)
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

    @lru_cache(maxsize=CACHE_SIZE)
    def get_message(self, message_id):
        request = (
            self.service.users()
            .messages()
            .get(format="full", userId=self.user_id, id=message_id)
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
    global client

    if client is None:
        assert (user_id := app.config.get("USER_ID")), "GMAIL_USER_ID must be set"
        search_limit = app.config.get("SEARCH_LIMIT", 5)
        client = GoogleMailClient(user_id, search_limit)

    return client
