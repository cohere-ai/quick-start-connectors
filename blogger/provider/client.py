import logging
import os.path

from flask import current_app as app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import UpstreamProviderError

logger = logging.getLogger(__name__)

client = None


class BloggerApiClient:
    SCOPES = [
        "https://www.googleapis.com/auth/blogger",
        "https://www.googleapis.com/auth/blogger.readonly",
    ]

    DISCOVERY_URL = "https://blogger.googleapis.com/$discovery/rest?version=v3"

    def __init__(self, user_account_info):
        self.credentials = None
        self.user_account_info = user_account_info
        self.get_oauth_credentials()

    def get_oauth_credentials(self):
        if os.path.exists("token.json"):
            logger.debug("Found token.json file")
            self.credentials = Credentials.from_authorized_user_file(
                "token.json", self.SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            logger.debug("No valid credentials found")
            if (
                self.credentials
                and self.credentials.expired
                and self.credentials.refresh_token
            ):
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    self.user_account_info, self.SCOPES
                )
                self.credentials = flow.run_local_server(port=8080)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(self.credentials.to_json())

    def get_service(self):
        if self.credentials.expired or not self.credentials.valid:
            self.credentials.refresh(Request())

        service = build(
            "blogger",
            "v3",
            credentials=self.credentials,
            discoveryServiceUrl=self.DISCOVERY_URL,
        )
        return service

    def get_blogs_posts(self, query):
        results = []
        try:
            service = self.get_service()
            blogs = service.blogs()
            user_blogs = blogs.listByUser(userId="self").execute()
            if "items" in user_blogs:
                for blog in user_blogs["items"]:
                    blog_posts = (
                        service.posts().search(blogId=blog["id"], q=query).execute()
                    )
                    if "items" in blog_posts:
                        results += blog_posts["items"]
        except HttpError as http_error:
            raise UpstreamProviderError(message=str(http_error)) from http_error

        return results


def get_client():
    global client
    assert (
        user_account_info := app.config.get("USER_ACCOUNT_INFO")
    ), "BLOGGER_USER_ACCOUNT_INFO must be set"

    if not client:
        client = BloggerApiClient(user_account_info)

    return client
