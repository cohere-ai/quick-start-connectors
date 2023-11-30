import logging

from flask import current_app as app

import jenkins

logger = logging.getLogger(__name__)

client = None


def filter_jobs_by_keywords(jobs, query):
    filtered_jobs = []
    keywords = query.split()
    for job in jobs:
        if any(keyword.lower() in job["name"].lower() for keyword in keywords):
            job["text"] = job.pop("fullname")
            job["title"] = job.pop("name")
            filtered_jobs.append(job)

    return filtered_jobs


def search(query):
    global client
    assert (host := app.config.get("SERVER_URL")), "JENKINS_SERVER_URL must be set"
    assert (user_name := app.config.get("USER_NAME")), "JENKINS_USER_NAME must be set"
    assert (api_key := app.config.get("API_KEY")), "JENKINS_API_KEY must be set"
    folder_depth = app.config.get("FOLDER_DEPTH", 0)
    folder_depth_per_request = app.config.get("FOLDER_DEPTH_PER_REQUEST", 10)

    if not client:
        client = jenkins.Jenkins(host, username=user_name, password=api_key)

    jobs = filter_jobs_by_keywords(
        client.get_jobs(folder_depth, folder_depth_per_request),
        query,
    )

    return jobs
