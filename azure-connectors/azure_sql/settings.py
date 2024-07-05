from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .credential import CredentialType


class AzureSqlSettings(BaseModel):
    """
    Represents the settings for connecting to an Azure SQL database.
    """

    server: str
    database: str
    driver: str
    credential_type: CredentialType
    SQL_COPT_SS_ACCESS_TOKEN: int = 1256

    @computed_field
    def connection_string(self) -> str:
        """
        Generates the connection string based on the provided settings.

        Returns:
            The connection string.
        """
        return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};"


class AzureSqlSettingsFromEnv(AzureSqlSettings, BaseSettings):
    """
    Represents the Azure SQL settings loaded from environment variables.

    This class inherits from `AzureSqlSettings` and `BaseSettings` and provides a convenient way to load Azure SQL settings
    from environment variables. It uses the `SettingsConfigDict` class to specify the configuration options for loading
    the settings.

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AZURE_SQL_",  # field env vars are prefixed with "AZURE_SQL_"
        extra="ignore",  # don't throw error for unrelated items in .env
        hide_input_in_errors=True,  # don't display any secrets in .env on ValidationError
    )
