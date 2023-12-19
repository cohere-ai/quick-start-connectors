import csv
import json
import os

import cohere
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    documents = []
    with open("./dev/bbq.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            doc = (
                f'Brand: {row["Brand"]}\n'
                + f'Description: {row["Description"]}\n'
                + f'Features: {row["Features"]}\n'
            )
            documents.append(
                {
                    "id": row["ID"],
                    "original": doc,
                    "title": row["Name"],
                    "link": "https://www.napoleon.com/en/us/grills/view-all",
                }
            )

    co = cohere.Client(os.environ["MILVUS_COHERE_APIKEY"])

    embedded_docs = {}
    batch_size = 50
    limit = len(documents)

    for i in range(0, limit, batch_size):
        texts = []
        if i + batch_size > limit:
            texts = [doc["original"] for doc in documents[i:]]
        else:
            texts = [doc["original"] for doc in documents[i : i + batch_size]]

        response = co.embed(
            texts,
            model=os.environ["MILVUS_COHERE_EMBED_MODEL"],
            input_type="search_document",
        )

        for e, _ in enumerate(response.embeddings):
            embedded_docs[documents[i + e]["id"]] = {
                **documents[i + e],
                "embedding": response.embeddings[e],
            }

    with open("./dev/bbq_embeddings.json", "w") as json_file:
        json.dump(embedded_docs, json_file)
