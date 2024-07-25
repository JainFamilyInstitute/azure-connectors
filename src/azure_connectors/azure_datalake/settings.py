from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

from azure_connectors.config import EnvPrefix, get_settings_config
from azure_connectors.validation import StorageAccountName


class DataLakeServiceClientSettings(BaseSettings):
    """
    Represents the settings for Azure DataLakeServiceClient.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_DATALAKE_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.

    """
    model_config = get_settings_config(EnvPrefix.AZURE_DATALAKE)

    # default=None prevents type complaints when using env settings.
    storage_account: StorageAccountName = Field(default=None, exclude=True)
    # TODO -- allow specifying storage account or account_url in env

    @computed_field  # type: ignore
    @property
    def account_url(self) -> str:
        """
        Generates the account URL from the storage account name.

        Returns:
            The connection string.
        """
        return f"https://{self.storage_account}.dfs.core.windows.net"

  

class FileSystemClientSettings(DataLakeServiceClientSettings):
    """
    Represents the settings for Azure (Data Lake) FileSystemClient.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_DATALAKE_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.
        file_system_name (str): The file system name.
    """

    file_system_name: str = Field(default=None)

  
class DataLakeDirectoryClientSettings(FileSystemClientSettings):
    """
    Represents the settings for Azure DataLakeDirectoryClient.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_DATALAKE_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.
        file_system_name (str): The file system name.
        directory_name (str): The directory name.
    """

    directory_name: str = Field(default=None)


class DataLakeFileClientSettings(DataLakeDirectoryClientSettings):
    """
    Represents the settings for Azure DataLakeFileClient.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_DATALAKE_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.
        file_system_name (str): The file system name.
        directory_name (str): The directory name.

    """

    ...