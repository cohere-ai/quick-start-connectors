import logging
import os
import uvicorn

from client import CustomClient
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Header, Request
from datamodels import DataItem, Request, Response


logging.basicConfig(level=logging.DEBUG)

load_dotenv()
SERVICE_API_KEY = os.getenv("CONNECTOR_API_KEY")
app = FastAPI()
client = CustomClient()


def authenticate(Authorization: str = Header(None)) -> None:
    """
    Authenticate the user using the 'Authorization' header.

    Args:
        Authorization (str, optional): Authorization header. Defaults to Header(None).
    """
    if Authorization is None or Authorization != f"Bearer {SERVICE_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    logging.debug("authenticate: (OK)")


@app.post("/search", response_model=Response)
async def search(request: Optional[Request] = None, 
                 user: None = Depends(authenticate)) -> Response:
    """
    Search Endpoint

    Args:
        request (Optional[Request], optional): Request object. Defaults to None.
        user (None, optional): User object. Defaults to Depends(authenticate).

    Returns:
        Response: Response object (see datamodels.py)
    """
    if request is None:
        logging.debug(f"search: missing_body")
        return Response(results=[])
    try:
        logging.debug(f"search:request.query: {request.query}")
        data = client.search(query=request.query)
        return Response(results=[DataItem(**d) for d in data])
    except Exception as error:
        logging.error(f"search:error: {error}")
        return Response(results=[])


if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8080)