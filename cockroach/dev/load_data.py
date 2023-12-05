import csv

import psycopg2
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

COCKROACH_DATABASE_URL = config["COCKROACH_DATABASE_URL"]


def create_bbq_table():
    conn = psycopg2.connect(COCKROACH_DATABASE_URL)
    cursor = conn.cursor()

    drop_table_query = """
    DROP TABLE IF EXISTS bbq
    """
    cursor.execute(drop_table_query)
    conn.commit()

    create_table_query = """
    CREATE TABLE bbq (
        id SERIAL PRIMARY KEY,
        a_id VARCHAR,
        brand VARCHAR,
        color VARCHAR,
        country VARCHAR,
        description VARCHAR,
        features TEXT,
        name VARCHAR,
        search_vector TSVECTOR GENERATED ALWAYS AS (
            to_tsvector('english', brand || ' ' || color || ' ' || description || ' ' || features || ' ' || a_id || ' ' || name)
        ) STORED
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    create_index_query = """
    CREATE INDEX idx_bbq_search_vector ON bbq USING gin(search_vector)
    """
    cursor.execute(create_index_query)
    conn.commit()

    cursor.close()
    conn.close()


def load_data():
    conn = psycopg2.connect(COCKROACH_DATABASE_URL)
    cursor = conn.cursor()

    with open("../../testdata/bbq.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            insert_query = """
            INSERT INTO bbq (a_id, brand, color, country, description, features, name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    row["ID"],
                    row["Brand"],
                    row["Color"],
                    row["Country"],
                    row["Description"],
                    row["Features"],
                    row["Name"],
                ),
            )
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_bbq_table()
    load_data()
