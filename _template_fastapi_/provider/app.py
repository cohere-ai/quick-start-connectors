import logging
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Header, Response, status

import provider
from config import AppConfig
from datamodels import SearchRequest, SearchResponse
from exceptions import UpstreamProviderError


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
config = AppConfig()

logger.info(f"CONNECTOR_ID: {config.CONNECTOR_ID}")


def authenticate(Authorization: str = Header(None)) -> None:
    """
    Authenticate the user using the 'Authorization' header.

    Args:
        Authorization (str, optional): Authorization header. Defaults to Header(None).
    """
    if Authorization is None or Authorization != f"Bearer {config.CONNECTOR_API_KEY}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Missing Authorization Header",
        )
    logger.debug("authenticate: (OK)")


@app.post("/search", response_model=SearchResponse)
async def search(
    response: Response,
    request: Optional[SearchRequest] = None,
    user: None = Depends(authenticate),
):
    """
    Search Endpoint

    Args:
        request (Optional[Request], optional): Request object. Defaults to None.
        user (None, optional): User object. Defaults to Depends(authenticate).

    Returns:
        JSONResponse: Response object
    """
    response.headers["X-Connector-ID"] = config.CONNECTOR_ID

    if request is None:
        return SearchResponse(results=[])

    try:
        data = provider.search(request.query)
    except UpstreamProviderError as error:
        logger.error(f"upstream_search_error: {error.message}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error with search provider",
        )

    return SearchResponse(results=data)
