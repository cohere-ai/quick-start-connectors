import base64
import asyncio
import aiohttp

import requests
from flask import current_app as app, request
from msal import ConfidentialClientApplication

from . import UpstreamProviderError

AUTHORIZATION_HEADER = "Authorization"
BEARER_PREFIX = "Bearer "


class MsTeamsClient:
    DEFAULT_SCOPES = ["https://graph.microsoft.com/.default"]
    SEARCH_URL = "https://graph.microsoft.com/v1.0/search/query"
    SEARCH_ENTITY_TYPES = ["chatMessage"]
    APPLICATION_AUTH = "application"
    DELEGATED_AUTH = "user"

    def __init__(self, auth_type, search_limit=5):
        self.access_token = None
        self.headers = None
        self.user = None
        self.auth_type = auth_type
        self.search_limit = search_limit
        self.session = None
        self.loop = None
        self._start_session()

    def set_user(self, user):
        self.user = user

    def get_auth_type(self):
        return self.auth_type

    def _close_loop(self):
        self.loop.stop()
        self.loop.close()

    def _start_session(self):
        self.loop = asyncio.new_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def _close_session(self):
        await self.session.close()

    def set_app_access_token(self, tenant_id, client_id, client_secret):
        try:
            credential = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=f"https://login.microsoftonline.com/{tenant_id}",
            )

            token_response = credential.acquire_token_for_client(
                scopes=self.DEFAULT_SCOPES,
            )
            if "access_token" not in token_response:
                raise UpstreamProviderError(
                    "Error while retrieving access token from Microsoft Graph API"
                )
            self.access_token = token_response["access_token"]
            self.headers = {"Authorization": f"Bearer {self.access_token}"}
        except Exception as e:
            raise UpstreamProviderError(
                f"Error while initializing Teams client: {str(e)}"
            )

    def set_user_access_token(self, token):
        self.access_token = token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    async def _gather_messages(self, hits):
        messages = [self._get_message(hit) for hit in hits]
        return await asyncio.gather(*messages)

    async def _get_message(self, hit):
        url = f"https://graph.microsoft.com/v1.0/chats/{hit['resource']['chatId']}/messages/{hit['resource']['id']}"
        params = {
            "$select": "id,subject,summary,body,from,createdDateTime,webUrl,attachments,eventDetail",
        }

        async with self.session.get(
            url,
            headers=self.headers,
            params=params,
        ) as response:
            content = await response.json()
            if not response.ok:
                return None
            content["link"] = hit["resource"]["webLink"]
            return content

    async def _gather_downloadable_attachments(self, attachments):
        downloadable_attachments = [
            self._prepare_attachment_download_url(attachment)
            for attachment in attachments
        ]
        return await asyncio.gather(*downloadable_attachments)

    async def _prepare_attachment_download_url(self, attachment):
        # prepare url to request download link see
        # https://learn.microsoft.com/en-us/answers/questions/1072289/download-directly-chat-attachment-using-contenturl
        content_url = attachment["contentUrl"]
        b64encoded = base64.b64encode(content_url.encode("utf-8")).decode("utf-8")
        prepared = "u!" + b64encoded.rstrip("=").replace("/", "_").replace("+", "-")
        graph_api_url = (
            f"https://graph.microsoft.com/v1.0/shares/{prepared}/driveItem/content"
        )
        async with self.session.get(graph_api_url, headers=self.headers) as response:
            content = await response.content.read()
            if not response.ok:
                return attachment
            attachment["content"] = content
            return attachment

    def _prepare_attachments(self, messages, results):
        attachments = []
        for message in messages:
            if message is not None:
                if "attachments" in message:
                    for attachment in message["attachments"]:
                        attachment["downloadUrl"] = None
                        if attachment["contentType"] == "reference":
                            if "contentUrl" in attachment:
                                attachments.append(attachment)
                results.append(message)
        if len(attachments) > 0:
            self.loop.run_until_complete(
                self._gather_downloadable_attachments(attachments)
            )
        # Close session and loop
        self.loop.run_until_complete(self._close_session())
        self._close_loop()
        return attachments

    def _process_hits(self, hits):
        results = []
        messages = self.loop.run_until_complete(self._gather_messages(hits))
        self._prepare_attachments(messages, results)
        return results

    def _delegated_search(self, query):
        results = []
        response = requests.post(
            self.SEARCH_URL,
            headers=self.headers,
            json={
                "requests": [
                    {
                        "entityTypes": self.SEARCH_ENTITY_TYPES,
                        "query": {
                            "queryString": query,
                            "size": self.search_limit,
                        },
                    }
                ]
            },
        )
        if not response.ok:
            raise UpstreamProviderError(
                f"Error while searching Outlook: {response.text}"
            )
        for hit_container in response.json()["value"][0]["hitsContainers"]:
            hits_to_process = []
            if hit_container["total"]:
                for hit in hit_container["hits"]:
                    if hit["resource"]["@odata.type"] == "microsoft.graph.chatMessage":
                        hits_to_process.append(hit)
            if len(hits_to_process) > 0:
                results = self._process_hits(hits_to_process)

        return results

    def _app_search(self, query, user=None):
        results = []
        messages = []
        graph_api_url = (
            f"https://graph.microsoft.com/v1.0/users/{self.user}/chats/getAllMessages"
        )

        params = {
            "$select": "id,subject,summary,body,from,createdDateTime,webUrl,attachments,eventDetail",
            "$top": self.search_limit,
        }
        # Make a request to the Microsoft Graph API to get messages
        response = requests.get(graph_api_url, headers=self.headers, params=params)
        if not response.ok:
            raise UpstreamProviderError(
                f"Error while searching Outlook: {response.text}"
            )
        data = response.json()
        if "value" in data:
            messages.extend(data["value"])
        if len(messages) > 0:
            self._prepare_attachments(messages, results)
        return results

    def search(self, query):
        if self.access_token is None:
            raise UpstreamProviderError("Access token not set")
        if self.auth_type == self.APPLICATION_AUTH:
            results = self._app_search(query)
        elif self.auth_type == self.DELEGATED_AUTH:
            results = self._delegated_search(query)
        else:
            raise UpstreamProviderError(f"Invalid auth type: {self.auth_type}")
        return results


def get_client():
    assert (
        auth_type := app.config.get("GRAPH_AUTH_TYPE")
    ), "MSTEAMS_GRAPH_AUTH_TYPE must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 5)
    client = MsTeamsClient(auth_type, search_limit)
    if auth_type == client.APPLICATION_AUTH:
        assert (
            tenant_id := app.config.get("GRAPH_TENANT_ID")
        ), "MSTEAMS_GRAPH_TENANT_ID must be set"
        assert (
            client_id := app.config.get("GRAPH_CLIENT_ID")
        ), "MSTEAMS_GRAPH_CLIENT_ID must be set"
        assert (
            client_secret := app.config.get("GRAPH_CLIENT_SECRET")
        ), "MSTEAMS_GRAPH_CLIENT_SECRET must be set"
        assert (user_id := app.config.get("USER_ID")), "MSTEAMS_USER_ID must be set"
        client.set_app_access_token(tenant_id, client_id, client_secret)
        client.set_user(user_id)
    elif auth_type == client.DELEGATED_AUTH:
        token = get_access_token()
        if token is None:
            raise UpstreamProviderError("No access token provided in request")
        client.set_user_access_token(token)
    else:
        raise UpstreamProviderError(f"Invalid auth type: {auth_type}")
    return client


def get_access_token():
    authorization_header = request.headers.get(AUTHORIZATION_HEADER, "")
    if authorization_header.startswith(BEARER_PREFIX):
        return authorization_header.removeprefix(BEARER_PREFIX)
    return None
