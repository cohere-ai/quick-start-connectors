import datetime
import logging

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
DEFAULT_SEARCH_LIMIT = 20


class GoogleCalendarClient:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
    ]

    def __init__(self, service_account_info, access_token, calendar_id, search_limit):
        self.search_limit = search_limit
        self.calendar_id = calendar_id
        self.service = build(
            "calendar",
            "v3",
            credentials=self._request_credentials(service_account_info, access_token),
        )

    def _request_credentials(self, service_account_info=None, access_token=None):
        if service_account_info is not None:
            logger.debug("Using service account credentials")
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=self.SCOPES
            )
            if credentials.expired or not credentials.valid:
                credentials.refresh(Request())

            return credentials
        elif access_token is not None:
            logger.debug("Using oauth credentials")
            return Credentials(access_token)
        else:
            raise UpstreamProviderError(
                "No service account or oauth credentials provided"
            )

    def _request(self, request):
        try:
            return request.execute()
        except HttpError as http_error:
            raise UpstreamProviderError(message=str(http_error)) from http_error

    def search_events(self, query):
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

        request = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=now,
            maxResults=self.search_limit,
            singleEvents=True,
            orderBy="startTime",
            q=query,
        )

        search_results = self._request(request).get("items", [])

        return search_results


def get_client():
    service_account_info = app.config.get("SERVICE_ACCOUNT_INFO", None)
    access_token = get_access_token()
    calendar_id = app.config.get("CALENDAR_ID", "primary")
    search_limit = app.config.get("SEARCH_LIMIT", DEFAULT_SEARCH_LIMIT)
    if service_account_info is None and access_token is None:
        raise AssertionError("No service account or oauth credentials provided")

    return GoogleCalendarClient(
        service_account_info, access_token, calendar_id, search_limit
    )


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
