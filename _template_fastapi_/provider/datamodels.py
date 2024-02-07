"""
Pydantic Data Models to implement a custom Cohere Connector
See https://docs.cohere.com/docs/connectors 
"""

from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class DataItem(BaseModel):
    """
    While the structure of the object in the results field is fully flexible, meaning any fields are allowed,
    Cohere recommends the following Document Structure:

    - Keep documents under 300 words or less.
    - Or add a text field which is truncated when prompt_truncation=true in the request.
    - Add a timestamp field to support temporal user queries.
    - Add an id field to allow identification of the relevant document.
    - Add a title field to allow the citations returned in the reply to be better-formatted.
    - Use excludes to exclude fields, such as the id, from the prompt.
    - Add a url field to allow the client to link to the document.

    See https://docs.cohere.com/docs/creating-and-deploying-a-connector
    """

    id: Optional[int] = None
    url: HttpUrl
    title: str
    text: str
    timestamp: datetime


class SearchRequest(BaseModel):
    """
    The Connector should accept a Request object with a query field.

    See https://docs.cohere.com/docs/creating-and-deploying-a-connector
    """

    query: Optional[str] = None


class SearchResponse(BaseModel):
    """
    The Connector should return a list of DataItems.

    See https://docs.cohere.com/docs/creating-and-deploying-a-connector
    """

    results: List[DataItem]
