from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

from azure_connectors.config import EnvPrefix, get_settings_config
from azure_connectors.validation import StorageAccountName


class BlobServiceClientSettings(BaseSettings):
    """
    Represents the settings for Azure BlobServiceClient.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_BLOB_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.

    """

    model_config = get_settings_config(EnvPrefix.AZURE_BLOB)

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
        return f"https://{self.storage_account}.blob.core.windows.net"


class ContainerClientSettings(BlobServiceClientSettings):
    """
    Represents the settings for Azure (Blob) ContainerClient.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_BLOB_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.
        container_name (str): The container name.
    """

    container_name: str = Field(default=None)


class BlobClientSettings(ContainerClientSettings):
    """
    Represents the settings for Azure BlobClient.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_BLOB_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.
        container_name (str): The container name.
        blob_name (str): The blob name.
    """

    blob_name: str = Field(default=None)
