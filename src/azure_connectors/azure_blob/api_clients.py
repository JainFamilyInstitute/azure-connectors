from azure.storage.blob import BlobServiceClient as AzBlobServiceClient

from azure_connectors.azure_blob.settings import AzureBlobServiceSettings
from azure_connectors.client_factory import ClientFactory
from azure_connectors.config import CredentialScope

BlobServiceClient = ClientFactory(
    AzBlobServiceClient,
    settings_class=AzureBlobServiceSettings,
    scope=CredentialScope.AZURE_BLOB,
).client
