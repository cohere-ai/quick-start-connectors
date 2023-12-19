import json
import os

from pymilvus import (
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    connections,
    utility,
)


if __name__ == "__main__":
    if "MILVUS_API_KEY" not in os.environ or os.environ["MILVUS_API_KEY"] == "":
        connections.connect(
            alias="default",
            uri=os.environ["MILVUS_CLUSTER_URI"],
        )
    else:
        connections.connect(
            alias="default",
            uri=os.environ["MILVUS_CLUSTER_URI"],
            token=os.environ["MILVUS_API_KEY"],
        )
    collection_name = os.environ["MILVUS_COLLECTION"]
    collection_schema = CollectionSchema(
        fields=[
            FieldSchema(
                name="id", dtype=DataType.VARCHAR, max_length=64, is_primary=True
            ),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=8192),
            FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="summary", dtype=DataType.FLOAT_VECTOR, dim=1024),
        ],
        description="BBQ Products",
    )

    if utility.has_collection(collection_name):
        print(f"Deleting existing collection <{collection_name}>")
        utility.drop_collection(collection_name)

    collection = Collection(collection_name, data=None, schema=collection_schema)

    bbq_embeddings = json.load(open("bbq_embeddings.json", "r"))
    docs = list(bbq_embeddings.values())

    records = [
        [doc["id"] for doc in docs],
        [doc["original"] for doc in docs],
        [doc["title"] for doc in docs],
        [doc["link"] for doc in docs],
        [doc["embedding"] for doc in docs],
    ]

    collection.insert(records)

    collection.create_index(
        field_name="summary",
        index_params={
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        },
    )

    connections.disconnect("default")
    print("Finished loading data")
