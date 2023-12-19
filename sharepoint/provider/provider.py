import logging
import os
from flask import current_app as app

from dotenv import load_dotenv

from .client import get_client
from .unstructured import get_unstructured_client


load_dotenv()

logger = logging.getLogger(__name__)


def search(query):
    sharepoint_client = get_client()

    search_response = sharepoint_client.search(query)

    hits = []
    for hit_container in search_response:
        hits.extend(hit_container.get("hits", []))

    drive_items = collect_items(sharepoint_client, hits)

    # Build and request async Unstructured calls
    files = [
        (hit["resource"]["id"], hit["resource"]["name"], content)
        for hit, content in drive_items
    ]
    unstructured_content = {}

    if len(files) > 0:
        unstructured_client = get_unstructured_client()
        unstructured_client.start_session()
        unstructured_content = unstructured_client.batch_get(files)

    # Serialize results
    results = []
    for hit, drive_item in drive_items:
        file_name = hit["resource"]["name"]

        content = None
        if file_name in unstructured_content:
            content = unstructured_content[file_name]

        serialized_drive_item = serialize_drive_item(hit, drive_item, content)

        if serialized_drive_item:
            results.append(serialized_drive_item)

    return results


def collect_items(sharepoint_client, hits):
    # Gather data
    drive_items = []
    for hit in hits:
        if hit["resource"]["@odata.type"] == sharepoint_client.DRIVE_ITEM_DATA_TYPE:
            parent_drive_id = hit["resource"]["parentReference"]["driveId"]
            resource_id = hit["resource"]["id"]
            drive_item = sharepoint_client.get_drive_item_content(
                parent_drive_id, resource_id
            )

            if drive_item:
                drive_items.append((hit, drive_item))

    return drive_items


def serialize_metadata(resource):
    data = {}

    # Only return primitive types, Coral cannot parse arrays/sub-dictionaries
    stripped_resource = {
        key: str(value)
        for key, value in resource.items()
        if isinstance(value, (str, int, bool))
    }
    data.update({**stripped_resource})

    if "name" in resource:
        data["title"] = resource["name"]

    if "webUrl" in resource:
        data["url"] = resource["webUrl"]

    return data


def serialize_drive_item(hit, item, content):
    _, file_extension = os.path.splitext(hit["resource"]["name"])

    if not file_extension:
        return None  # Ignore files without extensions

    passthrough_file_types = (
        app.config.get("PASSTHROUGH_FILE_TYPES").split(",")
        if app.config.get("PASSTHROUGH_FILE_TYPES")
        else []
    )

    if file_extension in passthrough_file_types:
        return item.decode("utf-8")

    text = None
    if content is not None:
        # Build text
        text = ""
        for element in content:
            text += f' {element.get("text")}'

    data = {}
    if (resource := hit.get("resource")) is not None:
        data = serialize_metadata(resource)

    if text is not None:
        data["text"] = text

    return data
