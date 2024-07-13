from azure.data.tables import TableServiceClient as AzTableServiceClient

from azure_connectors.azure_tables.settings import AzureTableServiceSettings
from azure_connectors.client_factory import ClientFactory
from azure_connectors.config import CredentialScope

TableServiceClient = ClientFactory(
    AzTableServiceClient,
    settings_class=AzureTableServiceSettings,
    scope=CredentialScope.AZURE_TABLES,
).client
