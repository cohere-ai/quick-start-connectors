import logging
from functools import reduce

from flask import current_app as app

from .client import get_client

logger = logging.getLogger(__name__)


def get_dict_value_by_dotted_key(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def search_by_keys_in_dict(dictionary, keys, query):
    for key in keys:
        value = get_dict_value_by_dotted_key(dictionary, key)
        value = value.lower() if isinstance(value, str) else ""
        query = query.lower()
        keywords = query.split()
        if any(keyword in value for keyword in keywords):
            return True
    return False


def check_result_by_campaign_attributes(result, query):
    campaign_searchable_attributes = ["attributes.name"]
    return search_by_keys_in_dict(result, campaign_searchable_attributes, query)


def check_result_by_message_attributes(result, query):
    message_searchable_attributes = [
        "attributes.label",
        "attributes.content.subject",
        "attributes.content.preview_text",
    ]
    for message in result["messages"]:
        if search_by_keys_in_dict(message, message_searchable_attributes, query):
            return True
    return False


def check_result_by_template_attributes(result, query):
    templates_searchable_attributes = [
        "attributes.name",
        "attributes.html",
        "attributes.text",
    ]
    for template in result["templates"]:
        if search_by_keys_in_dict(template, templates_searchable_attributes, query):
            return True
    return False


def search_results_by_query(results, query):
    search_results = []

    for result in results:
        if (
            check_result_by_campaign_attributes(result, query)
            or check_result_by_message_attributes(result, query)
            or check_result_by_template_attributes(result, query)
        ):
            result = serialize_record(result)
            search_results.append(result)

    return search_results


def get_campaigns_messages(client, campaign):
    messages_params = {
        "fields_campaign_message": ["content", "label"],
        "fields_template": ["name", "text", "html"],
        "include": ["template"],
    }
    campaign_messages = client.Campaigns.get_campaign_campaign_messages(
        campaign["id"], **messages_params
    )
    return campaign_messages


def serialize_record(record):
    # serialize record attributes
    if "attributes" in record and record["attributes"]:
        record["title"] = record["attributes"]["name"]
        record["url"] = (
            f'https://www.klaviyo.com/campaign/{record["id"]}/reports/overview'
        )
        for record_attribute, record_val in record["attributes"].items():
            if isinstance(record_val, dict):
                for record_val_key, record_val_val in record_val.items():
                    record[f"{record_attribute}_{record_val_key}"] = str(record_val_val)
            elif isinstance(record_val, str):
                record[record_attribute] = record_val
        record.pop("attributes")
        record.pop("relationships")
        record.pop("links")
    # serialize messages
    if "messages" in record and record["messages"]:
        for message in record["messages"]:
            if "attributes" in message and message["attributes"]:
                if "content" in message["attributes"]:
                    for message_attribute, message_val in message["attributes"][
                        "content"
                    ].items():
                        record[f"message_{message_attribute}"] = str(message_val)
    record.pop("messages")
    # serialize templates
    if "templates" in record and record["templates"]:
        for template in record["templates"]:
            if "attributes" in template and template["attributes"]:
                for template_attribute, template_val in template["attributes"].items():
                    record[f"template_{template_attribute}"] = str(template_val)
    record.pop("templates")
    record["text"] = (
        record["message_preview_text"]
        if "message_preview_text" in record and record["message_preview_text"]
        else record["message_subject"]
    )
    return record


def prepare_campaigns_to_search(client, campaigns, channel, results):
    if campaigns[channel]["data"]:
        use_templates_for_search = app.config.get("USE_TEMPLATES_FOR_SEARCH", 0)
        for campaign in campaigns[channel]["data"]:
            record_to_append = campaign
            record_to_append["channel"] = channel
            if use_templates_for_search == 1:
                campaign_messages = get_campaigns_messages(client, campaign)
                campaign_templates = (
                    campaign_messages["included"]
                    if "included" in campaign_messages
                    else []
                )
                campaign_messages = (
                    campaign_messages["data"] if "data" in campaign_messages else []
                )

                record_to_append["messages"] = campaign_messages
                record_to_append["templates"] = campaign_templates
            else:
                record_to_append["messages"] = [
                    message
                    for message in campaigns[channel]["included"]
                    if message["relationships"]["campaign"]["data"]["id"]
                    == campaign["id"]
                ]
                record_to_append["templates"] = []
            results.append(record_to_append)
    return results


def search(query):
    campaigns_created_after = app.config.get(
        "CAMPAIGNS_CREATED_AFTER", "2022-01-01T00:00:00Z"
    )

    client = get_client()

    campaigns = {
        "email": [],
        "sms": [],
    }
    all_results = []
    message_channels = ["email", "sms"]
    for channel in message_channels:
        params = {
            "filter": f'equals(messages.channel,"{channel}"),greater-or-equal(created_at,{campaigns_created_after})',
            "include": ["campaign-messages"],
            "fields_campaign_message": ["content", "label"],
        }
        campaigns[channel] = client.Campaigns.get_campaigns(**params)
        all_results = prepare_campaigns_to_search(
            client, campaigns, channel, all_results
        )

    return search_results_by_query(all_results, query)
