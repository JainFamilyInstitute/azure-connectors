from dataclasses import dataclass
from functools import cached_property

import azure.data.tables

from azure_connectors.credential import AzureCredential
from azure_connectors.enums import CredentialScope

from .settings import AzureTableSettings


@dataclass(frozen=True)
class AzureTableConnection:
    """
    Represents an Azure Tables connection.

    Can be used as a context manager to ensure that the underlying service client is properly set up and closed.

    Attributes:
        settings (AzureTableSettings): The settings for the Azure SQL connection.
        credential (AzureCredential): The credential for the Azure SQL connection.
        service_client (azure.data.tables.TableServiceClient): The TableServiceClient for the connection.

    Example:
    >>> with AzureTableConnection.from_env() as ts:
    >>>     for table in ts.list_tables():
    >>>         print(f"Table: {table.name}")

    """

    settings: AzureTableSettings
    credential: AzureCredential

    CREDENTIAL_SCOPE: CredentialScope = CredentialScope.AZURE_TABLES
  

    @classmethod
    def from_env(cls) -> "AzureTableConnection":
            """
            Create an AzureTableConnection instance using the settings and credentials from the environment.

            This method retrieves the settings and credentials required to create an AzureTableConnection instance from the environment.
            It uses the AzureTableSettings.from_env() method to retrieve the settings and the AzureCredentials.from_env() method to retrieve the credentials.

            Returns:
                AzureTableConnection: An instance of AzureTableConnection.

            Example:
                >>> client = AzureTableConnection.from_env()
            """
            settings = AzureTableSettings()
            credential = AzureCredential.from_env(scope=cls.CREDENTIAL_SCOPE)
            return cls(settings=settings, credential=credential)

    @cached_property
    def service_client(self) -> azure.data.tables.TableServiceClient:
            """
            Get the TableServiceClient for the storage account.

            Returns:
                azure.data.tables.TableServiceClient: The TableServiceClient object for the storage account.
            """
            table_service_client = azure.data.tables.TableServiceClient(
                endpoint=self.settings.server, 
                credential=self.credential._base_credential) 
            return table_service_client
    
    def __enter__(self):
            """
            Enter method for using the Azure Tables client as a context manager.
            
            This method is automatically called when using the client in a `with` statement.
            It ensures that the underlying service client is properly set up and returns the client object.
            
            Returns:
                The underlying service client object.
            """
            self.service_client.__enter__()
            return self.service_client
    
    def __exit__(self, exc_type, exc_value, traceback):
            """
            Exit method for using the Azure Tables client as a context manager.
            
            This method is automatically called when exiting a `with` statement that uses the client.
            It ensures that the underlying service client is properly closed.
            """
            return self.service_client.__exit__(exc_type, exc_value, traceback)