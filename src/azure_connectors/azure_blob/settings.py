import re

from pydantic import BaseModel, Field, computed_field, field_validator

from azure_connectors.config import EnvPrefix
from azure_connectors.utils import with_env_settings
from azure_connectors.validation import StorageAccountName


@with_env_settings(env_prefix=EnvPrefix.AZURE_BLOB)
class AzureBlobSettings(BaseModel):
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
    storage_account: StorageAccountName = Field(default=None)
    # TODO -- allow specifying storage account or account_url in env
    

    @computed_field  # type: ignore
    @property
    def account_url(self) -> str:
        """
        Generates the connection string based on the provided settings.

        Returns:
            The connection string.
        """
        return f"https://{self.storage_account}.blob.core.windows.net"
