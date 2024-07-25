from azure.mgmt.sql import SqlManagementClient as AzSqlManagementClient

from azure_connectors.client_factory import SqlManagementClientFactory
from azure_connectors.config import CredentialScope

from .settings import SqlManagementClientSettings

SqlManagementClient = SqlManagementClientFactory(
    AzSqlManagementClient,
    settings_class=SqlManagementClientSettings,
    scope=CredentialScope.AZURE_SQL,
).client
