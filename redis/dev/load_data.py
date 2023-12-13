import csv
import logging
import os

import redis
from dotenv import load_dotenv

from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType


logger = logging.getLogger(__name__)
logger.info("Loading BBQ Test Data")

load_dotenv()

r = redis.Redis(
    host=os.environ.get("REDISEARCH_HOST", "localhost"),
    port=os.environ.get("REDISEARCH_PORT", 6379),
    decode_responses=True,
)
fields = ["Name", "Description", "Features", "Brand", "Color", "Country", "Rank"]

with open("./dev/bbq.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        bbq_id = row["ID"]
        hash_name = f"bbq_{bbq_id}"

        for field in fields:
            field_name = field.lower()
            key = f"bbq_{field_name}_{bbq_id}"
            r.set(key, row[field])
            r.hset(f"bbq_{bbq_id}", field_name, row[field])

schema = (
    TextField("name"),
    TextField("description"),
    TextField("features"),
    TextField("color"),
    TextField("country"),
    TextField("rank"),
)

r.ft("bbq_index").create_index(
    schema, definition=IndexDefinition(prefix=["bbq_"], index_type=IndexType.HASH)
)
