import json
import os

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, UpdateStatus, VectorParams


if __name__ == "__main__":
    client = QdrantClient(
        os.environ["QDRANT_CLUSTER_HOST"], port=os.environ["QDRANT_CLUSTER_PORT"]
    )
    client.recreate_collection(
        collection_name=os.environ["QDRANT_COLLECTION"],
        vectors_config=VectorParams(size=1024, distance=Distance.DOT),
    )

    bbq_embeddings = json.load(open("/bbq_embeddings.json", "r"))
    docs = list(bbq_embeddings.values())

    records = [
        [doc["id"] for doc in docs],
        [doc["original"] for doc in docs],
        [doc["embedding"] for doc in docs],
    ]

    result = client.upsert(
        collection_name=os.environ["QDRANT_COLLECTION"],
        wait=True,
        points=[
            PointStruct(
                id=i,
                vector=doc["embedding"],
                payload={"pid": doc["id"], "text": doc["original"]},
            )
            for i, doc in enumerate(docs)
        ],
    )

    if result.status == UpdateStatus.COMPLETED:
        print("Finished loading data")
    else:
        print("Failed to load data")
        print(result)
