from typing import Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from azure_connectors.env_config import EnvConfig


class AzureTableSettings(BaseSettings):
    """
    Represents the settings for connecting to Azure Tables on Azure storage accounts.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_TABLES_" (defined in azure_connectors.enums).

    Attributes:
        server (str): The server name.
        database (str): The database name.
        driver (str): The driver name.

    """

    # default=None prevents type complaints when using env settings.
    storage_account: str = Field(default=None)

    model_config = SettingsConfigDict(env_prefix=EnvConfig.AZURE_TABLES_PREFIX, **EnvConfig.SETTINGS_BASE)

    @computed_field
    @property
    def server(self) -> str:
        """
        Generates the server address based on the provided settings.

        Returns:
            The connection string.
        """
        return f"https://{self.storage_account}.table.core.windows.net"

    @classmethod
    def from_env(
        cls,
        storage_account: Optional[str] = None,
    ) -> "AzureTableSettings":
        """
        Create an instance of AzureTableSettings by reading the settings not passed explicitly
        from the environment variables and .env file.

        Provided for consistency with dependent classes' from_env methods.

        Args:
            server (Optional[str]): The server name for the Azure SQL connection. If not provided, it will be read from the environment.
            database (Optional[str]): The database name for the Azure SQL connection. If not provided, it will be read from the environment.
            driver (Optional[str]): The driver name for the Azure SQL connection. If not provided, it will be read from the environment.

        Returns:
            AzureSqlSettings: An instance of AzureSqlSettings with the settings loaded from the environment.

        """
        # pass along only the non-None arguments, so BaseSettings can handle the rest from the env
        pass_kwargs = {
            k: v for k, v in locals().items() if v is not None and k != "cls"
        }
        return cls(**pass_kwargs)
