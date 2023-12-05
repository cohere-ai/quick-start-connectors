class Config(object):
    JIRA_USER = None
    JIRA_PASS = None
    JIRA_URL = None
    JIRA_KEY = None


class DevConfig(Config):
    pass


class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass
