from azure.data.tables import TableServiceClient as AzTableServiceClient

from azure_connectors.client_factory import ClientFactory
from azure_connectors.config import CredentialScope

from .settings import TableServiceClientSettings

TableServiceClient = ClientFactory(
    AzTableServiceClient,
    settings_class=TableServiceClientSettings,
    scope=CredentialScope.AZURE_TABLES,
).client
