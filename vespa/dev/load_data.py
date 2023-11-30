import csv
import json
import os

import requests

VESPA_HOST = os.getenv("VESPA_HOST", "vespa")
VESPA_PORT = os.getenv("VESPA_PORT", 8080)


if __name__ == "__main__":
    with open("./bbq.csv", "r") as datafile:
        reader = csv.DictReader(datafile)
        doc_count = 0
        for row in reader:
            document = {
                "fields": {
                    "id": row["ID"],
                    "name": row["Name"],
                    "description": row["Description"],
                    "features": row["Features"],
                    "brand": row["Brand"],
                    "color": row["Color"],
                    "country": row["Country"],
                    "rank": int(row["Rank"]),
                }
            }
            response = requests.post(
                f"http://{VESPA_HOST}:{VESPA_PORT}/document/v1/bbq/bbq/docid/{row['ID']}",
                data=json.dumps(document),
            )
            doc_count += 1
            if response.status_code != 200:
                print(
                    f"Failed to load document {row['ID']}. Response code:",
                    response.status_code,
                )
                break
        else:
            print(f"Loaded {doc_count} documents")
