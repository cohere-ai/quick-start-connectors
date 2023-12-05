import os
from .enums import EntityChoices

BASE_PATH = f"https://{os.environ.get('FRESHSALES_BUNDLE_ALIAS', '')}/api"
API_TOKEN = os.environ.get("FRESHSALES_API_KEY")
RESULTS_LIMIT = 15
ENTITY_ENV_VAR_ENABLED_MAPPING = {
    EntityChoices.USER: "USER_ENTITY_ENABLED",
    EntityChoices.CONTACT: "CONTACT_ENTITY_ENABLED",
    EntityChoices.SALES_ACCOUNT: "SALES_ACCOUNT_ENTITY_ENABLED",
    EntityChoices.DEAL: "DEAL_ENTITY_ENABLED",
}

CONTACT_PARAMETERS = [
    "sales_activities",
    "owner",
    "creater",
    "updater",
    "source",
    "campaign",
    "tasks",
    "appointments",
    "notes",
    "deals",
    "sales_accounts",
    "territory",
    "sales_account",
]

SALES_ACCOUNT_PARAMETERS = [
    "owner",
    "creater",
    "updater",
    "territory",
    "business_type",
    "tasks",
    "appointments",
    "contacts",
    "deals",
    "industry_type",
    "child_sales_accounts",
]

DEAL_PARAMETERS = [
    "sales_activities",
    "owner",
    "creater",
    "updater",
    "source",
    "contacts",
    "sales_account",
    "deal_stage",
    "deal_type",
    "deal_reason",
    "campaign",
    "deal_payment_status",
    "deal_product",
    "currency",
    "probability",
    "created_at",
    "updated_at",
]
