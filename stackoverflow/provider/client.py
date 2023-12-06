from flask import current_app as app
import requests

from . import UpstreamProviderError


client = None


class StackOverflowClient:
    BASE_API_URL = f"https://api.stackoverflowteams.com/2.3"

    def __init__(self, team, access_token):
        self.team = team
        self.headers = {"X-API-Access-Token": access_token}

    def search(self, query):
        params = {
            "order": "desc",
            "sort": "activity",
            "intitle": query,
            "team": self.team,
        }

        response = requests.get(
            f"{self.BASE_API_URL}/search", params=params, headers=self.headers
        )

        if response.status_code != 200:
            raise UpstreamProviderError(
                f"Error searching StackOverflow with query {query}."
            )

        return response.json()

    def get_question(self, question_id):
        params = {"team": self.team, "filter": "withbody"}

        response = requests.get(
            f"{self.BASE_API_URL}/questions/{question_id}",
            params=params,
            headers=self.headers,
        )

        if response.status_code != 200:
            return None

        return response.json()

    def get_answer(self, answer_id):
        params = {"team": self.team, "filter": "withbody"}

        response = requests.get(
            f"{self.BASE_API_URL}/answers/{answer_id}",
            params=params,
            headers=self.headers,
        )

        if response.status_code != 200:
            return None

        return response.json()


def get_client():
    global client

    if client is None:
        assert (team := app.config.get("TEAM")), "STACKOVERFLOW_TEAM must be set"
        assert (access_token := app.config.get("PAT")), "STACKOVERFLOW_PAT must be set"
        client = StackOverflowClient(team, access_token)

    return client
