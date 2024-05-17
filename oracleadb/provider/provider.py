import logging
import os
import oracledb
from flask import current_app as app
import time

import sys
from .client import get_client

logger = logging.getLogger(__name__)


def search(query):

    adbs_client = get_client()

    db_rag_output = adbs_client.search(query)

    return db_rag_output

