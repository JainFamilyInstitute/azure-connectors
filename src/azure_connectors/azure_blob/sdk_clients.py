from azure.storage.blob import BlobClient as AzBlobClient
from azure.storage.blob import BlobServiceClient as AzBlobServiceClient
from azure.storage.blob import ContainerClient as AzContainerClient

from azure_connectors.azure_blob.settings import (
    AzureBlobServiceSettings,
    AzureBlobSettings,
    AzureContainerSettings,
)
from azure_connectors.client_factory import ClientFactory
from azure_connectors.config import CredentialScope

BlobServiceClient = ClientFactory(
    AzBlobServiceClient,
    settings_class=AzureBlobServiceSettings,
    scope=CredentialScope.AZURE_BLOB,
).client

ContainerClient = ClientFactory(
    AzContainerClient,
    settings_class=AzureContainerSettings,
    scope=CredentialScope.AZURE_BLOB,
).client

BlobClient = ClientFactory(
    AzBlobClient, settings_class=AzureBlobSettings, scope=CredentialScope.AZURE_BLOB
).client
