import csv
import os

from atlassian import Confluence
from dotenv import load_dotenv

load_dotenv()


confluence = Confluence(
    url=os.environ.get("CONFLUENCE_PRODUCT_URL"),
    username=os.environ.get("CONFLUENCE_USER"),
    password=os.environ.get("CONFLUENCE_API_TOKEN"),
)
space = os.environ.get("CONFLUENCE_SPACE_NAME")

with open("../testdata/bbq.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        title = row["Name"]
        description = row["Description"]
        features = row["Features"]
        brand = row["Brand"]
        color = row["Color"]

        body = f"Brand: {brand}\nColor: {color}\n\n{description}\n{features}"

        if confluence.page_exists(space, title):
            page_id = confluence.get_page_id(space, title)
            status = confluence.update_page(
                parent_id=None,
                page_id=page_id,
                title=title,
                body=body,
                type="page",
                representation="wiki",
                minor_edit=False,
            )
            action = "Updated"
        else:
            status = confluence.create_page(space, title, body, representation="wiki")
            action = "Created"

        if status:
            print(f"{action} page {title} on Confluence.")
        else:
            print(f"Failed to {action.lower()} page {title} on Confluence.")
