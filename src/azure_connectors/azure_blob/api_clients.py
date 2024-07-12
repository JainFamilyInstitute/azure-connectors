from azure.storage.blob import BlobClient as AzBlobClient
from azure.storage.blob import BlobServiceClient as AzBlobServiceClient
from azure.storage.blob import ContainerClient as AzContainerClient

from azure_connectors.azure_blob.settings import AzureBlobServiceSettings
from azure_connectors.client_factory import create_azure_client_class
from azure_connectors.config import CredentialScope

BlobServiceClient = create_azure_client_class(AzBlobServiceClient, settings_class=AzureBlobServiceSettings, scope=CredentialScope.AZURE_BLOB)
# ContainerClient = create_azure_client_class(AzContainerClient, scope=CredentialScope.AZURE_BLOB)
