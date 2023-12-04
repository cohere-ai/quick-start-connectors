import logging
import os
import datetime

from flask import current_app as app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import UpstreamProviderError


logger = logging.getLogger(__name__)

client = None


class GoogleCalendarClient:
    DEFAULT_SEARCH_LIMIT = 20
    SCOPES = [
        "https://www.googleapis.com/auth/calendar.readonly",
    ]

    def __init__(self):
        creds = None
        # Handle Authentication
        if os.path.exists("token.json"):
            logger.debug("Found token.json file")
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            logger.debug("No valid credentials found")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def _request(self, request):
        try:
            return request.execute()
        except HttpError as http_error:
            raise UpstreamProviderError(message=str(http_error)) from http_error

    def search_events(self, query):
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        request = self.service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=self.DEFAULT_SEARCH_LIMIT,
            singleEvents=True,
            orderBy="startTime",
            q=query,
        )

        search_results = self._request(request).get("items", [])

        return search_results


def get_client():
    global client
    if client is None:
        client = GoogleCalendarClient()

    return client
