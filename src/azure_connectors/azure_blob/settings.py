from pydantic import BaseModel, Field, computed_field

from azure_connectors.config import EnvPrefix
from azure_connectors.utils import with_env_settings
from azure_connectors.validation import StorageAccountName


@with_env_settings(env_prefix=EnvPrefix.AZURE_BLOB)
class AzureBlobServiceSettings(BaseModel):
    """
    Represents the settings for connecting to Azure Blob Storage.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_BLOB_" (defined in azure_connectors.config.enums).

    Attributes:
        storage_account (StorageAccountName): The storage account name.
        account_url (str): The storage account URL.

    """

    # default=None prevents type complaints when using env settings.
    storage_account: StorageAccountName = Field(default=None)
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

    @computed_field  # type: ignore
    @property
    def client_settings(self) -> dict:
        """
        Generates the client settings for the storage account.

        Returns:
            The client settings.
        """
        return {
            "account_url": self.account_url,
        }
    
 