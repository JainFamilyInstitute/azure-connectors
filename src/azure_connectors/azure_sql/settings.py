import re

from pydantic import BaseModel, Field, computed_field, field_validator

from azure_connectors.config import EnvPrefix
from azure_connectors.utils import with_env_settings
from azure_connectors.validation import AzureSqlServerDomainName
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
    database: str = Field(default=None)
    driver: str = Field(default=AZURE_SQL_DEFAULT_DRIVER)

    @field_validator("database")
    @classmethod
    def database_must_be_valid_mssql_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Database name must not be empty.")
        if len(v) > 128:
            raise ValueError("Database name must be 128 characters or fewer.")
        if not v[0].isalpha():
            raise ValueError("Database name start with an alphabetic character.")
        if " " in v:
            raise ValueError("Database name must not contain spaces.")
        if re.search(r'[\\/\:*?"<>|]', v):
            raise ValueError("Database name contains invalid characters.")
        return v

    @computed_field  # type: ignore
    @property
    def connection_string(self) -> str:
        """
        Generates the connection string based on the provided settings.

        Returns:
            The connection string.
        """
        return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};"
