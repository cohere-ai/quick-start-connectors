from dropbox import Dropbox
from dropbox.exceptions import AuthError
from dropbox.files import FileStatus, SearchOptions  # type: ignore
from flask import current_app as app

from . import UpstreamProviderError


class DropboxClient:
    def __init__(self, token, search_limit, path):
        self.search_limit = search_limit
        self.path = path
        self.client = Dropbox(token)

        # Test connection
        try:
            self.client.users_get_current_account()
        except AuthError:
            raise UpstreamProviderError(
                "ERROR: Invalid access token; try re-generating an "
                "access token from the app console on the web."
            )

    def search(self, query):
        results = self.client.files_search_v2(
            query,
            SearchOptions(
                file_status=FileStatus.active,
                filename_only=False,
                max_results=self.search_limit,
                path=self.path,
            ),
            include_highlights=False,
        )

        return results

    def download_file(self, path):
        metadata, file = self.client.files_download(path)

        return metadata, file


def get_client(oauth_token=None):
    search_limit = app.config.get("SEARCH_LIMIT", 5)
    path = app.config.get("PATH", "")
    env_token = app.config.get("ACCESS_TOKEN", "")
    token = None

    if env_token != "":
        token = env_token
    elif oauth_token is not None:
        token = oauth_token
    else:
        raise AssertionError("No access token or Oauth credentials provided.")

    return DropboxClient(token, search_limit, path)
