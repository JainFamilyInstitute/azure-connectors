from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

from azure_connectors.config import CredentialScope, EnvPrefix, get_settings_config
from azure_connectors.validation import AzureSqlDatabaseName, AzureSqlServerDomainName

from .constants import AZURE_SQL_DEFAULT_DRIVER


class AzureSqlSettings(BaseSettings):
    """
    Represents the settings for connecting to Azure SQL.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_SQL_" (defined in azure_connectors.config.enums).

    Attributes:
        server (str): The server name.
        database (str): The database name.
        driver (str): The driver name.

    """

    model_config = get_settings_config(EnvPrefix.AZURE_SQL)

    # default=None prevents type complaints when using env settings.
    server: AzureSqlServerDomainName = Field(default=None, exclude=True)
    database: AzureSqlDatabaseName = Field(default=None, exclude=True)
    driver: str = Field(default=AZURE_SQL_DEFAULT_DRIVER, exclude=True)

    default_credential_scope: CredentialScope = Field(
        default=CredentialScope.AZURE_SQL, exclude=True
    )

    @property
    def connection_string(self) -> str:
        """
        Generates the connection string based on the provided settings.

        Returns:
            The connection string.
        """
        return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};"


class SqlManagementClientSettings(AzureSqlSettings):
    @computed_field  # type: ignore
    @property
    def base_url(self) -> AzureSqlServerDomainName:
        return self.server
