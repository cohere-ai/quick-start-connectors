from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """
    Application Configuration
    """

    CONNECTOR_ID: str = Field(..., env="CONNECTOR_ID")
    CONNECTOR_API_KEY: str = Field(..., env="CONNECTOR_API_KEY")
    CLIENT_AUTH_TOKEN: str = Field(..., env="CLIENT_AUTH_TOKEN")
    CLIENT_SEARCH_LIMIT: int = Field(5, env="CLIENT_SEARCH_LIMIT")

    class Config:
        """
        Loads environment variables from a file named .env
        """

        env_file = ".env"
        env_file_encoding = "utf-8"
