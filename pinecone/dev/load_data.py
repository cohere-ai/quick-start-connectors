import json
import os

import pinecone
from dotenv import load_dotenv

load_dotenv()
INDEX_NAME = os.environ["PINECONE_INDEX"]

if __name__ == "__main__":
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment=os.environ["PINECONE_ENVIRONMENT"],
    )

    if INDEX_NAME not in pinecone.list_indexes():
        print("Creating index")
        pinecone.create_index(
            INDEX_NAME,
            dimension=1024,
            metric="cosine",
            pods=1,
            replicas=1,
            pod_type="p1",
        )

    index = pinecone.Index(INDEX_NAME)

    bbq_embeddings = json.load(open("./dev/bbq_embeddings.json", "r"))
    docs = list(bbq_embeddings.values())
    batch_size = 50
    limit = len(docs)

    for i in range(0, limit, batch_size):
        records = []
        # The last batch may be smaller than the batch size, so we need to handle that
        if i + batch_size > limit:
            records = [
                (doc["id"], doc["embedding"], doc["metadata"]) for doc in docs[i:]
            ]
        else:
            records = [
                (doc["id"], doc["embedding"], doc["metadata"])
                for doc in docs[i : i + batch_size]
            ]

        print(f"Upserting {len(records)} records")
        index.upsert(records)

    print("Finished loading data")
