from agility_cms import Client

client = None


def get_client(api_domain, api_guid, api_key, api_locale):
    global client
    if not client:
        client = Client(
            api_guid, api_key, locale=api_locale, preview=False, url=api_domain
        )
    return client
