import csv
import json

import pysolr
import requests

SOLR_URL = "http://solr:8983/solr/bbq"


def create_field(field_name, field_type):
    field_payload = {
        "add-field": {
            "name": field_name,
            "type": field_type,
            "stored": True,
            "indexed": True,
        }
    }
    response = requests.post(f"{SOLR_URL}/schema", json=field_payload)
    response.raise_for_status()


def create_copyfield(source_field, dest_field):
    copyfield_payload = {"add-copy-field": {"source": source_field, "dest": dest_field}}
    response = requests.post(f"{SOLR_URL}/schema", json=copyfield_payload)
    response.raise_for_status()


if __name__ == "__main__":
    fields = [
        ("ID", "text_general"),
        ("Name", "text_general"),
        ("Description", "text_general"),
        ("Features", "text_general"),
        ("Brand", "text_general"),
        ("Color", "text_general"),
        ("full_text", "text_general"),
    ]

    for field_name, field_type in fields:
        create_field(field_name, field_type)

    copy_fields = [
        ("ID", "full_text"),
        ("Name", "full_text"),
        ("Description", "full_text"),
        ("Features", "full_text"),
        ("Brand", "full_text"),
        ("Color", "full_text"),
    ]

    for source_field, dest_field in copy_fields:
        create_copyfield(source_field, dest_field)

    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    solr.delete(q="*:*")
    docs = []

    with open("/bbq.csv", "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        docs = [dict(zip(headers, row)) for row in reader]

    solr.add(docs)
