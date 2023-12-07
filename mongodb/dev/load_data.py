import csv
import logging
import os

import pymongo
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logger.info("Loading BBQ Test Data")

load_dotenv()

connection_string = os.environ.get(
    "MONGODB_CONNECTION_STRING", "mongodb://root:example@mongo:27017"
)

client = pymongo.MongoClient(connection_string)

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
