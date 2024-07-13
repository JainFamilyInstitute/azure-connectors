from pydantic import BaseModel, Field, computed_field

from azure_connectors.config import EnvPrefix
from azure_connectors.utils import with_env_settings
from azure_connectors.validation import AzureSqlDatabaseName, AzureSqlServerDomainName

from .constants import AZURE_SQL_DEFAULT_DRIVER


@with_env_settings(env_prefix=EnvPrefix.AZURE_SQL)
class AzureSqlSettings(BaseModel):
    """
    Represents the settings for connecting to Azure SQL.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_SQL_" (defined in azure_connectors.config.enums).

    Attributes:
        server (str): The server name.
        database (str): The database name.
        driver (str): The driver name.

    """

    # default=None prevents type complaints when using env settings.
    server: AzureSqlServerDomainName = Field(default=None)
    database: AzureSqlDatabaseName = Field(default=None)
    driver: str = Field(default=AZURE_SQL_DEFAULT_DRIVER)

    @computed_field  # type: ignore
    @property
    def connection_string(self) -> str:
        """
        Generates the connection string based on the provided settings.

        Returns:
            The connection string.
        """
        return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};"


class AzureSqlManagementClientSettings(AzureSqlSettings):
    @computed_field  # type: ignore
    @property
    def client_settings(self) -> dict:
        """
        Generates the client settings for the storage account.

        Returns:
            The client settings.
        """
        return {
            "base_url": self.server,
        }
