import logging

import hubspot
from flask import current_app as app
from hubspot.crm.contacts import PublicObjectSearchRequest

logger = logging.getLogger(__name__)
client = None


def search_contacts(query):
    global client
    search_request = PublicObjectSearchRequest(
        query=query, limit=app.config.get("SEARCH_LIMIT", 20)
    )
    response = client.crm.contacts.search_api.do_search(
        public_object_search_request=search_request
    )
    results = []
    for result in response.results:
        contact = {
            "type": "contact",
            "id": result.id,
            "title": result.properties.get("firstname", "")
            + " "
            + result.properties.get("lastname", ""),
            "first_name": result.properties.get("firstname"),
            "last_name": result.properties.get("lastname"),
            "email": result.properties.get("email"),
            "url": f"https://app.hubspot.com/contacts/{app.config['HUB_ID']}/contact/{result.id}",
        }
        results.append(contact)
    return results


def search_companies(query):
    global client
    search_request = PublicObjectSearchRequest(
        query=query, limit=app.config.get("SEARCH_LIMIT", 20)
    )
    response = client.crm.companies.search_api.do_search(
        public_object_search_request=search_request
    )
    results = []
    for result in response.results:
        company = {
            "type": "company",
            "id": result.id,
            "title": result.properties.get("name"),
            "domain": result.properties.get("domain"),
            "url": f"https://app.hubspot.com/contacts/{app.config['HUB_ID']}/company/{result.id}",
        }
        results.append(company)
    return results


def search_notes(query):
    global client
    search_request = PublicObjectSearchRequest(
        query=query,
        properties=["hs_note_body", "associations.contact"],
        limit=app.config.get("SEARCH_LIMIT", 20),
    )
    response = client.crm.objects.notes.search_api.do_search(
        public_object_search_request=search_request
    )
    results = []
    for result in response.results:
        note = {
            "type": "note",
            "id": result.id,
            "text": result.properties.get("hs_note_body"),
        }
        results.append(note)
    return results


def search_tasks(query):
    global client
    search_request = PublicObjectSearchRequest(
        query=query,
        properties=["hs_task_subject", "hs_task_body", "hs_task_status"],
        limit=app.config.get("SEARCH_LIMIT", 20),
    )
    response = client.crm.objects.tasks.search_api.do_search(
        public_object_search_request=search_request
    )
    results = []
    for result in response.results:
        note = {
            "type": "task",
            "id": result.id,
            "title": result.properties.get("hs_task_subject"),
            "text": result.properties.get("hs_task_body"),
            "status": result.properties.get("hs_task_status"),
        }
        results.append(note)
    return results


def search(query):
    global client

    if not client:
        assert (
            access_token := app.config.get("ACCESS_TOKEN")
        ), "HUBSPOT_ACCESS_TOKEN env var must be set"
        assert app.config.get("HUB_ID"), "HUBSPOT_HUB_ID env var must be set"
        client = hubspot.Client.create(access_token=access_token)

    companies = search_companies(query)
    contacts = search_contacts(query)
    notes = search_notes(query)
    tasks = search_tasks(query)

    return [*contacts, *notes, *tasks, *companies]
