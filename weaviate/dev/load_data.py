import csv
import os

import weaviate

if __name__ == "__main__":
    client = weaviate.Client(
        url=os.environ["WEAVIATE_SERVER_URL"],
    )

    try:
        client.schema.delete_class(os.environ["WEAVIATE_SCHEMA_CLASS"])
    except:
        pass

    class_obj = {
        "class": os.environ["WEAVIATE_SCHEMA_CLASS"],
        "properties": [
            {
                "name": "ID",
                "dataType": ["text"],
            },
            {
                "name": "Name",
                "dataType": ["text"],
            },
            {
                "name": "Description",
                "dataType": ["text"],
            },
            {
                "name": "Features",
                "dataType": ["text"],
            },
            {
                "name": "Brand",
                "dataType": ["text"],
            },
            {
                "name": "Color",
                "dataType": ["text"],
            },
        ],
        "vectorizer": "text2vec-cohere",
    }

    client.schema.create_class(class_obj)
    upload_limit = 100

    with open("/bbq.csv", "r") as csv_file:
        with client.batch(batch_size=100) as batch:
            reader = csv.DictReader(csv_file)
            for i, row in enumerate(reader, start=1):
                if i == upload_limit:
                    break

                properties = {
                    k: row[k]
                    for k in ("ID", "Name", "Description", "Features", "Brand", "Color")
                }

                client.batch.add_data_object(
                    properties,
                    os.environ["WEAVIATE_SCHEMA_CLASS"],
                )

    print("Finished loading data")
