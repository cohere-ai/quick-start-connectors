import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class FirefliesApiClient:
    API_URL = "https://api.fireflies.ai/graphql"

    def __init__(self, api_key, search_limit):
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.search_limit = search_limit

    def get_search_limit(self):
        return self.search_limit

    def post(self, params={}):
        response = requests.post(self.API_URL, headers=self.headers, json=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def get_transcripts(self, limit=20):
        query = """
            query transcripts($limit: Int){ 
                    transcripts(limit: $limit){ 
                        id 
                        sentences{ 
                            index 
                            text 
                            raw_text 
                        } 
                        title 
                        host_email 
                        organizer_email 
                        fireflies_users 
                        participants 
                        date 
                        transcript_url 
                        duration 
                    } 
            }
        """
        params = {"query": query, "variables": {"limit": self.get_search_limit()}}
        return self.post(params)


def get_client():
    global client
    assert (api_key := app.config.get("API_KEY")), "FIREFLIES_API_KEY must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 20)

    if not client:
        client = FirefliesApiClient(api_key, search_limit)

    return client
