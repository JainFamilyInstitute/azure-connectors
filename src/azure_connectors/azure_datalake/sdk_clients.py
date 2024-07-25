from azure.storage.filedatalake import (
    DataLakeDirectoryClient as AzDataLakeDirectoryClient,
)
from azure.storage.filedatalake import DataLakeFileClient as AzDataLakeFileClient
from azure.storage.filedatalake import DataLakeServiceClient as AzDataLakeServiceClient
from azure.storage.filedatalake import FileSystemClient as AzFileSystemClient

from azure_connectors.client_factory import ClientFactory
from azure_connectors.config import CredentialScope

from .settings import (
    DataLakeDirectoryClientSettings,
    DataLakeFileClientSettings,
    DataLakeServiceClientSettings,
    FileSystemClientSettings,
)

DataLakeServiceClient = ClientFactory(
    AzDataLakeServiceClient,
    settings_class=DataLakeServiceClientSettings,
    scope=CredentialScope.AZURE_DATALAKE,
).client

FileSystemClient = ClientFactory(
    AzFileSystemClient,
    settings_class=FileSystemClientSettings,
    scope=CredentialScope.AZURE_DATALAKE,
).client

DataLakeDirectoryClient = ClientFactory(
    AzDataLakeDirectoryClient,
    settings_class=DataLakeDirectoryClientSettings,
    scope=CredentialScope.AZURE_DATALAKE,
).client

DataLakeFileClient = ClientFactory(
    AzDataLakeFileClient,
    settings_class=DataLakeFileClientSettings,
    scope=CredentialScope.AZURE_DATALAKE,
).client
