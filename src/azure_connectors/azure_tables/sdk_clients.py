from azure.data.tables import TableServiceClient as AzTableServiceClient

from azure_connectors.azure_tables.settings import TableServiceClientSettings
from azure_connectors.client_factory import ClientFactory
from azure_connectors.config import CredentialScope

TableServiceClient = ClientFactory(
    AzTableServiceClient,
    settings_class=TableServiceClientSettings,
    scope=CredentialScope.AZURE_TABLES,
).client
