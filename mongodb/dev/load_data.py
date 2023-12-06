import csv
import logging
import os

import pymongo
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logger.info("Loading BBQ Test Data")

load_dotenv()

client = pymongo.MongoClient(
    host=os.environ.get("MONGODB_HOST", "mongo"),
    port=os.environ.get("MONGODB_PORT", 27017),
    username=os.environ.get("MONGODB_ROOT_USERNAME", "root"),
    password=os.environ.get("MONGODB_ROOT_PASSWORD", "example"),
)

fields = []

db = client.bbq

with open("/bbq.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        db.bbqs.insert_one(row)

db.bbqs.drop_indexes()
db.bbqs.create_index(
    [
        ("Name", pymongo.TEXT),
        ("Description", pymongo.TEXT),
        ("Features", pymongo.TEXT),
        ("Brand", pymongo.TEXT),
        ("Color", pymongo.TEXT),
        ("Rank", pymongo.TEXT),
    ],
    name="bbq_index",
    default_language="english",
)
