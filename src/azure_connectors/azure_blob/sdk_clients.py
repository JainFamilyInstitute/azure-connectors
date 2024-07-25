from azure.storage.blob import BlobClient as AzBlobClient
from azure.storage.blob import BlobServiceClient as AzBlobServiceClient
from azure.storage.blob import ContainerClient as AzContainerClient

from azure_connectors.client_factory import ClientFactory
from azure_connectors.config import CredentialScope

from .settings import (
    BlobClientSettings,
    BlobServiceClientSettings,
    ContainerClientSettings,
)

BlobServiceClient = ClientFactory(
    AzBlobServiceClient,
    settings_class=BlobServiceClientSettings,
    scope=CredentialScope.AZURE_BLOB,
).client

ContainerClient = ClientFactory(
    AzContainerClient,
    settings_class=ContainerClientSettings,
    scope=CredentialScope.AZURE_BLOB,
).client

BlobClient = ClientFactory(
    AzBlobClient, settings_class=BlobClientSettings, scope=CredentialScope.AZURE_BLOB
).client
