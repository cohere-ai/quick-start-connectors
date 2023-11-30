import requests
from flask import current_app as app

from . import UpstreamProviderError

client = None


class LinearApiClient:
    API_URL = "https://api.linear.app/graphql"

    def __init__(self, api_key, search_limit):
        self.headers = {"Authorization": f"{api_key}"}
        self.search_limit = search_limit

    def get_search_limit(self):
        return self.search_limit

    def post(self, params={}):
        response = requests.post(self.API_URL, headers=self.headers, json=params)

        if response.status_code != 200:
            message = response.text or f"Error: HTTP {response.status_code}"
            raise UpstreamProviderError(message)

        return response.json()

    def search_issues_by_term(self, term):
        query = """
            query SearchQuery($term: String!, $first: Int) {
                searchIssues(term: $term, first: $first) {
                    nodes {
                        id
                        title
                        description
                        url
                        updatedAt
                        archivedAt  
                        assignee {
                            active
                            avatarUrl
                            email
                            displayName   
                            name   
                            organization {
                                id
                                name    
                            }  
                        }  
                        branchName
                        comments {
                            nodes {
                                id
                                documentContent 
                                {  
                                    id
                                    content
                                }
                                url
                            }  
                        }  
                        completedAt
                        createdAt
                        cycle {
                            id
                            name
                            startsAt
                            scopeHistory  
                        }
                        dueDate
                        priority
                        previousIdentifiers
                        startedAt
                        state {
                            id
                            name
                            type
                            color
                            description
                        }
                        trashed
                    }
                }
            }
        """
        params = {
            "query": query,
            "variables": {"term": term, "first": self.search_limit},
        }
        return self.post(params)


def get_client():
    global client
    assert (api_key := app.config.get("API_KEY")), "LINEAR_API_KEY must be set"
    search_limit = app.config.get("SEARCH_LIMIT", 20)

    if not client:
        client = LinearApiClient(api_key, search_limit)

    return client
