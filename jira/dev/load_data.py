import csv
import os
import random

from atlassian import Jira
from dotenv import load_dotenv

load_dotenv()

# Set your Jira details here
jira = Jira(
    url=os.environ.get("JIRA_PRODUCT_URL"),
    username=os.environ.get("JIRA_CLIENT_USER"),
    password=os.environ.get("JIRA_CLIENT_PASS"),
)
project_key = os.environ.get("JIRA_ISSUE_KEY")

with open("./dev/bbq.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for i, row in enumerate(reader, start=1):
        issue_key = f"{project_key}-{i}"
        summary = row["Name"]
        description = f"Brand: {row['Brand']}\nColor: {row['Color']}\n\n{row['Description']}\n{row['Features']}"

        issue_fields = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"},
        }

        new_issue = jira.issue_create(fields=issue_fields)

        if i % 20 == 1:
            jira.issue_transition(new_issue["key"], "Done")
        if i % 50 == 0:
            jira.issue_transition(new_issue["key"], "In Progress")
