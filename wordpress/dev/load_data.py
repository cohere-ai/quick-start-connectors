import csv
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def create_post(row):
    wp_url = os.environ.get("WORDPRESS_URL")
    url = f"{wp_url}/?rest_route=/wp/v2/posts"
    headers = {"Content-Type": "application/json"}
    content = f"Brand: {row['Brand']}\nColor: {row['Color']}\n\n{row['Features']}\n\n{row['Description']}"

    data = {"title": row["Name"], "content": content, "status": "publish"}

    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=(
            os.environ.get("WORDPRESS_USERNAME"),
            os.environ.get("WORDPRESS_PASSWORD"),
        ),
    )

    if response.ok:
        return 1
    else:
        print(f"Failed to create post '{row['Name']}':\n{response.text}")
        return 0


with open("./dev/bbq.csv", "r") as file:
    created_count = 0
    reader = csv.DictReader(file)
    for row in reader:
        created_count += create_post(row)

    print(f"Created {created_count} posts.")
