from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

from azure_connectors.config import EnvPrefix, get_settings_config
from azure_connectors.validation import StorageAccountName


class TableServiceClientSettings(BaseSettings):
    """
    Represents the settings for connecting to Azure Tables on Azure storage accounts.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_TABLES_" (defined in azure_connectors.config.enums).

    Attributes:
        server (str): The server name.
        database (str): The database name.
        driver (str): The driver name.

    """

    model_config = get_settings_config(EnvPrefix.AZURE_TABLES)

    # default=None prevents type complaints when using env settings.
    storage_account: StorageAccountName = Field(default=None, exclude=True)

    @computed_field  # type: ignore
    @property
    def endpoint(self) -> str:
        """
        Generates the server address based on the provided settings.

        Returns:
            The connection string.
        """
        return f"https://{self.storage_account}.table.core.windows.net"
